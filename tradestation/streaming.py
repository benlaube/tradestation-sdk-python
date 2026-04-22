"""
HTTP Streaming Session Management

Manages TradeStation HTTP streaming (long-lived NDJSON connections) for quotes,
orders, positions, balances, bars, and options. Includes retry/backoff helpers,
health tracking, and optional fallbacks to REST polling when streams fail.

Note: TradeStation API v3 uses HTTP Streaming (not WebSockets) for most feeds.
This module wraps HTTPClient.stream_data with async-friendly queues.

Dependencies: typing, HTTPClient
"""

import asyncio
import queue
import threading
import time
from collections.abc import AsyncGenerator, Callable
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, TypeVar

import requests

from .client import HTTPClient
from .config import sdk_config
from .exceptions import (
    ErrorDetails,
    InvalidRequestError,
    NetworkError,
    NonRecoverableError,
    RateLimitError,
    RecoverableError,
    StreamGoAwayError,
)
from .logger import setup_logger
from .models import BalanceStream, PositionsResponse
from .models.streaming import (
    OrderStream,
    PositionStream,
    QuoteStream,
)
from .session import Session, TokenManager
from .validation import validate_model

logger = setup_logger(__name__, sdk_config.log_level)

# Type variable for stream items
T = TypeVar("T")
_QUEUE_TIMEOUT = object()


def _is_recoverable_stream_error(exc: Exception) -> bool:
    """Return True when a stream error is eligible for retry or REST fallback."""
    return isinstance(
        exc,
        RecoverableError
        | NetworkError
        | RateLimitError
        | requests.exceptions.RequestException
        | TimeoutError
        | ConnectionError
        | OSError,
    )


def _stream_error_details(
    *,
    code: str,
    message: str,
    api_error_code: str,
    operation: str,
    endpoint: str,
    mode: str | None,
    payload: dict[str, Any],
) -> ErrorDetails:
    """Build structured details for broker stream control/error payloads."""
    return ErrorDetails(
        code=code,
        message=message,
        api_error_code=api_error_code,
        api_error_message=payload.get("Message") or payload.get("error_description"),
        request_endpoint=endpoint,
        response_body=payload,
        mode=mode,
        operation=operation,
    )


def _handle_stream_control_payload(
    payload: Any,
    *,
    stream_type: str,
    operation: str,
    endpoint: str,
    mode: str | None,
) -> bool:
    """Handle stream control/error payloads before strict model validation.

    Returns True when the payload is a handled control message that should be
    skipped. Raises a typed SDK error for terminal broker control messages.
    """
    if not isinstance(payload, dict):
        return False

    if "StreamStatus" in payload:
        status = str(payload.get("StreamStatus") or "")
        if status == "EndSnapshot":
            logger.debug("Initial %s snapshot complete, streaming live updates", stream_type)
            return True
        if status == "GoAway":
            message = payload.get("Message") or "TradeStation requested stream reconnect"
            logger.warning("%s stream received GoAway control status: %s", stream_type, message)
            raise StreamGoAwayError(
                _stream_error_details(
                    code="STREAM_GOAWAY",
                    message=str(message),
                    api_error_code="GoAway",
                    operation=operation,
                    endpoint=endpoint,
                    mode=mode,
                    payload=payload,
                )
            )
        return True

    error = payload.get("Error") or payload.get("error")
    if not error:
        return False

    error_code = str(error)
    message = payload.get("Message") or payload.get("error_description") or error_code
    if error_code.lower() == "goaway":
        logger.warning("%s stream received GoAway error payload: %s", stream_type, message)
        raise StreamGoAwayError(
            _stream_error_details(
                code="STREAM_GOAWAY",
                message=str(message),
                api_error_code="GoAway",
                operation=operation,
                endpoint=endpoint,
                mode=mode,
                payload=payload,
            )
        )

    if error_code.upper() == "FAILED":
        raise RecoverableError(
            _stream_error_details(
                code="STREAM_FAILED",
                message=str(message),
                api_error_code=error_code,
                operation=operation,
                endpoint=endpoint,
                mode=mode,
                payload=payload,
            )
        )

    raise NonRecoverableError(
        _stream_error_details(
            code="STREAM_ERROR",
            message=str(message),
            api_error_code=error_code,
            operation=operation,
            endpoint=endpoint,
            mode=mode,
            payload=payload,
        )
    )


async def _get_stream_queue_item(
    data_queue: queue.Queue[Any],
    stream_error: list[Exception | None],
    stream_type: str,
    timeout: float = 1.0,
) -> Any:
    """Read a thread-fed stream queue without blocking the event loop."""
    started_at = time.perf_counter()
    try:
        item = await asyncio.to_thread(data_queue.get, True, timeout)
    except queue.Empty:
        elapsed = time.perf_counter() - started_at
        if elapsed > timeout * 1.5:
            logger.warning(
                "%s stream queue poll exceeded expected latency: %.3fs (timeout %.3fs)",
                stream_type,
                elapsed,
                timeout,
            )
        if stream_error[0]:
            raise stream_error[0]
        return _QUEUE_TIMEOUT

    elapsed = time.perf_counter() - started_at
    if elapsed > timeout * 1.5:
        logger.warning(
            "%s stream queue poll exceeded expected latency: %.3fs (timeout %.3fs)",
            stream_type,
            elapsed,
            timeout,
        )
    return item


@dataclass
class StreamHealth:
    """
    Stream health metrics for monitoring stream reliability.

    Tracks message counts, errors, and uptime for each stream type.
    """

    stream_type: str  # "quotes", "orders", "positions", "balances"
    last_update_time: datetime | None = None
    message_count: int = 0
    error_count: int = 0
    consecutive_errors: int = 0
    uptime_seconds: float = 0.0
    is_healthy: bool = True
    start_time: datetime = field(default_factory=datetime.now)

    def update_on_message(self):
        """Update health metrics on successful message."""
        self.message_count += 1
        self.last_update_time = datetime.now()
        self.consecutive_errors = 0
        self.is_healthy = True
        self.uptime_seconds = (datetime.now() - self.start_time).total_seconds()

    def update_on_error(self):
        """Update health metrics on error."""
        self.error_count += 1
        self.consecutive_errors += 1
        # Consider unhealthy if 3+ consecutive errors
        self.is_healthy = self.consecutive_errors < 3
        self.uptime_seconds = (datetime.now() - self.start_time).total_seconds()


class StreamingManager:
    """
    Streaming session management for TradeStation HTTP streaming endpoints.

    Provides HTTP Streaming methods (stream_quotes, stream_orders, stream_positions)
    that use TradeStation API v3 HTTP Streaming endpoints.

    The original implementation was named "WebSocketManager" even though TradeStation
    v3 exposes HTTP streaming rather than true WebSockets. This class keeps the
    same interface but emphasizes the HTTP streaming transport.
    """

    def __init__(
        self, token_manager: TokenManager, client_id: str, client_secret: str, api_client: HTTPClient | None = None
    ):
        """
        Initialize streaming manager.

        Args:
            token_manager: TokenManager instance for token access
            client_id: TradeStation API client ID
            client_secret: TradeStation API client secret
            api_client: Optional HTTPClient for HTTP streaming (if None, will be created on demand)
        """
        self.token_manager = token_manager
        self.client_id = client_id
        self.client_secret = client_secret
        self._base_session: Session | None = None
        self._api_client = api_client

        # Stream health tracking
        self._stream_health: dict[str, StreamHealth] = {}

    @property
    def session(self) -> "StreamingManager | None":
        """
        Get streaming session for real-time streaming.

        Creates base Session lazily on first access.
        Returns self (StreamingManager instance) which acts as both the manager and session.
        Provides stream_quotes(), stream_orders(), and stream_positions() methods
        using HTTP Streaming.

        Uses tokens from active trading mode (sdk_config.trading_mode).
        Automatically ensures tokens are fresh before creating session.

        Returns:
            StreamingManager instance (self) or None if not authenticated

        Dependencies: Session, TokenManager
        """
        # Use tokens from active trading mode (for backward compatibility)
        mode = sdk_config.trading_mode
        # Ensure tokens are fresh before attempting to build a session
        self.token_manager.ensure_authenticated(mode)
        tokens = self.token_manager.get_tokens(mode)
        has_refresh = bool(tokens.get("refresh_token"))
        if not tokens["access_token"]:
            logger.warning("Cannot create streaming session: not authenticated")
            return None

        if self._base_session is None:
            try:
                # Create base Session with OAuth credentials
                if not has_refresh:
                    logger.warning("Cannot create streaming session: no refresh token")
                    return None

                self._base_session = Session(
                    api_key=self.client_id,
                    secret_key=self.client_secret,
                    refresh_token=tokens["refresh_token"],
                    access_token=tokens["access_token"],
                    is_test=(mode == "PAPER"),
                )
                logger.info(
                    f"✅ Streaming session created successfully for {mode} mode (HTTP Streaming support enabled)"
                )
            except Exception as e:
                logger.warning(f"Failed to create streaming session: {e}")
                logger.debug("Streaming features will be unavailable")
                return None

        return self

    async def _ensure_session(self, mode: str | None = None) -> bool:
        """
        Ensure streaming session is available, creating/refreshing if needed.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            True if session is available, False otherwise

        Dependencies: TokenManager.ensure_authenticated, Session
        """
        if mode is None:
            mode = sdk_config.trading_mode

        # Refresh tokens if needed
        self.token_manager.ensure_authenticated(mode)

        # Check if session exists and is valid
        if self._base_session is None:
            # Try to create session (uses existing session property logic)
            session = self.session
            if session is None:
                logger.warning("Cannot create streaming session")
                return False

        return True

    def get_stream_health(self, stream_type: str) -> StreamHealth | None:
        """
        Get health metrics for a stream type.

        Args:
            stream_type: Stream type ("quotes", "orders", "positions", "balances")

        Returns:
            StreamHealth object or None if stream hasn't been started
        """
        return self._stream_health.get(stream_type)

    async def _with_retry(
        self,
        stream_type: str,
        stream_func: Callable[[], AsyncGenerator[T, None]],
        max_retries: int = 10,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        auto_reconnect: bool = True,
        mode: str | None = None,
    ) -> AsyncGenerator[T, None]:
        """
        Generic retry wrapper for async generator streams.

        Wraps any async generator with automatic reconnection, retry logic,
        health tracking, and session recovery.

        Args:
            stream_type: Stream type identifier ("quotes", "orders", etc.)
            stream_func: Async function that returns an async generator
            max_retries: Maximum number of retry attempts
            retry_delay: Initial retry delay in seconds
            max_retry_delay: Maximum retry delay in seconds
            auto_reconnect: Enable automatic reconnection
            mode: Trading mode ("PAPER" or "LIVE")

        Yields:
            Items from the wrapped async generator

        Dependencies: _ensure_session, StreamHealth

        Raises:
            NonRecoverableError: For auth/validation errors that should not be retried.
            Exception: After max_retries are exceeded or on unexpected failures.
        """
        # Initialize health tracking
        if stream_type not in self._stream_health:
            self._stream_health[stream_type] = StreamHealth(stream_type=stream_type)

        health = self._stream_health[stream_type]
        consecutive_failures = 0
        current_retry_delay = retry_delay

        # Ensure session is available
        await self._ensure_session(mode)

        while True:  # Outer retry loop
            try:
                # Call the stream function to get the async generator
                async_gen = stream_func()

                async for item in async_gen:
                    # Reset failure counter on successful message
                    consecutive_failures = 0
                    current_retry_delay = retry_delay
                    health.update_on_message()
                    yield item

                logger.info(f"{stream_type} stream ended cleanly")
                break

            except asyncio.CancelledError:
                logger.info(f"{stream_type} stream cancelled")
                break
            except InvalidRequestError as e:
                health.update_on_error()
                logger.error(f"Validation or request error in {stream_type} stream: {e}")
                raise
            except NonRecoverableError as e:
                health.update_on_error()
                logger.error(f"Non-recoverable error in {stream_type} stream: {e}")
                raise
            except Exception as e:
                if not auto_reconnect:
                    health.update_on_error()
                    raise

                consecutive_failures += 1
                health.update_on_error()

                if consecutive_failures >= max_retries:
                    logger.critical(f"Max retries ({max_retries}) reached for {stream_type} stream")
                    raise

                if not _is_recoverable_stream_error(e):
                    logger.error(f"Non-recoverable error in {stream_type} stream: {e}", exc_info=True)
                    raise

                logger.warning(
                    f"{stream_type} stream error (failure #{consecutive_failures}): {e}, "
                    f"retrying in {current_retry_delay:.1f}s"
                )
                await asyncio.sleep(current_retry_delay)
                current_retry_delay = min(current_retry_delay * 2, max_retry_delay)

                # Try to recover session before retrying
                await self._ensure_session(mode)

    async def stream_quotes(
        self,
        symbols: list[str] | str,
        mode: str | None = None,
        max_retries: int = 10,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        auto_reconnect: bool = True,
        fallback_to_polling: bool = True,
        polling_interval: float = 1.0,
    ) -> AsyncGenerator[QuoteStream, None]:
        """
        Stream quotes via TradeStation HTTP Streaming API with automatic reconnection and retry.

        TradeStation API v3 supports HTTP Streaming (long-lived HTTP connections)
        for real-time quote data. This method provides automatic reconnection, retry logic,
        and REST polling fallback.

        Args:
            symbols: List of symbols or a comma-separated string (e.g., ["MNQZ25", "ESZ25"] or "MNQZ25,ESZ25")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            max_retries: Maximum number of retry attempts (default: 10)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            max_retry_delay: Maximum retry delay in seconds (default: 60.0)
            auto_reconnect: Enable automatic reconnection on errors (default: True)
            fallback_to_polling: Enable REST polling fallback if streaming fails (default: True)
            polling_interval: Interval for REST polling in seconds (default: 1.0)

        Yields:
            QuoteStream: Parsed quote data as Pydantic models

        Dependencies: HTTPClient.stream_data, QuoteStream

        Raises:
            NonRecoverableError: For authentication/validation failures.
            Exception: After retries are exhausted and fallback is disabled or also fails.

        Example:
            async for quote in streaming_manager.stream_quotes(["MNQZ25"]):
                print(quote.Symbol, quote.Last)
        """
        if mode is None:
            mode = sdk_config.trading_mode
        symbols_list = [symbol.strip() for symbol in symbols.split(",")] if isinstance(symbols, str) else symbols

        # Use generic retry wrapper
        async def _get_stream():
            """Create the quote stream generator."""
            # Try HTTP streaming first
            try:
                async for quote in self._stream_quotes_internal(symbols_list, mode):
                    yield quote
            except StreamGoAwayError:
                raise
            except InvalidRequestError:
                raise
            except Exception as e:
                if fallback_to_polling and _is_recoverable_stream_error(e):
                    logger.warning(
                        "HTTP quote streaming failed for %s; falling back to REST polling",
                        ",".join(symbols_list),
                        exc_info=True,
                    )
                    async for quote in self._poll_quotes_rest(symbols_list, mode, polling_interval):
                        yield quote
                else:
                    raise

        async for quote in self._with_retry(
            stream_type="quotes",
            stream_func=_get_stream,
            max_retries=max_retries,
            retry_delay=retry_delay,
            max_retry_delay=max_retry_delay,
            auto_reconnect=auto_reconnect,
            mode=mode,
        ):
            yield quote

    async def _stream_quotes_internal(self, symbols: list[str], mode: str) -> AsyncGenerator[QuoteStream, None]:
        """
        Internal method to stream quotes via HTTP Streaming (no retry logic).

        This is the core streaming implementation wrapped by stream_quotes() with retry logic.

        Args:
            symbols: List of symbols to stream
            mode: "PAPER" or "LIVE"

        Yields:
            QuoteStream: Parsed quote data
        """
        # Get API client (use provided or create from token manager)
        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        # TradeStation API v3 endpoint: marketdata/stream/quotes/{symbols}
        # Symbols are comma-separated in the path
        symbols_param = ",".join(symbols)
        endpoint = f"marketdata/stream/quotes/{symbols_param}"

        logger.info(f"Starting quote stream for {len(symbols)} symbol(s) via HTTP Streaming")

        # Use HTTPClient.stream_data for HTTP streaming
        # stream_data() is synchronous generator, so we run it in a thread
        # and use a queue to pass data to async context
        quote_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous stream in background thread."""
            try:
                for quote_data in self._api_client.stream_data(endpoint, mode=mode):
                    quote_queue.put(quote_data)
                quote_queue.put(None)  # Signal end
            except Exception as e:
                logger.exception("Quote stream worker failed for endpoint=%s mode=%s", endpoint, mode)
                stream_error[0] = e
                quote_queue.put(None)  # Signal end

        # Start streaming in background thread
        stream_thread = threading.Thread(target=run_stream, daemon=True)
        stream_thread.start()

        # Process quotes from queue
        while True:
            quote_data = await _get_stream_queue_item(quote_queue, stream_error, "quote")
            if quote_data is _QUEUE_TIMEOUT:
                continue

            # None signals end of stream
            if quote_data is None:
                if stream_error[0]:
                    raise stream_error[0]
                break

            if _handle_stream_control_payload(
                quote_data,
                stream_type="quote",
                operation="stream_quotes",
                endpoint=endpoint,
                mode=mode,
            ):
                continue

            # Filter out heartbeats
            if isinstance(quote_data, dict) and "Heartbeat" in quote_data and "Symbol" not in quote_data:
                continue

            # Parse and yield QuoteStream model
            try:
                quote = validate_model(
                    QuoteStream,
                    quote_data,
                    operation="stream_quotes",
                    endpoint=endpoint,
                    mode=mode,
                    source="response",
                )
                yield quote
            except Exception as e:
                logger.warning(f"Failed to parse quote data: {e}, raw data: {quote_data}")
                # Re-raise parsing errors - they indicate data issues
                raise

    async def _poll_quotes_rest(
        self, symbols: list[str], mode: str, interval: float
    ) -> AsyncGenerator[QuoteStream, None]:
        """
        REST polling fallback for quotes.

        Polls quote snapshots via REST API when HTTP streaming is unavailable.

        Args:
            symbols: List of symbols to poll
            mode: "PAPER" or "LIVE"
            interval: Polling interval in seconds

        Yields:
            QuoteStream: Parsed quote data
        """
        from .market_data import MarketDataOperations

        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        market_data = MarketDataOperations(self._api_client)
        symbols_str = ",".join(symbols)

        logger.info(f"Using REST polling fallback for quotes (interval: {interval}s)")

        while True:
            try:
                # Get quote snapshots
                quotes_response = market_data.get_quote_snapshots(symbols_str, mode=mode)
                quotes = quotes_response.get("Quotes", [])

                for quote_dict in quotes:
                    yield validate_model(
                        QuoteStream,
                        quote_dict,
                        operation="poll_quotes_rest",
                        endpoint=f"marketdata/quotes/{symbols_str}",
                        mode=mode,
                        source="response",
                    )

                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Quote REST polling fallback failed for symbols=%s mode=%s", symbols_str, mode)
                await asyncio.sleep(interval)  # Continue polling despite errors

    async def stream_bars(
        self,
        symbol: str,
        interval: int,
        unit: str,
        mode: str | None = None,
        max_retries: int = 10,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        auto_reconnect: bool = True,
        # Note: Bars typically don't fail back to polling easily due to continuity requirements
    ) -> AsyncGenerator[Any, None]:
        """
        Stream bars via TradeStation HTTP Streaming API.

        Args:
            symbol: Symbol to stream (e.g. "MNQZ25")
            interval: Bar interval (e.g. 1)
            unit: Bar unit (e.g. "Minute")
            mode: "PAPER" or "LIVE"
        """
        if mode is None:
            mode = sdk_config.trading_mode

        async def _get_stream():
            if not self._api_client:
                self._api_client = HTTPClient(self.token_manager)

            # Endpoint: marketdata/stream/barcharts/{symbol}/{interval}/{unit}
            endpoint = f"marketdata/stream/barcharts/{symbol}/{interval}/{unit}"
            logger.info(f"Starting bar stream for {symbol} ({interval} {unit}) via HTTP Streaming")

            # We reuse the internal threading logic here inline or refactor.
            # For speed, I'll inline the thread runner pattern used in stream_quotes_internal
            bar_queue = queue.Queue()
            stream_error = [None]

            def run_stream():
                try:
                    for bar_data in self._api_client.stream_data(endpoint, mode=mode):
                        bar_queue.put(bar_data)
                    bar_queue.put(None)
                except Exception as e:
                    stream_error[0] = e
                    bar_queue.put(None)

            stream_thread = threading.Thread(target=run_stream, daemon=True)
            stream_thread.start()

            while True:
                bar_data = await _get_stream_queue_item(bar_queue, stream_error, "bar")
                if bar_data is _QUEUE_TIMEOUT:
                    continue

                if bar_data is None:
                    if stream_error[0]:
                        raise stream_error[0]
                    break

                if _handle_stream_control_payload(
                    bar_data,
                    stream_type="bar",
                    operation="stream_bars",
                    endpoint=endpoint,
                    mode=mode,
                ):
                    continue

                if isinstance(bar_data, dict) and "Heartbeat" in bar_data:
                    continue

                # Yield raw dict, let service parse it to BarEvent
                yield bar_data

        async for bar in self._with_retry(
            stream_type="bars",
            stream_func=_get_stream,
            max_retries=max_retries,
            retry_delay=retry_delay,
            max_retry_delay=max_retry_delay,
            auto_reconnect=auto_reconnect,
            mode=mode,
        ):
            yield bar

    async def stream_orders(
        self,
        account_id: str,
        mode: str | None = None,
        max_retries: int = 10,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        auto_reconnect: bool = True,
        fallback_to_polling: bool = True,
        polling_interval: float = 1.0,
    ) -> AsyncGenerator[OrderStream, None]:
        """
        Stream order updates via TradeStation HTTP Streaming API with automatic reconnection and retry.

        Args:
            account_id: TradeStation account ID
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            max_retries: Maximum number of retry attempts (default: 10)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            max_retry_delay: Maximum retry delay in seconds (default: 60.0)
            auto_reconnect: Enable automatic reconnection on errors (default: True)
            fallback_to_polling: Enable REST polling fallback if streaming fails (default: True)
            polling_interval: Interval for REST polling in seconds (default: 1.0)

        Yields:
            OrderStream: Parsed order update data as Pydantic models

        Dependencies: HTTPClient.stream_data, OrderStream

        Raises:
            NonRecoverableError: For authentication/validation failures.
            Exception: After retries are exhausted and fallback is disabled or fails.
        """
        if mode is None:
            mode = sdk_config.trading_mode

        async def _get_stream():
            """Create the order stream generator."""
            try:
                async for order in self._stream_orders_internal(account_id, mode):
                    yield order
            except StreamGoAwayError:
                raise
            except Exception as e:
                if fallback_to_polling and _is_recoverable_stream_error(e):
                    logger.warning(
                        "HTTP order streaming failed for account_id=%s; falling back to REST polling",
                        account_id,
                        exc_info=True,
                    )
                    async for order in self._poll_orders_rest(account_id, mode, polling_interval):
                        yield order
                else:
                    raise

        async for order in self._with_retry(
            stream_type="orders",
            stream_func=_get_stream,
            max_retries=max_retries,
            retry_delay=retry_delay,
            max_retry_delay=max_retry_delay,
            auto_reconnect=auto_reconnect,
            mode=mode,
        ):
            yield order

    async def _stream_orders_internal(self, account_id: str, mode: str) -> AsyncGenerator[OrderStream, None]:
        """Internal method to stream orders via HTTP Streaming (no retry logic)."""
        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        endpoint = f"brokerage/stream/accounts/{account_id}/orders"
        logger.info(f"Starting order stream for account {account_id} via HTTP Streaming")

        order_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous order stream in background thread via HTTPClient.stream_data."""
            try:
                for order_data in self._api_client.stream_data(endpoint, params=None, mode=mode):
                    order_queue.put(order_data)
                order_queue.put(None)
            except Exception as e:
                logger.exception("Order stream worker failed for endpoint=%s mode=%s", endpoint, mode)
                stream_error[0] = e
                order_queue.put(None)

        stream_thread = threading.Thread(target=run_stream, daemon=True)
        stream_thread.start()

        while True:
            order_data = await _get_stream_queue_item(order_queue, stream_error, "order")
            if order_data is _QUEUE_TIMEOUT:
                continue

            if order_data is None:
                if stream_error[0]:
                    raise stream_error[0]
                break

            if _handle_stream_control_payload(
                order_data,
                stream_type="order",
                operation="stream_orders",
                endpoint=endpoint,
                mode=mode,
            ):
                continue

            if isinstance(order_data, dict) and "Heartbeat" in order_data and "OrderID" not in order_data:
                continue

            try:
                order = validate_model(
                    OrderStream,
                    order_data,
                    operation="stream_orders",
                    endpoint=endpoint,
                    mode=mode,
                    source="response",
                )
                yield order
            except Exception as e:
                logger.warning(f"Failed to parse order data: {e}, raw data: {order_data}")
                raise

    async def _poll_orders_rest(self, account_id: str, mode: str, interval: float) -> AsyncGenerator[OrderStream, None]:
        """REST polling fallback for orders."""
        from .accounts import AccountOperations
        from .orders import OrderOperations

        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        # OrderOperations requires AccountOperations
        accounts_ops = AccountOperations(self._api_client, account_id, mode)
        orders_ops = OrderOperations(self._api_client, accounts_ops, account_id, mode)

        logger.info(f"Using REST polling fallback for orders (interval: {interval}s)")

        while True:
            try:
                orders_response = orders_ops.get_current_orders(account_ids=account_id, mode=mode)
                orders = orders_response.get("Orders", [])

                for order_dict in orders:
                    yield validate_model(
                        OrderStream,
                        order_dict,
                        operation="poll_orders_rest",
                        endpoint=f"brokerage/accounts/{account_id}/orders",
                        mode=mode,
                        source="response",
                    )

                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Order REST polling fallback failed for account_id=%s mode=%s", account_id, mode)
                await asyncio.sleep(interval)

    async def stream_positions(
        self,
        account_id: str,
        mode: str | None = None,
        max_retries: int = 10,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        auto_reconnect: bool = True,
        fallback_to_polling: bool = True,
        polling_interval: float = 5.0,
    ) -> AsyncGenerator[PositionStream, None]:
        """
        Stream position updates via TradeStation HTTP Streaming API with automatic reconnection and retry.

        Args:
            account_id: TradeStation account ID
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            max_retries: Maximum number of retry attempts (default: 10)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            max_retry_delay: Maximum retry delay in seconds (default: 60.0)
            auto_reconnect: Enable automatic reconnection on errors (default: True)
            fallback_to_polling: Enable REST polling fallback if streaming fails (default: True)
            polling_interval: Interval for REST polling in seconds (default: 5.0)

        Yields:
            PositionStream: Parsed position update data as Pydantic models

        Dependencies: HTTPClient.stream_data, PositionStream

        Raises:
            NonRecoverableError: For authentication/validation failures.
            Exception: After retries are exhausted and fallback is disabled or fails.
        """
        if mode is None:
            mode = sdk_config.trading_mode

        async def _get_stream():
            """Create the position stream generator."""
            try:
                async for position in self._stream_positions_internal(account_id, mode):
                    yield position
            except StreamGoAwayError:
                raise
            except Exception as e:
                if fallback_to_polling and _is_recoverable_stream_error(e):
                    logger.warning(
                        "HTTP position streaming failed for account_id=%s; falling back to REST polling",
                        account_id,
                        exc_info=True,
                    )
                    async for position in self._poll_positions_rest(account_id, mode, polling_interval):
                        yield position
                else:
                    raise

        async for position in self._with_retry(
            stream_type="positions",
            stream_func=_get_stream,
            max_retries=max_retries,
            retry_delay=retry_delay,
            max_retry_delay=max_retry_delay,
            auto_reconnect=auto_reconnect,
            mode=mode,
        ):
            yield position

    async def _stream_positions_internal(self, account_id: str, mode: str) -> AsyncGenerator[PositionStream, None]:
        """Internal method to stream positions via HTTP Streaming (no retry logic)."""
        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        endpoint = f"brokerage/stream/accounts/{account_id}/positions"
        logger.info(f"Starting position stream for account {account_id} via HTTP Streaming")

        position_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous position stream in background thread via HTTPClient.stream_data."""
            try:
                for position_data in self._api_client.stream_data(endpoint, params=None, mode=mode):
                    position_queue.put(position_data)
                position_queue.put(None)
            except Exception as e:
                logger.exception("Position stream worker failed for endpoint=%s mode=%s", endpoint, mode)
                stream_error[0] = e
                position_queue.put(None)

        stream_thread = threading.Thread(target=run_stream, daemon=True)
        stream_thread.start()

        while True:
            position_data = await _get_stream_queue_item(position_queue, stream_error, "position")
            if position_data is _QUEUE_TIMEOUT:
                continue

            if position_data is None:
                if stream_error[0]:
                    raise stream_error[0]
                break

            if _handle_stream_control_payload(
                position_data,
                stream_type="position",
                operation="stream_positions",
                endpoint=endpoint,
                mode=mode,
            ):
                continue

            if isinstance(position_data, dict) and "Heartbeat" in position_data and "PositionID" not in position_data:
                continue

            try:
                position = validate_model(
                    PositionStream,
                    position_data,
                    operation="stream_positions",
                    endpoint=endpoint,
                    mode=mode,
                    source="response",
                )
                yield position
            except Exception as e:
                logger.warning(f"Failed to parse position data: {e}, raw data: {position_data}")
                raise

    async def _poll_positions_rest(
        self, account_id: str, mode: str, interval: float
    ) -> AsyncGenerator[PositionStream, None]:
        """REST polling fallback for positions."""
        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        logger.info(f"Using REST polling fallback for positions (interval: {interval}s)")

        while True:
            try:
                endpoint = f"brokerage/accounts/{account_id}/positions"
                response = self._api_client.make_request("GET", endpoint, mode=mode)
                parsed = validate_model(
                    PositionsResponse,
                    response,
                    operation="poll_positions_rest",
                    endpoint=endpoint,
                    mode=mode,
                    source="response",
                )

                for position in parsed.Positions:
                    yield validate_model(
                        PositionStream,
                        position.model_dump(exclude_none=True),
                        operation="poll_positions_rest",
                        endpoint=endpoint,
                        mode=mode,
                        source="response",
                    )

                await asyncio.sleep(interval)
            except asyncio.CancelledError:
                break
            except Exception:
                logger.exception("Position REST polling fallback failed for account_id=%s mode=%s", account_id, mode)
                await asyncio.sleep(interval)

    async def stream_balances(
        self,
        account_id: str,
        mode: str | None = None,
        max_retries: int = 10,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        auto_reconnect: bool = True,
    ) -> AsyncGenerator[BalanceStream, None]:
        """
        Stream real-time account balance updates via TradeStation HTTP Streaming API with automatic reconnection and retry.

        Args:
            account_id: TradeStation account ID
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            max_retries: Maximum number of retry attempts (default: 10)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            max_retry_delay: Maximum retry delay in seconds (default: 60.0)
            auto_reconnect: Enable automatic reconnection on errors (default: True)

        Yields:
            BalanceStream: Parsed balance updates as Pydantic models

        Dependencies: HTTPClient.stream_data

        Note: TradeStation API endpoint: GET /v3/brokerage/stream/accounts/{accountId}/balances

        Raises:
            NonRecoverableError: For authentication/validation failures.
            Exception: After retries are exhausted.
        """
        if mode is None:
            mode = sdk_config.trading_mode

        async def _get_stream():
            """Create the balance stream generator."""
            async for balance in self._stream_balances_internal(account_id, mode):
                yield balance

        async for balance in self._with_retry(
            stream_type="balances",
            stream_func=_get_stream,
            max_retries=max_retries,
            retry_delay=retry_delay,
            max_retry_delay=max_retry_delay,
            auto_reconnect=auto_reconnect,
            mode=mode,
        ):
            yield balance

    async def _stream_balances_internal(self, account_id: str, mode: str) -> AsyncGenerator[BalanceStream, None]:
        """Internal method to stream balances via HTTP Streaming (no retry logic)."""
        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        endpoint = f"brokerage/stream/accounts/{account_id}/balances"
        logger.info(f"Starting balance stream for account {account_id} via HTTP Streaming")

        balance_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous balance stream in background thread via HTTPClient.stream_data."""
            try:
                for balance_data in self._api_client.stream_data(endpoint, params=None, mode=mode):
                    balance_queue.put(balance_data)
                balance_queue.put(None)
            except Exception as e:
                logger.exception("Balance stream worker failed for endpoint=%s mode=%s", endpoint, mode)
                stream_error[0] = e
                balance_queue.put(None)

        stream_thread = threading.Thread(target=run_stream, daemon=True)
        stream_thread.start()

        while True:
            balance_data = await _get_stream_queue_item(balance_queue, stream_error, "balance")
            if balance_data is _QUEUE_TIMEOUT:
                continue

            if balance_data is None:
                if stream_error[0]:
                    raise stream_error[0]
                break

            if _handle_stream_control_payload(
                balance_data,
                stream_type="balance",
                operation="stream_balances",
                endpoint=endpoint,
                mode=mode,
            ):
                continue

            # Filter out heartbeats
            if isinstance(balance_data, dict) and "Heartbeat" in balance_data and "AccountID" not in balance_data:
                continue

            # Parse and yield BalanceStream model
            try:
                balance = validate_model(
                    BalanceStream,
                    balance_data,
                    operation="stream_balances",
                    endpoint=endpoint,
                    mode=mode,
                    source="response",
                )
                yield balance
            except Exception as e:
                logger.warning(f"Failed to parse balance data: {e}, raw data: {balance_data}")
                raise

    async def stream_orders_by_ids(
        self,
        account_ids: str,
        order_ids: str,
        mode: str | None = None,
        max_retries: int = 10,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        auto_reconnect: bool = True,
    ) -> AsyncGenerator[OrderStream, None]:
        """
        Stream specific orders by order ID(s) via TradeStation HTTP Streaming API with automatic reconnection and retry.

        Args:
            account_ids: Comma-separated account IDs (e.g., "123456782,123456789")
            order_ids: Comma-separated order IDs (e.g., "812767578,812941051")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            max_retries: Maximum number of retry attempts (default: 10)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            max_retry_delay: Maximum retry delay in seconds (default: 60.0)
            auto_reconnect: Enable automatic reconnection on errors (default: True)

        Yields:
            OrderStream: Parsed order update data as Pydantic models

        Dependencies: HTTPClient.stream_data, OrderStream

        Note: TradeStation API endpoint: GET /v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}
        """
        if mode is None:
            mode = sdk_config.trading_mode

        async def _get_stream():
            """Create the order stream by IDs generator."""
            async for order in self._stream_orders_by_ids_internal(account_ids, order_ids, mode):
                yield order

        async for order in self._with_retry(
            stream_type="orders_by_ids",
            stream_func=_get_stream,
            max_retries=max_retries,
            retry_delay=retry_delay,
            max_retry_delay=max_retry_delay,
            auto_reconnect=auto_reconnect,
            mode=mode,
        ):
            yield order

    async def _stream_orders_by_ids_internal(
        self, account_ids: str, order_ids: str, mode: str
    ) -> AsyncGenerator[OrderStream, None]:
        """Internal method to stream orders by IDs via HTTP Streaming (no retry logic)."""
        if not self._api_client:
            self._api_client = HTTPClient(self.token_manager)

        endpoint = f"brokerage/stream/accounts/{account_ids}/orders/{order_ids}"
        logger.info(f"Starting order stream by IDs: accounts={account_ids}, orders={order_ids} via HTTP Streaming")

        order_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous order stream (by IDs) in background thread via HTTPClient.stream_data."""
            try:
                for order_data in self._api_client.stream_data(endpoint, params=None, mode=mode):
                    order_queue.put(order_data)
                order_queue.put(None)
            except Exception as e:
                logger.exception("Order-by-id stream worker failed for endpoint=%s mode=%s", endpoint, mode)
                stream_error[0] = e
                order_queue.put(None)

        stream_thread = threading.Thread(target=run_stream, daemon=True)
        stream_thread.start()

        while True:
            order_data = await _get_stream_queue_item(order_queue, stream_error, "order-by-id")
            if order_data is _QUEUE_TIMEOUT:
                continue

            if order_data is None:
                if stream_error[0]:
                    raise stream_error[0]
                break

            if _handle_stream_control_payload(
                order_data,
                stream_type="order-by-id",
                operation="stream_orders_by_ids",
                endpoint=endpoint,
                mode=mode,
            ):
                continue

            if isinstance(order_data, dict) and "Heartbeat" in order_data and "OrderID" not in order_data:
                continue

            try:
                order = validate_model(
                    OrderStream,
                    order_data,
                    operation="stream_orders_by_ids",
                    endpoint=endpoint,
                    mode=mode,
                    source="response",
                )
                yield order
            except Exception as e:
                logger.warning(f"Failed to parse order data: {e}, raw data: {order_data}")
                raise


# Backward-compatible alias used across the project while we migrate terminology
WebSocketManager = StreamingManager

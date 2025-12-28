"""
Position Operations

Provides helpers to query positions, compute P&L, flatten holdings, and stream
real-time position updates. All methods are mode-aware (PAPER/LIVE) and
normalize API responses for downstream services.

Dependencies: typing, Optional
"""

from collections.abc import AsyncGenerator
from typing import Any

from .accounts import AccountOperations
from .client import HTTPClient
from .config import sdk_config
from .exceptions import TradeStationAPIError
from .logger import setup_logger
from .models import PositionsResponse

logger = setup_logger(__name__, sdk_config.log_level)


class PositionOperations:
    """
    Position-related API operations.

    Responsibilities:
    - Query single or all positions for an account
    - Compute today's and unrealized P&L
    - Flatten (close) one or all positions via order execution
    - Stream live position updates over HTTP streaming

    Modes:
    - Supports PAPER and LIVE; defaults to `sdk_config.trading_mode` unless overridden.
    """

    def __init__(
        self,
        client: HTTPClient,
        accounts: AccountOperations,
        account_id: str | None = None,
        default_mode: str | None = None,
    ):
        """
        Initialize position operations.

        Args:
            client: HTTPClient instance for making requests
            accounts: AccountOperations instance for account ID lookup
            account_id: Default account ID (can be overridden per request)
            default_mode: Default trading mode (PAPER/LIVE). If None, uses sdk_config.trading_mode
        """
        self.client = client
        self.accounts = accounts
        self.account_id = account_id
        # Store default mode - will be used when mode=None is passed to functions
        self.default_mode = default_mode or sdk_config.trading_mode

    def get_position(self, symbol: str, mode: str | None = None) -> int:
        """
        Get current position quantity for a symbol.

        Args:
            symbol: Futures symbol to check
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Position quantity (positive for long, negative for short, 0 for flat)

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info
        """
        if mode is None:
            mode = self.default_mode
        # Get account ID for the specified mode
        account_info = self.accounts.get_account_info(mode)
        account_id = account_info.get("account_id") or self.account_id

        endpoint = f"brokerage/accounts/{account_id}/positions"
        response = self.client.make_request("GET", endpoint, mode=mode)
        parsed = PositionsResponse(**response)

        positions = parsed.Positions
        positions_dicts = [p.model_dump() if hasattr(p, "model_dump") else p for p in positions]

        for pos in positions_dicts:
            if pos.get("Symbol") == symbol:
                quantity = int(float(pos.get("Quantity", 0)))
                logger.debug(f"Current position for {symbol}: {quantity}")
                return quantity

        logger.debug(f"No position found for {symbol}")
        return 0

    def get_all_positions(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get all current positions across all symbols.

        Args:
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            List of position dictionaries with Symbol and Quantity

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info
        """
        if mode is None:
            mode = self.default_mode
        # Get account ID for the specified mode
        account_info = self.accounts.get_account_info(mode)
        account_id = account_info.get("account_id") or self.account_id

        endpoint = f"brokerage/accounts/{account_id}/positions"
        response = self.client.make_request("GET", endpoint, mode=mode)
        parsed = PositionsResponse(**response)

        positions = parsed.Positions
        positions_dicts = [p.model_dump() if hasattr(p, "model_dump") else p for p in positions]

        # Filter out zero positions and format
        active_positions = []
        for pos in positions_dicts:
            quantity = int(float(pos.get("Quantity", 0)))
            if quantity != 0:
                active_positions.append({"symbol": pos.get("Symbol"), "quantity": quantity})

        return active_positions

    def flatten_position(
        self, symbol: str | None = None, order_operations=None, mode: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Close all positions. If symbol is provided, only flattens that symbol.
        Otherwise, flattens all positions across all symbols.

        Args:
            symbol: Optional symbol to flatten (if None, flattens all positions)
            order_operations: OrderOperations instance for placing orders (required for flattening)
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            List of dictionaries with order_id, symbol, side, quantity for each flattened position

        Dependencies: get_all_positions, get_position, OrderOperations.place_order
        """
        if mode is None:
            mode = self.default_mode
        if order_operations is None:
            logger.error("flatten_position requires order_operations parameter")
            return []

        if symbol:
            # Flatten single symbol
            current_position = self.get_position(symbol, mode)
            if current_position == 0:
                logger.info(f"No position to flatten for {symbol}")
                return []

            side = "SELL" if current_position > 0 else "BUY"
            quantity = abs(current_position)

            logger.info(f"Flattening position: {side} {quantity} {symbol}")
            order_id, status = order_operations.place_order(symbol, side, quantity, mode=mode)

            if order_id:
                return [{"order_id": order_id, "symbol": symbol, "side": side, "quantity": quantity, "status": status}]
            return []
        # Flatten all positions
        all_positions = self.get_all_positions(mode)
        if not all_positions:
            logger.info("No positions to flatten")
            return []

        logger.info(f"Flattening {len(all_positions)} position(s) across all symbols")
        flattened = []

        for pos in all_positions:
            pos_symbol = pos["symbol"]
            pos_quantity = pos["quantity"]
            side = "SELL" if pos_quantity > 0 else "BUY"
            quantity = abs(pos_quantity)

            logger.info(f"  Flattening {pos_symbol}: {side} {quantity}")
            order_id, status = order_operations.place_order(pos_symbol, side, quantity, mode=mode)

            if order_id:
                flattened.append(
                    {"order_id": order_id, "symbol": pos_symbol, "side": side, "quantity": quantity, "status": status}
                )

        if flattened:
            logger.info(f"✅ Flattened {len(flattened)} position(s)")
        else:
            logger.warning("⚠️  Failed to flatten some positions")

        return flattened

    async def stream_positions(
        self, account_id: str | None = None, mode: str | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream position updates via TradeStation HTTP Streaming API.

        Args:
            account_id: TradeStation account ID (optional)
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Yields:
            Position update dictionaries
        """
        if mode is None:
            mode = self.default_mode

        if not account_id:
            account_info = self.accounts.get_account_info(mode)
            account_id = account_info.get("account_id") or self.account_id

        if not account_id:
            raise ValueError("Account ID required for streaming positions")

        # TradeStation API v3 endpoint: brokerage/stream/accounts/{accountIds}/positions
        endpoint = f"brokerage/stream/accounts/{account_id}/positions"

        logger.info(f"Starting position stream for account {account_id} via HTTP Streaming")

        async for data in self._stream_helper(endpoint, mode=mode):
            yield data

    async def _stream_helper(
        self, endpoint: str, params: dict | None = None, mode: str | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Helper for async streaming"""
        import asyncio
        import queue
        import threading

        data_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous position stream in a background thread using HTTPClient.stream_data."""
            try:
                for data in self.client.stream_data(endpoint, params=params, mode=mode):
                    data_queue.put(data)
                data_queue.put(None)
            except Exception as e:
                stream_error[0] = e
                data_queue.put(None)

        stream_thread = threading.Thread(target=run_stream, daemon=True)
        stream_thread.start()

        while True:
            try:
                try:
                    data = data_queue.get_nowait()
                except queue.Empty:
                    if stream_error[0]:
                        raise stream_error[0]
                    await asyncio.sleep(0.01)
                    continue

                if data is None:
                    if stream_error[0]:
                        raise stream_error[0]
                    break

                if isinstance(data, dict) and "StreamStatus" in data:
                    continue

                yield data
            except Exception as e:
                logger.error(f"Stream error: {e}")
                raise

    def get_todays_profit_loss(self, mode: str | None = None) -> float:
        """
        Get today's profit and loss across all positions.

        Args:
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Total today's P&L as float (sum of TodaysProfitLoss from all positions)

        Dependencies: get_all_positions, HTTPClient.make_request, AccountOperations.get_account_info
        """
        try:
            if mode is None:
                mode = self.default_mode
            # Get account ID for the specified mode
            account_info = self.accounts.get_account_info(mode)
            account_id = account_info.get("account_id") or self.account_id

            endpoint = f"brokerage/accounts/{account_id}/positions"
            response = self.client.make_request("GET", endpoint, mode=mode)
            parsed = PositionsResponse(**response)

            positions = parsed.Positions
            positions_dicts = [p.model_dump() if hasattr(p, "model_dump") else p for p in positions]

            total_pnl = 0.0
            for pos in positions_dicts:
                todays_pnl = pos.get("TodaysProfitLoss")
                if todays_pnl is not None:
                    try:
                        total_pnl += float(todays_pnl)
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid TodaysProfitLoss value for {pos.get('Symbol')}: {todays_pnl}")

            logger.info(f"Today's total P&L: ${total_pnl:.2f}")
            return total_pnl

        except TradeStationAPIError as e:
            e.details.operation = "get_todays_profit_loss"
            if not e.details.message.startswith("Failed to get today's P&L"):
                e.details.message = f"Failed to get today's P&L: {e.details.message}"
            logger.error(f"Failed to get today's P&L: {e.details.to_human_readable()}", exc_info=True)
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get today's P&L: {e}", exc_info=True)
            return 0.0

    def get_todays_trades(self, order_operations=None, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get today's filled trades (orders that were filled today).

        Args:
            order_operations: OrderOperations instance (required to query order history)
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            List of filled order dictionaries from today (status FLL or FLP)

        Dependencies: OrderOperations.get_order_history

        Note: Requires OrderOperations instance to be passed to avoid circular dependencies.
        """
        try:
            from datetime import datetime

            if order_operations is None:
                logger.error("get_todays_trades requires order_operations parameter")
                return []

            if mode is None:
                mode = self.default_mode

            # Get today's date
            today = datetime.now().strftime("%Y-%m-%d")

            # Get today's order history
            orders = order_operations.get_order_history(start_date=today, end_date=today, limit=1000, mode=mode)

            # Filter for filled orders (FLL = Filled, FLP = Partial Fill)
            filled_trades = []
            for order in orders:
                status = order.get("Status", "").upper()
                if status in ["FLL", "FLP"]:
                    filled_trades.append(order)

            logger.info(f"Found {len(filled_trades)} filled trade(s) today")
            return filled_trades

        except Exception as e:
            logger.error(f"Failed to get today's trades: {e}", exc_info=True)
            return []

    def get_unrealized_profit_loss(self, mode: str | None = None) -> float:
        """
        Get unrealized profit and loss across all positions.

        Args:
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Total unrealized P&L as float (sum of UnrealizedProfitLoss from all positions)

        Dependencies: get_all_positions, HTTPClient.make_request, AccountOperations.get_account_info
        """
        try:
            if mode is None:
                mode = self.default_mode
            # Get account ID for the specified mode
            account_info = self.accounts.get_account_info(mode)
            account_id = account_info.get("account_id") or self.account_id

            endpoint = f"brokerage/accounts/{account_id}/positions"
            response = self.client.make_request("GET", endpoint, mode=mode)
            parsed = PositionsResponse(**response)

            positions = parsed.Positions
            positions_dicts = [p.model_dump() if hasattr(p, "model_dump") else p for p in positions]

            total_unrealized_pnl = 0.0
            for pos in positions_dicts:
                unrealized_pnl = pos.get("UnrealizedProfitLoss")
                if unrealized_pnl is not None:
                    try:
                        total_unrealized_pnl += float(unrealized_pnl)
                    except (ValueError, TypeError):
                        logger.warning(f"Invalid UnrealizedProfitLoss value for {pos.get('Symbol')}: {unrealized_pnl}")

            logger.info(f"Total unrealized P&L: ${total_unrealized_pnl:.2f}")
            return total_unrealized_pnl

        except TradeStationAPIError as e:
            e.details.operation = "get_unrealized_profit_loss"
            if not e.details.message.startswith("Failed to get unrealized P&L"):
                e.details.message = f"Failed to get unrealized P&L: {e.details.message}"
            logger.error(f"Failed to get unrealized P&L: {e.details.to_human_readable()}", exc_info=True)
            return 0.0
        except Exception as e:
            logger.error(f"Failed to get unrealized P&L: {e}", exc_info=True)
            return 0.0

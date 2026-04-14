"""
Market Data Operations

Provides typed helpers for historical bars, symbol discovery, quotes, options
metadata, and streaming endpoints. Each method is mode-aware (PAPER/LIVE) and
normalizes TradeStation API responses to dictionaries for downstream services.

Dependencies: typing
"""

from collections.abc import AsyncGenerator
from typing import Any

from .logger import setup_logger

from .client import HTTPClient
from .config import sdk_config
from .exceptions import TradeStationAPIError
from .models import QuotesResponse
from .validation import dump_model, raise_unexpected_error, validate_model

logger = setup_logger(__name__, sdk_config.log_level)


class MarketDataOperations:
    """
    Market data-related API operations.

    Responsibilities:
    - Historical bars (OHLCV) retrieval
    - Symbol search and curated futures index lists
    - Quote snapshots and symbol metadata
    - Options metadata (expirations, strikes, spread types, risk/reward)
    - Crypto symbol lists
    - Streaming quotes/bars/options/depth over HTTP streaming
    """

    def __init__(self, client: HTTPClient):
        """
        Initialize market data operations.

        Args:
            client: HTTPClient instance for making requests
        """
        self.client = client

    def get_bars(
        self,
        symbol: str,
        interval: str,
        unit: str,
        bars_back: int | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        session_template: str | None = None,
        mode: str | None = None,
        start_date_deprecated: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Fetch historical bar data for a symbol.

        Args:
            symbol: Symbol (e.g., MESZ5 for futures or AAPL for US equities)
            interval: Time interval (e.g., "30" for 30 seconds/minutes)
            unit: Bar unit ("Minute", "Daily", "Weekly", "Monthly")
            bars_back: Number of historical bars to fetch (mutually exclusive with start_date/start_date_deprecated)
            start_date: Start date in ISO format (YYYY-MM-DDTHH:MM:SSZ) → sent as `firstdate`
            end_date: End date in ISO format (YYYY-MM-DDTHH:MM:SSZ) → sent as `lastdate`
            session_template: US equity session template to include pre/post/24h bars (USEQPre, USEQPost, USEQPreAndPost, USEQ24Hour, Default). Ignored for non-US equity symbols.
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            start_date_deprecated: Deprecated API parameter `startdate` (mutually exclusive with bars_back/lastdate)

        Returns:
            List of bar dictionaries with OHLCV data

        Dependencies: HTTPClient.make_request

        Raises:
            TradeStationAPIError: For API-level errors (auth/validation/etc.)
            Exception: For unexpected errors when parsing response
        """
        endpoint = f"marketdata/barcharts/{symbol}"
        params = {"interval": interval, "unit": unit}
        allowed_templates = {"USEQPre", "USEQPost", "USEQPreAndPost", "USEQ24Hour", "Default"}

        if start_date_deprecated:
            params["startdate"] = start_date_deprecated
        if start_date:
            params["firstdate"] = start_date
            if end_date:
                params["lastdate"] = end_date
        elif bars_back:
            params["barsback"] = bars_back
        else:
            # Default to 200 bars back if nothing specified
            params["barsback"] = 200

        if session_template:
            if session_template in allowed_templates:
                params["sessiontemplate"] = session_template
            else:
                logger.warning(
                    "Ignoring unsupported session_template '%s' for symbol=%s; allowed=%s",
                    session_template,
                    symbol,
                    sorted(allowed_templates),
                )

        logger.debug(
            "Fetching bars for symbol=%s interval=%s unit=%s params=%s sessiontemplate=%s mode=%s",
            symbol,
            interval,
            unit,
            params,
            session_template or "default",
            mode or sdk_config.trading_mode,
        )
        response = self.client.make_request("GET", endpoint, params=params, mode=mode)
        bars = response.get("Bars", [])
        logger.debug(
            "Received %s bars for symbol=%s interval=%s unit=%s sessiontemplate=%s",
            len(bars),
            symbol,
            interval,
            unit,
            session_template or "default",
        )
        return bars

    def search_symbols(
        self, pattern: str = "", category: str | None = "Future", asset_type: str | None = None, mode: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Search for symbols matching criteria.

        Args:
            pattern: Symbol pattern to search (e.g., "MNQ", "ES")
            category: Symbol category (e.g., "Future", "Stock", "Option")
            asset_type: Asset type filter (e.g., "Index", "Equity")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of symbol dictionaries with symbol details

        Dependencies: HTTPClient.make_request
        """
        endpoint = "marketdata/symbols/search"
        params = {}

        # TradeStation API doesn't accept "*" as a pattern - it returns "invalid symbol" error
        # If pattern is empty, we need a valid pattern or use a different approach
        if not pattern or pattern == "*":
            # For empty pattern with Future category, use get_futures_index_symbols instead
            # This avoids infinite recursion since get_futures_index_symbols() calls API directly
            if category == "Future" and not asset_type:
                logger.debug("Empty pattern with Future category - delegating to get_futures_index_symbols()")
                return self.get_futures_index_symbols(mode=mode)
            # For other cases, use a common pattern that works (e.g., "MNQ" for futures)
            pattern = "MNQ" if category == "Future" else ""

        if pattern:
            params["pattern"] = pattern
        if category:
            params["category"] = category
        # Remove assetType filter when empty to get the full futures list.
        if asset_type:
            params["assetType"] = asset_type

        try:
            logger.debug(f"Searching symbols: pattern={pattern}, category={category}, assetType={asset_type}")
            response = self.client.make_request("GET", endpoint, params=params, mode=mode)
            symbols = response.get("Symbols", [])

            # Check for API errors in response
            errors = response.get("Errors", [])
            if errors:
                for error in errors:
                    if error.get("Error") == "NotFound" and "invalid symbol" in error.get("Message", ""):
                        logger.debug(
                            f"API returned invalid symbol error for pattern '{pattern}' - returning empty list"
                        )
                        return []

            logger.debug(f"Found {len(symbols)} symbols matching criteria")
            return symbols
        except TradeStationAPIError as e:
            e.details.operation = "search_symbols"
            if not e.details.message.startswith("Failed to search symbols"):
                e.details.message = f"Failed to search symbols: {e.details.message}"
            logger.error(f"Failed to search symbols: {e.details.to_human_readable()}")
            raise
        except Exception as e:
            logger.error(f"Failed to search symbols: {e}", exc_info=True)
            raise_unexpected_error(operation="search_symbols", endpoint=endpoint, mode=mode, exc=e)

    def get_futures_index_symbols(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get list of available futures index symbols (broad).

        Uses category=Future without assetType filter to avoid empty results
        from TradeStation, then filters to common index futures by base symbol.

        Note: This method calls the API directly to avoid infinite recursion with search_symbols().
        If the API requires a pattern, we query multiple common patterns and aggregate results.
        """
        endpoint = "marketdata/symbols/search"
        common_futures = ["MNQ", "MES", "MYM", "M2K", "NQ", "ES", "YM", "RTY"]

        # TradeStation API requires a pattern parameter - cannot call without pattern
        # Query each common base symbol and aggregate results
        all_symbols = []
        last_error: Exception | None = None
        common_futures = ["MNQ", "MES", "MYM", "M2K", "NQ", "ES", "YM", "RTY"]

        for base_symbol in common_futures:
            params = {"pattern": base_symbol, "category": "Future"}
            try:
                logger.debug(f"Fetching futures symbols from API: params={params}, mode={mode}")
                response = self.client.make_request("GET", endpoint, params=params, mode=mode)
                symbols = response.get("Symbols", [])

                # Check for API errors in response
                errors = response.get("Errors", [])
                if errors:
                    for error in errors:
                        error_msg = error.get("Message", "")
                        error_symbol = error.get("Symbol", "")
                        # Skip "invalid symbol" errors for this pattern and continue to next
                        if "invalid symbol" in error_msg.lower():
                            logger.debug(
                                f"TradeStation rejected pattern '{base_symbol}': {error_msg} (Symbol: {error_symbol})"
                            )
                            break
                else:
                    # No errors, add symbols (avoid duplicates)
                    for symbol in symbols:
                        if symbol not in all_symbols:
                            all_symbols.append(symbol)

            except TradeStationAPIError as e:
                last_error = e
                logger.debug(f"Failed to fetch symbols for pattern '{base_symbol}': {e}")
                continue
            except Exception as e:
                last_error = e
                logger.debug(f"Failed to fetch symbols for pattern '{base_symbol}': {e}")
                continue

        # Deduplicate symbols by Symbol field
        seen_symbols = {}
        for symbol_info in all_symbols:
            symbol = symbol_info.get("Symbol", "")
            if symbol:
                seen_symbols[symbol] = symbol_info

        all_symbols = list(seen_symbols.values())

        if not all_symbols:
            if last_error is not None:
                if isinstance(last_error, TradeStationAPIError):
                    last_error.details.operation = "get_futures_index_symbols"
                    if not last_error.details.message.startswith("Failed to get futures index symbols"):
                        last_error.details.message = f"Failed to get futures index symbols: {last_error.details.message}"
                    logger.error(f"Failed to get futures index symbols: {last_error.details.to_human_readable()}")
                    raise last_error
                raise_unexpected_error(
                    operation="get_futures_index_symbols",
                    endpoint=endpoint,
                    mode=mode,
                    exc=last_error,
                )
            logger.warning("Failed to fetch futures symbols from API, returning empty list")
            return []

        # Filter to common futures index symbols (already filtered if we used patterns)
        month_codes = "FGHJKMNQUVXZ"
        filtered = []

        for symbol_info in all_symbols:
            symbol = symbol_info.get("Symbol", "")
            base_symbol = ""
            if len(symbol) >= 3:
                for i in range(min(4, len(symbol))):
                    if symbol[i] in month_codes:
                        base_symbol = symbol[:i]
                        break
                else:
                    base_symbol = symbol[:3]

            if base_symbol in common_futures:
                filtered.append(symbol_info)

        logger.debug(f"Filtered {len(filtered)} common futures from {len(all_symbols)} total futures")
        return filtered

    async def stream_quotes(self, symbols: list[str], mode: str | None = None) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream quotes via TradeStation HTTP Streaming API.

        Args:
            symbols: List of symbols to stream
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Yields:
            Quote dictionaries as they arrive
        """
        if mode is None:
            mode = sdk_config.trading_mode

        # TradeStation API v3 endpoint: marketdata/stream/quotes/{symbols}
        symbols_param = ",".join(symbols)
        endpoint = f"marketdata/stream/quotes/{symbols_param}"

        logger.info(f"Starting quote stream for {len(symbols)} symbol(s) via HTTP Streaming")

        async for data in self._stream_helper(endpoint, mode=mode):
            yield data

    async def stream_bars(
        self,
        symbol: str,
        interval: str,
        unit: str,
        session_template: str | None = None,
        mode: str | None = None,
        bars_back: int | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream bars via TradeStation HTTP Streaming API.

        Args:
            symbol: Symbol to stream bars for
            interval: Time interval (e.g., "1", "5")
            unit: "Minute", "Daily", "Weekly", "Monthly"
            session_template: US equity session template to include pre/post/24h bars (USEQPre, USEQPost, USEQPreAndPost, USEQ24Hour, Default). Ignored for non-US equity symbols.
            mode: "PAPER" or "LIVE"
            bars_back: Optional bars back to include in the stream handshake

        Yields:
            Bar dictionaries as they arrive
        Dependencies: HTTPClient.stream_data
        """
        if mode is None:
            mode = sdk_config.trading_mode

        # TradeStation API v3 endpoint: marketdata/stream/barcharts/{symbol}
        endpoint = f"marketdata/stream/barcharts/{symbol}"
        params: dict[str, Any] = {"interval": interval, "unit": unit}
        allowed_templates = {"USEQPre", "USEQPost", "USEQPreAndPost", "USEQ24Hour", "Default"}

        if bars_back is not None:
            params["barsback"] = bars_back

        if session_template:
            if session_template in allowed_templates:
                params["sessiontemplate"] = session_template
            else:
                logger.warning(
                    "Ignoring unsupported session_template '%s' for symbol=%s; allowed=%s",
                    session_template,
                    symbol,
                    sorted(allowed_templates),
                )

        logger.info(
            "Starting bar stream for symbol=%s interval=%s unit=%s sessiontemplate=%s barsback=%s mode=%s params=%s",
            symbol,
            interval,
            unit,
            session_template or "default",
            bars_back,
            mode,
            params,
        )

        async for data in self._stream_helper(endpoint, params=params, mode=mode):
            yield data

    # Note: stream_option_chains is defined later with correct signature (underlying parameter)

    async def _stream_helper(
        self, endpoint: str, params: dict | None = None, mode: str | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Helper to bridge synchronous HTTP streaming to async generator.
        """
        import queue
        import threading

        data_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous HTTP stream in background thread (uses HTTPClient.stream_data)."""
            try:
                for data in self.client.stream_data(endpoint, params=params, mode=mode):
                    data_queue.put(data)
                data_queue.put(None)
            except Exception as e:
                logger.exception("Market data stream worker failed for endpoint=%s mode=%s", endpoint, mode)
                stream_error[0] = e
                data_queue.put(None)

        stream_thread = threading.Thread(target=run_stream, daemon=True)
        stream_thread.start()

        while True:
            try:
                # Non-blocking check with small sleep to allow context switching
                try:
                    data = data_queue.get_nowait()
                except queue.Empty:
                    if stream_error[0]:
                        raise stream_error[0]
                    await __import__("asyncio").sleep(0.01)
                    continue

                if data is None:
                    if stream_error[0]:
                        raise stream_error[0]
                    break

                if isinstance(data, dict) and "StreamStatus" in data:
                    continue

                yield data

            except Exception as e:
                logger.exception("Market data async stream bridge failed for endpoint=%s mode=%s", endpoint, mode)
                raise

    def get_quote_snapshots(self, symbols: str, mode: str | None = None) -> dict[str, Any]:
        """
        Get quote snapshots for one or more symbols.

        Fetches a full snapshot of the latest quote data. For real-time updates,
        use the quote stream endpoint instead.

        Args:
            symbols: Comma-separated symbol list (e.g., "MSFT,BTCUSD") - max 100 symbols
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with:
            - Quotes: List of quote dictionaries with full snapshot data
            - Errors: List of error dictionaries (if any)

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/marketdata/quotes/{symbols}
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = f"marketdata/quotes/{symbols}"

            logger.debug(f"Fetching quote snapshots: symbols={symbols}, mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)
            parsed = validate_model(
                QuotesResponse,
                response,
                operation="get_quote_snapshots",
                endpoint=endpoint,
                mode=mode,
                source="response",
            )

            # Convert Pydantic models to dicts for compatibility
            quotes = parsed.Quotes
            quotes_dicts = [dump_model(quote) for quote in quotes]
            errors = parsed.Errors or []

            if errors:
                logger.warning(f"Some symbols returned errors: {errors}")

            logger.info(f"Retrieved quote snapshots for {len(quotes_dicts)} symbol(s) (mode: {mode})")

            return {"Quotes": quotes_dicts, "Errors": errors}

        except TradeStationAPIError as e:
            e.details.operation = "get_quote_snapshots"
            if not e.details.message.startswith("Failed to get quote snapshots"):
                e.details.message = f"Failed to get quote snapshots: {e.details.message}"
            logger.error(f"Failed to get quote snapshots: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Failed to get quote snapshots: {e}", exc_info=True)
            raise_unexpected_error(operation="get_quote_snapshots", endpoint=endpoint, mode=mode, exc=e)

    def get_symbol_details(self, symbols: str, mode: str | None = None) -> dict[str, Any]:
        """
        Get symbol details and formatting information.

        Provides symbol metadata including price formatting, tick size, point value,
        and other display information needed to properly format prices and quantities.

        Args:
            symbols: Comma-separated symbol list (e.g., "MSFT,BTCUSD") - max 50 symbols
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with:
            - Symbols: List of symbol detail dictionaries
            - Errors: List of error dictionaries (if any)

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/marketdata/symbols/{symbols}
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = f"marketdata/symbols/{symbols}"

            logger.debug(f"Fetching symbol details: symbols={symbols}, mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)

            # Response structure: {"Symbols": [...], "Errors": [...]}
            symbol_details = response.get("Symbols", [])
            errors = response.get("Errors", [])

            if errors:
                logger.warning(f"Some symbols returned errors: {errors}")

            logger.info(f"Retrieved symbol details for {len(symbol_details)} symbol(s) (mode: {mode})")

            return {"Symbols": symbol_details, "Errors": errors}

        except TradeStationAPIError as e:
            e.details.operation = "get_symbol_details"
            if not e.details.message.startswith("Failed to get symbol details"):
                e.details.message = f"Failed to get symbol details: {e.details.message}"
            logger.error(f"Failed to get symbol details: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Failed to get symbol details: {e}", exc_info=True)
            raise_unexpected_error(operation="get_symbol_details", endpoint=endpoint, mode=mode, exc=e)

    def get_crypto_symbol_names(self, mode: str | None = None) -> list[str]:
        """
        Get list of available crypto symbol names.

        Returns all available cryptocurrency trading pairs.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of crypto symbol name strings

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/marketdata/symbollists/cryptopairs/symbolnames
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "marketdata/symbollists/cryptopairs/symbolnames"

            logger.debug(f"Fetching crypto symbol names: mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)

            # Response structure: {"SymbolNames": [...]}
            symbol_names = response.get("SymbolNames", [])

            logger.info(f"Retrieved {len(symbol_names)} crypto symbol name(s) (mode: {mode})")

            return symbol_names

        except TradeStationAPIError as e:
            e.details.operation = "get_crypto_symbol_names"
            if not e.details.message.startswith("Failed to get crypto symbol names"):
                e.details.message = f"Failed to get crypto symbol names: {e.details.message}"
            logger.error(f"Failed to get crypto symbol names: {e.details.to_human_readable()}")
            raise
        except Exception as e:
            logger.error(f"Failed to get crypto symbol names: {e}", exc_info=True)
            raise_unexpected_error(operation="get_crypto_symbol_names", endpoint=endpoint, mode=mode, exc=e)

    def get_option_expirations(
        self, underlying: str, mode: str | None = None, strike_price: float | None = None
    ) -> list[str]:
        """
        Get option expiration dates for an underlying symbol.

        Args:
            underlying: Underlying symbol (e.g., "MSFT")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            strike_price: Optional strike price filter per API

        Returns:
            List of expiration date strings (ISO format)

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/marketdata/options/expirations/{underlying}
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = f"marketdata/options/expirations/{underlying}"
            params: dict[str, Any] = {}
            if strike_price is not None:
                params["strikePrice"] = strike_price

            logger.debug(
                "Fetching option expirations: underlying=%s strike_price=%s mode=%s",
                underlying,
                strike_price,
                mode,
            )
            response = self.client.make_request("GET", endpoint, params=params or None, mode=mode)

            # Response structure: {"Expirations": [...]}
            expirations = response.get("Expirations", [])

            logger.info(
                "Retrieved %s expiration date(s) for %s (mode: %s params=%s)",
                len(expirations),
                underlying,
                mode,
                params or {},
            )

            return expirations

        except TradeStationAPIError as e:
            e.details.operation = "get_option_expirations"
            if not e.details.message.startswith("Failed to get option expirations"):
                e.details.message = f"Failed to get option expirations: {e.details.message}"
            logger.error(f"Failed to get option expirations: {e.details.to_human_readable()}")
            raise
        except Exception as e:
            logger.error(f"Failed to get option expirations: {e}", exc_info=True)
            raise_unexpected_error(operation="get_option_expirations", endpoint=endpoint, mode=mode, exc=e)

    def get_option_risk_reward(self, request: dict[str, Any], mode: str | None = None) -> dict[str, Any]:
        """
        Calculate option risk/reward analysis.

        Args:
            request: OptionRiskRewardRequest dictionary with option details
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with risk/reward calculations

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: POST /v3/marketdata/options/riskreward
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "marketdata/options/riskreward"

            logger.debug(f"Calculating option risk/reward: mode={mode}")
            response = self.client.make_request("POST", endpoint, json_data=request, mode=mode)

            logger.info(f"Option risk/reward calculation successful (mode: {mode})")

            return response

        except Exception as e:
            logger.error(f"Failed to calculate option risk/reward: {e}", exc_info=True)
            raise_unexpected_error(operation="get_option_risk_reward", endpoint=endpoint, mode=mode, exc=e)

    def get_option_spread_types(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get available option spread types.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of spread type dictionaries

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/marketdata/options/spreadtypes
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "marketdata/options/spreadtypes"

            logger.debug(f"Fetching option spread types: mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)

            # Response structure: {"SpreadTypes": [...]}
            spread_types = response.get("SpreadTypes", [])

            logger.info(f"Retrieved {len(spread_types)} spread type(s) (mode: {mode})")

            return spread_types

        except TradeStationAPIError as e:
            e.details.operation = "get_option_spread_types"
            if not e.details.message.startswith("Failed to get option spread types"):
                e.details.message = f"Failed to get option spread types: {e.details.message}"
            logger.error(f"Failed to get option spread types: {e.details.to_human_readable()}")
            raise
        except Exception as e:
            logger.error(f"Failed to get option spread types: {e}", exc_info=True)
            raise_unexpected_error(operation="get_option_spread_types", endpoint=endpoint, mode=mode, exc=e)

    def get_option_strikes(
        self,
        underlying: str,
        expiration_date: str | None = None,
        min_strike: float | None = None,
        max_strike: float | None = None,
        mode: str | None = None,
        spread_type: str | None = None,
        strike_interval: int | None = None,
        expiration: str | None = None,
        expiration2: str | None = None,
    ) -> list[float]:
        """
        Get available strike prices for an underlying and expiration.

        Args:
            underlying: Underlying symbol (e.g., "MSFT")
            expiration_date: Expiration date in ISO format (e.g., "2022-12-16") (kept for backward compatibility)
            min_strike: Optional minimum strike price filter (non-spec convenience)
            max_strike: Optional maximum strike price filter (non-spec convenience)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            spread_type: Optional spread type per API (default Single)
            strike_interval: Optional strike interval per API
            expiration: Optional primary expiration per API (alias to expiration_date if provided)
            expiration2: Optional secondary expiration for calendar/diagonal per API

        Returns:
            List of strike prices (floats)

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/marketdata/options/strikes/{underlying}
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = f"marketdata/options/strikes/{underlying}"
            params: dict[str, Any] = {}
            # API-aligned params
            if expiration or expiration_date:
                params["expiration"] = expiration or expiration_date
            if expiration2:
                params["expiration2"] = expiration2
            if spread_type:
                params["spreadType"] = spread_type
            if strike_interval is not None:
                params["strikeInterval"] = strike_interval
            # Non-spec convenience filters (kept for compatibility)
            if min_strike is not None:
                params["minStrike"] = str(min_strike)
            if max_strike is not None:
                params["maxStrike"] = str(max_strike)

            logger.debug(
                "Fetching option strikes: underlying=%s expiration=%s expiration2=%s spread_type=%s strike_interval=%s mode=%s params=%s",
                underlying,
                params.get("expiration"),
                expiration2,
                spread_type,
                strike_interval,
                mode,
                params,
            )
            response = self.client.make_request("GET", endpoint, params=params or None, mode=mode)

            # Response structure: {"Strikes": [...]}
            strikes = response.get("Strikes", [])

            logger.info(
                "Retrieved %s strike price(s) for %s (mode: %s params=%s)",
                len(strikes),
                underlying,
                mode,
                params or {},
            )

            return strikes

        except TradeStationAPIError as e:
            e.details.operation = "get_option_strikes"
            if not e.details.message.startswith("Failed to get option strikes"):
                e.details.message = f"Failed to get option strikes: {e.details.message}"
            logger.error(f"Failed to get option strikes: {e.details.to_human_readable()}")
            raise
        except Exception as e:
            logger.error(f"Failed to get option strikes: {e}", exc_info=True)
            raise_unexpected_error(operation="get_option_strikes", endpoint=endpoint, mode=mode, exc=e)

    async def stream_option_chains(
        self,
        underlying: str,
        mode: str | None = None,
        expiration: str | None = None,
        expiration2: str | None = None,
        strike_proximity: int | None = None,
        spread_type: str | None = None,
        risk_free_rate: float | None = None,
        price_center: float | None = None,
        strike_interval: int | None = None,
        enable_greeks: bool | None = None,
        strike_range: str | None = None,
        option_type: str | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream option chain data for an underlying symbol.

        Args:
            underlying: Underlying symbol (e.g., "MSFT")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            expiration: Optional expiration date
            expiration2: Optional secondary expiration (calendar/diagonal)
            strike_proximity: Optional number of spreads above/below price center
            spread_type: Optional spread type (default Single)
            risk_free_rate: Optional risk-free rate override
            price_center: Optional strike price center
            strike_interval: Optional strike interval
            enable_greeks: Optional flag to include greeks (default true)
            strike_range: Optional filter (All/ITM/OTM)
            option_type: Optional filter (All/Call/Put)

        Yields:
            Option chain update dictionaries

        Dependencies: HTTPClient.stream_data

        Note: TradeStation API endpoint: GET /v3/marketdata/stream/options/chains/{underlying}
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = f"marketdata/stream/options/chains/{underlying}"
            params: dict[str, Any] = {}
            if expiration:
                params["expiration"] = expiration
            if expiration2:
                params["expiration2"] = expiration2
            if strike_proximity is not None:
                params["strikeProximity"] = strike_proximity
            if spread_type:
                params["spreadType"] = spread_type
            if risk_free_rate is not None:
                params["riskFreeRate"] = risk_free_rate
            if price_center is not None:
                params["priceCenter"] = price_center
            if strike_interval is not None:
                params["strikeInterval"] = strike_interval
            if enable_greeks is not None:
                params["enableGreeks"] = enable_greeks
            if strike_range:
                params["strikeRange"] = strike_range
            if option_type:
                params["optionType"] = option_type

            logger.debug(
                "Starting option chain stream: underlying=%s mode=%s params=%s",
                underlying,
                mode,
                params or {},
            )

            async for data in self._stream_helper(endpoint, params=params or None, mode=mode):
                yield data

        except Exception as e:
            logger.error(f"Option chain stream error: {e}", exc_info=True)
            raise

    async def stream_option_quotes(
        self,
        legs: list[dict[str, str]],
        mode: str | None = None,
        risk_free_rate: float | None = None,
        enable_greeks: bool | None = None,
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream option quotes for specified option legs.

        Args:
            legs: List of leg dictionaries with Symbol field (e.g., [{"Symbol": "MSFT 221216C305"}]). Supports optional Ratio per leg.
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            risk_free_rate: Optional risk-free rate override
            enable_greeks: Optional flag to include greeks (default true)

        Yields:
            Option quote update dictionaries

        Dependencies: HTTPClient.stream_data

        Note: TradeStation API endpoint: GET /v3/marketdata/stream/options/quotes
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "marketdata/stream/options/quotes"
            params: dict[str, Any] = {}

            # Build query parameters for legs
            for i, leg in enumerate(legs):
                if "Symbol" in leg:
                    params[f"legs[{i}].Symbol"] = leg["Symbol"]
                if "Ratio" in leg:
                    params[f"legs[{i}].Ratio"] = leg["Ratio"]

            if not any(key.endswith(".Symbol") for key in params):
                raise ValueError("At least one leg with Symbol is required for option quote streaming")

            if risk_free_rate is not None:
                params["riskFreeRate"] = risk_free_rate
            if enable_greeks is not None:
                params["enableGreeks"] = enable_greeks

            logger.debug(
                "Starting option quotes stream: legs=%s risk_free_rate=%s enable_greeks=%s mode=%s params_keys=%s",
                len(legs),
                risk_free_rate,
                enable_greeks,
                mode,
                sorted(params.keys()),
            )

            async for data in self._stream_helper(endpoint, params=params, mode=mode):
                yield data

        except Exception as e:
            logger.error(f"Option quotes stream error: {e}", exc_info=True)
            raise

    async def stream_market_depth_quotes(
        self, symbol: str, mode: str | None = None, max_levels: int | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream Level 2 market depth quotes for a symbol.

        Args:
            symbol: Trading symbol (e.g., "MSFT")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            max_levels: Optional limit for depth levels (defaults to 20 per API)

        Yields:
            Market depth quote update dictionaries

        Dependencies: HTTPClient.stream_data

        Note: TradeStation API endpoint: GET /v3/marketdata/stream/marketdepth/quotes/{symbol}
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = f"marketdata/stream/marketdepth/quotes/{symbol}"
            params: dict[str, Any] = {}
            if max_levels is not None:
                params["maxlevels"] = max_levels

            logger.debug(
                "Starting market depth quotes stream: symbol=%s mode=%s max_levels=%s",
                symbol,
                mode,
                max_levels,
            )

            async for data in self._stream_helper(endpoint, params=params or None, mode=mode):
                yield data

        except Exception as e:
            logger.error(f"Market depth quotes stream error: {e}", exc_info=True)
            raise

    async def stream_market_depth_aggregates(
        self, symbol: str, mode: str | None = None, max_levels: int | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream aggregated market depth data for a symbol.

        Args:
            symbol: Trading symbol (e.g., "MSFT")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode
            max_levels: Optional limit for depth levels (defaults to 20 per API)

        Yields:
            Aggregated market depth update dictionaries

        Dependencies: HTTPClient.stream_data

        Note: TradeStation API endpoint: GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = f"marketdata/stream/marketdepth/aggregates/{symbol}"
            params: dict[str, Any] = {}
            if max_levels is not None:
                params["maxlevels"] = max_levels

            logger.debug(
                "Starting market depth aggregates stream: symbol=%s mode=%s max_levels=%s",
                symbol,
                mode,
                max_levels,
            )

            async for data in self._stream_helper(endpoint, params=params or None, mode=mode):
                yield data

        except Exception as e:
            logger.error(f"Market depth aggregates stream error: {e}", exc_info=True)
            raise

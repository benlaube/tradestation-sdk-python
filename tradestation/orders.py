"""
Order Query Operations

Covers read-only order retrieval and streaming via /brokerage/accounts/.../orders
endpoints. Provides helpers for historical orders, current/open orders, status-
filtered queries, and HTTP streaming of live order updates. Use
`OrderExecutionOperations` for placing/modifying/canceling orders.

Dependencies: typing, collections.abc.AsyncGenerator
"""

from collections.abc import AsyncGenerator
from typing import Any

from .logger import setup_logger

from .accounts import AccountOperations
from .client import HTTPClient
from .config import sdk_config
from .exceptions import TradeStationAPIError
from .models import OrdersResponse
from .validation import dump_model, raise_unexpected_error, validate_model

logger = setup_logger(__name__, sdk_config.log_level)


class OrderOperations:
    """
    Order query-related API operations.

    Responsibilities:
    - Order history queries (with pagination and date windows)
    - Current/open order queries and status-filtered lookups
    - Fetching orders by IDs (current or historical)
    - Streaming real-time order updates over HTTP streaming

    Note: For order placement, modification, cancellation, and executions, use
    `OrderExecutionOperations`.
    """

    def __init__(
        self,
        client: HTTPClient,
        accounts: AccountOperations,
        account_id: str | None = None,
        default_mode: str | None = None,
    ):
        """
        Initialize order operations.

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

    def get_order_history(
        self,
        start_date: str | None = None,
        end_date: str | None = None,
        limit: int = 100,
        mode: str | None = None,
        since: str | None = None,
        page_size: int | None = None,
        next_token: str | None = None,
    ) -> list[dict[str, Any]]:
        """
        Get historical orders from TradeStation API.

        Args:
            start_date: (Deprecated) Start date in ISO format (YYYY-MM-DD) - alias for since
            end_date: End date in ISO format (YYYY-MM-DD) or None for today (non-spec convenience)
            limit: Maximum number of orders to return (default: 100, max: 1000) - maps to pageSize when provided
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)
            since: Required by API; if None defaults to 7 days back. ISO date string.
            page_size: Optional page size (API pageSize, max 600 per spec)
            next_token: Optional pagination token (API nextToken)

        Returns:
            List of order dictionaries with:
            - OrderID: TradeStation order ID
            - Symbol: Trading symbol
            - TradeAction: BUY or SELL
            - Quantity: Number of contracts
            - OrderType: Order type (Market, Limit, etc.)
            - Status: Order status
            - FilledQuantity: Number of contracts filled
            - AverageFillPrice: Average fill price
            - PlacedTime: When order was placed
            - FilledTime: When order was filled (if applicable)

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info

        Note: TradeStation API endpoint for order history may require date filters.
        """
        try:
            if mode is None:
                mode = self.default_mode
            # Get account ID for the specified mode
            account_info = self.accounts.get_account_info(mode)
            account_id = account_info.get("account_id") or self.account_id

            # TradeStation API v3 endpoint for order history
            endpoint = f"brokerage/accounts/{account_id}/historicalorders"
            params: dict[str, Any] = {}

            # API requires `since`; default to 7 days back if not provided
            if since is None:
                if start_date:
                    since = start_date
                else:
                    from datetime import datetime, timedelta

                    since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")
            params["since"] = since

            if end_date:
                # Non-spec convenience: send endDate if caller supplied it
                params["endDate"] = end_date

            # Map legacy limit to pageSize unless explicit page_size provided
            effective_page_size = page_size if page_size is not None else limit
            if effective_page_size:
                # API pageSize max is 600
                params["pageSize"] = min(int(effective_page_size), 600)
            if next_token:
                params["nextToken"] = next_token

            logger.debug(
                "Fetching order history: endpoint=%s account_id=%s since=%s endDate=%s pageSize=%s nextToken=%s mode=%s params=%s",
                endpoint,
                account_id,
                since,
                end_date,
                params.get("pageSize"),
                next_token,
                mode,
                params,
            )
            response = self.client.make_request("GET", endpoint, params=params or None, mode=mode)

            # Try different response formats
            # TradeStation API v3 returns: {"Orders": [...]} for historical orders endpoint
            # (Note: API documentation shows "Orders" not "HistoricalOrders")
            if isinstance(response, list):
                normalized_response = {"Orders": response}
            elif isinstance(response, dict):
                normalized_response = {
                    "Orders": response.get(
                        "Orders", response.get("HistoricalOrders", response.get("orders", response.get("data", [])))
                    ),
                    "Errors": response.get("Errors", []),
                    "NextToken": response.get("NextToken"),
                }
            else:
                normalized_response = {"Orders": []}
            parsed = validate_model(
                OrdersResponse,
                normalized_response,
                operation="get_order_history",
                endpoint=endpoint,
                mode=mode,
                source="response",
            )
            orders = [dump_model(order) for order in parsed.Orders]

            logger.info(
                f"Retrieved {len(orders)} orders from TradeStation API (endpoint: {endpoint}, account: {account_id}, mode: {mode or sdk_config.trading_mode})"
            )

            if len(orders) == 0:
                logger.warning(
                    f"No orders found for account {account_id} (mode: {mode or sdk_config.trading_mode}). Response type: {type(response).__name__}"
                )
                if isinstance(response, dict):
                    logger.warning(f"Response keys: {list(response.keys())}")
                    logger.debug(f"Full response (first 1000 chars): {str(response)[:1000]}")
                else:
                    logger.debug(f"Response: {str(response)[:500]}")

            return orders

        except TradeStationAPIError as e:
            e.details.operation = "get_order_history"
            if not e.details.message.startswith("Failed to get order history"):
                e.details.message = f"Failed to get order history: {e.details.message}"
            logger.error(f"Failed to get order history: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Failed to get order history: {e}", exc_info=True)
            raise_unexpected_error(
                operation="get_order_history",
                endpoint=endpoint if "endpoint" in locals() else "brokerage/accounts/{account_id}/historicalorders",
                mode=mode,
                exc=e,
            )

    def get_current_orders(
        self,
        account_ids: str | None = None,
        next_token: str | None = None,
        mode: str | None = None,
        page_size: int | None = None,
    ) -> dict[str, Any]:
        """
        Get current/open orders for account(s).

        Args:
            account_ids: Comma-separated account IDs (e.g., "123456782,123456789") or None.
                       If None, uses the default account_id or gets from account info.
            next_token: Optional pagination token for retrieving next page
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)
            page_size: Optional page size (API pageSize, max 600 per spec)

        Returns:
            Dictionary with:
            - Orders: List of order dictionaries with detailed information
            - Errors: List of error dictionaries (if any)
            - NextToken: Pagination token for next page (if available)

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info

        Note: TradeStation API endpoint: GET /v3/brokerage/accounts/{accounts}/orders
        """
        try:
            if mode is None:
                mode = self.default_mode

            # Resolve account IDs
            if not account_ids:
                account_info = self.accounts.get_account_info(mode)
                account_id = account_info.get("account_id") or self.account_id
                if not account_id:
                    logger.error(f"No account ID available for {mode} mode - cannot fetch current orders")
                    return {"Orders": [], "Errors": []}
                account_ids = account_id

            # TradeStation API v3 endpoint: brokerage/accounts/{accounts}/orders
            endpoint = f"brokerage/accounts/{account_ids}/orders"
            params: dict[str, Any] = {}
            if next_token:
                params["nextToken"] = next_token
            if page_size:
                params["pageSize"] = min(int(page_size), 600)

            logger.debug(
                "Fetching current orders: endpoint=%s accounts=%s pageSize=%s nextToken=%s mode=%s",
                endpoint,
                account_ids,
                params.get("pageSize"),
                next_token,
                mode,
            )
            response = self.client.make_request("GET", endpoint, params=params or None, mode=mode)

            parsed = validate_model(
                OrdersResponse,
                response,
                operation="get_current_orders",
                endpoint=endpoint,
                mode=mode,
                source="response",
            )
            orders = [dump_model(order) for order in parsed.Orders]
            errors = parsed.Errors
            next_token_response = parsed.NextToken

            if errors:
                logger.warning(f"Some accounts returned errors: {errors}")

            logger.info(f"Retrieved {len(orders)} current order(s) for account(s) {account_ids} (mode: {mode})")

            result = {"Orders": orders, "Errors": errors}
            if next_token_response:
                result["NextToken"] = next_token_response

            return result

        except TradeStationAPIError as e:
            e.details.operation = "get_current_orders"
            if not e.details.message.startswith("Failed to get current orders"):
                e.details.message = f"Failed to get current orders: {e.details.message}"
            logger.error(f"Failed to get current orders: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Failed to get current orders: {e}", exc_info=True)
            raise_unexpected_error(
                operation="get_current_orders",
                endpoint=endpoint if "endpoint" in locals() else "brokerage/accounts/{accounts}/orders",
                mode=mode,
                exc=e,
            )

    def get_orders_by_ids(
        self, order_ids: str, account_ids: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Get specific current orders by order ID(s).

        Args:
            order_ids: Comma-separated order IDs (e.g., "286234131,286179863")
            account_ids: Comma-separated account IDs (e.g., "123456782,123456789") or None.
                        If None, uses the default account_id or gets from account info.
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with:
            - Orders: List of order dictionaries with detailed information
            - Errors: List of error dictionaries (if any)

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info

        Note: TradeStation API endpoint: GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}
        """
        try:
            if mode is None:
                mode = self.default_mode

            # Resolve account IDs
            if not account_ids:
                account_info = self.accounts.get_account_info(mode)
                account_id = account_info.get("account_id") or self.account_id
                if not account_id:
                    logger.error(f"No account ID available for {mode} mode - cannot fetch orders by IDs")
                    return {"Orders": [], "Errors": []}
                account_ids = account_id

            # TradeStation API v3 endpoint: brokerage/accounts/{accounts}/orders/{orderIds}
            endpoint = f"brokerage/accounts/{account_ids}/orders/{order_ids}"

            logger.debug(
                f"Fetching orders by IDs: endpoint={endpoint}, accounts={account_ids}, order_ids={order_ids}, mode={mode}"
            )
            response = self.client.make_request("GET", endpoint, mode=mode)

            parsed = validate_model(
                OrdersResponse,
                response,
                operation="get_orders_by_ids",
                endpoint=endpoint,
                mode=mode,
                source="response",
            )
            orders = [dump_model(order) for order in parsed.Orders]
            errors = parsed.Errors

            if errors:
                logger.warning(f"Some orders returned errors: {errors}")

            logger.info(f"Retrieved {len(orders)} order(s) by IDs for account(s) {account_ids} (mode: {mode})")

            return {"Orders": orders, "Errors": errors}

        except TradeStationAPIError as e:
            e.details.operation = "get_orders_by_ids"
            if not e.details.message.startswith("Failed to get orders by IDs"):
                e.details.message = f"Failed to get orders by IDs: {e.details.message}"
            logger.error(f"Failed to get orders by IDs: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Failed to get orders by IDs: {e}", exc_info=True)
            raise_unexpected_error(
                operation="get_orders_by_ids",
                endpoint=endpoint if "endpoint" in locals() else "brokerage/accounts/{accounts}/orders/{order_ids}",
                mode=mode,
                exc=e,
            )

    def get_historical_orders_by_ids(
        self,
        order_ids: str,
        account_ids: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
        mode: str | None = None,
        since: str | None = None,
    ) -> dict[str, Any]:
        """
        Get specific historical orders by order ID(s).

        Args:
            order_ids: Comma-separated order IDs (e.g., "286234131,286179863")
            account_ids: Comma-separated account IDs (e.g., "123456782,123456789") or None.
                        If None, uses the default account_id or gets from account info.
            start_date: Optional start date in ISO format (YYYY-MM-DD) for filtering (alias; prefer since)
            end_date: Optional end date in ISO format (YYYY-MM-DD) for filtering
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)
            since: Required by API; if None defaults to 7 days back. ISO date string.

        Returns:
            Dictionary with:
            - Orders: List of order dictionaries with detailed information
            - Errors: List of error dictionaries (if any)

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info

        Note: TradeStation API endpoint: GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}
        """
        try:
            if mode is None:
                mode = self.default_mode

            # Resolve account IDs
            if not account_ids:
                account_info = self.accounts.get_account_info(mode)
                account_id = account_info.get("account_id") or self.account_id
                if not account_id:
                    logger.error(f"No account ID available for {mode} mode - cannot fetch historical orders by IDs")
                    return {"Orders": [], "Errors": []}
                account_ids = account_id

            # TradeStation API v3 endpoint: brokerage/accounts/{accounts}/historicalorders/{orderIds}
            endpoint = f"brokerage/accounts/{account_ids}/historicalorders/{order_ids}"
            params: dict[str, Any] = {}
            if since is None:
                if start_date:
                    since = start_date
                else:
                    from datetime import datetime, timedelta

                    since = (datetime.utcnow() - timedelta(days=7)).strftime("%Y-%m-%d")

            params["since"] = since
            if end_date:
                params["endDate"] = end_date

            logger.debug(
                "Fetching historical orders by IDs: endpoint=%s accounts=%s order_ids=%s since=%s endDate=%s mode=%s params=%s",
                endpoint,
                account_ids,
                order_ids,
                since,
                end_date,
                mode,
                params,
            )
            response = self.client.make_request("GET", endpoint, params=params or None, mode=mode)

            parsed = validate_model(
                OrdersResponse,
                response,
                operation="get_historical_orders_by_ids",
                endpoint=endpoint,
                mode=mode,
                source="response",
            )
            orders = [dump_model(order) for order in parsed.Orders]
            errors = parsed.Errors

            if errors:
                logger.warning(f"Some orders returned errors: {errors}")

            logger.info(
                f"Retrieved {len(orders)} historical order(s) by IDs for account(s) {account_ids} (mode: {mode})"
            )

            return {"Orders": orders, "Errors": errors}

        except TradeStationAPIError as e:
            e.details.operation = "get_historical_orders_by_ids"
            if not e.details.message.startswith("Failed to get historical orders by IDs"):
                e.details.message = f"Failed to get historical orders by IDs: {e.details.message}"
            logger.error(f"Failed to get historical orders by IDs: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Failed to get historical orders by IDs: {e}", exc_info=True)
            raise_unexpected_error(
                operation="get_historical_orders_by_ids",
                endpoint=endpoint
                if "endpoint" in locals()
                else "brokerage/accounts/{accounts}/historicalorders/{order_ids}",
                mode=mode,
                exc=e,
            )

    async def stream_orders(
        self, account_id: str | None = None, mode: str | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """
        Stream order updates via TradeStation HTTP Streaming API.

        Args:
            account_id: TradeStation account ID (optional, defaults to initialized)
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Yields:
            Order update dictionaries
        """
        if mode is None:
            mode = self.default_mode

        # Resolve account ID
        if not account_id:
            account_info = self.accounts.get_account_info(mode)
            account_id = account_info.get("account_id") or self.account_id

        if not account_id:
            raise ValueError("Account ID required for streaming orders")

        # TradeStation API v3 endpoint: brokerage/stream/accounts/{accountIds}/orders
        endpoint = f"brokerage/stream/accounts/{account_id}/orders"

        logger.info(f"Starting order stream for account {account_id} via HTTP Streaming")

        async for data in self._stream_helper(endpoint, mode=mode):
            yield data

    async def _stream_helper(
        self, endpoint: str, params: dict | None = None, mode: str | None = None
    ) -> AsyncGenerator[dict[str, Any], None]:
        """Helper for async streaming (duplicated from MarketDataOperations to avoid circular deps)"""
        import asyncio
        import queue
        import threading

        data_queue = queue.Queue()
        stream_error = [None]

        def run_stream():
            """Run synchronous order stream in a background thread using HTTPClient.stream_data."""
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

    def get_orders_by_status(
        self,
        status: str | list[str],
        account_ids: str | None = None,
        next_token: str | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Get orders filtered by status(es).

        Args:
            status: Single status string or list of status strings to filter by.
                   Common statuses:
                   - Open: "OPN", "ACK", "PLA", "FPR", "RPD", "RSN", "UCN"
                   - Filled: "FLL", "FLP"
                   - Canceled: "CAN", "EXP", "OUT", "TSC", "UCH"
                   - Rejected: "REJ"
            account_ids: Comma-separated account IDs (optional)
            next_token: Optional pagination token
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with:
            - Orders: List of orders matching the status filter
            - Errors: List of error dictionaries (if any)
            - NextToken: Pagination token (if available)

        Dependencies: get_current_orders

        Note: Filters orders from get_current_orders() by status field.
        """
        try:
            if mode is None:
                mode = self.default_mode
            # Get all current orders
            all_orders_result = self.get_current_orders(account_ids, next_token, mode)
            all_orders = all_orders_result.get("Orders", [])

            # Normalize status to list
            if isinstance(status, str):
                status_list = [status.upper()]
            else:
                status_list = [s.upper() for s in status]

            # Filter by status
            filtered_orders = []
            for order in all_orders:
                order_status = order.get("Status", "").upper()
                if order_status in status_list:
                    filtered_orders.append(order)

            logger.info(
                f"Filtered {len(filtered_orders)} order(s) with status {status_list} from {len(all_orders)} total orders"
            )

            return {
                "Orders": filtered_orders,
                "Errors": all_orders_result.get("Errors", []),
                "NextToken": all_orders_result.get("NextToken"),
            }

        except Exception as e:
            logger.error(f"Failed to get orders by status: {e}", exc_info=True)
            raise_unexpected_error(
                operation="get_orders_by_status",
                endpoint="brokerage/accounts/{accounts}/orders",
                mode=mode,
                exc=e,
            )

    def get_open_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Get open/working orders (convenience function).

        Filters for orders with open statuses: OPN, ACK, PLA, FPR, RPD, RSN, UCN

        Args:
            account_ids: Comma-separated account IDs (optional)
            next_token: Optional pagination token
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with filtered open orders

        Dependencies: get_orders_by_status
        """
        if mode is None:
            mode = self.default_mode
        return self.get_orders_by_status(
            ["OPN", "ACK", "PLA", "FPR", "RPD", "RSN", "UCN"], account_ids, next_token, mode
        )

    def get_filled_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Get filled orders (convenience function).

        Filters for orders with filled statuses: FLL, FLP

        Args:
            account_ids: Comma-separated account IDs (optional)
            next_token: Optional pagination token
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with filtered filled orders

        Dependencies: get_orders_by_status
        """
        if mode is None:
            mode = self.default_mode
        return self.get_orders_by_status(["FLL", "FLP"], account_ids, next_token, mode)

    def get_canceled_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Get canceled orders (convenience function).

        Filters for orders with canceled statuses: CAN, EXP, OUT, TSC, UCH

        Args:
            account_ids: Comma-separated account IDs (optional)
            next_token: Optional pagination token
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with filtered canceled orders

        Dependencies: get_orders_by_status
        """
        if mode is None:
            mode = self.default_mode
        return self.get_orders_by_status(["CAN", "EXP", "OUT", "TSC", "UCH"], account_ids, next_token, mode)

    def get_rejected_orders(
        self, account_ids: str | None = None, next_token: str | None = None, mode: str | None = None
    ) -> dict[str, Any]:
        """
        Get rejected orders (convenience function).

        Filters for orders with rejected status: REJ

        Args:
            account_ids: Comma-separated account IDs (optional)
            next_token: Optional pagination token
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with filtered rejected orders

        Dependencies: get_orders_by_status
        """
        if mode is None:
            mode = self.default_mode
        return self.get_orders_by_status("REJ", account_ids, next_token, mode)

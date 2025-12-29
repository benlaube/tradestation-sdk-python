"""
Order Execution Operations

Handles all order execution operations using the /orderexecution/ API endpoints.
This includes order placement, modification, cancellation, executions, confirmations,
group orders (OCO/Bracket), and execution-related configuration.

Dependencies: typing, collections.abc.AsyncGenerator
"""

from typing import Any

from .accounts import AccountOperations
from .client import HTTPClient
from .config import sdk_config
from .exceptions import TradeStationAPIError
from .logger import setup_logger
from .models import (
    TradeStationExecutionResponse,
    CancelOrderResponse,
    ConfirmOrderResponse,
    ConfirmGroupOrderResponse,
)

logger = setup_logger(__name__, sdk_config.log_level)


class OrderExecutionOperations:
    """
    Order execution-related API operations.

    Handles all operations that use the /orderexecution/ endpoints:
    - Order placement, modification, cancellation
    - Order executions (fills)
    - Order confirmations
    - Group orders (OCO/Bracket)
    - Activation triggers and routing options
    - Convenience functions for common order types
    """

    def __init__(
        self,
        client: HTTPClient,
        accounts: AccountOperations,
        account_id: str | None = None,
        default_mode: str | None = None,
    ):
        """
        Initialize order execution operations.

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

    def place_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "Market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "DAY",
        _wait_for_fill: bool = False,
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place an order with support for multiple order types (TradeStation API v3).

        Args:
            symbol: Futures symbol
            side: "BUY" or "SELL"
            quantity: Number of contracts
            order_type: Order type - "Market", "Limit", "Stop", "StopLimit", "TrailingStop" (default: "Market")
            limit_price: Limit price for Limit or StopLimit orders (optional)
            stop_price: Stop price for Stop or StopLimit orders (optional)
            time_in_force: Time in force - "DAY", "GTC", "IOC", "FOK" (default: "DAY")
            wait_for_fill: If True, waits for fill confirmation (optional, for compatibility)
            trail_amount: Trail amount in price units (points) for TrailingStop orders (optional)
                Note: For futures, this is in price units, not dollar amounts.
                For MNQ: 1 point = $2.00, so trail_amount=1.5 means $3.00 trail
            trail_percent: Trail percentage for TrailingStop orders (optional, e.g., 1.0 for 1%)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (order_id, status_message) for compatibility with trade_service

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info

        Note: TradeStation API v3 format:
        - Endpoint: POST /v3/orderexecution/orders
        - OrderType: Market, Limit, Stop, StopLimit, TrailingStop
        - TimeInForce: {"Duration": "DAY"|"GTC"|"IOC"|"FOK"}
        - For TrailingStop: Requires TrailAmount (price units/points) or TrailPercent
          Note: TrailAmount is in price units, not dollar amounts. For MNQ, 1 point = $2.00
        """
        if mode is None:
            mode = sdk_config.trading_mode

        # Use instance default mode if not provided
        if mode is None:
            mode = self.default_mode

        # Validate mode
        if not isinstance(mode, str):
            logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
            return None, f"ERROR: mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}"
        mode_upper = mode.upper().strip()
        if mode_upper not in ["PAPER", "LIVE"]:
            logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
            return None, f"ERROR: mode must be 'PAPER' or 'LIVE', got '{mode}'"
        mode = mode_upper

        # Validate symbol
        if not symbol or not isinstance(symbol, str):
            logger.error(
                f"❌ symbol must be a non-empty string, got {type(symbol).__name__ if symbol is not None else 'None'}"
            )
            return (
                None,
                f"ERROR: symbol must be a non-empty string, got {type(symbol).__name__ if symbol is not None else 'None'}",
            )
        symbol = symbol.strip()
        if not symbol:
            logger.error("❌ symbol cannot be empty or whitespace only")
            return None, "ERROR: symbol cannot be empty or whitespace only"
        if len(symbol) > 50:
            logger.error(f"❌ symbol seems too long ({len(symbol)} characters). Maximum recommended: 50 characters")
            return None, f"ERROR: symbol seems too long ({len(symbol)} characters). Maximum recommended: 50"

        # Validate side
        if not side or not isinstance(side, str):
            logger.error(f"❌ side must be 'BUY' or 'SELL', got {type(side).__name__ if side is not None else 'None'}")
            return (
                None,
                f"ERROR: side must be 'BUY' or 'SELL', got {type(side).__name__ if side is not None else 'None'}",
            )
        side_upper = side.upper().strip()
        if side_upper not in ["BUY", "SELL"]:
            logger.error(f"❌ side must be 'BUY' or 'SELL', got '{side}'")
            return None, f"ERROR: side must be 'BUY' or 'SELL', got '{side}'"

        # Validate quantity
        if not isinstance(quantity, int):
            logger.error(f"❌ quantity must be an integer, got {type(quantity).__name__}")
            return None, f"ERROR: quantity must be an integer, got {type(quantity).__name__}"
        if quantity <= 0:
            logger.error(f"❌ quantity must be positive, got {quantity}")
            return None, f"ERROR: quantity must be positive, got {quantity}"
        if quantity > 10000:
            logger.error(
                f"❌ quantity seems unreasonably large ({quantity} contracts). Maximum recommended: 10,000 contracts"
            )
            return None, f"ERROR: quantity seems unreasonably large ({quantity} contracts). Maximum recommended: 10,000"

        # Validate order_type
        if not order_type or not isinstance(order_type, str):
            logger.error(
                f"❌ order_type must be a string, got {type(order_type).__name__ if order_type is not None else 'None'}"
            )
            return (
                None,
                f"ERROR: order_type must be a string, got {type(order_type).__name__ if order_type is not None else 'None'}",
            )
        valid_order_types = ["MARKET", "LIMIT", "STOP", "STOPLIMIT", "TRAILINGSTOP"]
        order_type_upper = order_type.upper().strip()
        if order_type_upper not in valid_order_types:
            logger.error(f"❌ order_type must be one of {valid_order_types}, got '{order_type}'")
            return None, f"ERROR: order_type must be one of {valid_order_types}, got '{order_type}'"

        # Validate time_in_force
        if not time_in_force or not isinstance(time_in_force, str):
            logger.error(
                f"❌ time_in_force must be a string, got {type(time_in_force).__name__ if time_in_force is not None else 'None'}"
            )
            return (
                None,
                f"ERROR: time_in_force must be a string, got {type(time_in_force).__name__ if time_in_force is not None else 'None'}",
            )
        valid_time_in_force = ["DAY", "DYP", "GTC", "GCP", "GTD", "GDP", "OPG", "CLO", "IOC", "FOK", "1", "3", "5"]
        time_in_force_upper = time_in_force.upper().strip()
        if time_in_force_upper not in valid_time_in_force:
            logger.error(f"❌ time_in_force must be one of {valid_time_in_force}, got '{time_in_force}'")
            return None, f"ERROR: time_in_force must be one of {valid_time_in_force}, got '{time_in_force}'"

        # Get account ID for the specified mode
        account_info = self.accounts.get_account_info(mode)
        account_id = account_info.get("account_id") or self.account_id

        endpoint = "orderexecution/orders"

        # Validate order type and required parameters
        if order_type_upper == "LIMIT" and limit_price is None:
            logger.error("❌ Limit order requires limit_price parameter")
            return None, "ERROR: Limit order requires limit_price"
        if order_type_upper == "STOP" and stop_price is None:
            logger.error("❌ Stop order requires stop_price parameter")
            return None, "ERROR: Stop order requires stop_price"
        if order_type_upper == "STOPLIMIT" and (limit_price is None or stop_price is None):
            logger.error("❌ StopLimit order requires both limit_price and stop_price parameters")
            return None, "ERROR: StopLimit order requires limit_price and stop_price"
        if order_type_upper == "TRAILINGSTOP":
            if trail_amount is None and trail_percent is None:
                logger.error("❌ TrailingStop order requires either trail_amount or trail_percent parameter")
                return None, "ERROR: TrailingStop order requires trail_amount or trail_percent"
            if trail_amount is not None and trail_percent is not None:
                logger.warning("⚠️  Both trail_amount and trail_percent provided - using trail_amount")

            # Validate trail_amount if provided
            if trail_amount is not None:
                if not isinstance(trail_amount, (int, float)):
                    logger.error(f"❌ trail_amount must be a number, got {type(trail_amount).__name__}")
                    return None, f"ERROR: trail_amount must be a number, got {type(trail_amount).__name__}"
                if trail_amount <= 0:
                    logger.error(f"❌ trail_amount must be positive, got {trail_amount}")
                    return None, f"ERROR: trail_amount must be positive, got {trail_amount}"
                if trail_amount > 10000:
                    logger.error(
                        f"❌ trail_amount seems unreasonably large ({trail_amount} points). Maximum recommended: 10000"
                    )
                    return (
                        None,
                        f"ERROR: trail_amount seems unreasonably large ({trail_amount} points). Maximum recommended: 10000",
                    )

            # Validate trail_percent if provided
            if trail_percent is not None:
                if not isinstance(trail_percent, (int, float)):
                    logger.error(f"❌ trail_percent must be a number, got {type(trail_percent).__name__}")
                    return None, f"ERROR: trail_percent must be a number, got {type(trail_percent).__name__}"
                if trail_percent <= 0:
                    logger.error(f"❌ trail_percent must be positive, got {trail_percent}")
                    return None, f"ERROR: trail_percent must be positive, got {trail_percent}"
                if trail_percent > 100:
                    logger.error(
                        f"❌ trail_percent seems unreasonably large ({trail_percent}%). Maximum recommended: 100%"
                    )
                    return (
                        None,
                        f"ERROR: trail_percent seems unreasonably large ({trail_percent}%). Maximum recommended: 100%",
                    )

        # Build order payload (TradeStation API v3 format)
        order = {
            "AccountID": account_id,
            "Symbol": symbol,
            "TradeAction": side_upper,
            "OrderType": order_type_upper,
            "Quantity": str(quantity),
            "TimeInForce": {"Duration": time_in_force_upper},
        }

        # Validate prices if provided
        import math

        if limit_price is not None:
            if not isinstance(limit_price, (int, float)):
                logger.error(f"❌ limit_price must be a number, got {type(limit_price).__name__}")
                return None, f"ERROR: limit_price must be a number, got {type(limit_price).__name__}"
            if limit_price <= 0:
                logger.error(f"❌ limit_price must be positive, got {limit_price}")
                return None, f"ERROR: limit_price must be positive, got {limit_price}"
            if limit_price > 1000000:
                logger.error(
                    f"❌ limit_price seems unreasonably large (${limit_price:,.2f}). Maximum recommended: $1,000,000"
                )
                return (
                    None,
                    f"ERROR: limit_price seems unreasonably large (${limit_price:,.2f}). Maximum recommended: $1,000,000",
                )
            if limit_price < 0.01:
                logger.error(
                    f"❌ limit_price seems unreasonably small (${limit_price:.4f}). Minimum recommended: $0.01"
                )
                return (
                    None,
                    f"ERROR: limit_price seems unreasonably small (${limit_price:.4f}). Minimum recommended: $0.01",
                )
            if math.isnan(limit_price) or math.isinf(limit_price):
                logger.error(f"❌ limit_price must be a finite number, got {limit_price}")
                return None, f"ERROR: limit_price must be a finite number, got {limit_price}"

        if stop_price is not None:
            if not isinstance(stop_price, (int, float)):
                logger.error(f"❌ stop_price must be a number, got {type(stop_price).__name__}")
                return None, f"ERROR: stop_price must be a number, got {type(stop_price).__name__}"
            if stop_price <= 0:
                logger.error(f"❌ stop_price must be positive, got {stop_price}")
                return None, f"ERROR: stop_price must be positive, got {stop_price}"
            if stop_price > 1000000:
                logger.error(
                    f"❌ stop_price seems unreasonably large (${stop_price:,.2f}). Maximum recommended: $1,000,000"
                )
                return (
                    None,
                    f"ERROR: stop_price seems unreasonably large (${stop_price:,.2f}). Maximum recommended: $1,000,000",
                )
            if stop_price < 0.01:
                logger.error(f"❌ stop_price seems unreasonably small (${stop_price:.4f}). Minimum recommended: $0.01")
                return (
                    None,
                    f"ERROR: stop_price seems unreasonably small (${stop_price:.4f}). Minimum recommended: $0.01",
                )
            if math.isnan(stop_price) or math.isinf(stop_price):
                logger.error(f"❌ stop_price must be a finite number, got {stop_price}")
                return None, f"ERROR: stop_price must be a finite number, got {stop_price}"

        # Add price parameters based on order type
        if order_type_upper == "LIMIT" and limit_price is not None:
            order["LimitPrice"] = str(limit_price)
        elif order_type_upper == "STOP" and stop_price is not None:
            order["StopPrice"] = str(stop_price)
        elif order_type_upper == "STOPLIMIT":
            if limit_price is not None:
                order["LimitPrice"] = str(limit_price)
            if stop_price is not None:
                order["StopPrice"] = str(stop_price)
            # Optional: Warn about potentially illogical price relationships
            if limit_price is not None and stop_price is not None:
                if side_upper == "BUY" and stop_price < limit_price:
                    logger.warning(
                        f"⚠️  BUY StopLimit: stop_price (${stop_price:.2f}) < limit_price (${limit_price:.2f}). This may be intentional."
                    )
                elif side_upper == "SELL" and stop_price > limit_price:
                    logger.warning(
                        f"⚠️  SELL StopLimit: stop_price (${stop_price:.2f}) > limit_price (${limit_price:.2f}). This may be intentional."
                    )
        elif order_type_upper == "TRAILINGSTOP":
            # Trailing stop orders require TrailAmount (points) or TrailPercent
            if trail_amount is not None:
                order["TrailAmount"] = str(trail_amount)
            elif trail_percent is not None:
                order["TrailPercent"] = str(trail_percent)
            # Optional: Reference price (if not provided, uses current market price)
            # Note: TradeStation may require a reference price for some trailing stop implementations

        try:
            order_desc = f"{order_type_upper} {side} {quantity} {symbol}"
            if limit_price:
                order_desc += f" @ ${limit_price:.2f}"
            if stop_price:
                order_desc += f" stop ${stop_price:.2f}"
            if trail_amount:
                order_desc += f" trail ${trail_amount:.2f}"
            if trail_percent:
                order_desc += f" trail {trail_percent:.2f}%"
            logger.info(f"📤 Placing order: {order_desc} ({mode} mode)")

            response = self.client.make_request("POST", endpoint, json_data=order, mode=mode)
            orders = response.get("Orders", [])
            if orders:
                order_id = orders[0].get("OrderID")
                message = orders[0].get("Message", "Order received")
                logger.info(f"✅ Order placed successfully - ID: {order_id}")
                return order_id, message
            logger.error("❌ No order returned in response")
            return None, "NO_ORDER_RETURNED"
        except TradeStationAPIError as e:
            # Add operation context to error
            e.details.operation = "place_order"
            if not e.details.message.startswith("Order placement failed"):
                e.details.message = f"Order placement failed: {e.details.message}"
            logger.error(f"❌ Order placement failed: {e.details.to_human_readable()}")
            return None, f"ERROR: {e.details.message}"
        except Exception as e:
            logger.error(f"❌ Order placement failed: {e}", exc_info=True)
            return None, f"ERROR: {str(e)}"

    def cancel_order(self, order_id: str, mode: str | None = None) -> tuple[bool, str]:
        """
        Cancel an order via TradeStation API.

        Args:
            order_id: TradeStation order ID to cancel
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (success: bool, message: str)

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: DELETE /v3/orderexecution/orders/{orderID}
        """
        # Validate order_id
        if not order_id or not isinstance(order_id, str):
            logger.error(
                f"❌ order_id must be a non-empty string, got {type(order_id).__name__ if order_id is not None else 'None'}"
            )
            return (
                False,
                f"ERROR: order_id must be a non-empty string, got {type(order_id).__name__ if order_id is not None else 'None'}",
            )
        order_id = order_id.strip()
        if not order_id:
            logger.error("❌ order_id cannot be empty or whitespace only")
            return False, "ERROR: order_id cannot be empty or whitespace only"
        if len(order_id) > 50:
            logger.error(f"❌ order_id seems too long ({len(order_id)} characters). Maximum recommended: 50 characters")
            return False, f"ERROR: order_id seems too long ({len(order_id)} characters). Maximum recommended: 50"

        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                return False, f"ERROR: mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}"
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                return False, f"ERROR: mode must be 'PAPER' or 'LIVE', got '{mode}'"
            mode = mode_upper

        try:
            endpoint = f"orderexecution/orders/{order_id}"
            logger.info(f"📤 Cancelling order: {order_id} ({mode or sdk_config.trading_mode} mode)")

            response = self.client.make_request("DELETE", endpoint, mode=mode)

            # TradeStation API may return different response formats
            if isinstance(response, dict):
                try:
                    parsed = CancelOrderResponse(**response)
                    success = bool(parsed.Success if parsed.Success is not None else True)
                    message = parsed.Message or "Order cancelled"
                    if success:
                        logger.info(f"✅ Order {order_id} cancelled successfully")
                        return parsed
                    logger.warning(f"⚠️  Order cancellation may have failed: {message}")
                    return parsed
                except Exception:
                    message = response.get("Message", "Order cancelled")
                    success = response.get("Success", True)
            else:
                message = "Order cancelled"
                success = True

            if success:
                logger.info(f"✅ Order {order_id} cancelled successfully")
                return CancelOrderResponse(Success=True, Message=str(message))
            logger.warning(f"⚠️  Order cancellation may have failed: {message}")
            return CancelOrderResponse(Success=bool(success), Message=str(message))

        except TradeStationAPIError as e:
            e.details.operation = "cancel_order"
            if not e.details.message.startswith("Order cancellation failed"):
                e.details.message = f"Order cancellation failed: {e.details.message}"
            logger.error(f"❌ Order cancellation failed: {e.details.to_human_readable()}")
            return False, f"ERROR: {e.details.message}"
        except Exception as e:
            logger.error(f"❌ Order cancellation failed: {e}", exc_info=True)
            return False, f"ERROR: {str(e)}"

    def cancel_all_orders_for_symbol(
        self, symbol: str, account_ids: str | None = None, mode: str | None = None
    ) -> list[dict[str, Any]]:
        """
        Cancel all open orders for a specific symbol.

        Args:
            symbol: Trading symbol to cancel orders for
            account_ids: Comma-separated account IDs (optional, uses default if None)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of dictionaries with cancellation results:
            - order_id: Order ID that was cancelled
            - symbol: Trading symbol
            - success: Whether cancellation succeeded
            - message: Status message

        Dependencies: HTTPClient.make_request, OrderExecutionOperations.cancel_order
        """
        # Validate symbol
        if not symbol or not isinstance(symbol, str):
            logger.error(
                f"❌ symbol must be a non-empty string, got {type(symbol).__name__ if symbol is not None else 'None'}"
            )
            return []
        symbol = symbol.strip()
        if not symbol:
            logger.error("❌ symbol cannot be empty or whitespace only")
            return []
        if len(symbol) > 50:
            logger.error(f"❌ symbol seems too long ({len(symbol)} characters). Maximum recommended: 50 characters")
            return []

        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                return []
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                return []
            mode = mode_upper

        if mode is None:
            mode = sdk_config.trading_mode

        # Get order operations instance (we need it to query orders)
        # Note: This assumes OrderOperations is available via self or we need to pass it
        # For now, we'll use the accounts to get account_id and query orders directly
        account_info = self.accounts.get_account_info(mode)
        account_id = account_info.get("account_id") or self.account_id

        if not account_id:
            logger.error(f"No account ID available for {mode} mode - cannot cancel orders")
            return []

        # Get current orders for the account
        # We need to import OrderOperations or access it differently
        # For now, let's query orders directly via HTTPClient
        try:
            endpoint = f"brokerage/accounts/{account_id}/orders"
            response = self.client.make_request("GET", endpoint, mode=mode)
            orders = response.get("Orders", [])

            # Filter orders by symbol
            symbol_orders = [
                order
                for order in orders
                if order.get("Symbol") == symbol and order.get("Status") not in ["FLL", "CNL", "REJ", "EXP"]
            ]

            if not symbol_orders:
                logger.info(f"No open orders found for symbol {symbol}")
                return []

            logger.info(f"Cancelling {len(symbol_orders)} order(s) for symbol {symbol}")

            # Cancel each order
            results = []
            for order in symbol_orders:
                order_id = order.get("OrderID")
                if order_id:
                    success, message = self.cancel_order(order_id, mode)
                    results.append({"order_id": order_id, "symbol": symbol, "success": success, "message": message})

            logger.info(
                f"✅ Cancelled {sum(1 for r in results if r['success'])} of {len(results)} order(s) for {symbol}"
            )
            return results

        except TradeStationAPIError as e:
            e.details.operation = "cancel_all_orders_for_symbol"
            if not e.details.message.startswith("Failed to cancel orders for symbol"):
                e.details.message = f"Failed to cancel orders for symbol: {e.details.message}"
            logger.error(f"Failed to cancel orders for symbol {symbol}: {e.details.to_human_readable()}")
            return []
        except Exception as e:
            logger.error(f"Failed to cancel orders for symbol {symbol}: {e}", exc_info=True)
            return []

    def cancel_all_orders(self, account_ids: str | None = None, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Cancel all open orders for account(s).

        Args:
            account_ids: Comma-separated account IDs (optional, uses default if None)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of dictionaries with cancellation results:
            - order_id: Order ID that was cancelled
            - symbol: Trading symbol
            - success: Whether cancellation succeeded
            - message: Status message

        Dependencies: HTTPClient.make_request, OrderExecutionOperations.cancel_order
        """
        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                return []
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                return []
            mode = mode_upper

        if mode is None:
            mode = sdk_config.trading_mode

        # Get account ID
        account_info = self.accounts.get_account_info(mode)
        account_id = account_info.get("account_id") or self.account_id

        if not account_id:
            logger.error(f"No account ID available for {mode} mode - cannot cancel orders")
            return []

        # Get current orders for the account
        try:
            endpoint = f"brokerage/accounts/{account_id}/orders"
            response = self.client.make_request("GET", endpoint, mode=mode)
            orders = response.get("Orders", [])

            # Filter out already filled/cancelled/rejected orders
            open_orders = [order for order in orders if order.get("Status") not in ["FLL", "CNL", "REJ", "EXP"]]

            if not open_orders:
                logger.info(f"No open orders found for account {account_id}")
                return []

            logger.info(f"Cancelling {len(open_orders)} open order(s) for account {account_id}")

            # Cancel each order
            results = []
            for order in open_orders:
                order_id = order.get("OrderID")
                symbol = order.get("Symbol", "UNKNOWN")
                if order_id:
                    success, message = self.cancel_order(order_id, mode)
                    results.append({"order_id": order_id, "symbol": symbol, "success": success, "message": message})

            successful = sum(1 for r in results if r["success"])
            logger.info(f"✅ Cancelled {successful} of {len(results)} order(s) for account {account_id}")
            return results

        except TradeStationAPIError as e:
            e.details.operation = "cancel_all_orders"
            if not e.details.message.startswith("Failed to cancel all orders"):
                e.details.message = f"Failed to cancel all orders: {e.details.message}"
            logger.error(f"Failed to cancel all orders: {e.details.to_human_readable()}")
            return []
        except Exception as e:
            logger.error(f"Failed to cancel all orders: {e}", exc_info=True)
            return []

    def replace_order(
        self,
        old_order_id: str,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "Market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "DAY",
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Replace an order by canceling the old one and placing a new one.

        This is useful when you need to change symbol, side, or other parameters
        that cannot be modified with modify_order().

        Args:
            old_order_id: Order ID to cancel
            symbol: New trading symbol
            side: "BUY" or "SELL" for new order
            quantity: Number of contracts for new order
            order_type: Order type for new order (default: "Market")
            limit_price: Limit price for new order (optional)
            stop_price: Stop price for new order (optional)
            time_in_force: Time in force for new order (default: "DAY")
            trail_amount: Trail amount for trailing stop (optional)
            trail_percent: Trail percentage for trailing stop (optional)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (new_order_id, status_message)
            If cancellation fails, returns (None, error_message)

        Dependencies: OrderExecutionOperations.cancel_order, OrderExecutionOperations.place_order

        Example:
            # Replace a limit order with a market order
            new_order_id, status = sdk.order_executions.replace_order(
                old_order_id="924243071",
                symbol="MNQZ25",
                side="BUY",
                quantity=2,
                order_type="Market",
                mode="PAPER"
            )
        """
        # Validate old_order_id
        if not old_order_id or not isinstance(old_order_id, str):
            logger.error(
                f"❌ old_order_id must be a non-empty string, got {type(old_order_id).__name__ if old_order_id is not None else 'None'}"
            )
            return (
                None,
                f"ERROR: old_order_id must be a non-empty string, got {type(old_order_id).__name__ if old_order_id is not None else 'None'}",
            )
        old_order_id = old_order_id.strip()
        if not old_order_id:
            logger.error("❌ old_order_id cannot be empty or whitespace only")
            return None, "ERROR: old_order_id cannot be empty or whitespace only"
        if len(old_order_id) > 50:
            logger.error(
                f"❌ old_order_id seems too long ({len(old_order_id)} characters). Maximum recommended: 50 characters"
            )
            return None, f"ERROR: old_order_id seems too long ({len(old_order_id)} characters). Maximum recommended: 50"

        # Validation for new order parameters is handled by place_order()
        # Cancel the old order
        logger.info(f"📤 Replacing order {old_order_id} with new order")
        cancel_success, cancel_message = self.cancel_order(old_order_id, mode)

        if not cancel_success:
            logger.error(f"❌ Failed to cancel order {old_order_id}: {cancel_message}")
            return None, f"Failed to cancel old order: {cancel_message}"

        logger.info(f"✅ Old order {old_order_id} cancelled, placing new order")

        # Place the new order
        new_order_id, place_message = self.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type=order_type,
            limit_price=limit_price,
            stop_price=stop_price,
            time_in_force=time_in_force,
            trail_amount=trail_amount,
            trail_percent=trail_percent,
            mode=mode,
        )

        if new_order_id:
            logger.info(f"✅ Order replaced: {old_order_id} → {new_order_id}")
            return new_order_id, f"Order replaced: {place_message}"
        else:
            logger.error(f"❌ Failed to place new order after cancelling {old_order_id}: {place_message}")
            return None, f"Old order cancelled but new order failed: {place_message}"

    def modify_order(
        self,
        order_id: str,
        quantity: int | None = None,
        limit_price: float | None = None,
        stop_price: float | None = None,
        mode: str | None = None,
    ) -> tuple[bool, str]:
        """
        Modify an existing order via TradeStation API.

        Args:
            order_id: TradeStation order ID to modify
            quantity: New quantity (optional)
            limit_price: New limit price (optional, for limit orders)
            stop_price: New stop price (optional, for stop orders)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (success: bool, message: str)

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: PUT /v3/orderexecution/orders/{orderID}
        """
        # Validate order_id
        if not order_id or not isinstance(order_id, str):
            logger.error(
                f"❌ order_id must be a non-empty string, got {type(order_id).__name__ if order_id is not None else 'None'}"
            )
            return (
                False,
                f"ERROR: order_id must be a non-empty string, got {type(order_id).__name__ if order_id is not None else 'None'}",
            )
        order_id = order_id.strip()
        if not order_id:
            logger.error("❌ order_id cannot be empty or whitespace only")
            return False, "ERROR: order_id cannot be empty or whitespace only"
        if len(order_id) > 50:
            logger.error(f"❌ order_id seems too long ({len(order_id)} characters). Maximum recommended: 50 characters")
            return False, f"ERROR: order_id seems too long ({len(order_id)} characters). Maximum recommended: 50"

        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                return False, f"ERROR: mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}"
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                return False, f"ERROR: mode must be 'PAPER' or 'LIVE', got '{mode}'"
            mode = mode_upper

        # At least one update must be provided
        if quantity is None and limit_price is None and stop_price is None:
            logger.error("❌ At least one update must be provided (quantity, limit_price, or stop_price)")
            return False, "ERROR: At least one update must be provided (quantity, limit_price, or stop_price)"

        # Validate quantity if provided
        if quantity is not None:
            if not isinstance(quantity, int):
                logger.error(f"❌ quantity must be an integer, got {type(quantity).__name__}")
                return False, f"ERROR: quantity must be an integer, got {type(quantity).__name__}"
            if quantity <= 0:
                logger.error(f"❌ quantity must be positive, got {quantity}")
                return False, f"ERROR: quantity must be positive, got {quantity}"
            if quantity > 10000:
                logger.error(
                    f"❌ quantity seems unreasonably large ({quantity} contracts). Maximum recommended: 10,000 contracts"
                )
                return (
                    False,
                    f"ERROR: quantity seems unreasonably large ({quantity} contracts). Maximum recommended: 10,000",
                )

        # Validate prices if provided
        import math

        if limit_price is not None:
            if not isinstance(limit_price, (int, float)):
                logger.error(f"❌ limit_price must be a number, got {type(limit_price).__name__}")
                return False, f"ERROR: limit_price must be a number, got {type(limit_price).__name__}"
            if limit_price <= 0:
                logger.error(f"❌ limit_price must be positive, got {limit_price}")
                return False, f"ERROR: limit_price must be positive, got {limit_price}"
            if limit_price > 1000000:
                logger.error(
                    f"❌ limit_price seems unreasonably large (${limit_price:,.2f}). Maximum recommended: $1,000,000"
                )
                return (
                    False,
                    f"ERROR: limit_price seems unreasonably large (${limit_price:,.2f}). Maximum recommended: $1,000,000",
                )
            if limit_price < 0.01:
                logger.error(
                    f"❌ limit_price seems unreasonably small (${limit_price:.4f}). Minimum recommended: $0.01"
                )
                return (
                    False,
                    f"ERROR: limit_price seems unreasonably small (${limit_price:.4f}). Minimum recommended: $0.01",
                )
            if math.isnan(limit_price) or math.isinf(limit_price):
                logger.error(f"❌ limit_price must be a finite number, got {limit_price}")
                return False, f"ERROR: limit_price must be a finite number, got {limit_price}"

        if stop_price is not None:
            if not isinstance(stop_price, (int, float)):
                logger.error(f"❌ stop_price must be a number, got {type(stop_price).__name__}")
                return False, f"ERROR: stop_price must be a number, got {type(stop_price).__name__}"
            if stop_price <= 0:
                logger.error(f"❌ stop_price must be positive, got {stop_price}")
                return False, f"ERROR: stop_price must be positive, got {stop_price}"
            if stop_price > 1000000:
                logger.error(
                    f"❌ stop_price seems unreasonably large (${stop_price:,.2f}). Maximum recommended: $1,000,000"
                )
                return (
                    False,
                    f"ERROR: stop_price seems unreasonably large (${stop_price:,.2f}). Maximum recommended: $1,000,000",
                )
            if stop_price < 0.01:
                logger.error(f"❌ stop_price seems unreasonably small (${stop_price:.4f}). Minimum recommended: $0.01")
                return (
                    False,
                    f"ERROR: stop_price seems unreasonably small (${stop_price:.4f}). Minimum recommended: $0.01",
                )
            if math.isnan(stop_price) or math.isinf(stop_price):
                logger.error(f"❌ stop_price must be a finite number, got {stop_price}")
                return False, f"ERROR: stop_price must be a finite number, got {stop_price}"

        try:
            endpoint = f"orderexecution/orders/{order_id}"

            # Build update payload with only provided fields
            updates = {}
            if quantity is not None:
                updates["Quantity"] = str(quantity)
            if limit_price is not None:
                updates["LimitPrice"] = str(limit_price)
            if stop_price is not None:
                updates["StopPrice"] = str(stop_price)

            logger.info(
                f"📤 Modifying order: {order_id} with updates: {updates} ({mode or sdk_config.trading_mode} mode)"
            )

            response = self.client.make_request("PUT", endpoint, json_data=updates, mode=mode)

            # TradeStation API may return different response formats
            if isinstance(response, dict):
                message = response.get("Message", "Order modified")
                success = response.get("Success", True)
            else:
                message = "Order modified"
                success = True

            if success:
                logger.info(f"✅ Order {order_id} modified successfully")
                return True, message
            logger.warning(f"⚠️  Order modification may have failed: {message}")
            return False, message

        except TradeStationAPIError as e:
            e.details.operation = "modify_order"
            if not e.details.message.startswith("Order modification failed"):
                e.details.message = f"Order modification failed: {e.details.message}"
            logger.error(f"❌ Order modification failed: {e.details.to_human_readable()}")
            return False, f"ERROR: {e.details.message}"
        except Exception as e:
            logger.error(f"❌ Order modification failed: {e}", exc_info=True)
            return False, f"ERROR: {str(e)}"

    def is_order_filled(self, order_id: str, mode: str | None = None) -> bool:
        """
        Check if an order has been filled.

        Args:
            order_id: TradeStation order ID
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            True if order is filled (status "FLL"), False otherwise

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info

        Example:
            if sdk.is_order_filled("924243071", mode="PAPER"):
                print("Order is filled!")
        """
        # Validate order_id
        if not order_id or not isinstance(order_id, str):
            logger.error(
                f"❌ order_id must be a non-empty string, got {type(order_id).__name__ if order_id is not None else 'None'}"
            )
            return False
        order_id = order_id.strip()
        if not order_id:
            logger.error("❌ order_id cannot be empty or whitespace only")
            return False
        if len(order_id) > 50:
            logger.error(f"❌ order_id seems too long ({len(order_id)} characters). Maximum recommended: 50 characters")
            return False

        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                return False
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                return False
            mode = mode_upper

        if mode is None:
            mode = sdk_config.trading_mode

        try:
            # Get account ID
            account_info = self.accounts.get_account_info(mode)
            account_id = account_info.get("account_id") or self.account_id

            if not account_id:
                logger.error(f"No account ID available for {mode} mode - cannot check order status")
                return False

            # Get order by ID
            endpoint = f"brokerage/accounts/{account_id}/orders/{order_id}"
            response = self.client.make_request("GET", endpoint, mode=mode)

            orders = response.get("Orders", [])
            if orders:
                order = orders[0]
                status = order.get("Status", "").upper()
                # FLL = Filled, FLP = Partial Fill (UROut)
                return status in ["FLL", "FLP"]

            return False

        except TradeStationAPIError as e:
            logger.debug(f"Failed to check order status for {order_id}: {e.details.to_human_readable()}")
            return False
        except Exception as e:
            logger.debug(f"Failed to check order status for {order_id}: {e}")
            return False

    def get_order_executions(self, order_id: str, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get execution details (fills) for a specific order.

        Args:
            order_id: TradeStation order ID
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of execution dictionaries with:
            - ExecutionID: TradeStation execution ID
            - Symbol: Trading symbol
            - TradeAction: BUY or SELL
            - Quantity: Number of contracts filled
            - Price: Fill price
            - Commission: Commission paid
            - ExchangeFees: Exchange fees
            - ExecutionTime: When execution occurred
            - Venue: Execution venue

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/orderexecution/orders/{orderID}/executions
        This retrieves all fills for an order, including partial fills.

        To simply check if an order is filled, use is_order_filled() instead.
        """
        # Validate order_id
        if not order_id or not isinstance(order_id, str):
            logger.error(
                f"❌ order_id must be a non-empty string, got {type(order_id).__name__ if order_id is not None else 'None'}"
            )
            return []
        order_id = order_id.strip()
        if not order_id:
            logger.error("❌ order_id cannot be empty or whitespace only")
            return []
        if len(order_id) > 50:
            logger.error(f"❌ order_id seems too long ({len(order_id)} characters). Maximum recommended: 50 characters")
            return []

        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                return []
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                return []
            mode = mode_upper

        try:
            endpoint = f"orderexecution/orders/{order_id}/executions"
            response = self.client.make_request("GET", endpoint, mode=mode)

            # Extract executions from response and parse as models
            executions_raw = response.get("Executions", [])
            executions = []
            for exec_data in executions_raw:
                try:
                    execution = TradeStationExecutionResponse(**exec_data)
                    executions.append(execution.model_dump())
                except Exception as e:
                    logger.warning(f"Failed to parse execution: {e}, raw data: {exec_data}")
                    executions.append(exec_data)  # Fallback to raw dict

            logger.debug(f"Retrieved {len(executions)} executions for order {order_id}")

            return executions

        except TradeStationAPIError as e:
            e.details.operation = "get_order_executions"
            if not e.details.message.startswith("Failed to get order executions"):
                e.details.message = f"Failed to get order executions: {e.details.message}"
            logger.error(f"Failed to get order executions for {order_id}: {e.details.to_human_readable()}")
            return []
        except Exception as e:
            logger.error(f"Failed to get order executions for {order_id}: {e}", exc_info=True)
            return []

    def confirm_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        order_type: str = "Market",
        limit_price: float | None = None,
        stop_price: float | None = None,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> ConfirmOrderResponse | dict[str, Any]:
        """
        Confirm an order (pre-flight check) to get estimated cost and commission.

        Args:
            symbol: Trading symbol
            side: "BUY" or "SELL"
            quantity: Number of contracts
            order_type: Order type (default: "Market")
            limit_price: Limit price (optional, for limit orders)
            stop_price: Stop price (optional, for stop orders)
            time_in_force: Time in force (default: "DAY")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with confirmation details (EstimatedCost, EstimatedCommission, etc.)

        Dependencies: HTTPClient.make_request, AccountOperations.get_account_info

        Note: TradeStation API endpoint: POST /v3/orderexecution/orderconfirm
        """
        # Validation is same as place_order - reuse validation logic
        # For confirm_order, we validate but don't return errors (let API handle it)
        # But we should still validate to prevent obvious errors

        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                raise ValueError(f"mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                raise ValueError(f"mode must be 'PAPER' or 'LIVE', got '{mode}'")
            mode = mode_upper

        if mode is None:
            mode = sdk_config.trading_mode

        # Validate symbol
        if not symbol or not isinstance(symbol, str):
            logger.error(
                f"❌ symbol must be a non-empty string, got {type(symbol).__name__ if symbol is not None else 'None'}"
            )
            raise ValueError(
                f"symbol must be a non-empty string, got {type(symbol).__name__ if symbol is not None else 'None'}"
            )
        symbol = symbol.strip()
        if not symbol:
            logger.error("❌ symbol cannot be empty or whitespace only")
            raise ValueError("symbol cannot be empty or whitespace only")

        # Validate side
        if not side or not isinstance(side, str):
            logger.error(f"❌ side must be 'BUY' or 'SELL', got {type(side).__name__ if side is not None else 'None'}")
            raise ValueError(f"side must be 'BUY' or 'SELL', got {type(side).__name__ if side is not None else 'None'}")
        side_upper = side.upper().strip()
        if side_upper not in ["BUY", "SELL"]:
            logger.error(f"❌ side must be 'BUY' or 'SELL', got '{side}'")
            raise ValueError(f"side must be 'BUY' or 'SELL', got '{side}'")

        # Validate quantity
        if not isinstance(quantity, int):
            logger.error(f"❌ quantity must be an integer, got {type(quantity).__name__}")
            raise TypeError(f"quantity must be an integer, got {type(quantity).__name__}")
        if quantity <= 0:
            logger.error(f"❌ quantity must be positive, got {quantity}")
            raise ValueError(f"quantity must be positive, got {quantity}")

        account_info = self.accounts.get_account_info(mode)
        account_id = account_info.get("account_id") or self.account_id

        endpoint = "orderexecution/orderconfirm"

        # Build order payload (same as place_order)
        order = {
            "AccountID": account_id,
            "Symbol": symbol,
            "TradeAction": side_upper,
            "OrderType": order_type.upper(),
            "Quantity": str(quantity),
            "TimeInForce": {"Duration": time_in_force.upper()},
        }

        if limit_price is not None:
            order["LimitPrice"] = str(limit_price)
        if stop_price is not None:
            order["StopPrice"] = str(stop_price)

        try:
            logger.debug(f"Confirming order: {order}")
            response = self.client.make_request("POST", endpoint, json_data=order, mode=mode)
            try:
                return ConfirmOrderResponse(**response)
            except Exception:
                return response
        except TradeStationAPIError as e:
            e.details.operation = "confirm_order"
            if not e.details.message.startswith("Order confirmation failed"):
                e.details.message = f"Order confirmation failed: {e.details.message}"
            logger.error(f"Order confirmation failed: {e.details.to_human_readable()}")
            raise
        except Exception as e:
            logger.error(f"Order confirmation failed: {e}", exc_info=True)
            raise

    def confirm_group_order(
        self, group_type: str, orders: list[dict[str, Any]], mode: str | None = None
    ) -> ConfirmGroupOrderResponse | dict[str, Any]:
        """
        Confirm a group order (OCO/Bracket) before placement.

        Validates a group order and returns estimated costs and commissions.
        Group types: "OCO" (Order Cancels Order), "BRK" (Bracket), "NORMAL"

        Args:
            group_type: Group type ("OCO", "BRK", or "NORMAL")
            orders: List of order dictionaries (same format as place_order)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with confirmation details including estimated costs

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: POST /v3/orderexecution/ordergroupconfirm
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "orderexecution/ordergroupconfirm"

            # Build group order request
            group_order = {"Type": group_type.upper(), "Orders": orders}

            logger.debug(f"Confirming group order: type={group_type}, orders={len(orders)}, mode={mode}")
            response = self.client.make_request("POST", endpoint, json_data=group_order, mode=mode)

            logger.info(f"Group order confirmation successful: type={group_type}, mode={mode}")

            try:
                return ConfirmGroupOrderResponse(**response)
            except Exception:
                return response

        except TradeStationAPIError as e:
            e.details.operation = "confirm_group_order"
            if not e.details.message.startswith("Group order confirmation failed"):
                e.details.message = f"Group order confirmation failed: {e.details.message}"
            logger.error(f"Group order confirmation failed: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Group order confirmation failed: {e}", exc_info=True)
            raise

    def place_group_order(
        self, group_type: str, orders: list[dict[str, Any]], mode: str | None = None
    ) -> dict[str, Any]:
        """
        Place a group order (OCO/Bracket).

        Submits a group of related orders. For OCO orders, if one fills, others are cancelled.
        For Bracket orders, used to exit positions with stop and limit orders.

        Args:
            group_type: Group type ("OCO", "BRK", or "NORMAL")
            orders: List of order dictionaries (same format as place_order)
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with GroupOrderResponse including order IDs and group information:
            - GroupID: Group order ID
            - GroupName: Group order name
            - Type: Group type
            - Orders: List of order responses with OrderIDs

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: POST /v3/orderexecution/ordergroups
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "orderexecution/ordergroups"

            # Build group order request
            group_order = {"Type": group_type.upper(), "Orders": orders}

            logger.debug(f"Placing group order: type={group_type}, orders={len(orders)}, mode={mode}")
            response = self.client.make_request("POST", endpoint, json_data=group_order, mode=mode)

            # Extract order IDs from response
            order_ids = []
            if "Orders" in response:
                for order in response["Orders"]:
                    if "OrderID" in order:
                        order_ids.append(order["OrderID"])

            logger.info(f"Group order placed: type={group_type}, order_ids={order_ids}, mode={mode}")

            return response

        except TradeStationAPIError as e:
            e.details.operation = "place_group_order"
            if not e.details.message.startswith("Group order placement failed"):
                e.details.message = f"Group order placement failed: {e.details.message}"
            logger.error(f"Group order placement failed: {e.details.to_human_readable()}", exc_info=True)
            raise
        except Exception as e:
            logger.error(f"Group order placement failed: {e}", exc_info=True)
            raise

    def get_activation_triggers(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get available activation trigger keys for conditional orders.

        Activation triggers are required for placing orders with conditional activation
        (e.g., stop orders). This method retrieves all available trigger methods.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of trigger dictionaries with:
            - Key: Trigger key (e.g., "STT", "STTN", "SBA")
            - Name: Human-readable trigger name
            - Description: Description of the trigger method

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/orderexecution/activationtriggers
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "orderexecution/activationtriggers"

            logger.debug(f"Fetching activation triggers: endpoint={endpoint}, mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)

            # Response structure: {"ActivationTriggers": [...]}
            triggers = response.get("ActivationTriggers", [])

            logger.info(f"Retrieved {len(triggers)} activation trigger(s) (mode: {mode})")

            return triggers

        except TradeStationAPIError as e:
            e.details.operation = "get_activation_triggers"
            if not e.details.message.startswith("Failed to get activation triggers"):
                e.details.message = f"Failed to get activation triggers: {e.details.message}"
            logger.error(f"Failed to get activation triggers: {e.details.to_human_readable()}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Failed to get activation triggers: {e}", exc_info=True)
            return []

    def get_routes(self, mode: str | None = None) -> list[dict[str, Any]]:
        """
        Get available routing options for order execution.

        Routing options determine how orders are executed (e.g., "Intelligent" routing).

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            List of route dictionaries with routing options

        Dependencies: HTTPClient.make_request

        Note: TradeStation API endpoint: GET /v3/orderexecution/routes
        """
        try:
            if mode is None:
                mode = sdk_config.trading_mode

            endpoint = "orderexecution/routes"

            logger.debug(f"Fetching routing options: endpoint={endpoint}, mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)

            # Response structure: {"Routes": [...]}
            routes = response.get("Routes", [])

            logger.info(f"Retrieved {len(routes)} routing option(s) (mode: {mode})")

            return routes

        except TradeStationAPIError as e:
            e.details.operation = "get_routes"
            if not e.details.message.startswith("Failed to get routing options"):
                e.details.message = f"Failed to get routing options: {e.details.message}"
            logger.error(f"Failed to get routing options: {e.details.to_human_readable()}", exc_info=True)
            return []
        except Exception as e:
            logger.error(f"Failed to get routing options: {e}", exc_info=True)
            return []

    # Convenience Functions for Common Order Types

    def place_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        limit_price: float,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a limit order (convenience wrapper).

        Args:
            symbol: Trading symbol
            side: "BUY" or "SELL"
            quantity: Number of contracts
            limit_price: Limit price
            time_in_force: "DAY", "GTC", "IOC", "FOK" (default: "DAY")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (order_id, status_message)

        Dependencies: OrderExecutionOperations.place_order

        Example:
            order_id, status = sdk.order_executions.place_limit_order(
                symbol="MNQZ25",
                side="BUY",
                quantity=2,
                limit_price=25000.00,
                mode="PAPER"
            )
        """
        return self.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type="Limit",
            limit_price=limit_price,
            time_in_force=time_in_force,
            mode=mode,
        )

    def place_stop_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        stop_price: float,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a stop order (convenience wrapper).

        Args:
            symbol: Trading symbol
            side: "BUY" or "SELL"
            quantity: Number of contracts
            stop_price: Stop price
            time_in_force: "DAY", "GTC", "IOC", "FOK" (default: "DAY")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (order_id, status_message)

        Dependencies: OrderExecutionOperations.place_order

        Example:
            order_id, status = sdk.order_executions.place_stop_order(
                symbol="MNQZ25",
                side="SELL",
                quantity=2,
                stop_price=24900.00,
                mode="PAPER"
            )
        """
        return self.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type="Stop",
            stop_price=stop_price,
            time_in_force=time_in_force,
            mode=mode,
        )

    def place_stop_limit_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        limit_price: float,
        stop_price: float,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a stop-limit order (convenience wrapper).

        Args:
            symbol: Trading symbol
            side: "BUY" or "SELL"
            quantity: Number of contracts
            limit_price: Limit price
            stop_price: Stop price
            time_in_force: "DAY", "GTC", "IOC", "FOK" (default: "DAY")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (order_id, status_message)

        Dependencies: OrderExecutionOperations.place_order

        Example:
            order_id, status = sdk.order_executions.place_stop_limit_order(
                symbol="MNQZ25",
                side="SELL",
                quantity=2,
                limit_price=24950.00,
                stop_price=24900.00,
                mode="PAPER"
            )
        """
        return self.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type="StopLimit",
            limit_price=limit_price,
            stop_price=stop_price,
            time_in_force=time_in_force,
            mode=mode,
        )

    def place_trailing_stop_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> tuple[str | None, str]:
        """
        Place a trailing stop order (convenience wrapper).

        Args:
            symbol: Trading symbol
            side: "BUY" or "SELL"
            quantity: Number of contracts
            trail_amount: Trail amount in price units (points) (optional)
                Note: For futures, this is in price units, not dollar amounts.
                For MNQ: 1 point = $2.00, so trail_amount=1.5 means $3.00 trail
            trail_percent: Trail percentage (optional, e.g., 1.0 for 1%)
            time_in_force: "DAY", "GTC", "IOC", "FOK" (default: "DAY")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Tuple of (order_id, status_message)

        Dependencies: OrderExecutionOperations.place_order

        Example:
            # Using trail amount (points)
            order_id, status = sdk.order_executions.place_trailing_stop_order(
                symbol="MNQZ25",
                side="SELL",
                quantity=2,
                trail_amount=1.5,  # $3.00 trail for MNQ
                mode="PAPER"
            )

            # Using trail percentage
            order_id, status = sdk.order_executions.place_trailing_stop_order(
                symbol="MNQZ25",
                side="SELL",
                quantity=2,
                trail_percent=1.0,  # 1% trail
                mode="PAPER"
            )
        """
        # Validation is handled by place_order(), but we validate trail parameters here for clearer errors
        if trail_amount is None and trail_percent is None:
            logger.error("❌ Trailing stop order requires either trail_amount or trail_percent")
            return None, "ERROR: Trailing stop requires trail_amount or trail_percent"

        # Validate trail_amount if provided
        if trail_amount is not None:
            if not isinstance(trail_amount, (int, float)):
                logger.error(f"❌ trail_amount must be a number, got {type(trail_amount).__name__}")
                return None, f"ERROR: trail_amount must be a number, got {type(trail_amount).__name__}"
            if trail_amount <= 0:
                logger.error(f"❌ trail_amount must be positive, got {trail_amount}")
                return None, f"ERROR: trail_amount must be positive, got {trail_amount}"
            if trail_amount > 10000:
                logger.error(
                    f"❌ trail_amount seems unreasonably large ({trail_amount} points). Maximum recommended: 10000"
                )
                return (
                    None,
                    f"ERROR: trail_amount seems unreasonably large ({trail_amount} points). Maximum recommended: 10000",
                )

        # Validate trail_percent if provided
        if trail_percent is not None:
            if not isinstance(trail_percent, (int, float)):
                logger.error(f"❌ trail_percent must be a number, got {type(trail_percent).__name__}")
                return None, f"ERROR: trail_percent must be a number, got {type(trail_percent).__name__}"
            if trail_percent <= 0:
                logger.error(f"❌ trail_percent must be positive, got {trail_percent}")
                return None, f"ERROR: trail_percent must be positive, got {trail_percent}"
            if trail_percent > 100:
                logger.error(f"❌ trail_percent seems unreasonably large ({trail_percent}%). Maximum recommended: 100%")
                return (
                    None,
                    f"ERROR: trail_percent seems unreasonably large ({trail_percent}%). Maximum recommended: 100%",
                )

        return self.place_order(
            symbol=symbol,
            side=side,
            quantity=quantity,
            order_type="TrailingStop",
            trail_amount=trail_amount,
            trail_percent=trail_percent,
            time_in_force=time_in_force,
            mode=mode,
        )

    def place_oco_order(self, orders: list[dict[str, Any]], mode: str | None = None) -> dict[str, Any]:
        """
        Place an OCO (One-Cancels-Other) order (convenience wrapper).

        OCO orders are a group of orders where if one fills, the others are cancelled.
        Commonly used for breakout strategies or entry orders with multiple price levels.

        Args:
            orders: List of 2+ order dictionaries (same format as place_order)
                Each order dict should have: AccountID, Symbol, TradeAction, OrderType, Quantity, etc.
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with GroupOrderResponse including:
            - GroupID: Group order ID
            - GroupName: Group order name
            - Type: "OCO"
            - Orders: List of order responses with OrderIDs

        Dependencies: OrderExecutionOperations.place_group_order

        Example:
            # OCO order: Buy if price breaks above 25010, or sell short if price breaks below 24990
            oco_orders = [
                {
                    "AccountID": "SIM123456",
                    "Symbol": "MNQZ25",
                    "TradeAction": "Buy",
                    "OrderType": "StopMarket",
                    "Quantity": "2",
                    "StopPrice": "25010.00",
                    "TimeInForce": {"Duration": "DAY"}
                },
                {
                    "AccountID": "SIM123456",
                    "Symbol": "MNQZ25",
                    "TradeAction": "SellShort",
                    "OrderType": "StopMarket",
                    "Quantity": "2",
                    "StopPrice": "24990.00",
                    "TimeInForce": {"Duration": "DAY"}
                }
            ]
            result = sdk.order_executions.place_oco_order(oco_orders, mode="PAPER")
        """
        if len(orders) < 2:
            logger.error("❌ OCO order requires at least 2 orders")
            raise ValueError("OCO order requires at least 2 orders")

        return self.place_group_order("OCO", orders, mode=mode)

    def place_bracket_order(
        self,
        symbol: str,
        entry_side: str,
        quantity: int,
        profit_target: float,
        stop_loss: float | None = None,
        trail_amount: float | None = None,
        trail_percent: float | None = None,
        use_trailing_stop: bool = False,
        entry_price: float | None = None,
        entry_order_type: str = "Market",
        time_in_force: str = "DAY",
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Place a bracket order (entry + profit target + stop-loss or trailing stop).

        Bracket orders are used to exit positions with both a profit target and stop-loss (or trailing stop).
        Uses the proper group order API (BRK type) to ensure orders are linked.

        For bracket orders:
        - Entry order: Opens the position (Market or Limit)
        - Profit target: Limit order to take profit (opposite side of entry)
        - Stop-loss: Stop order to limit loss (opposite side of entry) OR TrailingStop order

        Args:
            symbol: Trading symbol
            entry_side: "BUY" or "SELL" for entry
            quantity: Number of contracts
            profit_target: Profit target price (limit order)
            stop_loss: Stop-loss price (stop order) - Required if use_trailing_stop=False
            trail_amount: Trail amount in price units (points) for trailing stop (optional)
                Note: For futures, this is in price units, not dollar amounts.
                For MNQ: 1 point = $2.00, so trail_amount=1.5 means $3.00 trail
            trail_percent: Trail percentage for trailing stop (optional, e.g., 1.0 for 1%)
            use_trailing_stop: If True, use trailing stop instead of fixed stop-loss (default: False)
            entry_price: Entry limit price (None for market entry)
            entry_order_type: "Market" or "Limit" (default: "Market")
            time_in_force: "DAY", "GTC", "IOC", "FOK" (default: "DAY")
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with GroupOrderResponse including:
            - GroupID: Group order ID
            - GroupName: Group order name
            - Type: "BRK"
            - Orders: List of 3 order responses (entry, profit target, stop-loss/trailing-stop) with OrderIDs

        Dependencies: OrderExecutionOperations.place_group_order, AccountOperations.get_account_info

        Example:
            # Bracket order with fixed stop-loss
            result = sdk.order_executions.place_bracket_order(
                symbol="MNQZ25",
                entry_side="BUY",
                quantity=2,
                profit_target=25100.00,
                stop_loss=24900.00,
                entry_price=None,  # Market entry
                mode="PAPER"
            )

            # Bracket order with trailing stop
            result = sdk.order_executions.place_bracket_order(
                symbol="MNQZ25",
                entry_side="BUY",
                quantity=2,
                profit_target=25100.00,
                use_trailing_stop=True,
                trail_amount=1.5,  # $3.00 trail for MNQ
                entry_price=None,
                mode="PAPER"
            )

            # Extract order IDs
            entry_order_id = result["Orders"][0]["OrderID"]
            profit_order_id = result["Orders"][1]["OrderID"]
            stop_order_id = result["Orders"][2]["OrderID"]
        """
        if mode is None:
            mode = sdk_config.trading_mode

        # Get account ID
        account_info = self.accounts.get_account_info(mode)
        account_id = account_info.get("account_id") or self.account_id
        if not account_id:
            logger.error(f"No account ID available for {mode} mode - cannot place bracket order")
            raise ValueError(f"No account ID available for {mode} mode")

        # Validate symbol
        if not symbol or not isinstance(symbol, str):
            logger.error(
                f"❌ symbol must be a non-empty string, got {type(symbol).__name__ if symbol is not None else 'None'}"
            )
            raise ValueError(
                f"symbol must be a non-empty string, got {type(symbol).__name__ if symbol is not None else 'None'}"
            )
        symbol = symbol.strip()
        if not symbol:
            logger.error("❌ symbol cannot be empty or whitespace only")
            raise ValueError("symbol cannot be empty or whitespace only")
        if len(symbol) > 50:
            logger.error(f"❌ symbol seems too long ({len(symbol)} characters). Maximum recommended: 50 characters")
            raise ValueError(f"symbol seems too long ({len(symbol)} characters). Maximum recommended: 50")

        # Validate entry_side
        if not entry_side or not isinstance(entry_side, str):
            logger.error(
                f"❌ entry_side must be 'BUY' or 'SELL', got {type(entry_side).__name__ if entry_side is not None else 'None'}"
            )
            raise ValueError(
                f"entry_side must be 'BUY' or 'SELL', got {type(entry_side).__name__ if entry_side is not None else 'None'}"
            )
        entry_side_upper = entry_side.upper().strip()
        if entry_side_upper not in ["BUY", "SELL"]:
            logger.error(f"❌ entry_side must be 'BUY' or 'SELL', got '{entry_side}'")
            raise ValueError(f"entry_side must be 'BUY' or 'SELL', got '{entry_side}'")

        # Validate quantity
        if not isinstance(quantity, int):
            logger.error(f"❌ quantity must be an integer, got {type(quantity).__name__}")
            raise TypeError(f"quantity must be an integer, got {type(quantity).__name__}")
        if quantity <= 0:
            logger.error(f"❌ quantity must be positive, got {quantity}")
            raise ValueError(f"quantity must be positive, got {quantity}")
        if quantity > 10000:
            logger.error(
                f"❌ quantity seems unreasonably large ({quantity} contracts). Maximum recommended: 10,000 contracts"
            )
            raise ValueError(f"quantity seems unreasonably large ({quantity} contracts). Maximum recommended: 10,000")

        # Validate profit_target
        if not isinstance(profit_target, (int, float)):
            logger.error(f"❌ profit_target must be a number, got {type(profit_target).__name__}")
            raise TypeError(f"profit_target must be a number, got {type(profit_target).__name__}")
        if profit_target <= 0:
            logger.error(f"❌ profit_target must be positive, got {profit_target}")
            raise ValueError(f"profit_target must be positive, got {profit_target}")
        if profit_target > 1000000:
            logger.error(
                f"❌ profit_target seems unreasonably large (${profit_target:,.2f}). Maximum recommended: $1,000,000"
            )
            raise ValueError(
                f"profit_target seems unreasonably large (${profit_target:,.2f}). Maximum recommended: $1,000,000"
            )

        # Validate entry_order_type
        if not entry_order_type or not isinstance(entry_order_type, str):
            logger.error(
                f"❌ entry_order_type must be 'Market' or 'Limit', got {type(entry_order_type).__name__ if entry_order_type is not None else 'None'}"
            )
            raise ValueError(
                f"entry_order_type must be 'Market' or 'Limit', got {type(entry_order_type).__name__ if entry_order_type is not None else 'None'}"
            )
        entry_order_type_upper = entry_order_type.upper().strip()
        if entry_order_type_upper not in ["MARKET", "LIMIT"]:
            logger.error(f"❌ entry_order_type must be 'Market' or 'Limit', got '{entry_order_type}'")
            raise ValueError(f"entry_order_type must be 'Market' or 'Limit', got '{entry_order_type}'")

        # Validate time_in_force
        if not time_in_force or not isinstance(time_in_force, str):
            logger.error(
                f"❌ time_in_force must be a string, got {type(time_in_force).__name__ if time_in_force is not None else 'None'}"
            )
            raise ValueError(
                f"time_in_force must be a string, got {type(time_in_force).__name__ if time_in_force is not None else 'None'}"
            )
        valid_time_in_force = ["DAY", "DYP", "GTC", "GCP", "GTD", "GDP", "OPG", "CLO", "IOC", "FOK", "1", "3", "5"]
        time_in_force_upper = time_in_force.upper().strip()
        if time_in_force_upper not in valid_time_in_force:
            logger.error(f"❌ time_in_force must be one of {valid_time_in_force}, got '{time_in_force}'")
            raise ValueError(f"time_in_force must be one of {valid_time_in_force}, got '{time_in_force}'")

        # Validate mode if provided
        if mode is not None:
            if not isinstance(mode, str):
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
                raise ValueError(f"mode must be 'PAPER' or 'LIVE', got {type(mode).__name__}")
            mode_upper = mode.upper().strip()
            if mode_upper not in ["PAPER", "LIVE"]:
                logger.error(f"❌ mode must be 'PAPER' or 'LIVE', got '{mode}'")
                raise ValueError(f"mode must be 'PAPER' or 'LIVE', got '{mode}'")
            mode = mode_upper

        # Validate parameters
        if not use_trailing_stop and stop_loss is None:
            logger.error("❌ Bracket order requires stop_loss when use_trailing_stop=False")
            raise ValueError("stop_loss is required when use_trailing_stop=False")

        if use_trailing_stop and trail_amount is None and trail_percent is None:
            logger.error("❌ Bracket order with trailing stop requires either trail_amount or trail_percent")
            raise ValueError("trail_amount or trail_percent required when use_trailing_stop=True")

        # Validate stop_loss if provided
        if not use_trailing_stop and stop_loss is not None:
            if not isinstance(stop_loss, (int, float)):
                logger.error(f"❌ stop_loss must be a number, got {type(stop_loss).__name__}")
                raise TypeError(f"stop_loss must be a number, got {type(stop_loss).__name__}")
            if stop_loss <= 0:
                logger.error(f"❌ stop_loss must be positive, got {stop_loss}")
                raise ValueError(f"stop_loss must be positive, got {stop_loss}")
            if stop_loss > 1000000:
                logger.error(
                    f"❌ stop_loss seems unreasonably large (${stop_loss:,.2f}). Maximum recommended: $1,000,000"
                )
                raise ValueError(
                    f"stop_loss seems unreasonably large (${stop_loss:,.2f}). Maximum recommended: $1,000,000"
                )

        # Validate entry_price if provided
        if entry_price is not None:
            if not isinstance(entry_price, (int, float)):
                logger.error(f"❌ entry_price must be a number, got {type(entry_price).__name__}")
                raise TypeError(f"entry_price must be a number, got {type(entry_price).__name__}")
            if entry_price <= 0:
                logger.error(f"❌ entry_price must be positive, got {entry_price}")
                raise ValueError(f"entry_price must be positive, got {entry_price}")
            if entry_price > 1000000:
                logger.error(
                    f"❌ entry_price seems unreasonably large (${entry_price:,.2f}). Maximum recommended: $1,000,000"
                )
                raise ValueError(
                    f"entry_price seems unreasonably large (${entry_price:,.2f}). Maximum recommended: $1,000,000"
                )
            if entry_order_type_upper != "LIMIT":
                logger.warning(
                    f"⚠️  entry_price provided but entry_order_type is '{entry_order_type}'. entry_price is only used for Limit orders."
                )

        # Optional: Logical validation for bracket order prices
        if entry_price is not None:
            if entry_side_upper == "BUY":
                if profit_target <= entry_price:
                    logger.warning(
                        f"⚠️  BUY bracket: profit_target (${profit_target:.2f}) should typically be > entry_price (${entry_price:.2f})"
                    )
                if not use_trailing_stop and stop_loss is not None and stop_loss >= entry_price:
                    logger.warning(
                        f"⚠️  BUY bracket: stop_loss (${stop_loss:.2f}) should typically be < entry_price (${entry_price:.2f})"
                    )
            else:  # SELL
                if profit_target >= entry_price:
                    logger.warning(
                        f"⚠️  SELL bracket: profit_target (${profit_target:.2f}) should typically be < entry_price (${entry_price:.2f})"
                    )
                if not use_trailing_stop and stop_loss is not None and stop_loss <= entry_price:
                    logger.warning(
                        f"⚠️  SELL bracket: stop_loss (${stop_loss:.2f}) should typically be > entry_price (${entry_price:.2f})"
                    )

        if use_trailing_stop and trail_amount is not None and trail_percent is not None:
            logger.warning("⚠️  Both trail_amount and trail_percent provided - using trail_amount")

        # Validate trail_amount if provided
        if use_trailing_stop and trail_amount is not None:
            if not isinstance(trail_amount, (int, float)):
                logger.error(f"❌ trail_amount must be a number, got {type(trail_amount).__name__}")
                raise TypeError(f"trail_amount must be a number, got {type(trail_amount).__name__}")
            if trail_amount <= 0:
                logger.error(f"❌ trail_amount must be positive, got {trail_amount}")
                raise ValueError(f"trail_amount must be positive, got {trail_amount}")
            if trail_amount > 10000:
                logger.error(
                    f"❌ trail_amount seems unreasonably large ({trail_amount} points). Maximum recommended: 10000"
                )
                raise ValueError(
                    f"trail_amount seems unreasonably large ({trail_amount} points). Maximum recommended: 10000"
                )

        # Validate trail_percent if provided
        if use_trailing_stop and trail_percent is not None:
            if not isinstance(trail_percent, (int, float)):
                logger.error(f"❌ trail_percent must be a number, got {type(trail_percent).__name__}")
                raise TypeError(f"trail_percent must be a number, got {type(trail_percent).__name__}")
            if trail_percent <= 0:
                logger.error(f"❌ trail_percent must be positive, got {trail_percent}")
                raise ValueError(f"trail_percent must be positive, got {trail_percent}")
            if trail_percent > 100:
                logger.error(f"❌ trail_percent seems unreasonably large ({trail_percent}%). Maximum recommended: 100%")
                raise ValueError(
                    f"trail_percent seems unreasonably large ({trail_percent}%). Maximum recommended: 100%"
                )

        # Determine exit side (opposite of entry)
        exit_side = "SELL" if entry_side_upper == "BUY" else "BUY"

        # Build entry order
        entry_order = {
            "AccountID": account_id,
            "Symbol": symbol,
            "TradeAction": entry_side_upper,
            "OrderType": entry_order_type_upper,
            "Quantity": str(quantity),
            "TimeInForce": {"Duration": time_in_force_upper},
        }
        if entry_price is not None and entry_order_type_upper == "LIMIT":
            entry_order["LimitPrice"] = str(entry_price)

        # Build profit target order (limit order)
        profit_order = {
            "AccountID": account_id,
            "Symbol": symbol,
            "TradeAction": exit_side,
            "OrderType": "Limit",
            "Quantity": str(quantity),
            "LimitPrice": str(profit_target),
            "TimeInForce": {"Duration": time_in_force_upper},
        }

        # Build stop-loss order (stop order or trailing stop)
        if use_trailing_stop:
            # Trailing stop order
            stop_order = {
                "AccountID": account_id,
                "Symbol": symbol,
                "TradeAction": exit_side,
                "OrderType": "TrailingStop",
                "Quantity": str(quantity),
                "TimeInForce": {"Duration": time_in_force_upper},
            }
            if trail_amount is not None:
                stop_order["TrailAmount"] = str(trail_amount)
            elif trail_percent is not None:
                stop_order["TrailPercent"] = str(trail_percent)
        else:
            # Fixed stop-loss order
            stop_order = {
                "AccountID": account_id,
                "Symbol": symbol,
                "TradeAction": exit_side,
                "OrderType": "StopMarket",
                "Quantity": str(quantity),
                "StopPrice": str(stop_loss),
                "TimeInForce": {"Duration": time_in_force_upper},
            }

        # Place as bracket group order
        orders = [entry_order, profit_order, stop_order]

        logger.info("=" * 60)
        logger.info(f"📤 Placing BRACKET order: {entry_side} {quantity} {symbol}")
        logger.info(
            f"   Entry: {entry_order_type} @ ${entry_price:.2f}" if entry_price else f"   Entry: {entry_order_type}"
        )
        logger.info(f"   Profit Target: ${profit_target:.2f}")
        if use_trailing_stop:
            if trail_amount:
                logger.info(f"   Trailing Stop: ${trail_amount:.2f} points")
            elif trail_percent:
                logger.info(f"   Trailing Stop: {trail_percent:.2f}%")
        else:
            logger.info(f"   Stop Loss: ${stop_loss:.2f}")
        logger.info("=" * 60)

        try:
            return self.place_group_order("BRK", orders, mode=mode)
        except TradeStationAPIError as e:
            e.details.operation = "place_bracket_order"
            if not e.details.message.startswith("Bracket order placement failed"):
                e.details.message = f"Bracket order placement failed: {e.details.message}"
            logger.error(f"Bracket order placement failed: {e.details.to_human_readable()}")
            raise
        except Exception as e:
            logger.error(f"Bracket order placement failed: {e}", exc_info=True)
            raise

"""
TradeStation Data Mappers

Normalizes TradeStation API objects to consistent dictionary format.
Handles variations in API object attribute names (PascalCase, camelCase, snake_case).

Dependencies: None
"""

from typing import Any

from .logger import setup_logger

from .config import sdk_config

logger = setup_logger(__name__, sdk_config.log_level)


def normalize_order(order: Any) -> dict[str, Any] | None:
    """
    Normalize TradeStation order object to dictionary.

    Handles both camelCase and PascalCase attribute names from API responses.

    Args:
        order: Order object from TradeStation API (dict or object)

    Returns:
        Normalized order dictionary or None if invalid

    Dependencies: None
    """
    try:
        # Handle dict input (from API responses)
        if isinstance(order, dict):
            order_id = order.get("OrderID") or order.get("order_id") or order.get("orderId") or order.get("id")
            if not order_id:
                logger.warning(f"Order dict missing order_id: {order}")
                return None

            # Extract all fields from dict
            return {
                "order_id": str(order_id),
                "symbol": order.get("Symbol") or order.get("symbol"),
                "status": str(order.get("Status", "UNKNOWN")).upper(),
                "filled_quantity": int(float(order.get("FilledQuantity", 0))) if order.get("FilledQuantity") else 0,
                "remaining_quantity": int(float(order.get("QuantityRemaining", 0)))
                if order.get("QuantityRemaining")
                else None,
                "average_fill_price": float(order.get("AverageFillPrice", 0))
                if order.get("AverageFillPrice")
                else None,
                "reject_reason": order.get("RejectionReason") or order.get("rejection_reason"),
                "action": str(order.get("TradeAction", "")).upper() if order.get("TradeAction") else None,
                "quantity": int(float(order.get("Quantity", 0))) if order.get("Quantity") else None,
                "order_type": str(order.get("OrderType", "")).upper() if order.get("OrderType") else None,
                "group_id": str(order.get("GroupID") or order.get("GroupName", ""))
                if order.get("GroupID") or order.get("GroupName")
                else None,
                "group_type": str(order.get("Type", "")).upper() if order.get("Type") else None,
                "conditional_orders": order.get("ConditionalOrders") or order.get("conditional_orders"),
                "market_activation_rules": order.get("MarketActivationRules") or order.get("market_activation_rules"),
                "time_activation_rules": order.get("TimeActivationRules") or order.get("time_activation_rules"),
                "trailing_stop": order.get("TrailingStop") or order.get("trailing_stop"),
                "commission_fee": float(order.get("CommissionFee", 0)) if order.get("CommissionFee") else None,
                "unbundled_route_fee": float(order.get("UnbundledRouteFee", 0))
                if order.get("UnbundledRouteFee")
                else None,
                "price_used_for_buying_power": float(order.get("PriceUsedForBuyingPower", 0))
                if order.get("PriceUsedForBuyingPower")
                else None,
                "routing": order.get("Routing") or order.get("routing"),
                "currency": order.get("Currency") or order.get("currency") or "USD",
                "duration": order.get("Duration") or order.get("duration"),
                "good_till_date": order.get("GoodTillDate") or order.get("good_till_date"),
                "opened_date_time": order.get("OpenedDateTime")
                or order.get("opened_date_time")
                or order.get("PlacedTime"),
                "closed_date_time": order.get("ClosedDateTime")
                or order.get("closed_date_time")
                or order.get("FilledTime"),
                "filled_price": float(order.get("FilledPrice", 0)) if order.get("FilledPrice") else None,
                "status_description": order.get("StatusDescription") or order.get("status_description"),
                "advanced_options": order.get("AdvancedOptions") or order.get("advanced_options"),
                "order_params": {
                    "limit_price": float(order.get("LimitPrice", 0)) if order.get("LimitPrice") else None,
                    "stop_price": float(order.get("StopPrice", 0)) if order.get("StopPrice") else None,
                    "trailing_stop": order.get("TrailingStop") or order.get("trailing_stop") or {},
                },
            }

        # Handle object input (from SDK or other sources)
        # Extract order_id (try multiple variations)
        order_id = (
            getattr(order, "order_id", None)
            or getattr(order, "OrderID", None)
            or getattr(order, "orderId", None)
            or getattr(order, "id", None)
        )

        if not order_id:
            logger.warning(f"Order object missing order_id: {order}")
            return None

        # Extract status (normalize to uppercase)
        status = (
            getattr(order, "status", None)
            or getattr(order, "Status", None)
            or getattr(order, "order_status", None)
            or "UNKNOWN"
        )
        status = str(status).upper()

        # Extract other fields with fallbacks
        symbol = getattr(order, "symbol", None) or getattr(order, "Symbol", None) or getattr(order, "instrument", None)

        filled_quantity = (
            getattr(order, "filled_quantity", None)
            or getattr(order, "FilledQuantity", None)
            or getattr(order, "filledQuantity", None)
            or 0
        )

        remaining_quantity = (
            getattr(order, "unfilled_quantity", None)
            or getattr(order, "UnfilledQuantity", None)
            or getattr(order, "remainingQuantity", None)
            or getattr(order, "remaining_quantity", None)
        )

        average_fill_price = (
            getattr(order, "average_price", None)
            or getattr(order, "AverageFillPrice", None)
            or getattr(order, "averageFillPrice", None)
            or getattr(order, "avg_fill_price", None)
        )

        reject_reason = (
            getattr(order, "reject_reason", None)
            or getattr(order, "RejectReason", None)
            or getattr(order, "rejection_reason", None)
            or getattr(order, "rejectReason", None)
        )

        # Extract additional fields for comprehensive order tracking
        action = (
            getattr(order, "action", None)
            or getattr(order, "TradeAction", None)
            or getattr(order, "tradeAction", None)
            or getattr(order, "side", None)
        )

        quantity = (
            getattr(order, "quantity", None)
            or getattr(order, "Quantity", None)
            or getattr(order, "quantityOrdered", None)
            or getattr(order, "QuantityOrdered", None)
        )

        order_type = (
            getattr(order, "order_type", None) or getattr(order, "OrderType", None) or getattr(order, "orderType", None)
        )

        limit_price = (
            getattr(order, "limit_price", None)
            or getattr(order, "LimitPrice", None)
            or getattr(order, "limitPrice", None)
        )

        stop_price = (
            getattr(order, "stop_price", None) or getattr(order, "StopPrice", None) or getattr(order, "stopPrice", None)
        )

        # Extract group-related fields
        group_id = (
            getattr(order, "group_id", None)
            or getattr(order, "GroupID", None)
            or getattr(order, "groupId", None)
            or getattr(order, "GroupName", None)
        )

        group_type = (
            getattr(order, "group_type", None)
            or getattr(order, "GroupType", None)
            or getattr(order, "groupType", None)
            or getattr(order, "Type", None)
        )

        # Extract conditional orders (JSONB)
        conditional_orders = (
            getattr(order, "conditional_orders", None)
            or getattr(order, "ConditionalOrders", None)
            or getattr(order, "conditionalOrders", None)
        )

        # Extract activation rules (JSONB)
        market_activation_rules = (
            getattr(order, "market_activation_rules", None)
            or getattr(order, "MarketActivationRules", None)
            or getattr(order, "marketActivationRules", None)
        )

        time_activation_rules = (
            getattr(order, "time_activation_rules", None)
            or getattr(order, "TimeActivationRules", None)
            or getattr(order, "timeActivationRules", None)
        )

        # Extract trailing stop (JSONB)
        trailing_stop = (
            getattr(order, "trailing_stop", None)
            or getattr(order, "TrailingStop", None)
            or getattr(order, "trailingStop", None)
        )

        # Extract other fields
        commission_fee = (
            getattr(order, "commission_fee", None)
            or getattr(order, "CommissionFee", None)
            or getattr(order, "commissionFee", None)
        )

        unbundled_route_fee = (
            getattr(order, "unbundled_route_fee", None)
            or getattr(order, "UnbundledRouteFee", None)
            or getattr(order, "unbundledRouteFee", None)
        )

        price_used_for_buying_power = (
            getattr(order, "price_used_for_buying_power", None)
            or getattr(order, "PriceUsedForBuyingPower", None)
            or getattr(order, "priceUsedForBuyingPower", None)
        )

        routing = getattr(order, "routing", None) or getattr(order, "Routing", None)

        currency = getattr(order, "currency", None) or getattr(order, "Currency", None) or "USD"

        duration = getattr(order, "duration", None) or getattr(order, "Duration", None)

        good_till_date = (
            getattr(order, "good_till_date", None)
            or getattr(order, "GoodTillDate", None)
            or getattr(order, "goodTillDate", None)
        )

        opened_date_time = (
            getattr(order, "opened_date_time", None)
            or getattr(order, "OpenedDateTime", None)
            or getattr(order, "openedDateTime", None)
            or getattr(order, "PlacedTime", None)
        )

        closed_date_time = (
            getattr(order, "closed_date_time", None)
            or getattr(order, "ClosedDateTime", None)
            or getattr(order, "closedDateTime", None)
            or getattr(order, "FilledTime", None)
        )

        filled_price = (
            getattr(order, "filled_price", None)
            or getattr(order, "FilledPrice", None)
            or getattr(order, "filledPrice", None)
        )

        status_description = (
            getattr(order, "status_description", None)
            or getattr(order, "StatusDescription", None)
            or getattr(order, "statusDescription", None)
        )

        advanced_options = (
            getattr(order, "advanced_options", None)
            or getattr(order, "AdvancedOptions", None)
            or getattr(order, "advancedOptions", None)
        )

        # Build order_params JSONB with all order parameters
        order_params = {}
        if limit_price:
            order_params["limit_price"] = float(limit_price) if limit_price else None
        if stop_price:
            order_params["stop_price"] = float(stop_price) if stop_price else None
        if trailing_stop:
            order_params["trailing_stop"] = trailing_stop if isinstance(trailing_stop, dict) else {}

        return {
            "order_id": str(order_id),
            "symbol": symbol,
            "status": status,
            "filled_quantity": int(filled_quantity) if filled_quantity is not None else 0,
            "remaining_quantity": int(remaining_quantity) if remaining_quantity is not None else None,
            "average_fill_price": float(average_fill_price) if average_fill_price is not None else None,
            "reject_reason": reject_reason if status == "REJECTED" else None,
            "action": str(action).upper() if action else None,
            "quantity": int(quantity) if quantity is not None else None,
            "order_type": str(order_type).upper() if order_type else None,
            "group_id": str(group_id) if group_id else None,
            "group_type": str(group_type).upper() if group_type else None,
            "conditional_orders": conditional_orders if conditional_orders else None,
            "market_activation_rules": market_activation_rules if market_activation_rules else None,
            "time_activation_rules": time_activation_rules if time_activation_rules else None,
            "trailing_stop": trailing_stop if trailing_stop else None,
            "commission_fee": float(commission_fee) if commission_fee is not None else None,
            "unbundled_route_fee": float(unbundled_route_fee) if unbundled_route_fee is not None else None,
            "price_used_for_buying_power": float(price_used_for_buying_power)
            if price_used_for_buying_power is not None
            else None,
            "routing": str(routing) if routing else None,
            "currency": str(currency) if currency else "USD",
            "duration": str(duration) if duration else None,
            "good_till_date": str(good_till_date) if good_till_date else None,
            "opened_date_time": str(opened_date_time) if opened_date_time else None,
            "closed_date_time": str(closed_date_time) if closed_date_time else None,
            "filled_price": float(filled_price) if filled_price is not None else None,
            "status_description": str(status_description) if status_description else None,
            "advanced_options": str(advanced_options) if advanced_options else None,
            "order_params": order_params,
        }

    except Exception as e:
        logger.error(f"Failed to normalize order: {e}")
        return None


def normalize_position(position: Any) -> dict[str, Any] | None:
    """
    Normalize TradeStation position object to dictionary.

    Handles both camelCase and PascalCase attribute names from API responses.

    Args:
        position: Position object from TradeStation API (dict or object)

    Returns:
        Normalized position dictionary or None if invalid

    Dependencies: None
    """
    try:
        # Handle dict input (from API responses)
        if isinstance(position, dict):
            symbol = position.get("Symbol") or position.get("symbol") or position.get("instrument")
            if not symbol:
                return None

            quantity = int(float(position.get("Quantity", 0))) if position.get("Quantity") else 0

            if quantity == 0:
                return None

            side = "LONG" if quantity > 0 else "SHORT"

            return {
                "symbol": str(symbol),
                "quantity": quantity,
                "side": side,
                "average_entry_price": float(position.get("AveragePrice", 0)) if position.get("AveragePrice") else None,
                "unrealized_pnl": float(position.get("UnrealizedPnL", 0)) if position.get("UnrealizedPnL") else None,
                "position_id": str(position.get("PositionID", "")) if position.get("PositionID") else None,
                "average_price": float(position.get("AveragePrice", 0)) if position.get("AveragePrice") else None,
                "last": float(position.get("Last", 0)) if position.get("Last") else None,
                "bid": float(position.get("Bid", 0)) if position.get("Bid") else None,
                "ask": float(position.get("Ask", 0)) if position.get("Ask") else None,
                "todays_profit_loss": float(position.get("TodaysProfitLoss", 0))
                if position.get("TodaysProfitLoss")
                else None,
                "total_cost": float(position.get("TotalCost", 0)) if position.get("TotalCost") else None,
                "market_value": float(position.get("MarketValue", 0)) if position.get("MarketValue") else None,
                "mark_to_market_price": float(position.get("MarkToMarketPrice", 0))
                if position.get("MarkToMarketPrice")
                else None,
                "unrealized_profit_loss_percent": float(position.get("UnrealizedProfitLossPercent", 0))
                if position.get("UnrealizedProfitLossPercent")
                else None,
                "unrealized_profit_loss_qty": float(position.get("UnrealizedProfitLossQty", 0))
                if position.get("UnrealizedProfitLossQty")
                else None,
                "day_trade_requirement": float(position.get("DayTradeRequirement", 0))
                if position.get("DayTradeRequirement")
                else None,
                "initial_requirement": float(position.get("InitialRequirement", 0))
                if position.get("InitialRequirement")
                else None,
                "maintenance_margin": float(position.get("MaintenanceMargin", 0))
                if position.get("MaintenanceMargin")
                else None,
                "conversion_rate": float(position.get("ConversionRate", 1.0))
                if position.get("ConversionRate")
                else 1.0,
                "asset_type": position.get("AssetType") or position.get("asset_type"),
                "long_short": position.get("LongShort") or position.get("long_short"),
            }

        # Handle object input
        # Extract symbol
        symbol = (
            getattr(position, "symbol", None)
            or getattr(position, "Symbol", None)
            or getattr(position, "instrument", None)
        )

        if not symbol:
            return None

        # Extract quantity
        quantity = (
            getattr(position, "quantity", None)
            or getattr(position, "Quantity", None)
            or getattr(position, "qty", None)
            or 0
        )
        quantity = int(quantity) if quantity is not None else 0

        # Determine side
        side = None
        if quantity > 0:
            side = "LONG"
        elif quantity < 0:
            side = "SHORT"
        else:
            return None  # Flat position

        # Extract entry price
        entry_price = (
            getattr(position, "average_price", None)
            or getattr(position, "AveragePrice", None)
            or getattr(position, "averagePrice", None)
            or getattr(position, "entry_price", None)
            or getattr(position, "avg_entry_price", None)
        )

        # Extract unrealized P&L
        unrealized_pnl = (
            getattr(position, "unrealized_pnl", None)
            or getattr(position, "UnrealizedPnL", None)
            or getattr(position, "unrealizedPnL", None)
            or getattr(position, "unrealized_pnl", None)
            or getattr(position, "open_pnl", None)
        )

        # Extract additional fields from streaming positions endpoint
        position_id = (
            getattr(position, "position_id", None)
            or getattr(position, "PositionID", None)
            or getattr(position, "positionId", None)
        )

        average_price = (
            getattr(position, "average_price", None)
            or getattr(position, "AveragePrice", None)
            or getattr(position, "averagePrice", None)
            or entry_price
        )

        last = getattr(position, "last", None) or getattr(position, "Last", None)

        bid = getattr(position, "bid", None) or getattr(position, "Bid", None)

        ask = getattr(position, "ask", None) or getattr(position, "Ask", None)

        todays_profit_loss = (
            getattr(position, "todays_profit_loss", None)
            or getattr(position, "TodaysProfitLoss", None)
            or getattr(position, "todaysProfitLoss", None)
        )

        total_cost = (
            getattr(position, "total_cost", None)
            or getattr(position, "TotalCost", None)
            or getattr(position, "totalCost", None)
        )

        market_value = (
            getattr(position, "market_value", None)
            or getattr(position, "MarketValue", None)
            or getattr(position, "marketValue", None)
        )

        mark_to_market_price = (
            getattr(position, "mark_to_market_price", None)
            or getattr(position, "MarkToMarketPrice", None)
            or getattr(position, "markToMarketPrice", None)
        )

        unrealized_profit_loss_percent = (
            getattr(position, "unrealized_profit_loss_percent", None)
            or getattr(position, "UnrealizedProfitLossPercent", None)
            or getattr(position, "unrealizedProfitLossPercent", None)
        )

        unrealized_profit_loss_qty = (
            getattr(position, "unrealized_profit_loss_qty", None)
            or getattr(position, "UnrealizedProfitLossQty", None)
            or getattr(position, "unrealizedProfitLossQty", None)
        )

        day_trade_requirement = (
            getattr(position, "day_trade_requirement", None)
            or getattr(position, "DayTradeRequirement", None)
            or getattr(position, "dayTradeRequirement", None)
        )

        initial_requirement = (
            getattr(position, "initial_requirement", None)
            or getattr(position, "InitialRequirement", None)
            or getattr(position, "initialRequirement", None)
        )

        maintenance_margin = (
            getattr(position, "maintenance_margin", None)
            or getattr(position, "MaintenanceMargin", None)
            or getattr(position, "maintenanceMargin", None)
        )

        conversion_rate = (
            getattr(position, "conversion_rate", None)
            or getattr(position, "ConversionRate", None)
            or getattr(position, "conversionRate", None)
            or 1.0
        )

        asset_type = (
            getattr(position, "asset_type", None)
            or getattr(position, "AssetType", None)
            or getattr(position, "assetType", None)
        )

        long_short = (
            getattr(position, "long_short", None)
            or getattr(position, "LongShort", None)
            or getattr(position, "longShort", None)
        )

        return {
            "symbol": str(symbol),
            "quantity": quantity,
            "side": side,
            "average_entry_price": float(entry_price) if entry_price is not None else None,
            "unrealized_pnl": float(unrealized_pnl) if unrealized_pnl is not None else None,
            "position_id": str(position_id) if position_id else None,
            "average_price": float(average_price) if average_price is not None else None,
            "last": float(last) if last is not None else None,
            "bid": float(bid) if bid is not None else None,
            "ask": float(ask) if ask is not None else None,
            "todays_profit_loss": float(todays_profit_loss) if todays_profit_loss is not None else None,
            "total_cost": float(total_cost) if total_cost is not None else None,
            "market_value": float(market_value) if market_value is not None else None,
            "mark_to_market_price": float(mark_to_market_price) if mark_to_market_price is not None else None,
            "unrealized_profit_loss_percent": float(unrealized_profit_loss_percent)
            if unrealized_profit_loss_percent is not None
            else None,
            "unrealized_profit_loss_qty": float(unrealized_profit_loss_qty)
            if unrealized_profit_loss_qty is not None
            else None,
            "day_trade_requirement": float(day_trade_requirement) if day_trade_requirement is not None else None,
            "initial_requirement": float(initial_requirement) if initial_requirement is not None else None,
            "maintenance_margin": float(maintenance_margin) if maintenance_margin is not None else None,
            "conversion_rate": float(conversion_rate) if conversion_rate is not None else 1.0,
            "asset_type": str(asset_type) if asset_type else None,
            "long_short": str(long_short) if long_short else None,
        }
    except Exception as e:
        logger.error(f"Failed to normalize position: {e}")
        return None

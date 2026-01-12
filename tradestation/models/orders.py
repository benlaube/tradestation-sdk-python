"""
TradeStation Order Models

Pydantic models for TradeStation API order operations.
Includes request models, response models, and nested order components.

Dependencies: pydantic
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator

# Nested Order Models


class TradeStationTrailingStop(BaseModel):
    """Trailing stop parameters from TradeStation API."""

    Percent: str | None = Field(None, description="Trail percentage")
    Amount: str | None = Field(None, description="Trail amount in points")


class TradeStationOrderLeg(BaseModel):
    """Order leg for multi-leg orders (spreads, etc.)."""

    Symbol: str = Field(..., description="Leg symbol")
    AssetType: str | None = Field(None, description="STOCK, FUTURE, OPTION")
    BuyOrSell: str | None = Field(None, description="Buy or Sell")
    QuantityOrdered: str | None = Field(None, description="Quantity ordered")
    ExecQuantity: str | None = Field(None, description="Executed quantity")
    QuantityRemaining: str | None = Field(None, description="Remaining quantity")
    ExecutionPrice: str | None = Field(None, description="Execution price")
    OpenOrClose: str | None = Field(None, description="Open or Close")
    StrikePrice: str | None = Field(None, description="Strike price (options)")
    OptionType: str | None = Field(None, description="CALL or PUT (options)")
    ExpirationDate: str | None = Field(None, description="Expiration date (options)")
    Underlying: str | None = Field(None, description="Underlying symbol (options)")


class TradeStationMarketActivationRule(BaseModel):
    """Market activation rule for conditional orders."""

    RuleType: str | None = Field(None, description="Rule type (e.g., Price)")
    Symbol: str | None = Field(None, description="Trigger symbol")
    Predicate: str | None = Field(None, description="gt, lt, gte, lte, eq")
    TriggerKey: str | None = Field(None, description="Trigger key")
    Price: str | None = Field(None, description="Trigger price")


class TradeStationTimeActivationRule(BaseModel):
    """Time activation rule for conditional orders."""

    TimeUtc: str | None = Field(None, description="Activation time (UTC)")


class TradeStationConditionalOrder(BaseModel):
    """Conditional order relationship (OCO, OTO, OCA)."""

    Relationship: str | None = Field(None, description="OCO, OTO, or OCA")
    OrderID: str | None = Field(None, description="Related order ID")


# Request Models


class TradeStationOrderRequest(BaseModel):
    """
    TradeStation API order placement request model.

    Matches the exact structure TradeStation API v3 expects for order placement.

    Attributes:
        AccountID: TradeStation account ID
        Symbol: Trading symbol
        TradeAction: "Buy" or "Sell"
        OrderType: "Market", "Limit", "Stop", "StopLimit", "TrailingStop"
        Quantity: Number of contracts (as string, TradeStation format)
        LimitPrice: Limit price (optional, for Limit/StopLimit orders)
        StopPrice: Stop price (optional, for Stop/StopLimit orders)
        TimeInForce: Time in force object with Duration field
        TrailAmount: Trail amount in points (optional, for TrailingStop)
        TrailPercent: Trail percentage (optional, for TrailingStop)
    """

    AccountID: str = Field(..., description="TradeStation account ID")
    Symbol: str = Field(..., description="Trading symbol")
    TradeAction: str = Field(..., description="Buy or Sell")
    OrderType: str = Field(..., description="Market, Limit, Stop, StopLimit, TrailingStop")
    Quantity: str = Field(..., description="Number of contracts (as string)")
    LimitPrice: str | None = Field(None, description="Limit price (for Limit orders)")
    StopPrice: str | None = Field(None, description="Stop price (for Stop orders)")
    TimeInForce: dict[str, str] | None = Field(None, description="Time in force: {'Duration': 'DAY'|'GTC'|'IOC'|'FOK'}")
    TrailAmount: str | None = Field(None, description="Trail amount in points (for TrailingStop)")
    TrailPercent: str | None = Field(None, description="Trail percentage (for TrailingStop)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "AccountID": "SIM123456",
                "Symbol": "MNQZ25",
                "TradeAction": "Buy",
                "OrderType": "Market",
                "Quantity": "2",
                "TimeInForce": {"Duration": "DAY"},
            }
        }
    )


class TradeStationOrderGroupRequest(BaseModel):
    """
    TradeStation API group order request model (OCO/Bracket).

    Attributes:
        Type: Group type ("OCO", "BRK", or "NORMAL")
        Orders: List of order requests
    """

    Type: str = Field(..., description="Group type: OCO, BRK, or NORMAL")
    Orders: list[TradeStationOrderRequest] = Field(..., description="List of orders in the group")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Type": "OCO",
                "Orders": [
                    {
                        "AccountID": "SIM123456",
                        "Symbol": "MNQZ25",
                        "TradeAction": "Buy",
                        "OrderType": "Limit",
                        "Quantity": "2",
                        "LimitPrice": "25000.00",
                    }
                ],
            }
        }
    )


class OSO(TradeStationOrderGroupRequest):
    """Helper for OSO (Order Sends Order) groups."""

    Type: str = "OSO"

    @field_validator("Orders")
    @classmethod
    def validate_orders_count(cls, v: list[TradeStationOrderRequest]) -> list[TradeStationOrderRequest]:
        if len(v) < 2:
            raise ValueError("OSO orders must contain at least 2 orders (Parent + Child)")
        return v


class Bracket(TradeStationOrderGroupRequest):
    """Helper for Bracket groups."""

    Type: str = "BRK"

    @field_validator("Orders")
    @classmethod
    def validate_orders_count(cls, v: list[TradeStationOrderRequest]) -> list[TradeStationOrderRequest]:
        if len(v) < 3:
            raise ValueError("Bracket orders must contain at least 3 orders (Parent + Stop + Limit)")
        return v


# Response Models


class TradeStationOrderResponse(BaseModel):
    """
    Complete TradeStation API order response model.

    This model captures ALL fields from TradeStation API order responses,
    ensuring no data is lost when syncing orders from TradeStation.

    Attributes:
        AccountID: TradeStation account ID
        OrderID: TradeStation order ID
        OrderType: Order type (Market, Limit, etc.)
        Status: Order status (OPN, ACK, FLL, CNL, REJ)
        StatusDescription: Human-readable status
        OpenedDateTime: When order was opened
        ClosedDateTime: When order was closed (if applicable)
        Currency: Order currency
        Duration: Time in force (GTC, DAY, IOC, FOK)
        GoodTillDate: GTC expiration date
        Routing: Order routing method
        CommissionFee: Commission fee
        UnbundledRouteFee: Route fee
        PriceUsedForBuyingPower: Price for margin calculation
        FilledPrice: Fill price (if filled)
        LimitPrice: Limit price (for limit orders)
        StopPrice: Stop price (for stop orders)
        TrailingStop: Trailing stop parameters
        Legs: Array of order legs (for multi-leg orders)
        MarketActivationRules: Market activation rules
        TimeActivationRules: Time activation rules
        ConditionalOrders: Related conditional orders
        GroupName: Order group name (for OCO/Bracket)
        GroupID: Order group ID (for OCO/Bracket)
        AdvancedOptions: Advanced options string
        Message: Status message
        RejectionReason: Rejection reason (if rejected)
    """

    AccountID: str = Field(..., description="TradeStation account ID")
    OrderID: str = Field(..., description="TradeStation order ID")
    OrderType: str | None = Field(None, description="Order type")
    Status: str | None = Field(None, description="Order status")
    StatusDescription: str | None = Field(None, description="Human-readable status")
    OpenedDateTime: str | None = Field(None, description="When order was opened")
    ClosedDateTime: str | None = Field(None, description="When order was closed")
    Currency: str | None = Field(None, description="Order currency")
    Duration: str | None = Field(None, description="Time in force")
    GoodTillDate: str | None = Field(None, description="GTC expiration date")
    Routing: str | None = Field(None, description="Order routing method")
    CommissionFee: str | None = Field(None, description="Commission fee")
    UnbundledRouteFee: str | None = Field(None, description="Route fee")
    PriceUsedForBuyingPower: str | None = Field(None, description="Price for margin calculation")
    FilledPrice: str | None = Field(None, description="Fill price")
    LimitPrice: str | None = Field(None, description="Limit price")
    StopPrice: str | None = Field(None, description="Stop price")
    TrailingStop: TradeStationTrailingStop | dict[str, Any] | None = Field(None, description="Trailing stop parameters")
    Legs: list[TradeStationOrderLeg] | list[dict[str, Any]] | None = Field(
        None, description="Order legs (multi-leg orders)"
    )
    MarketActivationRules: list[TradeStationMarketActivationRule] | list[dict[str, Any]] | None = Field(
        None, description="Market activation rules"
    )
    TimeActivationRules: list[TradeStationTimeActivationRule] | list[dict[str, Any]] | None = Field(
        None, description="Time activation rules"
    )
    ConditionalOrders: list[TradeStationConditionalOrder] | list[dict[str, Any]] | None = Field(
        None, description="Conditional order relationships"
    )
    GroupName: str | None = Field(None, description="Order group name")
    GroupID: str | None = Field(None, description="Order group ID")
    AdvancedOptions: str | None = Field(None, description="Advanced options string")
    Message: str | None = Field(None, description="Status message")
    RejectionReason: str | None = Field(None, description="Rejection reason")

    # Additional fields that may be present
    Symbol: str | None = Field(None, description="Trading symbol (if not in Legs)")
    TradeAction: str | None = Field(None, description="Buy or Sell (if not in Legs)")
    Quantity: str | None = Field(None, description="Quantity (if not in Legs)")
    FilledQuantity: str | None = Field(None, description="Filled quantity")
    AverageFillPrice: str | None = Field(None, description="Average fill price")
    PlacedTime: str | None = Field(None, description="Placed time (alternative to OpenedDateTime)")
    FilledTime: str | None = Field(None, description="Filled time (alternative to ClosedDateTime)")
    TimeInForce: dict[str, str] | None = Field(None, description="Time in force (alternative to Duration)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "AccountID": "SIM123456",
                "OrderID": "924243071",
                "OrderType": "Market",
                "Status": "FLL",
                "StatusDescription": "Filled",
                "Symbol": "MNQZ25",
                "TradeAction": "Buy",
                "Quantity": "2",
                "FilledQuantity": "2",
                "AverageFillPrice": "25016.50",
            }
        }
    )


class TradeStationOrderGroupResponse(BaseModel):
    """
    TradeStation API group order response (OCO/Bracket).

    Attributes:
        GroupID: Group order ID
        GroupName: Group order name
        Type: Group type (OCO, BRK, NORMAL)
        Orders: List of orders in the group
    """

    GroupID: str | None = Field(None, description="Group order ID")
    GroupName: str | None = Field(None, description="Group order name")
    Type: str | None = Field(None, description="Group type: OCO, BRK, or NORMAL")
    Orders: list[TradeStationOrderResponse] | list[dict[str, Any]] = Field(..., description="Orders in the group")

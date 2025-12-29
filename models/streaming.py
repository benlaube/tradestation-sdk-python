"""
TradeStation API Streaming Response Models

Pydantic models specifically for HTTP Streaming responses.
Streaming responses have different structures than REST API responses.

Streaming endpoints return NDJSON (newline-delimited JSON) with:
- Data objects (quotes, orders, positions, balances)
- Control messages (StreamStatus, Heartbeat)
- Error responses

Dependencies: pydantic
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class MarketFlags(BaseModel):
    """Market-specific flags for a symbol."""

    IsBats: bool | None = Field(None, description="Is BATS exchange")
    IsDelayed: bool | None = Field(None, description="Is delayed data")
    IsHalted: bool | None = Field(None, description="Is trading halted")
    IsHardToBorrow: bool | None = Field(None, description="Is hard to borrow")


class QuoteStream(BaseModel):
    """
    Quote data from TradeStation HTTP Streaming API.

    Streaming quotes contain more fields than REST quote snapshots,
    including 52-week highs/lows, market flags, restrictions, and more.

    This model captures ALL fields from the QuoteStream schema in API v3.

    Attributes:
        Symbol: Trading symbol (REQUIRED)
        Last: Last traded price
        Bid: Current bid price
        Ask: Current ask price
        BidSize: Bid size (contracts/shares)
        AskSize: Ask size (contracts/shares)
        Volume: Daily volume
        TradeTime: Time of last trade
        Open: Opening price of the day
        High: Highest price of the day
        Low: Lowest price of the day
        Close: Closing price (current or previous)
        PreviousClose: Previous day's closing price
        NetChange: Net change from previous close
        NetChangePct: Net change percentage
        VWAP: Volume-weighted average price
        High52Week: 52-week high price
        High52WeekTimestamp: Date of 52-week high
        Low52Week: 52-week low price
        Low52WeekTimestamp: Date of 52-week low
        PreviousVolume: Previous day's volume
        DailyOpenInterest: Open interest (futures/options)
        MarketFlags: Market-specific flags
        Restrictions: Trading restrictions (array)
        MinPrice: Minimum price (futures)
        MaxPrice: Maximum price (futures)
        FirstNoticeDate: First notice date (futures)
        LastTradingDate: Last trading date (futures)
        TickSizeTier: Trading increment tier
        LastSize: Size of last trade
        LastVenue: Exchange of last trade
        Error: Error message (if any)
    """

    Symbol: str = Field(..., description="Trading symbol")
    Last: str | None = Field(None, description="Last traded price")
    Bid: str | None = Field(None, description="Current bid price")
    Ask: str | None = Field(None, description="Current ask price")
    BidSize: str | None = Field(None, description="Bid size (contracts/shares)")
    AskSize: str | None = Field(None, description="Ask size (contracts/shares)")
    Volume: str | None = Field(None, description="Daily volume")
    TradeTime: str | None = Field(None, description="Time of last trade")
    Open: str | None = Field(None, description="Opening price of the day")
    High: str | None = Field(None, description="Highest price of the day")
    Low: str | None = Field(None, description="Lowest price of the day")
    Close: str | None = Field(None, description="Closing price")
    PreviousClose: str | None = Field(None, description="Previous day's closing price")
    NetChange: str | None = Field(None, description="Net change from previous close")
    NetChangePct: str | None = Field(None, description="Net change percentage")
    VWAP: str | None = Field(None, description="Volume-weighted average price")
    High52Week: str | None = Field(None, description="52-week high price")
    High52WeekTimestamp: str | None = Field(None, description="Date of 52-week high")
    Low52Week: str | None = Field(None, description="52-week low price")
    Low52WeekTimestamp: str | None = Field(None, description="Date of 52-week low")
    PreviousVolume: str | None = Field(None, description="Previous day's volume")
    DailyOpenInterest: str | None = Field(None, description="Open interest (futures/options)")
    MarketFlags: dict[str, Any] | None = Field(None, description="Market-specific flags")
    Restrictions: list[str] | None = Field(None, description="Trading restrictions")
    MinPrice: str | None = Field(None, description="Minimum price (futures)")
    MaxPrice: str | None = Field(None, description="Maximum price (futures)")
    FirstNoticeDate: str | None = Field(None, description="First notice date (futures)")
    LastTradingDate: str | None = Field(None, description="Last trading date (futures)")
    TickSizeTier: str | None = Field(None, description="Trading increment tier")
    LastSize: str | None = Field(None, description="Size of last trade")
    LastVenue: str | None = Field(None, description="Exchange of last trade")
    Error: str | None = Field(None, description="Error message (if any)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "Symbol": "MNQZ25",
                "Last": "21450.25",
                "Bid": "21450.00",
                "Ask": "21450.50",
                "BidSize": "15",
                "AskSize": "12",
                "Volume": "12345",
                "TradeTime": "2025-11-25T16:44:27Z",
                "Open": "21449.00",
                "High": "21452.00",
                "Low": "21448.50",
                "Close": "21450.25",
                "VWAP": "21449.85",
            }
        }
    )


class OrderStream(BaseModel):
    """
    Order update from TradeStation HTTP Streaming API.

    Streaming order updates have the same structure as REST order responses,
    but are delivered in real-time as order status changes occur.

    This model extends TradeStationOrderResponse to ensure we capture
    all streaming-specific fields if any are added in the future.

    Note: OrderStream uses the same structure as TradeStationOrderResponse,
    but we create a separate model for clarity and potential future differences.
    """

    # All fields from TradeStationOrderResponse
    AccountID: str = Field(..., description="TradeStation account ID")
    OrderID: str = Field(..., description="TradeStation order ID")
    OrderType: str | None = Field(None, description="Order type")
    Status: str | None = Field(None, description="Order status (OPN, ACK, FLL, CNL, REJ)")
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
    TrailingStop: dict[str, Any] | None = Field(None, description="Trailing stop parameters")
    Legs: list[dict[str, Any]] | None = Field(None, description="Order legs (multi-leg orders)")
    MarketActivationRules: list[dict[str, Any]] | None = Field(None, description="Market activation rules")
    TimeActivationRules: list[dict[str, Any]] | None = Field(None, description="Time activation rules")
    ConditionalOrders: list[dict[str, Any]] | None = Field(None, description="Conditional order relationships")
    GroupName: str | None = Field(None, description="Order group name")
    GroupID: str | None = Field(None, description="Order group ID")
    AdvancedOptions: str | None = Field(None, description="Advanced options string")
    Message: str | None = Field(None, description="Status message")
    RejectionReason: str | None = Field(None, description="Rejection reason")
    Symbol: str | None = Field(None, description="Trading symbol (if not in Legs)")
    TradeAction: str | None = Field(None, description="Buy or Sell (if not in Legs)")
    Quantity: str | None = Field(None, description="Quantity (if not in Legs)")
    FilledQuantity: str | None = Field(None, description="Filled quantity")
    AverageFillPrice: str | None = Field(None, description="Average fill price")

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


class PositionStream(BaseModel):
    """
    Position update from TradeStation HTTP Streaming API.

    Streaming position updates contain detailed information including
    pricing, P&L, margin requirements, and market values that are
    NOT available in the REST positions endpoint.

    This model captures ALL fields from the Position schema in API v3.

    Attributes:
        AccountID: TradeStation account ID
        PositionID: Unique position identifier
        Symbol: Trading symbol
        AssetType: STOCK, STOCKOPTION, FUTURE, INDEXOPTION
        LongShort: Long or Short
        Quantity: Number of contracts/shares (negative for short)
        AveragePrice: Average entry price
        Last: Last traded price
        Bid: Current bid price
        Ask: Current ask price
        MarketValue: Current market value
        TotalCost: Total cost of position
        TodaysProfitLoss: Today's P&L (equity/options only)
        UnrealizedProfitLoss: Unrealized P&L
        UnrealizedProfitLossPercent: Unrealized P&L percentage
        UnrealizedProfitLossQty: Unrealized P&L per unit
        MarkToMarketPrice: Mark-to-market price (equity/options)
        Timestamp: Position entry timestamp
        ConversionRate: Currency conversion rate
        DayTradeRequirement: Day trade margin requirement
        InitialRequirement: Initial margin requirement
        MaintenanceMargin: Maintenance margin requirement
        ExpirationDate: Expiration date (futures/options)
        Deleted: True if position was closed (deletion notification)
    """

    AccountID: str = Field(..., description="TradeStation account ID")
    PositionID: str | None = Field(None, description="Unique position identifier")
    Symbol: str = Field(..., description="Trading symbol")
    AssetType: str | None = Field(None, description="STOCK, STOCKOPTION, FUTURE, INDEXOPTION")
    LongShort: str | None = Field(None, description="Long or Short")
    Quantity: str = Field(..., description="Number of contracts/shares (negative for short)")
    AveragePrice: str | None = Field(None, description="Average entry price")
    Last: str | None = Field(None, description="Last traded price")
    Bid: str | None = Field(None, description="Current bid price")
    Ask: str | None = Field(None, description="Current ask price")
    MarketValue: str | None = Field(None, description="Current market value")
    TotalCost: str | None = Field(None, description="Total cost of position")
    TodaysProfitLoss: str | None = Field(None, description="Today's P&L (equity/options only)")
    UnrealizedProfitLoss: str | None = Field(None, description="Unrealized P&L")
    UnrealizedProfitLossPercent: str | None = Field(None, description="Unrealized P&L percentage")
    UnrealizedProfitLossQty: str | None = Field(None, description="Unrealized P&L per unit")
    MarkToMarketPrice: str | None = Field(None, description="Mark-to-market price (equity/options)")
    Timestamp: str | None = Field(None, description="Position entry timestamp")
    ConversionRate: str | None = Field(None, description="Currency conversion rate")
    DayTradeRequirement: str | None = Field(None, description="Day trade margin requirement")
    InitialRequirement: str | None = Field(None, description="Initial margin requirement")
    MaintenanceMargin: str | None = Field(None, description="Maintenance margin requirement")
    ExpirationDate: str | None = Field(None, description="Expiration date (futures/options)")
    Deleted: bool | None = Field(None, description="True if position was closed (deletion notification)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "AccountID": "SIM123456",
                "PositionID": "64630792",
                "Symbol": "MNQZ25",
                "AssetType": "FUTURE",
                "LongShort": "Long",
                "Quantity": "2",
                "AveragePrice": "25016.50",
                "Last": "25017.00",
                "Bid": "25016.75",
                "Ask": "25017.25",
                "MarketValue": "50034.00",
                "TotalCost": "50033.00",
                "TodaysProfitLoss": "1.00",
                "UnrealizedProfitLoss": "1.00",
                "UnrealizedProfitLossPercent": "0.002",
                "Timestamp": "2025-11-25T16:00:00Z",
            }
        }
    )


class StreamStatus(BaseModel):
    """
    Stream status control message from TradeStation HTTP Streaming API.

    Control messages are interspersed with data messages in the stream.

    Attributes:
        StreamStatus: Status value ("EndSnapshot", "GoAway", "Error")
    """

    StreamStatus: str = Field(..., description="Status: EndSnapshot, GoAway, or Error")


class Heartbeat(BaseModel):
    """
    Heartbeat message from TradeStation HTTP Streaming API.

    Sent every 5 seconds on idle streams to keep connection alive.

    Attributes:
        Heartbeat: Heartbeat indicator (integer, typically 1)
        Timestamp: Timestamp of heartbeat
    """

    Heartbeat: int = Field(..., description="Heartbeat indicator")
    Timestamp: str = Field(..., description="Heartbeat timestamp")


class StreamErrorResponse(BaseModel):
    """
    Error response from TradeStation HTTP Streaming API.

    Attributes:
        Error: Error type (Forbidden, InternalServerError, ServiceUnavailable, GatewayTimeout, Failed)
        Message: Error description
        AccountID: Account ID (if applicable)
        Symbol: Symbol (if applicable, for quote errors)
    """

    Error: str = Field(..., description="Error type")
    Message: str = Field(..., description="Error description")
    AccountID: str | None = Field(None, description="Account ID (if applicable)")
    Symbol: str | None = Field(None, description="Symbol (if applicable, for quote errors)")


class BalanceStream(BaseModel):
    """
    Streaming account balance update from TradeStation HTTP Streaming API.

    Streaming balances differ from REST responses and include real-time P&L fields.

    Attributes:
        AccountID: TradeStation account ID
        Equity: Total equity
        BuyingPower: Buying power
        CashBalance: Cash balance
        TodaysProfitLoss: Today's profit/loss
        UnrealizedProfitLoss: Unrealized profit/loss
        MarginAvailable: Margin available
        MarginUsed: Margin used
        MaintenanceMargin: Maintenance margin
        InitialMarginRequirement: Initial margin requirement
        NetLiquidationValue: Net liquidation value
        DayTradingBuyingPower: Day trading buying power
        OpenPnL: Open P&L
        RealizedPnL: Realized P&L
        Timestamp: Timestamp of the update (if provided)
    """

    AccountID: str = Field(..., description="TradeStation account ID")
    Equity: float | str | None = Field(None, description="Total equity")
    BuyingPower: float | str | None = Field(None, description="Buying power")
    CashBalance: float | str | None = Field(None, description="Cash balance")
    TodaysProfitLoss: float | str | None = Field(None, description="Today's profit/loss")
    UnrealizedProfitLoss: float | str | None = Field(None, description="Unrealized profit/loss")
    MarginAvailable: float | str | None = Field(None, description="Margin available")
    MarginUsed: float | str | None = Field(None, description="Margin used")
    MaintenanceMargin: float | str | None = Field(None, description="Maintenance margin")
    InitialMarginRequirement: float | str | None = Field(None, description="Initial margin requirement")
    NetLiquidationValue: float | str | None = Field(None, description="Net liquidation value")
    DayTradingBuyingPower: float | str | None = Field(None, description="Day trading buying power")
    OpenPnL: float | str | None = Field(None, description="Open P&L")
    RealizedPnL: float | str | None = Field(None, description="Realized P&L")
    Timestamp: str | None = Field(None, description="Timestamp of the update (if provided)")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "AccountID": "SIM123456",
                "Equity": "25000.00",
                "BuyingPower": "100000.00",
                "CashBalance": "12000.00",
                "TodaysProfitLoss": "150.00",
                "UnrealizedProfitLoss": "200.00",
                "NetLiquidationValue": "25200.00",
            }
        }
    )


class BarStream(BaseModel):
    """
    Bar data from TradeStation HTTP Streaming API (marketdata/stream/barcharts/{symbol}).

    Each item represents an OHLCV bar plus tick/volume statistics and status flags.
    The payload mirrors the TradeStation Bar schema.
    """

    TimeStamp: str = Field(..., description="ISO timestamp of the bar close time")
    Open: str = Field(..., description="Opening price for the bar")
    High: str = Field(..., description="Highest price during the bar")
    Low: str = Field(..., description="Lowest price during the bar")
    Close: str = Field(..., description="Closing price for the bar")
    TotalVolume: str = Field(..., description="Total volume for the bar")
    Epoch: int = Field(..., description="Unix epoch timestamp in milliseconds")
    BarStatus: str | None = Field(None, description='Bar status flag (e.g., "Closed", "Open")')
    IsRealtime: bool | None = Field(None, description="True if the bar is being built in real time")
    IsEndOfHistory: bool | None = Field(None, description="True when all historical bars have been delivered")
    OpenInterest: str | None = Field(None, description="Open interest (futures/options)")
    DownTicks: int | None = Field(None, description="Number of downticks in the bar")
    UpTicks: int | None = Field(None, description="Number of upticks in the bar")
    DownVolume: int | None = Field(None, description="Volume on downticks")
    UpVolume: int | None = Field(None, description="Volume on upticks")
    TotalTicks: int | None = Field(None, description="Total tick count in the bar")
    UnchangedTicks: int | None = Field(None, description="Number of unchanged ticks")
    UnchangedVolume: int | None = Field(None, description="Volume on unchanged ticks")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "TimeStamp": "2025-01-15T10:01:00Z",
                "Open": "21450.00",
                "High": "21452.00",
                "Low": "21448.50",
                "Close": "21450.25",
                "TotalVolume": "12345",
                "Epoch": 1705314060000,
                "BarStatus": "Closed",
                "IsRealtime": False,
                "IsEndOfHistory": False,
                "OpenInterest": "0",
                "DownTicks": 231,
                "UpTicks": 229,
                "DownVolume": 1957,
                "UpVolume": 2273,
                "TotalTicks": 460,
                "UnchangedTicks": 0,
                "UnchangedVolume": 0,
            }
        }
    )


class OptionChainStream(BaseModel):
    """Streaming option chain update (structure varies by request)."""

    class Config:
        extra = "allow"


class OptionQuoteStream(BaseModel):
    """Streaming option quote update."""

    class Config:
        extra = "allow"


class MarketDepthQuoteStream(BaseModel):
    """Streaming Level 2 market depth quote update."""

    class Config:
        extra = "allow"


class MarketDepthAggregateStream(BaseModel):
    """Streaming aggregated market depth update."""

    class Config:
        extra = "allow"

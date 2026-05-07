"""
TradeStation Quote Models

Pydantic models for REST quote responses.
These capture quote snapshots from /marketdata/quotes/{symbols}.

Dependencies: pydantic
"""

from typing import Any

from pydantic import Field

from .base import TradeStationModel, strict_model_config
from .streaming import TradeStationMarketFlags

NumericText = float | int | str


class QuoteSnapshot(TradeStationModel):
    """
    Quote snapshot from TradeStation REST API.

    REST quote snapshots usually contain fewer fields than streaming quotes,
    but TradeStation can include the richer quote schema in snapshot responses.

    Attributes:
        Symbol: Trading symbol
        Last: Last traded price
        Bid: Current bid price
        Ask: Current ask price
        BidSize: Bid size
        AskSize: Ask size
        Volume: Daily volume
        TradeTime: Time of last trade
        Open: Opening price
        High: Highest price
        Low: Lowest price
        Close: Closing price
        PreviousClose: Previous day's closing price
        NetChange: Net change from previous close
        NetChangePct: Net change percentage
        VWAP: Volume-weighted average price
        High52Week: 52-week high price
        Low52Week: 52-week low price
        MarketFlags: Market-specific flags
        MarketFlagsDisplay: Display-form market flags
    """

    Symbol: str = Field(..., description="Trading symbol")
    Last: NumericText | None = Field(None, description="Last traded price")
    Bid: NumericText | None = Field(None, description="Current bid price")
    Ask: NumericText | None = Field(None, description="Current ask price")
    BidSize: NumericText | None = Field(None, description="Bid size")
    AskSize: NumericText | None = Field(None, description="Ask size")
    Volume: NumericText | None = Field(None, description="Daily volume")
    TradeTime: str | None = Field(None, description="Time of last trade")
    Open: NumericText | None = Field(None, description="Opening price")
    High: NumericText | None = Field(None, description="Highest price")
    Low: NumericText | None = Field(None, description="Lowest price")
    Close: NumericText | None = Field(None, description="Closing price")
    PreviousClose: NumericText | None = Field(None, description="Previous day's closing price")
    NetChange: NumericText | None = Field(None, description="Net change from previous close")
    NetChangePct: NumericText | None = Field(None, description="Net change percentage")
    VWAP: NumericText | None = Field(None, description="Volume-weighted average price")
    High52Week: NumericText | None = Field(None, description="52-week high price")
    High52WeekTimestamp: str | None = Field(None, description="Date of 52-week high")
    Low52Week: NumericText | None = Field(None, description="52-week low price")
    Low52WeekTimestamp: str | None = Field(None, description="Date of 52-week low")
    PreviousVolume: NumericText | None = Field(None, description="Previous day's volume")
    DailyOpenInterest: NumericText | None = Field(None, description="Open interest (futures/options)")
    MarketFlags: TradeStationMarketFlags | None = Field(None, description="Market-specific flags")
    MarketFlagsDisplay: str | None = Field(None, description="Display-form market flags")
    Restrictions: list[str] | None = Field(None, description="Trading restrictions")
    MinPrice: NumericText | None = Field(None, description="Minimum price")
    MaxPrice: NumericText | None = Field(None, description="Maximum price")
    FirstNoticeDate: str | None = Field(None, description="First notice date")
    LastTradingDate: str | None = Field(None, description="Last trading date")
    TickSizeTier: str | None = Field(None, description="Trading increment tier")
    LastSize: NumericText | None = Field(None, description="Size of last trade")
    LastVenue: str | None = Field(None, description="Exchange of last trade")
    Error: str | None = Field(None, description="Quote-level error message")

    model_config = strict_model_config(
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
                "High52Week": "22200.00",
                "Low52Week": "18000.00",
            }
        }
    )


class QuotesResponse(TradeStationModel):
    """Response wrapper for REST quotes endpoint."""

    Quotes: list[QuoteSnapshot] = Field(..., description="List of quote snapshots")
    Errors: list[dict[str, Any]] | None = Field(None, description="List of errors (if any)")

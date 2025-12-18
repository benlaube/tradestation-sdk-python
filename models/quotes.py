"""
TradeStation Quote Models

Pydantic models for REST quote responses.
These capture quote snapshots from /marketdata/quotes/{symbols}.

Dependencies: pydantic
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class QuoteSnapshot(BaseModel):
    """
    Quote snapshot from TradeStation REST API.

    REST quote snapshots contain fewer fields than streaming quotes,
    but provide a one-time snapshot of current market data.

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
    """

    Symbol: str = Field(..., description="Trading symbol")
    Last: str | None = Field(None, description="Last traded price")
    Bid: str | None = Field(None, description="Current bid price")
    Ask: str | None = Field(None, description="Current ask price")
    BidSize: str | None = Field(None, description="Bid size")
    AskSize: str | None = Field(None, description="Ask size")
    Volume: str | None = Field(None, description="Daily volume")
    TradeTime: str | None = Field(None, description="Time of last trade")
    Open: str | None = Field(None, description="Opening price")
    High: str | None = Field(None, description="Highest price")
    Low: str | None = Field(None, description="Lowest price")
    Close: str | None = Field(None, description="Closing price")
    PreviousClose: str | None = Field(None, description="Previous day's closing price")
    NetChange: str | None = Field(None, description="Net change from previous close")
    NetChangePct: str | None = Field(None, description="Net change percentage")

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
            }
        }
    )


class QuotesResponse(BaseModel):
    """Response wrapper for REST quotes endpoint."""

    Quotes: list[QuoteSnapshot] | list[dict[str, Any]] = Field(..., description="List of quote snapshots")
    Errors: list[dict[str, Any]] | None = Field(None, description="List of errors (if any)")

"""
TradeStation Position Models

Pydantic models for positions REST responses.
These capture key fields from /brokerage/accounts/{accountId}/positions.

Dependencies: pydantic
"""

from typing import Any

from pydantic import BaseModel, Field


class PositionResponse(BaseModel):
    """
    Position response from TradeStation REST API.

    Attributes:
        AccountID: TradeStation account ID
        PositionID: Unique position identifier
        Symbol: Trading symbol
        AssetType: STOCK, STOCKOPTION, FUTURE, INDEXOPTION
        LongShort: Long or Short
        Quantity: Number of contracts/shares (negative for short)
        AveragePrice: Average entry price
        MarketValue: Current market value
        TotalCost: Total cost of position
        TodaysProfitLoss: Today's P&L
        UnrealizedProfitLoss: Unrealized P&L
        UnrealizedProfitLossPercent: Unrealized P&L percentage
        UnrealizedProfitLossQty: Unrealized P&L per unit
        MarkToMarketPrice: Mark-to-market price
        Timestamp: Position entry timestamp
        ConversionRate: Currency conversion rate
        DayTradeRequirement: Day trade margin requirement
        InitialRequirement: Initial margin requirement
        MaintenanceMargin: Maintenance margin requirement
        ExpirationDate: Expiration date (futures/options)
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
    TodaysProfitLoss: str | None = Field(None, description="Today's P&L")
    UnrealizedProfitLoss: str | None = Field(None, description="Unrealized P&L")
    UnrealizedProfitLossPercent: str | None = Field(None, description="Unrealized P&L percentage")
    UnrealizedProfitLossQty: str | None = Field(None, description="Unrealized P&L per unit")
    MarkToMarketPrice: str | None = Field(None, description="Mark-to-market price")
    Timestamp: str | None = Field(None, description="Position entry timestamp")
    ConversionRate: str | None = Field(None, description="Currency conversion rate")
    DayTradeRequirement: str | None = Field(None, description="Day trade margin requirement")
    InitialRequirement: str | None = Field(None, description="Initial margin requirement")
    MaintenanceMargin: str | None = Field(None, description="Maintenance margin requirement")
    ExpirationDate: str | None = Field(None, description="Expiration date (futures/options)")
    Deleted: bool | None = Field(None, description="True if position closed")


class PositionsResponse(BaseModel):
    """Wrapper for positions response."""

    Positions: list[PositionResponse] | list[dict[str, Any]] = Field(..., description="List of positions")

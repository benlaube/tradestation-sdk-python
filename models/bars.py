"""
Bar response models for REST barchart endpoints.
"""

from typing import List

from pydantic import BaseModel, Field


class BarResponse(BaseModel):
    """Single bar (OHLCV + tick/volume stats) from /v3/marketdata/barcharts/{symbol}."""

    High: str = Field(..., description="High price of the bar")
    Low: str = Field(..., description="Low price of the bar")
    Open: str = Field(..., description="Open price of the bar")
    Close: str = Field(..., description="Close price of the bar")
    TimeStamp: str = Field(..., description="ISO timestamp of the bar")
    TotalVolume: str = Field(..., description="Total volume traded during the bar")
    DownTicks: int | None = Field(None, description="Number of downticks")
    DownVolume: int | None = Field(None, description="Volume on downticks")
    OpenInterest: str | None = Field(None, description="Open interest (futures/options)")
    IsRealtime: bool | None = Field(None, description="True when bar is being built in real time")
    IsEndOfHistory: bool | None = Field(None, description="True when historical bars are complete")
    TotalTicks: int | None = Field(None, description="Total ticks in the bar")
    UnchangedTicks: int | None = Field(None, description="Unchanged tick count")
    UnchangedVolume: int | None = Field(None, description="Volume on unchanged ticks")
    UpTicks: int | None = Field(None, description="Number of upticks")
    UpVolume: int | None = Field(None, description="Volume on upticks")
    Epoch: int | None = Field(None, description="Epoch milliseconds for the bar timestamp")
    BarStatus: str | None = Field(None, description="Bar status flag (Closed/Open/etc.)")


class BarsResponse(BaseModel):
    """Wrapper for list of bars returned by /v3/marketdata/barcharts/{symbol}."""

    Bars: List[BarResponse] = Field(default_factory=list, description="List of bars")

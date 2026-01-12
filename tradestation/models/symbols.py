"""
Symbol detail and search response models.
"""

from typing import Any

from pydantic import BaseModel, Field


class SymbolDetail(BaseModel):
    """Symbol metadata for /v3/marketdata/symbols/{symbols}."""

    Symbol: str = Field(..., description="Trading symbol")
    CompanyName: str | None = Field(None, description="Company or instrument name")
    AssetType: str | None = Field(None, description="Asset type (e.g., Future, Stock)")
    Exchange: str | None = Field(None, description="Primary exchange")
    Decimals: int | None = Field(None, description="Number of price decimals")
    TickSize: float | str | None = Field(None, description="Minimum price increment")
    PointValue: float | str | None = Field(None, description="Point value for futures")

    class Config:
        extra = "allow"


class SymbolDetailsResponse(BaseModel):
    """Response wrapper for GET /v3/marketdata/symbols/{symbols}."""

    Symbols: list[SymbolDetail] = Field(default_factory=list, description="List of symbol details")
    Errors: list[Any] = Field(default_factory=list, description="Error list from API (if any)")


class SymbolSearchResponse(BaseModel):
    """Response wrapper for GET /v3/marketdata/symbols/search."""

    Symbols: list[SymbolDetail] = Field(default_factory=list, description="Matched symbols")
    Errors: list[Any] = Field(default_factory=list, description="Error list from API (if any)")

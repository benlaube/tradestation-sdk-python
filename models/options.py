"""
Option response models (expirations, strikes, risk/reward, spread types).
"""

from typing import Any, List

from pydantic import BaseModel, Field


class OptionExpirationsResponse(BaseModel):
    """Response wrapper for GET /v3/marketdata/options/expirations/{underlying}."""

    Expirations: List[str] = Field(default_factory=list, description="Expiration dates")
    Errors: List[Any] = Field(default_factory=list, description="Errors (if any)")


class OptionStrikesResponse(BaseModel):
    """Response wrapper for GET /v3/marketdata/options/strikes/{underlying}."""

    Strikes: List[float | str] = Field(default_factory=list, description="Available strikes")
    Errors: List[Any] = Field(default_factory=list, description="Errors (if any)")


class OptionRiskRewardResponse(BaseModel):
    """Response for POST /v3/marketdata/options/riskreward (structure varies; allow extra)."""

    class Config:
        extra = "allow"


class OptionSpreadType(BaseModel):
    """Single spread type entry."""

    Name: str | None = Field(None, description="Spread name (e.g., Single, Vertical)")
    Description: str | None = Field(None, description="Spread description")

    class Config:
        extra = "allow"


class OptionSpreadTypesResponse(BaseModel):
    """Response wrapper for GET /v3/marketdata/options/spreadtypes."""

    SpreadTypes: List[OptionSpreadType] = Field(default_factory=list, description="Spread types")
    Errors: List[Any] = Field(default_factory=list, description="Errors (if any)")

"""
TradeStation Order Execution Models

Pydantic models for TradeStation API order execution (fill) responses.
Executions represent the actual fills of orders.

Dependencies: pydantic
"""

from pydantic import BaseModel, Field


class TradeStationExecutionResponse(BaseModel):
    """
    TradeStation API execution (fill) response model.

    Executions represent the actual fills of orders. Each order can have
    multiple executions if it's filled in multiple parts.

    Attributes:
        ExecutionID: TradeStation execution ID
        Symbol: Trading symbol
        TradeAction: Buy or Sell
        Quantity: Number of contracts filled
        Price: Fill price
        Commission: Commission paid
        ExchangeFees: Exchange fees
        ExecutionTime: When execution occurred
        Venue: Execution venue
    """

    ExecutionID: str | None = Field(None, description="TradeStation execution ID")
    Symbol: str = Field(..., description="Trading symbol")
    TradeAction: str = Field(..., description="Buy or Sell")
    Quantity: int | str = Field(..., description="Number of contracts filled")
    Price: float | str = Field(..., description="Fill price")
    Commission: float | str | None = Field(None, description="Commission paid")
    ExchangeFees: float | str | None = Field(None, description="Exchange fees")
    ExecutionTime: str = Field(..., description="Execution timestamp")
    Venue: str | None = Field(None, description="Execution venue")

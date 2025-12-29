"""
Wrapper and confirm/cancel response models for order queries.
"""

from typing import List, Any

from pydantic import BaseModel, Field

from .orders import TradeStationOrderResponse


class OrdersWrapper(BaseModel):
    """Wrapper for current/historical orders list responses."""

    Orders: List[TradeStationOrderResponse] = Field(default_factory=list, description="Order list")
    NextPageToken: str | None = Field(None, description="Pagination token, if provided")
    Errors: List[Any] = Field(default_factory=list, description="Errors, if any")


class CancelOrderResponse(BaseModel):
    """Response for DELETE /v3/orderexecution/orders/{orderID}."""

    Success: bool | None = Field(None, description="True if cancel succeeded")
    Message: str | None = Field(None, description="Status message")

    class Config:
        extra = "allow"


class ConfirmOrderResponse(BaseModel):
    """Response for POST /v3/orderexecution/orderconfirm."""

    class Config:
        extra = "allow"


class ConfirmGroupOrderResponse(BaseModel):
    """Response for POST /v3/orderexecution/ordergroupconfirm."""

    class Config:
        extra = "allow"

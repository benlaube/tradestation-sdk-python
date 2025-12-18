"""
TradeStation Account and Balance Models

Pydantic models for account and balance REST responses.
These capture key fields from /brokerage/accounts and related endpoints.

Dependencies: pydantic
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field


class AccountSummary(BaseModel):
    """Account summary information from TradeStation API."""

    AccountID: str = Field(..., description="TradeStation account ID")
    AccountType: str | None = Field(None, description="Account type")
    Status: str | None = Field(None, description="Account status")
    Currency: str | None = Field(None, description="Account currency")
    Alias: str | None = Field(None, description="Account alias")

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "AccountID": "SIM123456",
                "AccountType": "INDIVIDUAL",
                "Status": "ACTIVE",
                "Currency": "USD",
                "Alias": "Paper",
            }
        }
    )


class BalanceDetail(BaseModel):
    """Detailed balance information."""

    Equity: float | str | None = Field(None, description="Total equity")
    CashBalance: float | str | None = Field(None, description="Cash balance")
    BuyingPower: float | str | None = Field(None, description="Buying power")
    DayTradingBuyingPower: float | str | None = Field(None, description="Day trading buying power")
    MarginAvailable: float | str | None = Field(None, description="Margin available")
    MarginUsed: float | str | None = Field(None, description="Margin used")
    MaintenanceMargin: float | str | None = Field(None, description="Maintenance margin")
    InitialMarginRequirement: float | str | None = Field(None, description="Initial margin requirement")
    NetLiquidationValue: float | str | None = Field(None, description="Net liquidation value")
    OpenPnL: float | str | None = Field(None, description="Open P&L")
    RealizedPnL: float | str | None = Field(None, description="Realized P&L")
    UnrealizedPnL: float | str | None = Field(None, description="Unrealized P&L")


class AccountBalancesResponse(BaseModel):
    """
    Account balances response.
    Returned from /brokerage/accounts/{accountId} and detailed balances endpoint.
    """

    Account: AccountSummary = Field(..., description="Account info")
    Balances: BalanceDetail | dict[str, Any] | None = Field(None, description="Balances detail")


class BODBalance(BaseModel):
    """Beginning-of-day balance entry."""

    AccountID: str = Field(..., description="TradeStation account ID")
    Date: str | None = Field(None, description="Date of BOD balance")
    Equity: float | str | None = Field(None, description="Equity at BOD")
    CashBalance: float | str | None = Field(None, description="Cash balance at BOD")
    BuyingPower: float | str | None = Field(None, description="Buying power at BOD")
    MarginUsed: float | str | None = Field(None, description="Margin used at BOD")
    NetLiquidationValue: float | str | None = Field(None, description="Net liquidation value at BOD")


class BODBalancesResponse(BaseModel):
    """Response for BOD balances endpoint."""

    BODBalances: list[BODBalance] | list[dict[str, Any]] = Field(..., description="List of BOD balances")
    Errors: list[dict[str, Any]] | None = Field(default_factory=list, description="List of errors from API")

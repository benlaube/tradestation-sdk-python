"""
TradeStation Account and Balance Models

Pydantic models for account and balance REST responses.
These capture key fields from /brokerage/accounts and related endpoints.

Dependencies: pydantic
"""

from __future__ import annotations

from typing import Any

from pydantic import AliasChoices, Field

from .base import TradeStationModel, strict_model_config


class AccountDetailPayload(TradeStationModel):
    """Detailed account metadata returned on v3 account list responses."""

    CryptoEnabled: bool | None = Field(None, description="Whether crypto trading is enabled for the account")
    DayTradingQualified: bool | None = Field(None, description="Whether the account is qualified for day trading")
    EnrolledInRegTProgram: bool | None = Field(None, description="Whether the account is enrolled in Reg T")
    IsStockLocateEligible: bool | None = Field(None, description="Whether the account is eligible for stock locates")
    OptionApprovalLevel: int | None = Field(None, description="Options approval level")
    PatternDayTrader: bool | None = Field(None, description="Whether the account is marked as a pattern day trader")
    RequiresBuyingPowerWarning: bool | None = Field(
        None,
        description="Whether the account receives buying power warning alerts",
    )


class AccountSummary(TradeStationModel):
    """Account summary information from TradeStation API."""

    AccountID: str = Field(..., description="TradeStation account ID")
    AccountType: str | None = Field(None, description="Account type")
    Status: str | None = Field(None, description="Account status")
    Currency: str | None = Field(None, description="Account currency")
    Alias: str | None = Field(None, description="Account alias")
    AltID: str | None = Field(None, description="Alternate account ID, used for some regional accounts")
    AccountDetail: AccountDetailPayload | None = Field(None, description="Optional account detail metadata")
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

    model_config = strict_model_config(
        json_schema_extra={
            "example": {
                "AccountID": "SIM123456",
                "AccountType": "INDIVIDUAL",
                "Status": "ACTIVE",
                "Currency": "USD",
                "Alias": "Paper",
                "AccountDetail": {
                    "DayTradingQualified": True,
                    "EnrolledInRegTProgram": False,
                    "CryptoEnabled": False,
                    "IsStockLocateEligible": False,
                    "OptionApprovalLevel": 0,
                    "PatternDayTrader": False,
                    "RequiresBuyingPowerWarning": False,
                },
            }
        }
    )


class BalanceDetail(TradeStationModel):
    """Detailed balance information."""

    CostOfPositions: float | str | None = Field(None, description="Cost basis used to calculate today's P/L")
    DayTradeExcess: float | str | None = Field(None, description="Day trade excess buying power")
    DayTradeMargin: float | str | None = Field(None, description="Futures day trade margin")
    DayTradeOpenOrderMargin: float | str | None = Field(None, description="Futures margin reserved for open orders")
    DayTrades: float | str | None = Field(None, description="Recent day trade count")
    Equity: float | str | None = Field(None, description="Total equity")
    CashBalance: float | str | None = Field(None, description="Cash balance")
    BuyingPower: float | str | None = Field(None, description="Buying power")
    DayTradingBuyingPower: float | str | None = Field(None, description="Day trading buying power")
    InitialMargin: float | str | None = Field(None, description="Futures initial margin")
    MarginAvailable: float | str | None = Field(None, description="Margin available")
    MarginUsed: float | str | None = Field(None, description="Margin used")
    MaintenanceMargin: float | str | None = Field(None, description="Maintenance margin")
    MaintenanceRate: float | str | None = Field(None, description="Maintenance margin rate")
    MarginRequirement: float | str | None = Field(None, description="Real-time account margin requirement")
    InitialMarginRequirement: float | str | None = Field(None, description="Initial margin requirement")
    NetLiquidationValue: float | str | None = Field(None, description="Net liquidation value")
    OpenOrderMargin: float | str | None = Field(None, description="Futures open-order margin")
    OpenPnL: float | str | None = Field(None, description="Open P&L")
    OptionBuyingPower: float | str | None = Field(None, description="Options buying power")
    OptionsMarketValue: float | str | None = Field(None, description="Options market value")
    OvernightBuyingPower: float | str | None = Field(None, description="Overnight buying power")
    RealizedPnL: float | str | None = Field(None, description="Realized P&L")
    RealizedProfitLoss: float | str | None = Field(None, description="Realized profit/loss")
    RequiredMargin: float | str | None = Field(None, description="Required margin")
    SecurityOnDeposit: float | str | None = Field(None, description="Special securities deposited for purchasing power")
    TodayRealTimeTradeEquity: float | str | None = Field(None, description="Futures unrealized P/L for today")
    TradeEquity: float | str | None = Field(None, description="Futures unrealized profit and loss")
    UnrealizedPnL: float | str | None = Field(None, description="Unrealized P&L")
    UnrealizedProfitLoss: float | str | None = Field(None, description="Unrealized profit/loss")
    UnsettledFunds: float | str | None = Field(None, description="Unsettled funds")


class CurrencyDetail(TradeStationModel):
    """Currency-specific balance information."""

    Currency: str | None = Field(None, description="Currency code")
    Commission: float | str | None = Field(None, description="Commission total for this currency")
    AccountConversionRate: float | str | None = Field(None, description="Account currency conversion rate")
    ConversionRate: float | str | None = Field(None, description="Currency conversion rate")


class AccountBalancesResponse(TradeStationModel):
    """
    Account balances response.
    Returned from /brokerage/accounts/{accountId} and detailed balances endpoint.
    """

    Account: AccountSummary = Field(..., description="Account info")
    Balances: BalanceDetail | None = Field(None, description="Balances detail")


AccountBalanceDetail = BalanceDetail


class BODBalance(TradeStationModel):
    """Beginning-of-day balance entry."""

    AccountID: str = Field(..., description="TradeStation account ID")
    Date: str | None = Field(None, description="Date of BOD balance")
    Equity: float | str | None = Field(None, description="Equity at BOD")
    CashBalance: float | str | None = Field(None, description="Cash balance at BOD")
    BuyingPower: float | str | None = Field(None, description="Buying power at BOD")
    MarginUsed: float | str | None = Field(None, description="Margin used at BOD")
    NetLiquidationValue: float | str | None = Field(None, description="Net liquidation value at BOD")


class DetailedBalance(TradeStationModel):
    """Detailed current balance entry from the account balances endpoint."""

    AccountID: str = Field(..., description="TradeStation account ID")
    AccountType: str | None = Field(None, description="TradeStation account type")
    Equity: float | str | None = Field(None, description="Current account equity")
    CashBalance: float | str | None = Field(None, description="Cash balance")
    BuyingPower: float | str | None = Field(None, description="Buying power")
    DayTradingBuyingPower: float | str | None = Field(None, description="Day trading buying power")
    MarketValue: float | str | None = Field(None, description="Current market value")
    TodaysProfitLoss: float | str | None = Field(
        None,
        validation_alias=AliasChoices("TodaysProfitLoss", "TodaysPnL"),
        description="Today's profit/loss",
    )
    UnrealizedProfitLoss: float | str | None = Field(
        None,
        validation_alias=AliasChoices("UnrealizedProfitLoss", "UnrealizedPnL"),
        description="Unrealized profit/loss",
    )
    RealizedProfitLoss: float | str | None = Field(None, description="Realized profit/loss")
    UnclearedDeposit: float | str | None = Field(None, description="Uncleared deposits")
    BalanceDetail: AccountBalanceDetail | None = Field(None, description="Detailed futures balance payload")
    CurrencyDetails: list[CurrencyDetail] | CurrencyDetail | None = Field(
        None, description="Currency-specific balance details"
    )
    Commission: float | str | None = Field(None, description="Commission total")


class BODBalancesResponse(TradeStationModel):
    """Response for BOD balances endpoint."""

    BODBalances: list[BODBalance] = Field(
        ...,
        description="List of BOD balances",
        validation_alias=AliasChoices("BODBalances", "Balances"),
    )
    Errors: list[dict[str, Any]] | None = Field(default_factory=list, description="List of errors from API")


class DetailedBalancesResponse(TradeStationModel):
    """Response for the detailed balances endpoint."""

    Balances: list[DetailedBalance] = Field(default_factory=list, description="List of balance records")
    Errors: list[dict[str, Any]] = Field(default_factory=list, description="Unstructured API errors")


AccountDetail = AccountDetailPayload

"""
TradeStation Account List Models

Pydantic models for REST account list endpoint responses.
This file contains models for GET /v3/brokerage/accounts (list all accounts).

Dependencies: pydantic
"""

from pydantic import Field

from .accounts import AccountSummary
from .base import TradeStationModel, strict_model_config


class AccountsListResponse(TradeStationModel):
    """Response for GET /brokerage/accounts."""

    Accounts: list[AccountSummary] = Field(..., description="List of accounts")

    model_config = strict_model_config(
        json_schema_extra={
            "example": {
                "Accounts": [
                    {
                        "AccountID": "SIM123456",
                        "AccountType": "INDIVIDUAL",
                        "Status": "ACTIVE",
                        "Currency": "USD",
                        "Alias": "Paper",
                    }
                ]
            }
        }
    )

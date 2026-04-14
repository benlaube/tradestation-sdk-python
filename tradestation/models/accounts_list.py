"""
TradeStation Account List Models

Pydantic models for REST account list endpoint responses.
This file contains models for GET /v3/brokerage/accounts (list all accounts).

Dependencies: pydantic
"""

from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from .accounts import AccountSummary


class AccountsListResponse(BaseModel):
    """Response for GET /brokerage/accounts."""

    Accounts: list[AccountSummary] | list[dict[str, Any]] = Field(..., description="List of accounts")

    model_config = ConfigDict(
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

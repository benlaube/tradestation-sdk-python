"""
Account Operations

Provides typed, mode-aware helpers for fetching account metadata and balances
from TradeStation. All methods normalize API responses to predictable dicts
so callers (bots, services, notebooks) can consume them without worrying about
Pydantic models or API shape differences.

Dependencies: typing
"""

from typing import Any

import requests

from .client import HTTPClient
from .config import sdk_config
from .exceptions import TradeStationAPIError
from .logger import setup_logger
from .models import (
    AccountBalancesResponse,
    AccountsListResponse,
    BODBalancesResponse,
)

logger = setup_logger(__name__, sdk_config.log_level)


class AccountOperations:
    """
    Account-related API operations.

    Responsibilities:
    - Discover accounts for the authenticated user and pick a working account ID
    - Retrieve summary and detailed balances (including BOD balances)
    - Normalize TradeStation response fields into stable, typed dictionaries

    Modes:
    - PAPER and LIVE supported; defaults to `sdk_config.trading_mode` unless overridden.
    """

    def __init__(self, client: HTTPClient, account_id: str | None = None, default_mode: str | None = None):
        """
        Initialize account operations.

        Args:
            client: HTTPClient instance for making requests
            account_id: Default account ID (can be overridden per request)
            default_mode: Default trading mode (PAPER/LIVE). If None, uses sdk_config.trading_mode
        """
        self.client = client
        self.account_id = account_id
        # Store default mode - will be used when mode=None is passed to functions
        self.default_mode = default_mode or sdk_config.trading_mode

    def get_account_info(self, mode: str | None = None) -> dict:
        """
        Get account information including account ID.

        Args:
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with account details

        Raises:
            TradeStationAPIError: When API responds with an error status.
            Exception: For unexpected errors (logged and returned as empty dict).

        Dependencies: HTTPClient.make_request
        """
        try:
            if mode is None:
                mode = self.default_mode
            response = self.client.make_request("GET", "brokerage/accounts", mode=mode)
            accounts_parsed = AccountsListResponse(**response)
            accounts = accounts_parsed.Accounts

            if not accounts:
                logger.warning("No accounts found")
                return {}

            # Convert Pydantic models to dicts for compatibility
            accounts_dicts = [a.model_dump() if hasattr(a, "model_dump") else a for a in accounts]

            # Log all returned accounts (at debug)
            account_ids = [
                a.get("AccountID") if isinstance(a, dict) else getattr(a, "AccountID", None) for a in accounts_dicts
            ]
            logger.debug(f"Accounts returned: {account_ids}")

            # Prefer an explicit account_id from secrets if provided
            explicit = getattr(sdk_config, "account_id", None)
            selected = None
            if explicit:
                selected = next((a for a in accounts_dicts if a.get("AccountID") == explicit), None)

            # Otherwise prefer a futures account, else first account
            if not selected:
                futures = [a for a in accounts_dicts if str(a.get("AccountType", "")).lower().startswith("future")]
                selected = futures[0] if futures else accounts_dicts[0]

            self.account_id = selected.get("AccountID")
            account_name = selected.get("Alias", f"Account {self.account_id}")

            logger.info(f"Account detected: {account_name} (ID: {self.account_id})")

            # Return the selected account plus full list for multi-account handling
            return {
                "account_id": self.account_id,
                "name": account_name,
                "type": selected.get("AccountType", "Unknown"),
                "status": selected.get("Status", "Unknown"),
                "currency": selected.get("Currency", "USD"),
                "accounts": accounts_dicts,
            }
        except TradeStationAPIError as e:
            e.details.operation = "get_account_info"
            if not e.details.message.startswith("Failed to get account info"):
                e.details.message = f"Failed to get account info: {e.details.message}"
            logger.error(f"Failed to get account info: {e.details.to_human_readable()}")
            return {}
        except Exception as e:
            logger.error(f"Failed to get account info: {e}", exc_info=True)
            return {}

    def _extract_balances(self, account: dict[str, Any]) -> dict[str, Any]:
        """
        Extract and normalize balance fields from a TradeStation account object.

        Args:
            account: Raw account dict returned by TradeStation.

        Returns:
            Dict with normalized numeric balance fields and currency.
        """
        return {
            "equity": float(account.get("Equity", 0)),
            "cash_balance": float(account.get("CashBalance", 0)),
            "buying_power": float(account.get("BuyingPower", 0)),
            "day_trading_buying_power": float(account.get("DayTradingBuyingPower", 0)),
            "margin_available": float(account.get("MarginAvailable", 0)),
            "margin_used": float(account.get("MarginUsed", 0)),
            "maintenance_margin": float(account.get("MaintenanceMargin", 0)),
            "initial_margin_requirement": float(account.get("InitialMarginRequirement", 0)),
            "net_liquidation_value": float(account.get("NetLiquidationValue", 0)),
            "open_pnl": float(account.get("OpenPnL", 0)),
            "realized_pnl": float(account.get("RealizedPnL", 0)),
            "unrealized_pnl": float(account.get("UnrealizedPnL", 0)),
            "currency": account.get("Currency", "USD"),
        }

    def get_account_balances(self, mode: str | None = None, account_id: str | None = None) -> dict[str, Any]:
        """
        Get account balances including equity, buying power, margin, and P&L.

        Args:
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)
            account_id: Optional TradeStation account ID. If provided, uses this directly.
                       If not provided, queries API for account list and uses first account.

        Returns:
            Dictionary with balance information:
            - equity: Total account equity
            - cash_balance: Available cash
            - buying_power: Total buying power
            - day_trading_buying_power: Day trading buying power
            - margin_available: Available margin
            - margin_used: Margin in use
            - maintenance_margin: Maintenance margin requirement
            - initial_margin_requirement: Initial margin requirement
            - net_liquidation_value: Net liquidation value
            - open_pnl: Open P&L
            - realized_pnl: Realized P&L
            - unrealized_pnl: Unrealized P&L
            - currency: Account currency

        Dependencies: HTTPClient.make_request, get_account_info

        Note: TradeStation API endpoint may vary. This uses the account details endpoint
        which includes balance information.

        Raises:
            TradeStationAPIError: When API returns an error response.
        """
        try:
            if mode is None:
                mode = self.default_mode
            # Always load the account list first; it contains balances in many responses
            self.client.token_manager.ensure_authenticated(mode)
            accounts_resp = self.client.make_request("GET", "brokerage/accounts", mode=mode)
            accounts = accounts_resp.get("Accounts", [])

            # Choose account: explicit ID, or first account
            selected_account = None
            if account_id:
                selected_account = next((a for a in accounts if a.get("AccountID") == account_id), None)
            if not selected_account:
                explicit = getattr(sdk_config, "account_id", None)
                if explicit:
                    selected_account = next((a for a in accounts if a.get("AccountID") == explicit), None)
            if not selected_account and accounts:
                futures = [a for a in accounts if str(a.get("AccountType", "")).lower().startswith("future")]
                selected_account = futures[0] if futures else accounts[0]
            if selected_account:
                account_id = selected_account.get("AccountID")

            if not account_id:
                logger.error(f"No account ID available for {mode or 'default'} mode - cannot fetch balances")
                return {}

            # Try detail endpoint for authoritative balances
            account_detail = None
            try:
                endpoint = f"brokerage/accounts/{account_id}"
                response = self.client.make_request("GET", endpoint, mode=mode)

                # Preserve raw Account dict to retain any balance fields that may be
                # omitted by strict Pydantic models (tests inject balances here).
                account_detail_raw = response.get("Account") if isinstance(response, dict) else None

                parsed = AccountBalancesResponse(**response)
                account_detail = parsed.Account.model_dump() if parsed.Account else None

                # Prefer raw account dict if it includes balance fields the model might drop
                account_obj = account_detail_raw or account_detail or {}
            except Exception as e:
                logger.debug(f"Account detail fetch failed for {account_id}: {e}")
                account_obj = selected_account or {}

            # Map TradeStation API fields to our standard format
            balances = self._extract_balances(account_obj)

            logger.debug(
                f"Account balances retrieved: Equity=${balances['equity']:.2f}, Buying Power=${balances['buying_power']:.2f}"
            )
            return balances

        except requests.HTTPError as e:
            # Handle 404 errors gracefully (account doesn't exist)
            if hasattr(e, "response") and e.response.status_code == 404:
                logger.debug(f"Account not found in {mode or 'default'} mode (404) - balance unavailable")
                return {}
            logger.error(f"HTTP error getting account balances: {e}")
            return {}
        except TradeStationAPIError as e:
            e.details.operation = "get_account_balances"
            # Handle 404 errors gracefully (account doesn't exist)
            if e.details.response_status == 404:
                logger.debug(f"Account not found in {mode or 'default'} mode - balance unavailable")
                return {}
            if not e.details.message.startswith("Failed to get account balances"):
                e.details.message = f"Failed to get account balances: {e.details.message}"
            logger.error(f"Failed to get account balances: {e.details.to_human_readable()}")
            return {}
        except Exception as e:
            error_str = str(e).lower()
            # Handle 404 errors gracefully (account doesn't exist)
            if "404" in error_str or "not found" in error_str:
                logger.debug(f"Account not found in {mode or 'default'} mode - balance unavailable")
                return {}
            logger.error(f"Failed to get account balances: {e}", exc_info=True)
            return {}

    def get_account_balances_detailed(self, account_ids: str | None = None, mode: str | None = None) -> dict[str, Any]:
        """
        Get detailed account balances using the dedicated balances endpoint.

        This endpoint provides more detailed balance information including BalanceDetail
        and CurrencyDetails (for futures accounts) compared to the account detail endpoint.

        Args:
            account_ids: Comma-separated account IDs (e.g., "123456782,123456789") or None.
                        If None, uses the default account_id or gets from account info.
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with:
            - Balances: List of balance dictionaries with detailed information
            - Errors: List of error dictionaries (if any)

        Dependencies: HTTPClient.make_request, get_account_info

        Note: TradeStation API endpoint: GET /v3/brokerage/accounts/{accounts}/balances
        """
        try:
            if mode is None:
                mode = self.default_mode

            # Resolve account IDs
            if not account_ids:
                account_info = self.get_account_info(mode)
                account_id = account_info.get("account_id") or self.account_id
                if not account_id:
                    logger.error(f"No account ID available for {mode} mode - cannot fetch detailed balances")
                    return {"Balances": [], "Errors": []}
                account_ids = account_id

            # TradeStation API v3 endpoint: brokerage/accounts/{accounts}/balances
            endpoint = f"brokerage/accounts/{account_ids}/balances"

            logger.debug(f"Fetching detailed balances: endpoint={endpoint}, accounts={account_ids}, mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)

            # Response structure: {"Balances": [...], "Errors": [...]}
            balances = response.get("Balances", [])
            errors = response.get("Errors", [])

            if errors:
                logger.warning(f"Some accounts returned errors: {errors}")

            logger.info(f"Retrieved detailed balances for {len(balances)} account(s) (mode: {mode})")

            return {"Balances": balances, "Errors": errors}

        except TradeStationAPIError as e:
            e.details.operation = "get_account_balances_detailed"
            if not e.details.message.startswith("Failed to get detailed account balances"):
                e.details.message = f"Failed to get detailed account balances: {e.details.message}"
            logger.error(f"Failed to get detailed account balances: {e.details.to_human_readable()}", exc_info=True)
            return {"Balances": [], "Errors": []}
        except Exception as e:
            logger.error(f"Failed to get detailed account balances: {e}", exc_info=True)
            return {"Balances": [], "Errors": []}

    def get_account_balances_bod(self, account_ids: str | None = None, mode: str | None = None) -> dict[str, Any]:
        """
        Get Beginning of Day balances for account(s).

        This endpoint provides BOD (Beginning of Day) balance snapshots which are
        useful for tracking daily starting balances and comparing to current balances.

        Args:
            account_ids: Comma-separated account IDs (e.g., "123456782,123456789") or None.
                        If None, uses the default account_id or gets from account info.
            mode: "PAPER" or "LIVE". If None, uses instance default_mode (from SDK initialization or last authenticated mode)

        Returns:
            Dictionary with:
            - BODBalances: List of BOD balance dictionaries with BalanceDetail
            - Errors: List of error dictionaries (if any)

        Dependencies: HTTPClient.make_request, get_account_info

        Note: TradeStation API endpoint: GET /v3/brokerage/accounts/{accounts}/bodbalances
        """
        try:
            if mode is None:
                mode = self.default_mode

            # Resolve account IDs
            if not account_ids:
                account_info = self.get_account_info(mode)
                account_id = account_info.get("account_id") or self.account_id
                if not account_id:
                    logger.error(f"No account ID available for {mode} mode - cannot fetch BOD balances")
                    return {"BODBalances": [], "Errors": []}
                account_ids = account_id

            # TradeStation API v3 endpoint: brokerage/accounts/{accounts}/bodbalances
            endpoint = f"brokerage/accounts/{account_ids}/bodbalances"

            logger.debug(f"Fetching BOD balances: endpoint={endpoint}, accounts={account_ids}, mode={mode}")
            response = self.client.make_request("GET", endpoint, mode=mode)
            parsed = BODBalancesResponse(**response)

            # Extract errors from parsed model
            errors = parsed.Errors or []

            if errors:
                logger.warning(f"Some accounts returned errors: {errors}")

            bod_balances = parsed.BODBalances
            bod_balances_dicts = [b.model_dump() if hasattr(b, "model_dump") else b for b in bod_balances]

            logger.info(f"Retrieved BOD balances for {len(bod_balances_dicts)} account(s) (mode: {mode})")

            return {"BODBalances": bod_balances_dicts, "Errors": errors}

        except TradeStationAPIError as e:
            e.details.operation = "get_account_balances_bod"
            if not e.details.message.startswith("Failed to get BOD balances"):
                e.details.message = f"Failed to get BOD balances: {e.details.message}"
            logger.error(f"Failed to get BOD balances: {e.details.to_human_readable()}", exc_info=True)
            return {"BODBalances": [], "Errors": []}
        except Exception as e:
            logger.error(f"Failed to get BOD balances: {e}", exc_info=True)
            return {"BODBalances": [], "Errors": []}

"""
AccountOperations Unit Tests

Tests for AccountOperations class including account info and balance queries.
"""

import pytest
from tradestation.exceptions import ErrorDetails, InvalidRequestError, TradeStationAPIError
from tradestation.accounts import AccountOperations

from .fixtures import api_responses

# ============================================================================
# AccountOperations get_account_info Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.accounts
class TestAccountOperationsGetAccountInfo:
    """Tests for get_account_info method."""

    def test_get_account_info_success(self, mock_http_client, mocker):
        """Test get_account_info returns account information."""
        # Mock API response
        mock_response = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_ACCOUNTS_LIST
        )

        account_ops = AccountOperations(mock_http_client, account_id="SIM123456", default_mode="PAPER")
        result = account_ops.get_account_info("PAPER")

        # Verify endpoint was called
        mock_response.assert_called_once_with("GET", "brokerage/accounts", mode="PAPER")

        # Verify result structure
        assert "account_id" in result
        assert result["account_id"] == "SIM123456"
        assert "name" in result
        assert "accounts" in result

    def test_get_account_info_response_parsing(self, mock_http_client, mocker):
        """Test get_account_info parses response correctly."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ACCOUNTS_LIST)

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        result = account_ops.get_account_info("PAPER")

        # Verify account selection logic
        assert result["account_id"] in ["SIM123456", "SIM789012"]
        assert len(result["accounts"]) == 2

    def test_get_account_info_preserves_v3_account_detail(self, mock_http_client, mocker):
        """Test get_account_info accepts v3 AccountDetail payloads without validation failure."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ACCOUNTS_LIST)

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        result = account_ops.get_account_info("PAPER")

        assert result["accounts"][0]["AccountDetail"]["DayTradingQualified"] is True
        assert result["accounts"][0]["AccountDetail"]["OptionApprovalLevel"] == 0

    def test_get_account_info_account_id_selection(self, mock_http_client, mocker):
        """Test get_account_info selects account ID correctly."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ACCOUNTS_LIST)

        account_ops = AccountOperations(mock_http_client, account_id="SIM123456", default_mode="PAPER")
        result = account_ops.get_account_info("PAPER")

        # Verify account_id was set
        assert account_ops.account_id == result["account_id"]

    def test_get_account_info_mode_parameter(self, mock_http_client, mocker):
        """Test get_account_info respects mode parameter."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_ACCOUNTS_LIST
        )

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        account_ops.get_account_info("LIVE")

        # Verify mode was passed correctly
        mock_request.assert_called_once_with("GET", "brokerage/accounts", mode="LIVE")

    def test_get_account_info_error_handling(self, mock_http_client, mocker):
        """Test get_account_info fails loud on broker errors."""
        mocker.patch.object(mock_http_client, "make_request", side_effect=TradeStationAPIError("API Error"))

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        with pytest.raises(TradeStationAPIError):
            account_ops.get_account_info("PAPER")

    def test_get_account_info_no_accounts_raises(self, mock_http_client, mocker):
        """Test get_account_info fails loud when no accounts are returned."""
        mocker.patch.object(mock_http_client, "make_request", return_value={"Accounts": []})

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")

        with pytest.raises(InvalidRequestError) as exc_info:
            account_ops.get_account_info("PAPER")

        assert exc_info.value.details.operation == "get_account_info"


# ============================================================================
# AccountOperations get_account_balances Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.accounts
class TestAccountOperationsGetAccountBalances:
    """Tests for get_account_balances method."""

    def test_get_account_balances_success(self, mock_http_client, mocker):
        """Test get_account_balances returns balance information."""
        # Mock both API calls: account list + account detail
        mock_request = mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=[
                {
                    "Accounts": [
                        {
                            "AccountID": "SIM123456",
                            "Equity": 100000.00,
                            "CashBalance": 100000.00,
                            "BuyingPower": 400000.00,
                        }
                    ]
                },  # Account list
                {
                    "Account": {
                        "AccountID": "SIM123456",
                        "Equity": 100000.00,
                        "CashBalance": 100000.00,
                        "BuyingPower": 400000.00,
                    }
                },  # Account detail
            ],
        )

        account_ops = AccountOperations(mock_http_client, account_id="SIM123456", default_mode="PAPER")
        result = account_ops.get_account_balances("PAPER", "SIM123456")

        # Verify both endpoints were called (account list + account detail)
        assert mock_request.call_count == 2
        # First call: account list
        mock_request.assert_any_call("GET", "brokerage/accounts", mode="PAPER")
        # Second call: account detail
        mock_request.assert_any_call("GET", "brokerage/accounts/SIM123456", mode="PAPER")

        # Verify result structure
        assert "equity" in result
        assert "cash_balance" in result
        assert "buying_power" in result

    def test_get_account_balances_response_structure(self, mock_http_client, mocker):
        """Test get_account_balances extracts balance fields correctly."""
        # Mock both API calls: account list + account detail
        # Account detail response should match AccountBalancesResponse structure
        # Note: AccountSummary model only has AccountID, AccountType, Status, Currency, Alias
        # But TradeStation API may return balance fields in the Account object
        # _extract_balances() reads from account object, so we need balance fields there
        account_list_item = {
            "AccountID": "SIM123456",
            "AccountType": "INDIVIDUAL",
            "Status": "ACTIVE",
            "Currency": "USD",
            "Alias": "Paper",
        }
        account_detail_item = {
            "AccountID": "SIM123456",
            "AccountType": "INDIVIDUAL",
            "Status": "ACTIVE",
            "Currency": "USD",
            "Alias": "Paper",
            "Equity": 100000.00,  # Balance fields in Account object
            "CashBalance": 100000.00,
            "BuyingPower": 400000.00,
            "DayTradingBuyingPower": 200000.00,
            "MarginAvailable": 300000.00,
            "MarginUsed": 0.00,
            "MaintenanceMargin": 0.00,
            "InitialMarginRequirement": 0.00,
            "NetLiquidationValue": 100000.00,
            "OpenPnL": 0.00,
            "RealizedPnL": 0.00,
            "UnrealizedPnL": 0.00,
        }
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=[
                {"Accounts": [account_list_item]},  # Account list
                {
                    "Account": account_detail_item,
                    "Balances": None,
                },  # Account detail (AccountBalancesResponse structure)
            ],
        )

        account_ops = AccountOperations(mock_http_client, account_id="SIM123456", default_mode="PAPER")
        result = account_ops.get_account_balances("PAPER", "SIM123456")

        # Verify all balance fields are present
        assert result["equity"] == 100000.00
        assert result["cash_balance"] == 100000.00
        assert result["buying_power"] == 400000.00

    def test_get_account_balances_account_id_parameter(self, mock_http_client, mocker):
        """Test get_account_balances handles account_id parameter."""
        # Mock both API calls: account list + account detail
        mock_request = mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=[
                {
                    "Accounts": [
                        {
                            "AccountID": "SIM789012",
                            "Equity": "100000.00",
                            "CashBalance": "100000.00",
                            "BuyingPower": "400000.00",
                        }
                    ]
                },  # Account list
                {
                    "Account": {
                        "AccountID": "SIM789012",
                        "Equity": "100000.00",
                        "CashBalance": "100000.00",
                        "BuyingPower": "400000.00",
                    }
                },  # Account detail
            ],
        )

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        account_ops.get_account_balances("PAPER", account_id="SIM789012")

        # Verify both endpoints were called (account list + account detail)
        assert mock_request.call_count == 2
        # First call: account list
        mock_request.assert_any_call("GET", "brokerage/accounts", mode="PAPER")
        # Second call: account detail with account ID
        mock_request.assert_any_call("GET", "brokerage/accounts/SIM789012", mode="PAPER")

    def test_get_account_balances_404_raises(self, mock_http_client, mocker):
        """Test get_account_balances fails loud when the target account is not found."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=[
                api_responses.MOCK_ACCOUNTS_LIST,
                TradeStationAPIError(
                    ErrorDetails(
                        message="account not found",
                        response_status=404,
                        request_endpoint="brokerage/accounts/SIM123456",
                    )
                ),
            ],
        )

        account_ops = AccountOperations(mock_http_client, account_id="SIM123456", default_mode="PAPER")

        with pytest.raises(InvalidRequestError) as exc_info:
            account_ops.get_account_balances("PAPER", "SIM123456")

        assert exc_info.value.details.code == "ACCOUNT_NOT_FOUND"


# ============================================================================
# AccountOperations get_account_balances_detailed Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.accounts
class TestAccountOperationsGetAccountBalancesDetailed:
    """Tests for get_account_balances_detailed method."""

    def test_get_account_balances_detailed_success(self, mock_http_client, mocker):
        """Test get_account_balances_detailed returns detailed balances."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_DETAILED_BALANCES
        )

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        result = account_ops.get_account_balances_detailed("SIM123456,SIM789012", "PAPER")

        # Verify endpoint was called
        mock_request.assert_called_once_with("GET", "brokerage/accounts/SIM123456,SIM789012/balances", mode="PAPER")

        # Verify result structure
        assert "Balances" in result or isinstance(result, list)

    def test_get_account_balances_detailed_multiple_accounts(self, mock_http_client, mocker):
        """Test get_account_balances_detailed handles multiple account IDs."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_DETAILED_BALANCES)

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        result = account_ops.get_account_balances_detailed("SIM123456,SIM789012", "PAPER")

        # Verify multiple accounts were requested
        assert result is not None

    def test_get_account_balances_detailed_requires_resolved_account(self, mock_http_client, mocker):
        """Test detailed balances fail loud when no account can be resolved."""
        mocker.patch.object(mock_http_client, "make_request", return_value={"Accounts": []})

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")

        with pytest.raises(InvalidRequestError) as exc_info:
            account_ops.get_account_balances_detailed(None, "PAPER")

        assert exc_info.value.details.operation == "get_account_balances_detailed"


# ============================================================================
# AccountOperations get_account_balances_bod Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.accounts
class TestAccountOperationsGetAccountBalancesBOD:
    """Tests for get_account_balances_bod method."""

    def test_get_account_balances_bod_success(self, mock_http_client, mocker):
        """Test get_account_balances_bod returns BOD balances."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_BOD_BALANCES
        )

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        result = account_ops.get_account_balances_bod("SIM123456", "PAPER")

        # Verify endpoint was called
        mock_request.assert_called_once_with("GET", "brokerage/accounts/SIM123456/bodbalances", mode="PAPER")

        # Verify result structure (returns dict with "BODBalances" key)
        assert "BODBalances" in result
        assert isinstance(result["BODBalances"], list)

    def test_get_account_balances_bod_response(self, mock_http_client, mocker):
        """Test get_account_balances_bod parses BOD balance response."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_BOD_BALANCES)

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        result = account_ops.get_account_balances_bod("SIM123456", "PAPER")

        # Verify BOD balance data is present
        assert result is not None

    def test_get_account_balances_bod_requires_resolved_account(self, mock_http_client, mocker):
        """Test BOD balances fail loud when no account can be resolved."""
        mocker.patch.object(mock_http_client, "make_request", return_value={"Accounts": []})

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")

        with pytest.raises(InvalidRequestError) as exc_info:
            account_ops.get_account_balances_bod(None, "PAPER")

        assert exc_info.value.details.operation == "get_account_balances_bod"


# ============================================================================
# AccountOperations Mode Switching Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.accounts
class TestAccountOperationsModeSwitching:
    """Tests for mode switching in AccountOperations."""

    def test_mode_switching_paper_to_live(self, mock_http_client, mocker):
        """Test switching from PAPER to LIVE mode."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_ACCOUNTS_LIST
        )

        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")

        # Call with PAPER mode
        account_ops.get_account_info("PAPER")
        call1 = mock_request.call_args

        # Call with LIVE mode
        account_ops.get_account_info("LIVE")
        call2 = mock_request.call_args

        # Verify both calls used correct modes
        assert call1[1]["mode"] == "PAPER"
        assert call2[1]["mode"] == "LIVE"

    def test_default_mode_used_when_none(self, mock_http_client, mocker):
        """Test default mode is used when mode=None."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_ACCOUNTS_LIST
        )

        account_ops = AccountOperations(mock_http_client, default_mode="LIVE")
        account_ops.get_account_info(None)

        # Verify default mode was used
        mock_request.assert_called_once_with("GET", "brokerage/accounts", mode="LIVE")

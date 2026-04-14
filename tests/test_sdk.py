"""
TradeStationSDK Unit Tests

Tests for TradeStationSDK class including initialization, function delegation, and end-to-end workflows.
"""

import pytest
from tradestation import TradeStationSDK, TradeStationSDKConfig

# ============================================================================
# TradeStationSDK Initialization Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.sdk
class TestTradeStationSDKInitialization:
    """Tests for TradeStationSDK initialization."""

    def test_sdk_initialization_default(self, mocker):
        """Test SDK creation with default settings."""
        sdk = TradeStationSDK(
            config=TradeStationSDKConfig(
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="http://localhost:8888",
                account_id="SIM123456",
                trading_mode="PAPER",
                log_level="DEBUG",
            ),
            enable_full_logging=False,
        )

        # Verify SDK was created
        assert sdk is not None
        assert sdk.client_id == "test_client_id"
        assert sdk.account_id == "SIM123456"
        assert sdk.default_mode == "PAPER"

    def test_sdk_initialization_full_logging(self):
        """Test SDK creation with enable_full_logging=True."""
        sdk = TradeStationSDK(
            config=TradeStationSDKConfig(
                client_id="test_client_id",
                client_secret="test_client_secret",
                redirect_uri="http://localhost:8888",
                account_id="SIM123456",
                trading_mode="PAPER",
                log_level="DEBUG",
            ),
            enable_full_logging=True,
        )

        # Verify full logging is enabled
        assert sdk._client.enable_full_logging is True

    def test_sdk_initialization_from_env(self, monkeypatch):
        """Test SDK creation loads env on construction when no config is supplied."""
        monkeypatch.setattr("tradestation.config._load_env_file", lambda: None)
        monkeypatch.setenv("TRADESTATION_CLIENT_ID", "env_client_id")
        monkeypatch.setenv("TRADESTATION_CLIENT_SECRET", "env_client_secret")
        monkeypatch.setenv("TRADESTATION_REDIRECT_URI", "http://localhost:9999/callback")
        monkeypatch.setenv("TRADESTATION_ACCOUNT_ID", "SIMENV123")
        monkeypatch.setenv("TRADESTATION_MODE", "LIVE")
        monkeypatch.delenv("TRADING_MODE", raising=False)

        sdk = TradeStationSDK(enable_full_logging=False)

        assert sdk.client_id == "env_client_id"
        assert sdk.client_secret == "env_client_secret"
        assert sdk.redirect_uri == "http://localhost:9999/callback"
        assert sdk.account_id == "SIMENV123"
        assert sdk.default_mode == "LIVE"

    def test_sdk_initialization_prefers_tradestation_mode_over_trading_mode(
        self, monkeypatch
    ):
        """Test TRADESTATION_MODE overrides deprecated TRADING_MODE."""
        monkeypatch.setattr("tradestation.config._load_env_file", lambda: None)
        monkeypatch.setenv("TRADESTATION_CLIENT_ID", "env_client_id")
        monkeypatch.setenv("TRADESTATION_CLIENT_SECRET", "env_client_secret")
        monkeypatch.setenv("TRADESTATION_MODE", "PAPER")
        monkeypatch.setenv("TRADING_MODE", "LIVE")

        sdk = TradeStationSDK(enable_full_logging=False)

        assert sdk.default_mode == "PAPER"

    def test_sdk_all_modules_initialized(self, sdk_instance):
        """Test all operation modules are initialized."""
        assert sdk_instance._accounts is not None
        assert sdk_instance._market_data is not None
        assert sdk_instance._positions is not None
        assert sdk_instance._order_executions is not None
        assert sdk_instance._orders is not None
        assert sdk_instance._streaming is not None


# ============================================================================
# TradeStationSDK Function Delegation Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.sdk
class TestTradeStationSDKFunctionDelegation:
    """Tests for SDK method delegation to operation modules."""

    def test_get_account_info_delegates(self, sdk_instance, mocker):
        """Test get_account_info delegates to AccountOperations."""
        mock_accounts = mocker.patch.object(sdk_instance._accounts, "get_account_info")
        mock_accounts.return_value = {"account_id": "SIM123456"}

        sdk_instance.get_account_info("PAPER")

        mock_accounts.assert_called_once_with("PAPER")

    def test_get_bars_delegates(self, sdk_instance, mocker):
        """Test get_bars delegates to MarketDataOperations."""
        mock_market_data = mocker.patch.object(sdk_instance._market_data, "get_bars")
        mock_market_data.return_value = []

        sdk_instance.get_bars("MNQZ25", "1", "Minute", bars_back=200, mode="PAPER")

        mock_market_data.assert_called_once()
        call_args = mock_market_data.call_args
        assert call_args[0][0] == "MNQZ25"
        assert call_args[0][-1] == "PAPER"

    def test_place_order_delegates(self, sdk_instance, mocker):
        """Test place_order delegates to OrderExecutionOperations."""
        mock_order_exec = mocker.patch.object(sdk_instance._order_executions, "place_order")
        mock_order_exec.return_value = ("924243071", "SUCCESS")

        sdk_instance.place_order("MNQZ25", "BUY", 2, "Market", mode="PAPER")

        mock_order_exec.assert_called_once()
        call_args = mock_order_exec.call_args
        assert call_args[0][0] == "MNQZ25"
        assert call_args[0][1] == "BUY"
        assert call_args[0][2] == 2

    def test_get_position_delegates(self, sdk_instance, mocker):
        """Test get_position delegates to PositionOperations."""
        mock_positions = mocker.patch.object(sdk_instance._positions, "get_position")
        mock_positions.return_value = 2

        result = sdk_instance.get_position("MNQZ25", mode="PAPER")

        mock_positions.assert_called_once_with("MNQZ25", "PAPER")
        assert result == 2

    def test_mode_parameter_propagation(self, sdk_instance, mocker):
        """Test mode parameter propagates to operation modules."""
        mock_accounts = mocker.patch.object(sdk_instance._accounts, "get_account_info")
        mock_accounts.return_value = {"account_id": "SIM123456"}

        sdk_instance.get_account_info("LIVE")

        # Verify mode was passed
        mock_accounts.assert_called_once_with("LIVE")

    def test_account_id_handling(self, sdk_instance, mocker):
        """Test account_id handling in SDK methods."""
        mock_accounts = mocker.patch.object(sdk_instance._accounts, "get_account_balances")
        mock_accounts.return_value = {"equity": 100000.0}

        sdk_instance.get_account_balances(mode="PAPER", account_id="SIM789012")

        mock_accounts.assert_called_once_with("PAPER", "SIM789012")


# ============================================================================
# TradeStationSDK End-to-End Workflows Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.sdk
class TestTradeStationSDKWorkflows:
    """Tests for complete SDK workflows."""

    def test_order_placement_workflow(self, sdk_instance, mocker):
        """Test complete order placement workflow."""
        # Mock account info
        mocker.patch.object(sdk_instance._accounts, "get_account_info", return_value={"account_id": "SIM123456"})

        # Mock order placement
        mocker.patch.object(sdk_instance._order_executions, "place_order", return_value=("924243071", "SUCCESS"))

        # Execute workflow
        order_id, status = sdk_instance.place_order("MNQZ25", "BUY", 2, "Market", mode="PAPER")

        assert order_id == "924243071"
        assert status == "SUCCESS"

    def test_position_management_workflow(self, sdk_instance, mocker):
        """Test position management workflow."""
        # Mock get position
        mocker.patch.object(sdk_instance._positions, "get_position", return_value=2)

        # Mock get all positions
        mocker.patch.object(
            sdk_instance._positions, "get_all_positions", return_value=[{"symbol": "MNQZ25", "quantity": 2}]
        )

        # Execute workflow
        position = sdk_instance.get_position("MNQZ25", mode="PAPER")
        all_positions = sdk_instance.get_all_positions(mode="PAPER")

        assert position == 2
        assert len(all_positions) == 1

    def test_market_data_order_workflow(self, sdk_instance, mocker):
        """Test market data + order placement workflow."""
        # Mock get bars
        mocker.patch.object(sdk_instance._market_data, "get_bars", return_value=[{"Close": 25000.0}])

        # Mock account info
        mocker.patch.object(sdk_instance._accounts, "get_account_info", return_value={"account_id": "SIM123456"})

        # Mock order placement
        mocker.patch.object(sdk_instance._order_executions, "place_order", return_value=("924243071", "SUCCESS"))

        # Execute workflow: get bars, analyze, place order
        bars = sdk_instance.get_bars("MNQZ25", "1", "Minute", bars_back=200, mode="PAPER")
        assert len(bars) > 0

        # Simulate analysis and order placement
        order_id, status = sdk_instance.place_order("MNQZ25", "BUY", 2, "Market", mode="PAPER")
        assert order_id == "924243071"

"""
PositionOperations Unit Tests

Tests for PositionOperations class including position queries and flattening.
"""

import pytest

from tradestation.operations.positions import PositionOperations

from .fixtures import api_responses

# ============================================================================
# PositionOperations get_position Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestPositionOperationsGetPosition:
    """Tests for get_position method."""

    def test_get_position_success(self, mock_http_client, mocker):
        """Test get_position returns position for symbol."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mock_request = mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_POSITIONS)

        position_ops = PositionOperations(mock_http_client, mock_accounts, account_id="SIM123456", default_mode="PAPER")
        result = position_ops.get_position("MNQZ25", mode="PAPER")

        # Verify endpoint
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "brokerage/accounts/SIM123456/positions" in call_args[0][1]

        # Verify result (should be quantity as int)
        assert isinstance(result, int)
        assert result == 2

    def test_get_position_zero_position(self, mock_http_client, mocker):
        """Test get_position returns 0 when no position exists."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_EMPTY_POSITIONS)

        position_ops = PositionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = position_ops.get_position("ESZ25", mode="PAPER")

        assert result == 0

    def test_get_position_extraction_logic(self, mock_http_client, mocker):
        """Test get_position extracts position for specific symbol."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        # Mock response with multiple positions
        multi_positions = {"Positions": [{"Symbol": "MNQZ25", "Quantity": "2"}, {"Symbol": "ESZ25", "Quantity": "1"}]}

        mocker.patch.object(mock_http_client, "make_request", return_value=multi_positions)

        position_ops = PositionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = position_ops.get_position("MNQZ25", mode="PAPER")

        assert result == 2


# ============================================================================
# PositionOperations get_all_positions Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestPositionOperationsGetAllPositions:
    """Tests for get_all_positions method."""

    def test_get_all_positions_success(self, mock_http_client, mocker):
        """Test get_all_positions returns all positions."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mock_request = mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_POSITIONS)

        position_ops = PositionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = position_ops.get_all_positions(mode="PAPER")

        # Verify endpoint
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "brokerage/accounts/SIM123456/positions" in call_args[0][1]

        # Verify result
        assert isinstance(result, list)
        if result:
            assert "Symbol" in result[0] or "symbol" in result[0]


# ============================================================================
# PositionOperations flatten_position Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestPositionOperationsFlattenPosition:
    """Tests for flatten_position method."""

    def test_flatten_position_specific_symbol(self, mock_http_client, mocker):
        """Test flatten_position flattens position for specific symbol."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        # Mock get_position to return position
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=[
                api_responses.MOCK_POSITIONS,  # get_position response
                api_responses.MOCK_ORDER_PLACEMENT_SUCCESS,  # place_order response
            ],
        )

        # Mock OrderOperations.place_order
        from tradestation.operations.order_executions import OrderExecutionOperations

        mock_order_exec = mocker.MagicMock(spec=OrderExecutionOperations)
        mock_order_exec.place_order.return_value = ("924243071", "SUCCESS")

        position_ops = PositionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        position_ops._order_executions = mock_order_exec  # Inject mock

        _ = position_ops.flatten_position("MNQZ25", mock_order_exec, mode="PAPER")

        # Verify get_position was called
        assert mock_http_client.make_request.call_count >= 1
        # Verify place_order was called to close position
        mock_order_exec.place_order.assert_called_once()

    def test_flatten_position_all_positions(self, mock_http_client, mocker):
        """Test flatten_position with symbol=None flattens all positions."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        # Mock get_all_positions to return multiple positions
        multi_positions = {"Positions": [{"Symbol": "MNQZ25", "Quantity": "2"}, {"Symbol": "ESZ25", "Quantity": "1"}]}

        mocker.patch.object(mock_http_client, "make_request", return_value=multi_positions)

        from tradestation.operations.order_executions import OrderExecutionOperations

        mock_order_exec = mocker.MagicMock(spec=OrderExecutionOperations)
        mock_order_exec.place_order.return_value = ("924243071", "SUCCESS")

        position_ops = PositionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        position_ops._order_executions = mock_order_exec

        _ = position_ops.flatten_position(None, mock_order_exec, mode="PAPER")

        # Verify place_order was called for each position
        assert mock_order_exec.place_order.call_count == 2

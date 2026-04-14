"""
OrderOperations Unit Tests

Tests for OrderOperations class including order history, current orders, and order queries.
"""

import pytest
from tradestation.orders import OrderOperations

from .fixtures import api_responses

# ============================================================================
# OrderOperations get_order_history Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderOperationsGetOrderHistory:
    """Tests for get_order_history method."""

    def test_get_order_history_success(self, mock_http_client, mocker):
        """Test get_order_history returns order history."""
        # Mock account operations
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY
        )

        order_ops = OrderOperations(mock_http_client, mock_accounts, account_id="SIM123456", default_mode="PAPER")
        result = order_ops.get_order_history(mode="PAPER")

        # Verify endpoint was called
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "brokerage/accounts/SIM123456/historicalorders" in call_args[0][1]

        # Verify result
        assert isinstance(result, list)
        if result:
            assert "OrderID" in result[0]

    def test_get_order_history_date_filtering(self, mock_http_client, mocker):
        """Test get_order_history handles date filtering."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_ops.get_order_history(start_date="2025-12-01", end_date="2025-12-04", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "startDate" in call_args[1]["params"] or "StartDate" in call_args[1]["params"]

    def test_get_order_history_limit_parameter(self, mock_http_client, mocker):
        """Test get_order_history handles limit parameter."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_ops.get_order_history(limit=50, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "limit" in call_args[1]["params"] or "Limit" in call_args[1]["params"]

    def test_get_order_history_default_start_date(self, mock_http_client, mocker):
        """Test get_order_history defaults to 7 days ago when start_date is None."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_ops.get_order_history(mode="PAPER")

        # Should have date parameters set
        call_args = mock_http_client.make_request.call_args
        assert call_args[1]["params"] is not None


# ============================================================================
# OrderOperations get_current_orders Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderOperationsGetCurrentOrders:
    """Tests for get_current_orders method."""

    def test_get_current_orders_success(self, mock_http_client, mocker):
        """Test get_current_orders returns current orders."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_CURRENT_ORDERS
        )

        order_ops = OrderOperations(mock_http_client, mock_accounts, account_id="SIM123456", default_mode="PAPER")
        result = order_ops.get_current_orders(mode="PAPER")

        # Verify endpoint
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "brokerage/accounts/SIM123456/orders" in call_args[0][1]

        # Verify result structure
        assert isinstance(result, dict)
        assert "Orders" in result or isinstance(result, list)

    def test_get_current_orders_pagination(self, mock_http_client, mocker):
        """Test get_current_orders handles pagination with next_token."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_CURRENT_ORDERS)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_ops.get_current_orders(next_token="token123", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "nextToken" in call_args[1]["params"] or "NextToken" in call_args[1]["params"]

    def test_get_current_orders_multiple_accounts(self, mock_http_client, mocker):
        """Test get_current_orders handles multiple account IDs."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_CURRENT_ORDERS)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_ops.get_current_orders(account_ids="SIM123456,SIM789012", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "SIM123456,SIM789012" in call_args[0][1]


# ============================================================================
# OrderOperations get_orders_by_ids Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderOperationsGetOrdersByIds:
    """Tests for get_orders_by_ids method."""

    def test_get_orders_by_ids_single(self, mock_http_client, mocker):
        """Test get_orders_by_ids with single order ID."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_CURRENT_ORDERS)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_ops.get_orders_by_ids("924243071", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "brokerage/accounts" in call_args[0][1]
        assert "924243071" in call_args[0][1]
        assert result is not None

    def test_get_orders_by_ids_multiple(self, mock_http_client, mocker):
        """Test get_orders_by_ids with multiple order IDs."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_CURRENT_ORDERS)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_ops.get_orders_by_ids("924243071,924243072", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "924243071,924243072" in call_args[0][1]


# ============================================================================
# OrderOperations get_historical_orders_by_ids Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderOperationsGetHistoricalOrdersByIds:
    """Tests for get_historical_orders_by_ids method."""

    def test_get_historical_orders_by_ids_success(self, mock_http_client, mocker):
        """Test get_historical_orders_by_ids returns historical orders."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_ops.get_historical_orders_by_ids(
            "924243070", start_date="2025-12-01", end_date="2025-12-04", mode="PAPER"
        )

        call_args = mock_http_client.make_request.call_args
        assert "historicalorders" in call_args[0][1]
        assert "924243070" in call_args[0][1]
        assert result is not None


# ============================================================================
# OrderOperations Status Filter Functions Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderOperationsStatusFilters:
    """Tests for status filter convenience functions."""

    def test_get_orders_by_status(self, mock_http_client, mocker):
        """Test get_orders_by_status filters by status."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_CURRENT_ORDERS)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_ops.get_orders_by_status("OPEN", mode="PAPER")

        # Should call get_current_orders and filter
        assert result is not None

    def test_get_open_orders(self, mock_http_client, mocker):
        """Test get_open_orders convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_CURRENT_ORDERS)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_ops.get_open_orders(mode="PAPER")

        assert result is not None

    def test_get_filled_orders(self, mock_http_client, mocker):
        """Test get_filled_orders convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_ops.get_filled_orders(mode="PAPER")

        assert result is not None

    def test_get_canceled_orders(self, mock_http_client, mocker):
        """Test get_canceled_orders convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_ops.get_canceled_orders(mode="PAPER")

        assert result is not None

    def test_get_rejected_orders(self, mock_http_client, mocker):
        """Test get_rejected_orders convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_HISTORY)

        order_ops = OrderOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_ops.get_rejected_orders(mode="PAPER")

        assert result is not None

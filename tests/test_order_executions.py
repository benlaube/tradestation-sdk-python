"""
OrderExecutionOperations Unit Tests

Tests for OrderExecutionOperations class including order placement, modification, cancellation,
executions, confirmations, and group orders (OCO/Bracket).
"""

import pytest
from src.lib.tradestation.order_executions import OrderExecutionOperations

from .fixtures import api_responses

# ============================================================================
# OrderExecutionOperations place_order Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsPlaceOrder:
    """Tests for place_order method."""

    def test_place_order_market(self, mock_http_client, mocker):
        """Test place_order with Market order type."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS
        )

        order_exec = OrderExecutionOperations(
            mock_http_client, mock_accounts, account_id="SIM123456", default_mode="PAPER"
        )
        order_id, status = order_exec.place_order("MNQZ25", "BUY", 2, "Market", mode="PAPER")

        # Verify endpoint
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "orderexecution/orders" in call_args[0][1]
        assert call_args[0][0] == "POST"

        # Verify request body
        json_data = call_args[1]["json_data"]
        assert json_data["Symbol"] == "MNQZ25"
        assert json_data["TradeAction"] == "BUY"
        assert json_data["Quantity"] == "2"
        assert json_data["OrderType"] == "Market"

        # Verify response parsing
        assert order_id is not None

    def test_place_order_limit(self, mock_http_client, mocker):
        """Test place_order with Limit order type."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_order("MNQZ25", "BUY", 2, "Limit", limit_price=25000.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "Limit"
        assert json_data["LimitPrice"] == "25000.0"

    def test_place_order_stop(self, mock_http_client, mocker):
        """Test place_order with Stop order type."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_order("MNQZ25", "BUY", 2, "Stop", stop_price=24900.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "Stop"
        assert json_data["StopPrice"] == "24900.0"

    def test_place_order_stop_limit(self, mock_http_client, mocker):
        """Test place_order with StopLimit order type."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_order("MNQZ25", "BUY", 2, "StopLimit", limit_price=25000.0, stop_price=24900.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "StopLimit"
        assert json_data["LimitPrice"] == "25000.0"
        assert json_data["StopPrice"] == "24900.0"

    def test_place_order_trailing_stop(self, mock_http_client, mocker):
        """Test place_order with TrailingStop order type."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_order("MNQZ25", "BUY", 2, "TrailingStop", trail_amount=1.5, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "TrailingStop"
        assert json_data["TrailAmount"] == "1.5"

    def test_place_order_trailing_stop_percent(self, mock_http_client, mocker):
        """Test place_order with TrailingStop using trail_percent."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_order("MNQZ25", "BUY", 2, "TrailingStop", trail_percent=1.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["TrailPercent"] == "1.0"

    def test_place_order_time_in_force(self, mock_http_client, mocker):
        """Test place_order handles time_in_force options."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_order("MNQZ25", "BUY", 2, "Market", time_in_force="GTC", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["TimeInForce"]["Duration"] == "GTC"

    def test_place_order_response_parsing(self, mock_http_client, mocker):
        """Test place_order extracts order_id from response."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_id, status = order_exec.place_order("MNQZ25", "BUY", 2, "Market", mode="PAPER")

        # Verify order_id was extracted
        assert order_id == "924243071"


# ============================================================================
# OrderExecutionOperations cancel_order Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsCancelOrder:
    """Tests for cancel_order method."""

    def test_cancel_order_success(self, mock_http_client, mocker):
        """Test cancel_order cancels an order."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_CANCEL_SUCCESS
        )

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_id, status = order_exec.cancel_order("924243071", mode="PAPER")

        # Verify endpoint
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "orderexecution/orders/924243071" in call_args[0][1]
        assert call_args[0][0] == "DELETE"

        # Verify response
        assert order_id == "924243071"


# ============================================================================
# OrderExecutionOperations modify_order Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsModifyOrder:
    """Tests for modify_order method."""

    def test_modify_order_quantity(self, mock_http_client, mocker):
        """Test modify_order changes quantity."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_MODIFY_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.modify_order("924243071", quantity=3, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert call_args[0][0] == "PUT"
        json_data = call_args[1]["json_data"]
        assert json_data["Quantity"] == "3"

    def test_modify_order_limit_price(self, mock_http_client, mocker):
        """Test modify_order changes limit price."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_MODIFY_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.modify_order("924243071", limit_price=25010.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["LimitPrice"] == "25010.0"

    def test_modify_order_partial(self, mock_http_client, mocker):
        """Test modify_order with partial modifications."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_MODIFY_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.modify_order("924243071", quantity=3, limit_price=25010.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert "Quantity" in json_data
        assert "LimitPrice" in json_data


# ============================================================================
# OrderExecutionOperations get_order_executions Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsGetOrderExecutions:
    """Tests for get_order_executions method."""

    def test_get_order_executions_success(self, mock_http_client, mocker):
        """Test get_order_executions returns execution data."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_EXECUTIONS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_exec.get_order_executions("924243071", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "orderexecution/orders/924243071/executions" in call_args[0][1]
        assert isinstance(result, list)

    def test_is_order_filled(self, mock_http_client, mocker):
        """Test is_order_filled convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        # Mock order query to return filled order
        filled_order = {
            "Orders": [
                {
                    "OrderID": "924243071",
                    "Status": "FLL",  # Filled
                }
            ]
        }

        mocker.patch.object(mock_http_client, "make_request", return_value=filled_order)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        is_filled = order_exec.is_order_filled("924243071", mode="PAPER")

        assert is_filled is True


# ============================================================================
# OrderExecutionOperations confirm_order Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsConfirmOrder:
    """Tests for confirm_order method."""

    def test_confirm_order_success(self, mock_http_client, mocker):
        """Test confirm_order performs pre-flight check."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_CONFIRM)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_exec.confirm_order("MNQZ25", "BUY", 2, "Market", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "orderexecution/orderconfirm" in call_args[0][1]
        assert call_args[0][0] == "POST"
        assert result["IsValid"] is True


# ============================================================================
# OrderExecutionOperations Group Orders Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsGroupOrders:
    """Tests for group order methods (OCO, Bracket)."""

    def test_place_group_order_oco(self, mock_http_client, mocker):
        """Test place_group_order with OCO group type."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_GROUP_ORDER_PLACEMENT)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        orders = [
            {"Symbol": "MNQZ25", "TradeAction": "BUY", "Quantity": "2", "OrderType": "Limit", "LimitPrice": "25000"},
            {"Symbol": "MNQZ25", "TradeAction": "SELL", "Quantity": "2", "OrderType": "Limit", "LimitPrice": "25100"},
        ]
        result = order_exec.place_group_order("OCO", orders, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "orderexecution/ordergroups" in call_args[0][1]
        json_data = call_args[1]["json_data"]
        assert json_data["GroupType"] == "OCO"

    def test_place_group_order_bracket(self, mock_http_client, mocker):
        """Test place_group_order with BRK (Bracket) group type."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_GROUP_ORDER_PLACEMENT)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        orders = [
            {"Symbol": "MNQZ25", "TradeAction": "BUY", "Quantity": "2", "OrderType": "Market"},
            {"Symbol": "MNQZ25", "TradeAction": "SELL", "Quantity": "2", "OrderType": "Limit", "LimitPrice": "25100"},
            {"Symbol": "MNQZ25", "TradeAction": "SELL", "Quantity": "2", "OrderType": "Stop", "StopPrice": "24900"},
        ]
        result = order_exec.place_group_order("BRK", orders, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["GroupType"] == "BRK"

    def test_confirm_group_order(self, mock_http_client, mocker):
        """Test confirm_group_order performs pre-flight check."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_CONFIRM)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        orders = [{"Symbol": "MNQZ25", "TradeAction": "BUY", "Quantity": "2"}]
        result = order_exec.confirm_group_order("OCO", orders, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "orderexecution/ordergroupconfirm" in call_args[0][1]


# ============================================================================
# OrderExecutionOperations Convenience Functions Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsConvenienceFunctions:
    """Tests for convenience order placement functions."""

    def test_place_limit_order(self, mock_http_client, mocker):
        """Test place_limit_order convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_id, status = order_exec.place_limit_order("MNQZ25", "BUY", 2, 25000.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "Limit"
        assert json_data["LimitPrice"] == "25000.0"

    def test_place_stop_order(self, mock_http_client, mocker):
        """Test place_stop_order convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_stop_order("MNQZ25", "BUY", 2, 24900.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "Stop"

    def test_place_stop_limit_order(self, mock_http_client, mocker):
        """Test place_stop_limit_order convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_stop_limit_order("MNQZ25", "BUY", 2, 25000.0, 24900.0, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "StopLimit"

    def test_place_trailing_stop_order(self, mock_http_client, mocker):
        """Test place_trailing_stop_order convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_PLACEMENT_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec.place_trailing_stop_order("MNQZ25", "BUY", 2, trail_amount=1.5, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["OrderType"] == "TrailingStop"

    def test_place_oco_order(self, mock_http_client, mocker):
        """Test place_oco_order convenience function."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_GROUP_ORDER_PLACEMENT)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        orders = [
            {"Symbol": "MNQZ25", "TradeAction": "BUY", "Quantity": "2", "OrderType": "Limit", "LimitPrice": "25000"},
            {"Symbol": "MNQZ25", "TradeAction": "SELL", "Quantity": "2", "OrderType": "Limit", "LimitPrice": "25100"},
        ]
        result = order_exec.place_oco_order(orders, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["GroupType"] == "OCO"

    def test_place_bracket_order(self, mock_http_client, mocker):
        """Test place_bracket_order with profit target and stop-loss."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_GROUP_ORDER_PLACEMENT)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_exec.place_bracket_order(
            "MNQZ25", "BUY", 2, profit_target=25100.0, stop_loss=24900.0, mode="PAPER"
        )

        call_args = mock_http_client.make_request.call_args
        json_data = call_args[1]["json_data"]
        assert json_data["GroupType"] == "BRK"
        # Verify bracket order structure (entry + profit + stop)
        assert len(json_data["Orders"]) == 3


# ============================================================================
# OrderExecutionOperations Other Methods Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.orders
class TestOrderExecutionOperationsOtherMethods:
    """Tests for other OrderExecutionOperations methods."""

    def test_get_activation_triggers(self, mock_http_client, mocker):
        """Test get_activation_triggers returns trigger keys."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ACTIVATION_TRIGGERS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_exec.get_activation_triggers("PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "orderexecution/activationtriggers" in call_args[0][1]
        assert result is not None

    def test_get_routes(self, mock_http_client, mocker):
        """Test get_routes returns routing options."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ROUTES)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        result = order_exec.get_routes("PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "orderexecution/routes" in call_args[0][1]
        assert result is not None

    def test_cancel_all_orders_for_symbol(self, mock_http_client, mocker):
        """Test cancel_all_orders_for_symbol cancels all orders for a symbol."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        # Mock get_current_orders to return orders
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=[
                api_responses.MOCK_CURRENT_ORDERS,  # get_current_orders response
                api_responses.MOCK_ORDER_CANCEL_SUCCESS,  # cancel_order response
            ],
        )

        # Need to mock OrderOperations.get_current_orders
        from src.lib.tradestation.orders import OrderOperations

        mock_order_ops = mocker.MagicMock(spec=OrderOperations)
        mock_order_ops.get_current_orders.return_value = api_responses.MOCK_CURRENT_ORDERS

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec._orders = mock_order_ops  # Inject mock

        result = order_exec.cancel_all_orders_for_symbol("MNQZ25", mode="PAPER")

        # Verify get_current_orders was called
        mock_order_ops.get_current_orders.assert_called_once()
        # Verify cancel_order was called for each order
        assert mock_http_client.make_request.call_count >= 2

    def test_cancel_all_orders(self, mock_http_client, mocker):
        """Test cancel_all_orders cancels all orders."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        from src.lib.tradestation.orders import OrderOperations

        mock_order_ops = mocker.MagicMock(spec=OrderOperations)
        mock_order_ops.get_current_orders.return_value = api_responses.MOCK_CURRENT_ORDERS

        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_ORDER_CANCEL_SUCCESS)

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_exec._orders = mock_order_ops

        result = order_exec.cancel_all_orders(mode="PAPER")

        mock_order_ops.get_current_orders.assert_called_once()

    def test_replace_order(self, mock_http_client, mocker):
        """Test replace_order cancels old and places new order."""
        mock_accounts = mocker.MagicMock()
        mock_accounts.get_account_info.return_value = {"account_id": "SIM123456"}

        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=[
                api_responses.MOCK_ORDER_CANCEL_SUCCESS,  # cancel_order
                api_responses.MOCK_ORDER_PLACEMENT_SUCCESS,  # place_order
            ],
        )

        order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")
        order_id, status = order_exec.replace_order(
            "924243070", "MNQZ25", "BUY", 3, "Limit", limit_price=25010.0, mode="PAPER"
        )

        # Verify both cancel and place were called
        assert mock_http_client.make_request.call_count == 2
        # First call should be DELETE (cancel)
        assert mock_http_client.make_request.call_args_list[0][0][0] == "DELETE"
        # Second call should be POST (place)
        assert mock_http_client.make_request.call_args_list[1][0][0] == "POST"

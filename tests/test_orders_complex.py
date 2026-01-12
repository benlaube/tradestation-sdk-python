import pytest

from tradestation.models.orders import OSO, Bracket, TradeStationOrderRequest


@pytest.mark.unit
class TestComplexOrders:
    def test_oso_order_structure(self):
        """Test creating an OSO (Order Sends Order)."""
        # Parent order
        parent = TradeStationOrderRequest(
            AccountID="SIM123", Symbol="AAPL", Quantity="10", OrderType="Market", TradeAction="BUY", Route="Intelligent"
        )

        # Child order
        child = TradeStationOrderRequest(
            AccountID="SIM123",
            Symbol="AAPL",
            Quantity="10",
            OrderType="Limit",
            LimitPrice="160.00",
            TradeAction="SELL",
            Route="Intelligent",
        )

        # OSO structure
        oso = OSO(Type="OSO", Orders=[parent, child])

        assert len(oso.Orders) == 2
        assert oso.Orders[0].TradeAction == "BUY"
        assert oso.Orders[1].TradeAction == "SELL"

    def test_bracket_order_structure(self):
        """Test creating a Bracket order."""
        # Parent
        parent = TradeStationOrderRequest(
            AccountID="SIM123", Symbol="ESZ25", Quantity="1", OrderType="Market", TradeAction="BUY", Route="Intelligent"
        )

        # Stop Loss
        stop = TradeStationOrderRequest(
            AccountID="SIM123",
            Symbol="ESZ25",
            Quantity="1",
            OrderType="StopMarket",
            StopPrice="4000.00",
            TradeAction="SELL",
            Route="Intelligent",
        )

        # Take Profit
        limit = TradeStationOrderRequest(
            AccountID="SIM123",
            Symbol="ESZ25",
            Quantity="1",
            OrderType="Limit",
            LimitPrice="4200.00",
            TradeAction="SELL",
            Route="Intelligent",
        )

        bracket = Bracket(Type="Brk", Orders=[parent, stop, limit])

        assert len(bracket.Orders) == 3
        # Verify order types
        types = [o.OrderType for o in bracket.Orders]
        assert "Market" in types
        assert "StopMarket" in types
        assert "Limit" in types

    def test_complex_order_validation(self):
        """Test that complex orders require at least 2 orders."""
        with pytest.raises(ValueError):
            OSO(Type="OSO", Orders=[])

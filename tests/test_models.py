import pytest
from pydantic import ValidationError

from tradestation.models.accounts import AccountSummary
from tradestation.models.orders import TradeStationOrderRequest, TradeStationTimeActivationRule
from tradestation.models.streaming import QuoteStream


@pytest.mark.unit
class TestOrderModels:
    def test_order_request_validation_success(self):
        """Test valid order request creation."""
        order = TradeStationOrderRequest(
            AccountID="SIM123", Symbol="AAPL", Quantity="10", OrderType="Market", TradeAction="BUY", Route="Intelligent"
        )
        assert order.AccountID == "SIM123"
        assert order.Quantity == "10"

    def test_order_request_validation_missing_fields(self):
        """Test validation fails when required fields are missing."""
        with pytest.raises(ValidationError):
            TradeStationOrderRequest(AccountID="SIM123")  # Missing Symbol, Quantity, etc.

    def test_time_activation_rule(self):
        """Test TimeActivationRule serialization."""
        rule = TradeStationTimeActivationRule(TimeUtc="2023-01-01T10:00:00Z")
        assert rule.TimeUtc == "2023-01-01T10:00:00Z"


@pytest.mark.unit
class TestAccountModels:
    def test_account_model(self):
        """Test Account model."""
        acc = AccountSummary(AccountID="123", AccountType="Cash", Currency="USD")
        assert acc.AccountID == "123"


@pytest.mark.unit
class TestStreamingModels:
    def test_quote_stream_parsing(self):
        """Test parsing of quote stream data."""
        data = {"Symbol": "AAPL", "Last": "150.0", "Bid": "149.9", "Ask": "150.1"}
        # Verify model instantiation
        quote = QuoteStream(**data)
        assert quote.Symbol == "AAPL"
        assert quote.Last == "150.0"

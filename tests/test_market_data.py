"""
MarketDataOperations Unit Tests

Tests for MarketDataOperations class including historical bars, symbol search, quotes, and streaming.
"""

import pytest
from tradestation.exceptions import ErrorDetails, TradeStationAPIError
from tradestation.market_data import MarketDataOperations

from .fixtures import api_responses

# ============================================================================
# MarketDataOperations get_bars Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.market_data
class TestMarketDataOperationsGetBars:
    """Tests for get_bars method."""

    def test_get_bars_success(self, mock_http_client, mocker):
        """Test get_bars returns historical bar data."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_BARS_RESPONSE
        )

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_bars("MNQZ25", "1", "Minute", bars_back=200, mode="PAPER")

        # Verify endpoint was called
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "marketdata/barcharts/MNQZ25" in call_args[0][1]
        assert call_args[1]["params"]["interval"] == "1"
        assert call_args[1]["params"]["unit"] == "Minute"
        assert call_args[1]["params"]["barsback"] == 200

        # Verify result structure
        assert isinstance(result, list)
        assert len(result) == 2
        assert "Time" in result[0]
        assert "Open" in result[0]

    def test_get_bars_interval_unit_parameters(self, mock_http_client, mocker):
        """Test get_bars handles interval and unit parameters correctly."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_BARS_RESPONSE)

        market_data = MarketDataOperations(mock_http_client)
        market_data.get_bars("MNQZ25", "5", "Minute", bars_back=100, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert call_args[1]["params"]["interval"] == "5"
        assert call_args[1]["params"]["unit"] == "Minute"

    def test_get_bars_bars_back_vs_dates(self, mock_http_client, mocker):
        """Test get_bars uses bars_back vs start_date/end_date correctly."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_BARS_RESPONSE)

        market_data = MarketDataOperations(mock_http_client)

        # Test with bars_back
        market_data.get_bars("MNQZ25", "1", "Minute", bars_back=100, mode="PAPER")
        call1 = mock_http_client.make_request.call_args
        assert "barsback" in call1[1]["params"]
        assert "firstDate" not in call1[1]["params"]

        # Test with start_date/end_date
        market_data.get_bars(
            "MNQZ25", "1", "Minute", start_date="2025-12-04T09:00:00Z", end_date="2025-12-04T16:00:00Z", mode="PAPER"
        )
        call2 = mock_http_client.make_request.call_args
        assert "firstdate" in call2[1]["params"]
        assert "lastdate" in call2[1]["params"]
        assert "barsback" not in call2[1]["params"]

    def test_get_bars_default_bars_back(self, mock_http_client, mocker):
        """Test get_bars defaults to 200 bars_back when nothing specified."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_BARS_RESPONSE)

        market_data = MarketDataOperations(mock_http_client)
        market_data.get_bars("MNQZ25", "1", "Minute", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert call_args[1]["params"]["barsback"] == 200


# ============================================================================
# MarketDataOperations search_symbols Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.market_data
class TestMarketDataOperationsSearchSymbols:
    """Tests for search_symbols method."""

    def test_search_symbols_success(self, mock_http_client, mocker):
        """Test search_symbols returns matching symbols."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_SYMBOL_SEARCH
        )

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.search_symbols("MNQ", category="Future", mode="PAPER")

        # Verify endpoint was called
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "marketdata/symbols/search" in call_args[0][1]
        assert call_args[1]["params"]["pattern"] == "MNQ"
        assert call_args[1]["params"]["category"] == "Future"

        # Verify result
        assert isinstance(result, list)
        assert len(result) == 2

    def test_search_symbols_pattern_matching(self, mock_http_client, mocker):
        """Test search_symbols pattern matching."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_SYMBOL_SEARCH)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.search_symbols("ES", category="Future", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert call_args[1]["params"]["pattern"] == "ES"

    def test_search_symbols_category_filtering(self, mock_http_client, mocker):
        """Test search_symbols category filtering."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_SYMBOL_SEARCH)

        market_data = MarketDataOperations(mock_http_client)
        market_data.search_symbols("MNQ", category="Future", asset_type="Index", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert call_args[1]["params"]["category"] == "Future"
        assert call_args[1]["params"]["assetType"] == "Index"

    def test_search_symbols_api_error_raises(self, mock_http_client, mocker):
        """Test search_symbols bubbles broker errors instead of returning an empty list."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError(ErrorDetails(message="upstream search failure")),
        )

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.search_symbols("MNQ", category="Future", mode="PAPER")

        assert exc_info.value.details.operation == "search_symbols"


# ============================================================================
# MarketDataOperations get_futures_index_symbols Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.market_data
class TestMarketDataOperationsGetFuturesIndexSymbols:
    """Tests for get_futures_index_symbols method."""

    def test_get_futures_index_symbols_success(self, mock_http_client, mocker):
        """Test get_futures_index_symbols returns futures index symbols."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_SYMBOL_SEARCH
        )

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_futures_index_symbols("PAPER")

        assert mock_request.call_count == 8
        call_args = mock_request.call_args_list[0]
        assert "marketdata/symbols/search" in call_args[0][1]

        # Verify result
        assert isinstance(result, list)

    def test_get_futures_index_symbols_response_parsing(self, mock_http_client, mocker):
        """Test get_futures_index_symbols parses response correctly."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_SYMBOL_SEARCH)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_futures_index_symbols("PAPER")

        # Verify symbols are returned
        assert result is not None

    def test_get_futures_index_symbols_raises_when_all_queries_fail(self, mock_http_client, mocker):
        """Test get_futures_index_symbols raises if every underlying API call fails."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError(ErrorDetails(message="all symbol searches failed")),
        )

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.get_futures_index_symbols("PAPER")

        assert exc_info.value.details.operation == "get_futures_index_symbols"


# ============================================================================
# MarketDataOperations get_quote_snapshots Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.market_data
class TestMarketDataOperationsGetQuoteSnapshots:
    """Tests for get_quote_snapshots method."""

    def test_get_quote_snapshots_single_symbol(self, mock_http_client, mocker):
        """Test get_quote_snapshots with single symbol."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_QUOTE_SNAPSHOT
        )

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_quote_snapshots("MNQZ25", mode="PAPER")

        # Verify endpoint
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "marketdata/quotes/MNQZ25" in call_args[0][1]

        # Verify result
        assert "Quotes" in result or isinstance(result, list)

    def test_get_quote_snapshots_multiple_symbols(self, mock_http_client, mocker):
        """Test get_quote_snapshots with multiple symbols."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_QUOTE_SNAPSHOT)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_quote_snapshots("MNQZ25,ESZ25", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "MNQZ25,ESZ25" in call_args[0][1]

    def test_get_quote_snapshots_response_structure(self, mock_http_client, mocker):
        """Test get_quote_snapshots response structure."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_QUOTE_SNAPSHOT)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_quote_snapshots("MNQZ25", mode="PAPER")

        # Verify quote data structure
        assert result is not None


# ============================================================================
# MarketDataOperations get_symbol_details Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.market_data
class TestMarketDataOperationsGetSymbolDetails:
    """Tests for get_symbol_details method."""

    def test_get_symbol_details_success(self, mock_http_client, mocker):
        """Test get_symbol_details returns symbol details."""
        mock_request = mocker.patch.object(
            mock_http_client, "make_request", return_value=api_responses.MOCK_SYMBOL_DETAILS
        )

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_symbol_details("MNQZ25", mode="PAPER")

        # Verify endpoint
        mock_request.assert_called_once()
        call_args = mock_request.call_args
        assert "marketdata/symbols/MNQZ25" in call_args[0][1]

        # Verify result
        assert "Symbols" in result or isinstance(result, list)

    def test_get_symbol_details_api_error_raises(self, mock_http_client, mocker):
        """Test get_symbol_details bubbles broker errors instead of returning an empty payload."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError(ErrorDetails(message="symbol details unavailable")),
        )

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.get_symbol_details("MNQZ25", mode="PAPER")

        assert exc_info.value.details.operation == "get_symbol_details"

    def test_get_symbol_details_runtime_error_raises_structured_error(self, mock_http_client, mocker):
        """Test get_symbol_details wraps unexpected runtime failures in structured SDK errors."""
        mocker.patch.object(mock_http_client, "make_request", side_effect=RuntimeError("broken parser"))

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.get_symbol_details("MNQZ25", mode="PAPER")

        assert exc_info.value.details.operation == "get_symbol_details"
        assert exc_info.value.details.code == "SDK_RUNTIME_ERROR"


# ============================================================================
# MarketDataOperations Other Methods Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.market_data
class TestMarketDataOperationsOtherMethods:
    """Tests for other MarketDataOperations methods."""

    def test_get_crypto_symbol_names(self, mock_http_client, mocker):
        """Test get_crypto_symbol_names returns crypto symbols."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_CRYPTO_SYMBOLS)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_crypto_symbol_names("PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "marketdata/symbollists/cryptopairs/symbolnames" in call_args[0][1]
        assert result is not None

    def test_get_crypto_symbol_names_api_error_raises(self, mock_http_client, mocker):
        """Test get_crypto_symbol_names fails loud on broker errors."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError(ErrorDetails(message="crypto symbols unavailable")),
        )

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.get_crypto_symbol_names("PAPER")

        assert exc_info.value.details.operation == "get_crypto_symbol_names"

    def test_get_option_expirations(self, mock_http_client, mocker):
        """Test get_option_expirations returns option expirations."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_OPTION_EXPIRATIONS)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_option_expirations("SPY", mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "marketdata/options/expirations/SPY" in call_args[0][1]
        assert result is not None

    def test_get_option_expirations_api_error_raises(self, mock_http_client, mocker):
        """Test get_option_expirations fails loud on broker errors."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError(ErrorDetails(message="expiration query failed")),
        )

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.get_option_expirations("SPY", mode="PAPER")

        assert exc_info.value.details.operation == "get_option_expirations"

    def test_get_option_risk_reward(self, mock_http_client, mocker):
        """Test get_option_risk_reward returns risk/reward data."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_OPTION_RISK_REWARD)

        market_data = MarketDataOperations(mock_http_client)
        request_data = {"Symbol": "SPY", "Strike": 250}
        result = market_data.get_option_risk_reward(request_data, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "marketdata/options/riskreward" in call_args[0][1]
        assert call_args[1]["json_data"] == request_data
        assert result is not None

    def test_get_option_spread_types(self, mock_http_client, mocker):
        """Test get_option_spread_types returns spread types."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_OPTION_SPREAD_TYPES)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_option_spread_types("PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "marketdata/options/spreadtypes" in call_args[0][1]
        assert result is not None

    def test_get_option_spread_types_api_error_raises(self, mock_http_client, mocker):
        """Test get_option_spread_types fails loud on broker errors."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError(ErrorDetails(message="spread types unavailable")),
        )

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.get_option_spread_types("PAPER")

        assert exc_info.value.details.operation == "get_option_spread_types"

    def test_get_option_strikes(self, mock_http_client, mocker):
        """Test get_option_strikes returns option strikes."""
        mocker.patch.object(mock_http_client, "make_request", return_value=api_responses.MOCK_OPTION_STRIKES)

        market_data = MarketDataOperations(mock_http_client)
        result = market_data.get_option_strikes("SPY", "2025-12-19", min_strike=25000, max_strike=25200, mode="PAPER")

        call_args = mock_http_client.make_request.call_args
        assert "marketdata/options/strikes/SPY" in call_args[0][1]
        assert call_args[1]["params"]["expiration"] == "2025-12-19"
        assert result is not None

    def test_get_option_strikes_api_error_raises(self, mock_http_client, mocker):
        """Test get_option_strikes fails loud on broker errors."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError(ErrorDetails(message="strike lookup failed")),
        )

        market_data = MarketDataOperations(mock_http_client)

        with pytest.raises(TradeStationAPIError) as exc_info:
            market_data.get_option_strikes("SPY", "2025-12-19", mode="PAPER")

        assert exc_info.value.details.operation == "get_option_strikes"

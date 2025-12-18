"""
StreamingManager Unit Tests

Tests for StreamingManager class including HTTP streaming for quotes, orders, positions, and balances.
Note: Tests use mocked HTTP streaming responses (newline-delimited JSON).
"""

import json

import pytest
from src.lib.tradestation.streaming import StreamingManager

from .fixtures import api_responses

# ============================================================================
# StreamingManager stream_quotes Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.streaming
@pytest.mark.slow
class TestStreamingManagerStreamQuotes:
    """Tests for stream_quotes method."""

    @pytest.mark.asyncio
    async def test_stream_quotes_success(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_quotes returns quote stream data."""
        # Mock stream_data to yield quote data
        mock_stream_data = [
            json.loads(api_responses.MOCK_STREAM_QUOTE.strip()),
            json.loads(api_responses.MOCK_STREAM_STATUS_END.strip()),
        ]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_stream_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        # Collect stream items
        quotes = []
        async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER"):
            quotes.append(quote)
            if len(quotes) >= 1:  # Limit to prevent infinite loop
                break

        # Verify quotes were received
        assert len(quotes) > 0
        if quotes:
            assert "Symbol" in quotes[0] or "Type" in quotes[0]

    @pytest.mark.asyncio
    async def test_stream_quotes_endpoint(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_quotes calls correct endpoint."""
        mock_stream = mocker.patch.object(
            mock_http_client,
            "stream_data",
            return_value=iter([json.loads(api_responses.MOCK_STREAM_STATUS_END.strip())]),
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        async for _ in streaming.stream_quotes("MNQZ25", mode="PAPER"):
            break

        # Verify endpoint was called
        mock_stream.assert_called_once()
        call_args = mock_stream.call_args
        assert "marketdata/stream/quotes/MNQZ25" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_stream_quotes_multiple_symbols(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_quotes with multiple symbols."""
        mocker.patch.object(
            mock_http_client,
            "stream_data",
            return_value=iter([json.loads(api_responses.MOCK_STREAM_STATUS_END.strip())]),
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        async for _ in streaming.stream_quotes("MNQZ25,ESZ25", mode="PAPER"):
            break

        call_args = mock_http_client.stream_data.call_args
        assert "MNQZ25,ESZ25" in call_args[0][1]

    @pytest.mark.asyncio
    async def test_stream_quotes_handles_stream_status(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_quotes handles StreamStatus messages."""
        mock_data = [
            json.loads(api_responses.MOCK_STREAM_QUOTE.strip()),
            json.loads(api_responses.MOCK_STREAM_STATUS_END.strip()),
        ]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        quotes = []
        async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER"):
            quotes.append(quote)
            if len(quotes) >= 1:
                break

        # Should receive quote data, not StreamStatus
        assert len(quotes) > 0


# ============================================================================
# StreamingManager stream_orders Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.streaming
@pytest.mark.slow
class TestStreamingManagerStreamOrders:
    """Tests for stream_orders method."""

    @pytest.mark.asyncio
    async def test_stream_orders_success(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_orders returns order stream data."""
        mock_data = [
            json.loads(api_responses.MOCK_STREAM_ORDER.strip()),
            json.loads(api_responses.MOCK_STREAM_STATUS_END.strip()),
        ]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        orders = []
        async for order in streaming.stream_orders("SIM123456", mode="PAPER"):
            orders.append(order)
            if len(orders) >= 1:
                break

        assert len(orders) > 0

    @pytest.mark.asyncio
    async def test_stream_orders_endpoint(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_orders calls correct endpoint."""
        mocker.patch.object(
            mock_http_client,
            "stream_data",
            return_value=iter([json.loads(api_responses.MOCK_STREAM_STATUS_END.strip())]),
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        async for _ in streaming.stream_orders("SIM123456", mode="PAPER"):
            break

        call_args = mock_http_client.stream_data.call_args
        assert "brokerage/stream/accounts/SIM123456/orders" in call_args[0][1]


# ============================================================================
# StreamingManager stream_positions Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.streaming
@pytest.mark.slow
class TestStreamingManagerStreamPositions:
    """Tests for stream_positions method."""

    @pytest.mark.asyncio
    async def test_stream_positions_success(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_positions returns position stream data."""
        mock_data = [
            json.loads(api_responses.MOCK_STREAM_POSITION.strip()),
            json.loads(api_responses.MOCK_STREAM_STATUS_END.strip()),
        ]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        positions = []
        async for position in streaming.stream_positions("SIM123456", mode="PAPER"):
            positions.append(position)
            if len(positions) >= 1:
                break

        assert len(positions) > 0

    @pytest.mark.asyncio
    async def test_stream_positions_endpoint(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_positions calls correct endpoint."""
        mocker.patch.object(
            mock_http_client,
            "stream_data",
            return_value=iter([json.loads(api_responses.MOCK_STREAM_STATUS_END.strip())]),
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        async for _ in streaming.stream_positions("SIM123456", mode="PAPER"):
            break

        call_args = mock_http_client.stream_data.call_args
        assert "brokerage/stream/accounts/SIM123456/positions" in call_args[0][1]


# ============================================================================
# StreamingManager stream_balances Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.streaming
@pytest.mark.slow
class TestStreamingManagerStreamBalances:
    """Tests for stream_balances method."""

    @pytest.mark.asyncio
    async def test_stream_balances_success(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_balances returns balance stream data."""
        mock_data = [
            json.loads(api_responses.MOCK_STREAM_BALANCE.strip()),
            json.loads(api_responses.MOCK_STREAM_STATUS_END.strip()),
        ]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        balances = []
        async for balance in streaming.stream_balances("SIM123456", mode="PAPER"):
            balances.append(balance)
            if len(balances) >= 1:
                break

        assert len(balances) > 0

    @pytest.mark.asyncio
    async def test_stream_balances_endpoint(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_balances calls correct endpoint."""
        mocker.patch.object(
            mock_http_client,
            "stream_data",
            return_value=iter([json.loads(api_responses.MOCK_STREAM_STATUS_END.strip())]),
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        async for _ in streaming.stream_balances("SIM123456", mode="PAPER"):
            break

        call_args = mock_http_client.stream_data.call_args
        assert "brokerage/stream/accounts/SIM123456/balances" in call_args[0][1]


# ============================================================================
# StreamingManager stream_orders_by_ids Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.streaming
@pytest.mark.slow
class TestStreamingManagerStreamOrdersByIds:
    """Tests for stream_orders_by_ids method."""

    @pytest.mark.asyncio
    async def test_stream_orders_by_ids_success(self, mock_token_manager, mock_http_client, mocker):
        """Test stream_orders_by_ids returns order stream for specific orders."""
        mocker.patch.object(
            mock_http_client,
            "stream_data",
            return_value=iter([json.loads(api_responses.MOCK_STREAM_STATUS_END.strip())]),
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        async for _ in streaming.stream_orders_by_ids("SIM123456", "924243071,924243072", mode="PAPER"):
            break

        call_args = mock_http_client.stream_data.call_args
        assert "brokerage/stream/accounts/SIM123456/orders" in call_args[0][1]
        assert "924243071,924243072" in call_args[1]["params"]["ordersIds"] or "924243071,924243072" in str(
            call_args[1]
        )


# ============================================================================
# StreamingManager Error Handling Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.streaming
class TestStreamingManagerErrorHandling:
    """Tests for error handling in streaming methods."""

    @pytest.mark.asyncio
    async def test_stream_handles_goaway_status(self, mock_token_manager, mock_http_client, mocker):
        """Test stream handles GoAway status message."""
        mock_data = [json.loads(api_responses.MOCK_STREAM_STATUS_GOAWAY.strip())]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        quotes = []
        async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER"):
            quotes.append(quote)
            break

        # GoAway should cause stream to end
        assert len(quotes) == 0

    @pytest.mark.asyncio
    async def test_stream_handles_error_status(self, mock_token_manager, mock_http_client, mocker):
        """Test stream handles error status message."""
        mock_data = [json.loads(api_responses.MOCK_STREAM_ERROR.strip())]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        # Should raise exception on error
        with pytest.raises(Exception):
            async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER"):
                break

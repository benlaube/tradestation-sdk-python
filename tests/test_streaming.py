"""
StreamingManager Unit Tests

Tests for StreamingManager class including HTTP streaming for quotes, orders, positions, and balances.
Note: Tests use mocked HTTP streaming responses (newline-delimited JSON).
"""

import asyncio
import json
import logging
import time

import pytest
import requests

from tradestation.exceptions import NonRecoverableError, StreamGoAwayError
from tradestation.models.streaming import QuoteStream
from tradestation.streaming import StreamingManager

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
            assert quotes[0].Symbol == "MNQZ25"

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
        assert "marketdata/stream/quotes/MNQZ25" in call_args[0][0]

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
        assert "MNQZ25,ESZ25" in call_args[0][0]

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

    @pytest.mark.asyncio
    async def test_stream_quotes_validation_failure_raises(self, mock_token_manager, mock_http_client, mocker):
        """Test malformed quote payloads raise instead of being swallowed."""
        mock_data = [{"Symbol": "MNQZ25", "Bid": "25000.0", "UnexpectedField": "boom"}]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        with pytest.raises(Exception):
            async for _ in streaming.stream_quotes("MNQZ25", mode="PAPER"):
                break

    @pytest.mark.asyncio
    async def test_stream_quotes_falls_back_only_for_recoverable_errors(
        self, mock_token_manager, mock_http_client, mocker, caplog
    ):
        """Test quote streaming only falls back to REST polling for recoverable transport failures."""

        async def raise_stream_error(*args, **kwargs):
            if False:
                yield None
            raise requests.exceptions.ConnectionError("stream socket closed")

        async def poll_once(*args, **kwargs):
            yield QuoteStream.model_validate(json.loads(api_responses.MOCK_STREAM_QUOTE.strip()))

        caplog.set_level(logging.WARNING, logger="tradestation.streaming")
        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)
        mocker.patch.object(streaming, "_stream_quotes_internal", side_effect=raise_stream_error)
        mock_poll = mocker.patch.object(streaming, "_poll_quotes_rest", side_effect=poll_once)

        quotes = []
        async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER"):
            quotes.append(quote)
            break

        assert len(quotes) == 1
        assert quotes[0].Symbol == "MNQZ25"
        assert mock_poll.call_count == 1
        assert "falling back to REST polling" in caplog.text

    @pytest.mark.asyncio
    async def test_stream_quotes_unexpected_errors_do_not_fallback(self, mock_token_manager, mock_http_client, mocker):
        """Test unexpected programming/runtime failures bubble instead of degrading to polling."""

        async def raise_programming_error(*args, **kwargs):
            if False:
                yield None
            raise RuntimeError("unexpected quote parser bug")

        async def poll_once(*args, **kwargs):
            yield QuoteStream.model_validate(json.loads(api_responses.MOCK_STREAM_QUOTE.strip()))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)
        mocker.patch.object(streaming, "_stream_quotes_internal", side_effect=raise_programming_error)
        mock_poll = mocker.patch.object(streaming, "_poll_quotes_rest", side_effect=poll_once)

        with pytest.raises(RuntimeError):
            async for _ in streaming.stream_quotes("MNQZ25", mode="PAPER"):
                break

        assert mock_poll.call_count == 0

    @pytest.mark.asyncio
    async def test_stream_quotes_reconnects_after_goaway_error_payload(
        self, mock_token_manager, mock_http_client, mocker
    ):
        """Test Error=GoAway payloads reconnect instead of being validated as quotes."""
        mocker.patch.object(
            mock_http_client,
            "stream_data",
            side_effect=[
                iter([json.loads(api_responses.MOCK_STREAM_ERROR_GOAWAY.strip())]),
                iter(
                    [
                        json.loads(api_responses.MOCK_STREAM_QUOTE.strip()),
                        json.loads(api_responses.MOCK_STREAM_STATUS_END.strip()),
                    ]
                ),
            ],
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        quotes = []
        async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER", max_retries=2, retry_delay=0):
            quotes.append(quote)
            break

        assert len(quotes) == 1
        assert quotes[0].Symbol == "MNQZ25"
        assert mock_http_client.stream_data.call_count == 2


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
        assert orders[0].OrderID == "924243071"

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
        assert "brokerage/stream/accounts/SIM123456/orders" in call_args[0][0]

    @pytest.mark.asyncio
    async def test_stream_orders_logs_background_worker_failures(
        self, mock_token_manager, mock_http_client, mocker, caplog
    ):
        """Test background-thread order stream failures are logged with context before bubbling."""
        mocker.patch.object(mock_http_client, "stream_data", side_effect=RuntimeError("worker exploded"))
        caplog.set_level(logging.ERROR, logger="tradestation.streaming")

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        with pytest.raises(RuntimeError):
            async for _ in streaming.stream_orders("SIM123456", mode="PAPER", fallback_to_polling=False):
                break

        assert "Order stream worker failed" in caplog.text


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
        assert positions[0].Symbol == "MNQZ25"

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
        assert "brokerage/stream/accounts/SIM123456/positions" in call_args[0][0]


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
        assert balances[0].AccountID == "SIM123456"

    @pytest.mark.asyncio
    async def test_stream_balances_accepts_futures_fields(self, mock_token_manager, mock_http_client, mocker):
        """Test PAPER futures balance stream fields do not break validation."""
        mock_data = [
            {
                "AccountID": "SIM123456",
                "AccountType": "Futures",
                "Equity": "100000.00",
                "MarketValue": "0",
                "UnclearedDeposit": "0",
                "BalanceDetail": {"InitialMargin": "0"},
                "CurrencyDetails": [{"Currency": "USD", "ConversionRate": "1"}],
                "Commission": "0",
            },
            json.loads(api_responses.MOCK_STREAM_STATUS_END.strip()),
        ]
        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        balances = []
        async for balance in streaming.stream_balances("SIM123456", mode="PAPER"):
            balances.append(balance)
            if len(balances) >= 1:
                break

        assert balances[0].AccountType == "Futures"
        assert balances[0].CurrencyDetails == [{"Currency": "USD", "ConversionRate": "1"}]

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
        assert "brokerage/stream/accounts/SIM123456/balances" in call_args[0][0]


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
        assert "brokerage/stream/accounts/SIM123456/orders" in call_args[0][0]
        assert "924243071,924243072" in call_args[0][0]


# ============================================================================
# StreamingManager Error Handling Tests
# ============================================================================


@pytest.mark.unit
@pytest.mark.streaming
class TestStreamingManagerErrorHandling:
    """Tests for error handling in streaming methods."""

    @pytest.mark.asyncio
    async def test_stream_queue_wait_does_not_block_event_loop(self, mock_token_manager, mock_http_client, mocker):
        """Test empty stream queues wait off the event loop while the worker is delayed."""

        def delayed_stream():
            time.sleep(0.25)
            yield json.loads(api_responses.MOCK_STREAM_STATUS_GOAWAY.strip())

        mocker.patch.object(mock_http_client, "stream_data", return_value=delayed_stream())
        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)
        ticks = 0

        async def consume_stream():
            async for _ in streaming.stream_quotes("MNQZ25", mode="PAPER", retry_delay=0):
                pass

        async def heartbeat():
            nonlocal ticks
            deadline = asyncio.get_running_loop().time() + 0.05
            while asyncio.get_running_loop().time() < deadline:
                ticks += 1
                await asyncio.sleep(0.005)

        await asyncio.gather(consume_stream(), heartbeat())

        assert ticks > 1

    @pytest.mark.asyncio
    async def test_stream_handles_goaway_status(self, mock_token_manager, mock_http_client, mocker):
        """Test stream handles GoAway status message."""
        mock_data = [json.loads(api_responses.MOCK_STREAM_STATUS_GOAWAY.strip())]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        quotes = []
        async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER", retry_delay=0):
            quotes.append(quote)
            break

        # GoAway should reconnect and the exhausted test stream then ends cleanly.
        assert len(quotes) == 0

    @pytest.mark.asyncio
    @pytest.mark.parametrize(
        ("method_name", "args"),
        [
            ("_stream_quotes_internal", (["MNQZ25"], "PAPER")),
            ("_stream_orders_internal", ("SIM123456", "PAPER")),
            ("_stream_positions_internal", ("SIM123456", "PAPER")),
            ("_stream_balances_internal", ("SIM123456", "PAPER")),
            ("_stream_orders_by_ids_internal", ("SIM123456", "924243071", "PAPER")),
        ],
    )
    async def test_stream_goaway_error_payload_raises_recoverable_before_validation(
        self, method_name, args, mock_token_manager, mock_http_client, mocker
    ):
        """Test Error=GoAway control payloads are typed as recoverable stream errors."""
        mocker.patch.object(
            mock_http_client,
            "stream_data",
            return_value=iter([json.loads(api_responses.MOCK_STREAM_ERROR_GOAWAY.strip())]),
        )

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        with pytest.raises(StreamGoAwayError) as exc_info:
            async for _ in getattr(streaming, method_name)(*args):
                break

        assert exc_info.value.details.code == "STREAM_GOAWAY"
        assert exc_info.value.details.api_error_code == "GoAway"

    @pytest.mark.asyncio
    async def test_stream_handles_error_status(self, mock_token_manager, mock_http_client, mocker):
        """Test stream handles error status message."""
        mock_data = [json.loads(api_responses.MOCK_STREAM_ERROR.strip())]

        mocker.patch.object(mock_http_client, "stream_data", return_value=iter(mock_data))

        streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

        # Should raise exception on error
        with pytest.raises(NonRecoverableError):
            async for quote in streaming.stream_quotes("MNQZ25", mode="PAPER"):
                break

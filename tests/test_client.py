"""
HTTPClient Unit Tests

Tests for HTTPClient class including request/response logging, error handling, and mode support.
"""

import json
from unittest.mock import MagicMock

import pytest
import requests
from tradestation.client import get_base_url, parse_api_error_response
from tradestation.exceptions import (
    NonRecoverableError,
    RecoverableError,
)

from .fixtures import api_responses

# ============================================================================
# get_base_url Tests
# ============================================================================


@pytest.mark.unit
class TestGetBaseURL:
    """Tests for get_base_url function."""

    def test_get_base_url_paper(self, mocker):
        """Test get_base_url returns PAPER URL for PAPER mode."""
        mocker.patch("tradestation.client.sdk_config.trading_mode", "PAPER")
        url = get_base_url("PAPER")
        assert url == "https://sim-api.tradestation.com/v3"

    def test_get_base_url_live(self, mocker):
        """Test get_base_url returns LIVE URL for LIVE mode."""
        mocker.patch("tradestation.client.sdk_config.trading_mode", "LIVE")
        url = get_base_url("LIVE")
        assert url == "https://api.tradestation.com/v3"

    def test_get_base_url_default(self, mocker):
        """Test get_base_url uses secrets.trading_mode when mode is None."""
        mocker.patch("tradestation.client.sdk_config.trading_mode", "PAPER")
        url = get_base_url(None)
        assert url == "https://sim-api.tradestation.com/v3"


# ============================================================================
# parse_api_error_response Tests
# ============================================================================


@pytest.mark.unit
class TestParseAPIErrorResponse:
    """Tests for parse_api_error_response function."""

    def test_parse_error_format1(self):
        """Test parsing TradeStation error format: {"Error": "...", "Code": "..."}."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"Error": "Invalid symbol", "Code": "INVALID_SYMBOL"}

        details = parse_api_error_response(mock_response)
        assert details.api_error_code == "INVALID_SYMBOL"
        assert details.api_error_message == "Invalid symbol"
        assert details.message == "Invalid symbol"

    def test_parse_error_format2(self):
        """Test parsing errors array format: {"Errors": [...]}."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"Errors": [{"Error": "Invalid request", "Code": "INVALID_REQUEST"}]}

        details = parse_api_error_response(mock_response)
        assert details.api_error_code == "INVALID_REQUEST"
        assert details.api_error_message == "Invalid request"

    def test_parse_error_format3(self):
        """Test parsing Message format: {"Message": "..."}."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"Message": "Bad request"}

        details = parse_api_error_response(mock_response)
        assert details.message == "Bad request"
        assert details.api_error_message == "Bad request"

    def test_parse_oauth_error(self):
        """Test parsing OAuth error format: {"error": "...", "error_description": "..."}."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {
            "error": "invalid_grant",
            "error_description": "The provided authorization code is invalid",
        }

        details = parse_api_error_response(mock_response)
        assert details.api_error_code == "invalid_grant"
        assert details.api_error_message == "The provided authorization code is invalid"

    def test_parse_non_json_error(self):
        """Test parsing non-JSON error response."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_response.text = "Internal Server Error"

        details = parse_api_error_response(mock_response)
        assert details.message == "Internal Server Error"

    def test_parse_error_sets_code_from_status(self):
        """Test that error code is set from status code when not in response."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = {}

        details = parse_api_error_response(mock_response)
        # parse_api_error_response maps 401 to "AUTHENTICATION_ERROR", not "HTTP_401"
        assert details.code == "AUTHENTICATION_ERROR"
        assert details.api_error_code is None


# ============================================================================
# HTTPClient Request Logging Tests
# ============================================================================


@pytest.mark.unit
class TestHTTPClientRequestLogging:
    """Tests for HTTPClient request logging."""

    def test_log_request_basic(self, mock_http_client, mocker):
        """Test _log_request logs method, endpoint, params, body."""
        # Mock log_with_context to verify it's called correctly
        mock_log = mocker.patch("tradestation.client.log_with_context")

        mock_http_client._log_request("GET", "/v3/brokerage/accounts", {"key": "value"}, None)

        # Verify log_with_context was called
        assert mock_log.called
        call_args = mock_log.call_args
        assert call_args[0][2]  # message argument
        assert "API Request: GET /v3/brokerage/accounts" in call_args[0][2]
        assert "Params: {'key': 'value'}" in call_args[0][2]

    def test_log_request_sanitizes_tokens(self, mock_http_client, mocker):
        """Test _log_request sanitizes sensitive data (tokens, secrets)."""
        mock_log = mocker.patch("tradestation.client.log_with_context")

        sensitive_data = {
            "access_token": "secret_token_123",
            "refresh_token": "refresh_secret",
            "client_secret": "client_secret_value",
        }
        mock_http_client._log_request("POST", "/v3/oauth/token", None, sensitive_data)

        # Verify log_with_context was called
        assert mock_log.called
        call_args = mock_log.call_args
        log_message = call_args[0][2]

        assert "secret_token_123" not in log_message
        assert "<redacted>" in log_message

    def test_log_request_truncates_body_when_full_logging_disabled(self, mock_http_client, mocker):
        """Test _log_request truncates body when enable_full_logging=False."""
        mock_log = mocker.patch("tradestation.client.log_with_context")

        long_body = {"data": "x" * 1000}
        mock_http_client._log_request("POST", "/v3/endpoint", None, long_body)

        assert mock_log.called
        call_args = mock_log.call_args
        log_message = call_args[0][2]

        assert "... (truncated)" in log_message

    def test_log_request_full_body_when_full_logging_enabled(self, mock_http_client_full_logging, mocker):
        """Test _log_request logs full body when enable_full_logging=True."""
        mock_log = mocker.patch("tradestation.client.log_with_context")

        long_body = {"data": "x" * 1000}
        mock_http_client_full_logging._log_request("POST", "/v3/endpoint", None, long_body)

        assert mock_log.called
        call_args = mock_log.call_args
        log_message = call_args[0][2]

        assert "... (truncated)" not in log_message
        assert "x" * 1000 in log_message


# ============================================================================
# HTTPClient Response Logging Tests
# ============================================================================


@pytest.mark.unit
class TestHTTPClientResponseLogging:
    """Tests for HTTPClient response logging."""

    def test_log_response_basic(self, mock_http_client, mocker):
        """Test _log_response logs status, time, size, body."""
        mock_log = mocker.patch("tradestation.client.log_with_context")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = '{"result": "success"}'
        mock_response.content = b'{"result": "success"}'
        mock_response.json.return_value = {"result": "success"}

        mock_http_client._log_response("GET", "/v3/brokerage/accounts", mock_response, 0.123)

        assert mock_log.called
        call_args = mock_log.call_args
        log_message = call_args[0][2]

        assert "API Response: GET /v3/brokerage/accounts" in log_message
        assert "Status: 200" in log_message
        assert "Time: 0.123" in log_message

    def test_log_response_error_at_warning_level(self, mock_http_client, mocker):
        """Test _log_response logs errors at WARNING level."""
        mock_log = mocker.patch("tradestation.client.log_with_context")

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"Error": "Bad request"}'
        mock_response.content = b'{"Error": "Bad request"}'
        mock_response.json.return_value = {"Error": "Bad request"}

        mock_http_client._log_response("GET", "/v3/endpoint", mock_response, 0.123)

        # Verify log_with_context was called multiple times (debug + warning)
        assert mock_log.call_count >= 2

        # Check that warning-level log was called
        warning_calls = [call for call in mock_log.call_args_list if call[0][1] == "warning"]
        assert len(warning_calls) > 0
        assert "API Error Response" in warning_calls[0][0][2]

    def test_log_response_truncates_body_when_full_logging_disabled(self, mock_http_client, mocker):
        """Test _log_response truncates body when enable_full_logging=False."""
        mock_log = mocker.patch("tradestation.client.log_with_context")

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.text = "x" * 1000
        mock_response.content = b"x" * 1000
        mock_response.json.side_effect = ValueError("Not JSON")

        mock_http_client._log_response("GET", "/v3/endpoint", mock_response, 0.123)

        assert mock_log.called
        call_args = mock_log.call_args
        log_message = call_args[0][2]

        assert "... (truncated)" in log_message


# ============================================================================
# HTTPClient Request Execution Tests
# ============================================================================


@pytest.mark.unit
class TestHTTPClientRequestExecution:
    """Tests for HTTPClient make_request method."""

    def test_make_request_calls_correct_endpoint(self, mock_http_client, mocker):
        """Test make_request calls correct endpoint with correct method."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_response.text = '{"result": "success"}'
        mock_response.content = b'{"result": "success"}'
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        result = mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        # Verify request was called
        assert mock_request.called

        # Verify method and URL
        call_args = mock_request.call_args
        assert call_args[0][0] == "GET"
        assert "brokerage/accounts" in call_args[0][1]
        assert "sim-api.tradestation.com" in call_args[0][1]

    def test_make_request_includes_authorization_header(self, mock_http_client, mocker):
        """Test make_request includes Authorization token in headers."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        # Verify Authorization header
        call_args = mock_request.call_args
        headers = call_args[1]["headers"]
        assert "Authorization" in headers
        assert "Bearer" in headers["Authorization"]

    def test_make_request_passes_query_parameters(self, mock_http_client, mocker):
        """Test make_request passes query parameters correctly."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        params = {"symbol": "MNQZ25", "interval": "1"}
        mock_http_client.make_request("GET", "marketdata/barcharts/MNQZ25", params=params, mode="PAPER")

        # Verify params were passed
        call_args = mock_request.call_args
        assert call_args[1]["params"] == params

    def test_make_request_sends_json_body_for_post(self, mock_http_client, mocker):
        """Test make_request sends JSON body for POST requests."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"OrderID": "123"}
        mock_response.text = '{"OrderID": "123"}'
        mock_response.content = b'{"OrderID": "123"}'
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        json_data = {"Symbol": "MNQZ25", "Quantity": "2"}
        mock_http_client.make_request("POST", "orderexecution/orders", json_data=json_data, mode="PAPER")

        # Verify JSON body was sent
        call_args = mock_request.call_args
        assert call_args[1]["json"] == json_data

    def test_make_request_timeout_for_order_operations(self, mock_http_client, mocker):
        """Test make_request uses 30s timeout for order operations."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("POST", "orderexecution/orders", json_data={}, mode="PAPER")

        # Verify timeout is 30 seconds for order operations
        call_args = mock_request.call_args
        assert call_args[1]["timeout"] == 30

    def test_make_request_timeout_for_non_order_operations(self, mock_http_client, mocker):
        """Test make_request uses 10s timeout for non-order operations."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        # Verify timeout is 10 seconds for non-order operations
        call_args = mock_request.call_args
        assert call_args[1]["timeout"] == 10


# ============================================================================
# HTTPClient Error Handling Tests
# ============================================================================


@pytest.mark.unit
class TestHTTPClientErrorHandling:
    """Tests for HTTPClient error handling."""

    def test_401_error_raises_non_recoverable_error(self, mock_http_client, mocker):
        """Test 401 errors raise NonRecoverableError."""
        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = api_responses.MOCK_ERROR_401
        mock_response.text = json.dumps(api_responses.MOCK_ERROR_401)
        mock_response.content = json.dumps(api_responses.MOCK_ERROR_401).encode()
        mock_response.headers = {"Content-Type": "application/json"}

        mocker.patch("requests.request", return_value=mock_response)

        with pytest.raises(NonRecoverableError):
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

    def test_429_error_raises_recoverable_error(self, mock_http_client, mocker):
        """Test 429 errors raise RecoverableError."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.json.return_value = api_responses.MOCK_ERROR_429
        mock_response.text = json.dumps(api_responses.MOCK_ERROR_429)
        mock_response.content = json.dumps(api_responses.MOCK_ERROR_429).encode()
        mock_response.headers = {"Content-Type": "application/json"}

        mocker.patch("requests.request", return_value=mock_response)

        with pytest.raises(RecoverableError):
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

    def test_400_error_raises_non_recoverable_error(self, mock_http_client, mocker):
        """Test 400 errors raise NonRecoverableError."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = api_responses.MOCK_ERROR_400
        mock_response.text = json.dumps(api_responses.MOCK_ERROR_400)
        mock_response.content = json.dumps(api_responses.MOCK_ERROR_400).encode()
        mock_response.headers = {"Content-Type": "application/json"}

        mocker.patch("requests.request", return_value=mock_response)

        with pytest.raises(NonRecoverableError):
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

    def test_500_error_raises_recoverable_error(self, mock_http_client, mocker):
        """Test 500+ errors raise RecoverableError."""
        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = api_responses.MOCK_ERROR_500
        mock_response.text = json.dumps(api_responses.MOCK_ERROR_500)
        mock_response.content = json.dumps(api_responses.MOCK_ERROR_500).encode()
        mock_response.headers = {"Content-Type": "application/json"}

        mocker.patch("requests.request", return_value=mock_response)

        with pytest.raises(RecoverableError):
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

    def test_network_error_raises_recoverable_error(self, mock_http_client, mocker):
        """Test network errors raise RecoverableError."""
        mocker.patch("requests.request", side_effect=requests.exceptions.ConnectionError("Connection failed"))

        with pytest.raises(RecoverableError):
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

    def test_error_details_populated_correctly(self, mock_http_client, mocker):
        """Test error details are populated correctly in exceptions."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = api_responses.MOCK_ERROR_400
        mock_response.text = json.dumps(api_responses.MOCK_ERROR_400)
        mock_response.content = json.dumps(api_responses.MOCK_ERROR_400).encode()
        mock_response.headers = {"Content-Type": "application/json"}

        mocker.patch("requests.request", return_value=mock_response)

        with pytest.raises(NonRecoverableError) as exc_info:
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        error = exc_info.value
        assert error.details.response_status == 400
        assert error.details.request_method == "GET"
        assert "brokerage/accounts" in error.details.request_endpoint


# ============================================================================
# HTTPClient Mode Support Tests
# ============================================================================


@pytest.mark.unit
class TestHTTPClientModeSupport:
    """Tests for HTTPClient mode support (PAPER/LIVE)."""

    def test_paper_mode_uses_sim_api(self, mock_http_client, mocker):
        """Test PAPER mode uses sim-api.tradestation.com."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        call_args = mock_request.call_args
        url = call_args[0][1]
        assert "sim-api.tradestation.com" in url

    def test_live_mode_uses_api(self, mock_http_client, mocker):
        """Test LIVE mode uses api.tradestation.com."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mock_request = mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="LIVE")

        call_args = mock_request.call_args
        url = call_args[0][1]
        assert "api.tradestation.com" in url
        assert "sim-api" not in url

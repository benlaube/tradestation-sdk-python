"""
Exception Handling Unit Tests

Tests for TradeStation SDK exception types, error details, and error parsing.
"""

import pytest
from tradestation.client import parse_api_error_response
from tradestation.exceptions import (
    AuthenticationError,
    ErrorDetails,
    InvalidRequestError,
    InvalidTokenError,
    NetworkError,
    NonRecoverableError,
    RateLimitError,
    RecoverableError,
    TokenExpiredError,
    TradeStationAPIError,
)

from .fixtures import api_responses

# ============================================================================
# Exception Types Tests
# ============================================================================


@pytest.mark.unit
class TestExceptionTypes:
    """Tests for exception type hierarchy and instantiation."""

    def test_authentication_error_for_401(self):
        """Test AuthenticationError for 401 errors."""
        details = ErrorDetails(code="AUTH_FAILED", message="Unauthorized", response_status=401)
        error = AuthenticationError(details)

        assert isinstance(error, TradeStationAPIError)
        assert isinstance(error, AuthenticationError)
        assert error.details.response_status == 401

    def test_rate_limit_error_for_429(self):
        """Test RateLimitError for 429 errors."""
        details = ErrorDetails(code="RATE_LIMIT", message="Rate limit exceeded", response_status=429)
        error = RateLimitError(details)

        assert isinstance(error, TradeStationAPIError)
        assert isinstance(error, RateLimitError)
        assert error.details.response_status == 429

    def test_invalid_request_error_for_400(self):
        """Test InvalidRequestError for 400 errors."""
        details = ErrorDetails(code="INVALID_REQUEST", message="Bad request", response_status=400)
        error = InvalidRequestError(details)

        assert isinstance(error, TradeStationAPIError)
        assert isinstance(error, InvalidRequestError)

    def test_network_error_for_500(self):
        """Test NetworkError for 500+ errors."""
        details = ErrorDetails(code="SERVER_ERROR", message="Internal server error", response_status=500)
        error = NetworkError(details)

        assert isinstance(error, TradeStationAPIError)
        assert isinstance(error, NetworkError)

    def test_token_expired_error(self):
        """Test TokenExpiredError for expired tokens."""
        details = ErrorDetails(code="TOKEN_EXPIRED", message="Access token has expired")
        error = TokenExpiredError(details)

        assert isinstance(error, AuthenticationError)
        assert isinstance(error, TokenExpiredError)

    def test_invalid_token_error(self):
        """Test InvalidTokenError for invalid tokens."""
        details = ErrorDetails(code="INVALID_TOKEN", message="Invalid or missing token")
        error = InvalidTokenError(details)

        assert isinstance(error, AuthenticationError)
        assert isinstance(error, InvalidTokenError)

    def test_recoverable_error(self):
        """Test RecoverableError for retryable errors."""
        details = ErrorDetails(code="NETWORK_ERROR", message="Connection timeout")
        error = RecoverableError(details)

        assert isinstance(error, TradeStationAPIError)
        assert isinstance(error, RecoverableError)

    def test_non_recoverable_error(self):
        """Test NonRecoverableError for non-retryable errors."""
        details = ErrorDetails(code="AUTH_FAILED", message="Authentication failed")
        error = NonRecoverableError(details)

        assert isinstance(error, TradeStationAPIError)
        assert isinstance(error, NonRecoverableError)


# ============================================================================
# ErrorDetails Tests
# ============================================================================


@pytest.mark.unit
class TestErrorDetails:
    """Tests for ErrorDetails structure and methods."""

    def test_error_details_structure(self):
        """Test ErrorDetails contains all expected fields."""
        details = ErrorDetails(
            code="TEST_ERROR",
            message="Test error message",
            api_error_code="API_123",
            api_error_message="API error message",
            request_method="GET",
            request_endpoint="/v3/brokerage/accounts",
            request_params={"key": "value"},
            request_body={"data": "test"},
            response_status=400,
            response_body={"Error": "Bad request"},
            mode="PAPER",
            operation="get_account_info",
        )

        assert details.code == "TEST_ERROR"
        assert details.message == "Test error message"
        assert details.api_error_code == "API_123"
        assert details.request_method == "GET"
        assert details.mode == "PAPER"
        assert details.operation == "get_account_info"

    def test_to_human_readable(self):
        """Test to_human_readable generates readable error message."""
        details = ErrorDetails(
            code="INVALID_REQUEST",
            message="Invalid symbol",
            api_error_code="INVALID_SYMBOL",
            api_error_message="Symbol not found",
            request_method="GET",
            request_endpoint="/v3/marketdata/barcharts/INVALID",
            response_status=400,
            mode="PAPER",
            operation="get_bars",
        )

        readable = details.to_human_readable()

        assert "Get Bars failed" in readable
        assert "Invalid symbol" in readable
        assert "API Error Code: INVALID_SYMBOL" in readable
        assert "Method: GET" in readable
        assert "Mode: PAPER" in readable

    def test_to_dict(self):
        """Test to_dict serializes error details."""
        details = ErrorDetails(
            code="TEST_ERROR",
            message="Test message",
            api_error_code="API_123",
            request_method="POST",
            response_status=400,
        )

        error_dict = details.to_dict()

        assert isinstance(error_dict, dict)
        assert error_dict["code"] == "TEST_ERROR"
        assert error_dict["message"] == "Test message"
        assert error_dict["api_error_code"] == "API_123"
        assert error_dict["request_method"] == "POST"
        assert error_dict["response_status"] == 400

    def test_sanitize_dict(self):
        """Test _sanitize_dict redacts sensitive data."""
        details = ErrorDetails()
        data = {
            "access_token": "secret_token",
            "refresh_token": "refresh_secret",
            "client_secret": "client_secret_value",
            "normal_field": "normal_value",
        }

        sanitized = details._sanitize_dict(data)

        assert sanitized["access_token"] == "***REDACTED***"
        assert sanitized["refresh_token"] == "***REDACTED***"
        assert sanitized["client_secret"] == "***REDACTED***"
        assert sanitized["normal_field"] == "normal_value"

    def test_sanitize_nested_dict(self):
        """Test _sanitize_dict handles nested dictionaries."""
        details = ErrorDetails()
        data = {
            "request": {"access_token": "secret_token", "data": "normal"},
            "response": {"refresh_token": "refresh_secret"},
        }

        sanitized = details._sanitize_dict(data)

        assert sanitized["request"]["access_token"] == "***REDACTED***"
        assert sanitized["request"]["data"] == "normal"
        assert sanitized["response"]["refresh_token"] == "***REDACTED***"


# ============================================================================
# Error Parsing Tests
# ============================================================================


@pytest.mark.unit
class TestErrorParsing:
    """Tests for parse_api_error_response function."""

    def test_parse_tradestation_error_format(self):
        """Test parsing TradeStation error format: {"Error": "...", "Code": "..."}."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = api_responses.MOCK_ERROR_400

        details = parse_api_error_response(mock_response)

        assert details.api_error_code == "INVALID_REQUEST"
        assert details.api_error_message == "Invalid request"
        assert details.message == "Invalid request"

    def test_parse_errors_array_format(self):
        """Test parsing errors array format: {"Errors": [...]}."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = api_responses.MOCK_ERROR_ARRAY

        details = parse_api_error_response(mock_response)

        assert details.api_error_code == "INVALID_SYMBOL"
        assert details.api_error_message == "Invalid symbol"

    def test_parse_oauth_error_format(self):
        """Test parsing OAuth error format."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 401
        mock_response.json.return_value = api_responses.MOCK_OAUTH_ERROR

        details = parse_api_error_response(mock_response)

        assert details.api_error_code == "invalid_grant"
        assert "invalid" in details.api_error_message.lower()

    def test_parse_generic_error_format(self):
        """Test parsing generic error formats."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.return_value = {"Message": "Server error"}

        details = parse_api_error_response(mock_response)

        assert details.message == "Server error"
        assert details.api_error_message == "Server error"

    def test_parse_non_json_error(self):
        """Test parsing non-JSON error response."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 500
        mock_response.json.side_effect = ValueError("Not JSON")
        mock_response.text = "Internal Server Error"

        details = parse_api_error_response(mock_response)

        assert details.message == "Internal Server Error"
        assert details.api_error_message == "Internal Server Error"

    def test_parse_error_sets_code_from_status(self):
        """Test that error code is set from status code when not in response."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 404
        mock_response.json.return_value = {}

        details = parse_api_error_response(mock_response)

        assert details.code == "NOT_FOUND"
        assert details.api_error_code is None

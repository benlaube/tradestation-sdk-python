"""
Pytest configuration and fixtures for TradeStation SDK tests.

Provides shared fixtures for mocking HTTP requests, tokens, and SDK instances.
"""

import json
from typing import Any
from unittest.mock import MagicMock

import pytest

from tradestation import TradeStationSDK
from tradestation.session import TokenManager
from tradestation.utils.client import HTTPClient

from .fixtures import api_responses, mock_requests

# ============================================================================
# Token Manager Fixtures
# ============================================================================


@pytest.fixture
def mock_token_manager(mocker):
    """
    Mock TokenManager with valid tokens for both PAPER and LIVE modes.

    Returns:
        Mock TokenManager instance
    """
    mock_tm = MagicMock(spec=TokenManager)
    mock_tm.client_id = "test_client_id"
    mock_tm.client_secret = "test_client_secret"
    mock_tm.redirect_uri = "http://localhost:8888"

    # Mock tokens for both modes
    mock_tm._tokens = {
        "PAPER": {
            "access_token": "mock_paper_access_token",
            "refresh_token": "mock_paper_refresh_token",
            "token_expires_at": 9999999999,  # Far future
        },
        "LIVE": {
            "access_token": "mock_live_access_token",
            "refresh_token": "mock_live_refresh_token",
            "token_expires_at": 9999999999,
        },
    }

    # Mock methods
    mock_tm.get_tokens.return_value = mock_tm._tokens["PAPER"]
    mock_tm.ensure_authenticated.return_value = True
    mock_tm.last_mode = "PAPER"

    return mock_tm


@pytest.fixture
def mock_token_manager_live(mock_token_manager):
    """Mock TokenManager configured for LIVE mode."""
    mock_token_manager.last_mode = "LIVE"
    mock_token_manager.get_tokens.return_value = mock_token_manager._tokens["LIVE"]
    return mock_token_manager


# ============================================================================
# HTTP Client Fixtures
# ============================================================================


@pytest.fixture
def mock_http_client(mock_token_manager, mocker):
    """
    Mock HTTPClient with mocked requests.

    Returns:
        HTTPClient instance with mocked requests.request
    """
    client = HTTPClient(mock_token_manager, enable_full_logging=False)

    # Mock requests.request
    mock_request = mocker.patch("requests.request")

    # Default successful response
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_response.text = "{}"
    mock_response.content = b"{}"
    mock_response.headers = {"Content-Type": "application/json"}
    mock_request.return_value = mock_response

    # Store mock for access in tests
    client._mock_request = mock_request

    return client


@pytest.fixture
def mock_http_client_full_logging(mock_token_manager, mocker):
    """HTTPClient with full logging enabled."""
    client = HTTPClient(mock_token_manager, enable_full_logging=True)
    mock_request = mocker.patch("requests.request")
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = {}
    mock_response.text = "{}"
    mock_response.content = b"{}"
    mock_response.headers = {"Content-Type": "application/json"}
    mock_request.return_value = mock_response
    client._mock_request = mock_request
    return client


# ============================================================================
# SDK Instance Fixtures
# ============================================================================


@pytest.fixture
def sdk_instance(mocker):
    """
    TradeStationSDK instance with all dependencies mocked.

    Returns:
        TradeStationSDK instance with mocked HTTP client and token manager
    """
    # Mock secrets
    mock_secrets = MagicMock()
    mock_secrets.client_id = "test_client_id"
    mock_secrets.client_secret = "test_client_secret"
    mock_secrets.redirect_uri = "http://localhost:8888"
    mock_secrets.account_id = "SIM123456"
    mock_secrets.trading_mode = "PAPER"
    mock_secrets.log_level = "DEBUG"

    mocker.patch("config.secrets.secrets", mock_secrets)

    # Mock logger
    mocker.patch("utils.logger.setup_logger")

    # Create SDK instance
    sdk = TradeStationSDK(enable_full_logging=False)

    # Mock token manager
    sdk._token_manager = mock_token_manager(mocker)

    # Mock HTTP client
    sdk._client = mock_http_client(sdk._token_manager, mocker)

    return sdk


@pytest.fixture
def sdk_instance_full_logging(mocker):
    """TradeStationSDK instance with full logging enabled."""
    mock_secrets = MagicMock()
    mock_secrets.client_id = "test_client_id"
    mock_secrets.client_secret = "test_client_secret"
    mock_secrets.redirect_uri = "http://localhost:8888"
    mock_secrets.account_id = "SIM123456"
    mock_secrets.trading_mode = "PAPER"
    mock_secrets.log_level = "DEBUG"

    mocker.patch("config.secrets.secrets", mock_secrets)
    mocker.patch("utils.logger.setup_logger")

    sdk = TradeStationSDK(enable_full_logging=True)
    sdk._token_manager = mock_token_manager(mocker)
    sdk._client = mock_http_client_full_logging(sdk._token_manager, mocker)

    return sdk


# ============================================================================
# Mock Response Fixtures
# ============================================================================


@pytest.fixture
def sample_account_data():
    """Sample account response data."""
    return api_responses.MOCK_ACCOUNTS_LIST


@pytest.fixture
def sample_account_balances():
    """Sample account balances response data."""
    return api_responses.MOCK_ACCOUNT_BALANCES


@pytest.fixture
def sample_order_data():
    """Sample order response data."""
    return api_responses.MOCK_ORDER_PLACEMENT_SUCCESS


@pytest.fixture
def sample_position_data():
    """Sample position response data."""
    return api_responses.MOCK_POSITIONS


@pytest.fixture
def sample_market_data():
    """Sample market data response."""
    return api_responses.MOCK_BARS_RESPONSE


@pytest.fixture
def sample_quote_data():
    """Sample quote snapshot data."""
    return api_responses.MOCK_QUOTE_SNAPSHOT


# ============================================================================
# Request Mocking Fixtures
# ============================================================================


@pytest.fixture
def mock_requests_lib(mocker):
    """
    Mock requests library for HTTP calls.

    Returns:
        Mock object for requests.request
    """
    return mocker.patch("requests.request")


@pytest.fixture
def mock_requests_success(mock_requests_lib):
    """
    Configure mock_requests_lib to return successful responses by default.

    Args:
        mock_requests_lib: Mock requests.request fixture

    Returns:
        Configured mock
    """

    def _make_response(data: dict[str, Any] | None = None, status_code: int = 200):
        """Build a mock `requests.Response` object for fixture-driven HTTP tests."""
        mock_response = MagicMock()
        mock_response.status_code = status_code
        mock_response.headers = {"Content-Type": "application/json"}

        if data is None:
            data = {}

        mock_response.json.return_value = data
        mock_response.text = json.dumps(data)
        mock_response.content = json.dumps(data).encode()

        return mock_response

    mock_requests_lib.return_value = _make_response()
    mock_requests_lib._make_response = _make_response

    return mock_requests_lib


# ============================================================================
# Logger Fixtures
# ============================================================================


@pytest.fixture
def mock_logger(mocker):
    """Mock logger for log verification."""
    return mocker.patch("utils.client.logger")


# ============================================================================
# Mode Fixtures
# ============================================================================


@pytest.fixture(params=["PAPER", "LIVE"])
def trading_mode(request):
    """Parametrized fixture for testing both PAPER and LIVE modes."""
    return request.param


@pytest.fixture
def paper_mode():
    """PAPER mode constant."""
    return "PAPER"


@pytest.fixture
def live_mode():
    """LIVE mode constant."""
    return "LIVE"


# ============================================================================
# Base URL Fixtures
# ============================================================================


@pytest.fixture
def paper_base_url():
    """PAPER mode base URL."""
    return "https://sim-api.tradestation.com/v3"


@pytest.fixture
def live_base_url():
    """LIVE mode base URL."""
    return "https://api.tradestation.com/v3"


# ============================================================================
# Error Response Fixtures
# ============================================================================


@pytest.fixture
def mock_error_401():
    """Mock 401 Unauthorized error response."""
    return api_responses.MOCK_ERROR_401


@pytest.fixture
def mock_error_400():
    """Mock 400 Bad Request error response."""
    return api_responses.MOCK_ERROR_400


@pytest.fixture
def mock_error_429():
    """Mock 429 Rate Limit error response."""
    return api_responses.MOCK_ERROR_429


@pytest.fixture
def mock_error_500():
    """Mock 500 Server Error response."""
    return api_responses.MOCK_ERROR_500


# ============================================================================
# Helper Functions
# ============================================================================


def create_mock_response(
    data: dict[str, Any] | str, status_code: int = 200, headers: dict[str, str] | None = None
) -> MagicMock:
    """
    Create a mock requests.Response object.

    Args:
        data: Response data (dict for JSON, str for text)
        status_code: HTTP status code
        headers: Optional response headers

    Returns:
        Mock Response object
    """
    return mock_requests.create_mock_response(data, status_code, headers)

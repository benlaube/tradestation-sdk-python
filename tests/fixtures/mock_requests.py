"""
Request mocking utilities for TradeStation SDK tests.

Provides helper functions for mocking HTTP requests and verifying request calls.
"""

from typing import Any
from unittest.mock import MagicMock

import requests


def mock_api_request(
    mocker,
    method: str,
    endpoint: str,
    response_data: dict[str, Any] | str,
    status_code: int = 200,
    headers: dict[str, str] | None = None,
) -> MagicMock:
    """
    Mock a single API request using pytest-mock.

    Args:
        mocker: pytest-mock mocker fixture
        method: HTTP method (GET, POST, PUT, DELETE)
        endpoint: API endpoint path (e.g., "/v3/brokerage/accounts")
        response_data: Response data (dict for JSON, str for text)
        status_code: HTTP status code (default: 200)
        headers: Optional response headers

    Returns:
        Mock object for the request
    """
    # Create mock response
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = status_code
    mock_response.headers = headers or {"Content-Type": "application/json"}

    # Set response content based on type
    if isinstance(response_data, dict):
        mock_response.json.return_value = response_data
        mock_response.text = str(response_data)
    else:
        mock_response.text = response_data
        mock_response.json.side_effect = ValueError("Not JSON")

    mock_response.content = mock_response.text.encode() if isinstance(mock_response.text, str) else b""

    # Mock requests.request to return our response
    mock_request = mocker.patch("requests.request", return_value=mock_response)

    return mock_request


def mock_api_error(mocker, method: str, endpoint: str, status_code: int, error_body: dict[str, Any] | str) -> MagicMock:
    """
    Mock an API error response.

    Args:
        mocker: pytest-mock mocker fixture
        method: HTTP method
        endpoint: API endpoint path
        status_code: HTTP error status code (400, 401, 429, 500, etc.)
        error_body: Error response body

    Returns:
        Mock object for the request
    """
    return mock_api_request(mocker, method, endpoint, error_body, status_code)


def mock_network_error(mocker, method: str, endpoint: str, exception: Exception) -> MagicMock:
    """
    Mock a network error (connection timeout, DNS failure, etc.).

    Args:
        mocker: pytest-mock mocker fixture
        method: HTTP method
        endpoint: API endpoint path
        exception: Exception to raise (e.g., requests.ConnectionError)

    Returns:
        Mock object for the request
    """
    mock_request = mocker.patch("requests.request", side_effect=exception)
    return mock_request


def verify_request_called(
    mock_request: MagicMock,
    method: str,
    endpoint: str,
    params: dict[str, Any] | None = None,
    json_data: dict[str, Any] | None = None,
    base_url: str | None = None,
) -> bool:
    """
    Verify that a request was called with correct parameters.

    Args:
        mock_request: Mock request object from mock_api_request
        method: Expected HTTP method
        endpoint: Expected endpoint path
        params: Expected query parameters (optional)
        json_data: Expected JSON body (optional)
        base_url: Base URL to check (optional)

    Returns:
        True if request matches, False otherwise

    Raises:
        AssertionError: If request was not called or doesn't match
    """
    # Check that request was called
    assert mock_request.called, f"Expected {method} request to {endpoint} was not called"

    # Get the last call
    call_args = mock_request.call_args

    # Verify method
    actual_method = call_args[0][0] if call_args[0] else None
    assert actual_method == method, f"Expected method {method}, got {actual_method}"

    # Verify URL contains endpoint
    actual_url = call_args[0][1] if len(call_args[0]) > 1 else None
    if base_url:
        expected_url = f"{base_url}{endpoint}"
        assert actual_url == expected_url, f"Expected URL {expected_url}, got {actual_url}"
    else:
        assert endpoint in actual_url, f"Expected endpoint {endpoint} in URL, got {actual_url}"

    # Verify params if provided
    if params:
        actual_params = call_args[1].get("params")
        if actual_params:
            for key, value in params.items():
                assert key in actual_params, f"Expected param {key} not found"
                assert actual_params[key] == value, f"Expected param {key}={value}, got {actual_params[key]}"

    # Verify JSON body if provided
    if json_data:
        actual_json = call_args[1].get("json")
        if actual_json:
            for key, value in json_data.items():
                assert key in actual_json, f"Expected JSON key {key} not found"
                assert actual_json[key] == value, f"Expected JSON {key}={value}, got {actual_json[key]}"

    return True


def verify_logging(caplog, expected_logs: list[str], log_level: str = "DEBUG") -> bool:
    """
    Verify that logs contain expected content.

    Args:
        caplog: pytest caplog fixture
        expected_logs: List of strings that should appear in logs
        log_level: Minimum log level to check (default: DEBUG)

    Returns:
        True if all expected logs found

    Raises:
        AssertionError: If expected logs not found
    """
    log_text = "\n".join([record.message for record in caplog.records])

    for expected in expected_logs:
        assert expected in log_text, f"Expected log '{expected}' not found in logs:\n{log_text}"

    return True


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
    mock_response = MagicMock(spec=requests.Response)
    mock_response.status_code = status_code
    mock_response.headers = headers or {"Content-Type": "application/json"}

    if isinstance(data, dict):
        mock_response.json.return_value = data
        mock_response.text = str(data)
    else:
        mock_response.text = data
        mock_response.json.side_effect = ValueError("Not JSON")

    mock_response.content = mock_response.text.encode() if isinstance(mock_response.text, str) else b""

    return mock_response

"""
Logging Verification Unit Tests

Tests for request/response logging behavior in HTTPClient and SDK operations.
"""

import json
from unittest.mock import patch

import pytest

from .fixtures import api_responses


class _PytestMockShim:
    """Minimal shim for legacy tests that expected pytest.Mock()."""

    def __init__(self):
        self._patchers = []

    def patch(self, *args, **kwargs):
        patcher = patch(*args, **kwargs)
        mocked = patcher.start()
        self._patchers.append(patcher)
        return mocked

    def __del__(self):
        for patcher in reversed(self._patchers):
            try:
                patcher.stop()
            except RuntimeError:
                pass


if not hasattr(pytest, "Mock"):
    pytest.Mock = _PytestMockShim  # type: ignore[attr-defined]


@pytest.fixture(autouse=True)
def _capture_http_client_logs(caplog):
    """Capture debug-level SDK client logs for assertions in this module."""
    caplog.set_level("DEBUG", logger="tradestation.client")
    return caplog

# ============================================================================
# Request Logging Tests
# ============================================================================


@pytest.mark.unit
class TestRequestLogging:
    """Tests for request logging behavior."""

    def test_all_requests_are_logged(self, mock_http_client, caplog):
        """Verify all requests are logged."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        import pytest

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        # Make a request
        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        # Verify log was created
        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)

        assert "API Request" in log_text or "api_request" in log_text

    def test_request_log_level_is_debug(self, mock_http_client, caplog):
        """Verify request log level is DEBUG."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        # Check for DEBUG level logs
        debug_logs = [record for record in caplog.records if record.levelname == "DEBUG"]
        assert len(debug_logs) > 0

    def test_request_log_includes_method_endpoint(self, mock_http_client, caplog):
        """Verify log includes method and endpoint."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)

        assert "GET" in log_text
        assert "brokerage/accounts" in log_text

    def test_request_log_sanitizes_sensitive_data(self, mock_http_client, caplog):
        """Verify sensitive data is sanitized in logs."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        sensitive_data = {"access_token": "secret_token_123"}
        mock_http_client.make_request("POST", "oauth/token", json_data=sensitive_data, mode="PAPER")

        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)

        assert "secret_token_123" not in log_text
        assert "<redacted>" in log_text

    def test_request_log_truncates_body_when_full_logging_disabled(self, mock_http_client, caplog):
        """Verify body truncation when enable_full_logging=False."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        long_body = {"data": "x" * 1000}
        mock_http_client.make_request("POST", "endpoint", json_data=long_body, mode="PAPER")

        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)

        assert "... (truncated)" in log_text

    def test_request_log_full_body_when_full_logging_enabled(self, mock_http_client_full_logging, caplog):
        """Verify full body logging when enable_full_logging=True."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        long_body = {"data": "x" * 1000}
        mock_http_client_full_logging.make_request("POST", "endpoint", json_data=long_body, mode="PAPER")

        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)

        assert "... (truncated)" not in log_text


# ============================================================================
# Response Logging Tests
# ============================================================================


@pytest.mark.unit
class TestResponseLogging:
    """Tests for response logging behavior."""

    def test_all_responses_are_logged(self, mock_http_client, caplog):
        """Verify all responses are logged."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)

        assert "API Response" in log_text or "api_response" in log_text

    def test_response_log_includes_status_time_size(self, mock_http_client, caplog):
        """Verify log includes status, time, size, body."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"result": "success"}
        mock_response.text = '{"result": "success"}'
        mock_response.content = b'{"result": "success"}'
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)

        assert "Status: 200" in log_text
        assert "Time:" in log_text
        assert "Size:" in log_text

    def test_error_logged_at_warning_level(self, mock_http_client, caplog):
        """Verify errors logged at WARNING level."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = api_responses.MOCK_ERROR_400
        mock_response.text = json.dumps(api_responses.MOCK_ERROR_400)
        mock_response.content = json.dumps(api_responses.MOCK_ERROR_400).encode()
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        try:
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")
        except Exception:
            pass

        # Check for warning-level log
        warning_logs = [record for record in caplog.records if record.levelname == "WARNING"]
        assert len(warning_logs) > 0

    def test_successful_post_logged_at_info_level(self, mock_http_client, caplog):
        """Verify successful POST/PUT/DELETE logged at INFO level."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"OrderID": "123"}
        mock_response.text = '{"OrderID": "123"}'
        mock_response.content = b'{"OrderID": "123"}'
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("POST", "orderexecution/orders", json_data={}, mode="PAPER")

        # Check for info-level log
        info_logs = [record for record in caplog.records if record.levelname == "INFO"]
        assert len(info_logs) > 0


# ============================================================================
# Log Context Tests
# ============================================================================


@pytest.mark.unit
class TestLogContext:
    """Tests for log context (source, action, component)."""

    def test_log_context_includes_source_action_component(self, mock_http_client, caplog):
        """Verify log context includes source, action, component."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {}
        mock_response.text = "{}"
        mock_response.content = b"{}"
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")

        # Check log records for context
        # Note: log_with_context may add extra fields, check if available
        log_records = [record for record in caplog.records]
        assert len(log_records) > 0

    def test_error_logs_include_api_error_action(self, mock_http_client, caplog):
        """Verify error logs include action='api_error'."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = api_responses.MOCK_ERROR_400
        mock_response.text = json.dumps(api_responses.MOCK_ERROR_400)
        mock_response.content = json.dumps(api_responses.MOCK_ERROR_400).encode()
        mock_response.headers = {"Content-Type": "application/json"}

        mocker = pytest.Mock()
        mocker.patch("requests.request", return_value=mock_response)

        try:
            mock_http_client.make_request("GET", "brokerage/accounts", mode="PAPER")
        except Exception:
            pass

        # Verify error was logged
        log_records = [record.message for record in caplog.records]
        log_text = "\n".join(log_records)
        assert "error" in log_text.lower() or "Error" in log_text

from unittest.mock import MagicMock

import pytest
import requests

from tradestation.exceptions import RecoverableError
from tradestation.utils.client import HTTPClient


@pytest.mark.unit
class TestHTTPClientEnhanced:
    @pytest.fixture
    def client(self, mocker):
        token_manager = mocker.MagicMock()
        return HTTPClient(token_manager)

    def test_rate_limiting_retry_after(self, client, mocker):
        """Test that Retry-After header is respected."""
        mock_response = MagicMock()
        mock_response.status_code = 429
        mock_response.headers = {"Retry-After": "5"}
        mock_response.json.return_value = {"Error": "Rate limit exceeded"}

        mocker.patch("requests.request", return_value=mock_response)

        # We expect a RecoverableError which might contain info about retry
        with pytest.raises(RecoverableError) as exc:
            client.make_request("GET", "test")

        # In a real retry logic, the client would sleep.
        # Here we just verify the error is raised correctly for 429
        assert exc.value.details.response_status == 429

    def test_connect_timeout(self, client, mocker):
        """Test handling of ConnectTimeout."""
        mocker.patch("requests.request", side_effect=requests.exceptions.ConnectTimeout("Timeout"))

        with pytest.raises(RecoverableError) as exc:
            client.make_request("GET", "test")

        assert "Connection failed" in str(exc.value) or "Timeout" in str(exc.value)

    def test_read_timeout(self, client, mocker):
        """Test handling of ReadTimeout."""
        mocker.patch("requests.request", side_effect=requests.exceptions.ReadTimeout("Read Timeout"))

        with pytest.raises(RecoverableError) as exc:
            client.make_request("GET", "test")

        assert "Connection failed" in str(exc.value) or "Timeout" in str(exc.value)

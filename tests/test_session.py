"""
Session and TokenManager Unit Tests

Tests for TokenManager class including token management, authentication, and token refresh.
Note: OAuth flow is mocked to avoid real browser interaction.
"""

import json
from unittest.mock import MagicMock

import pytest
from src.lib.tradestation.exceptions import AuthenticationError
from src.lib.tradestation.session import TokenManager

from .fixtures import api_responses

# ============================================================================
# TokenManager Token Management Tests
# ============================================================================


@pytest.mark.unit
class TestTokenManagerTokenManagement:
    """Tests for TokenManager token loading and saving."""

    def test_token_loading_from_file_paper(self, mocker, tmp_path):
        """Test token loading from file for PAPER mode."""
        # Mock token file path
        token_file = tmp_path / "tokens_paper.json"
        token_data = {
            "access_token": "loaded_paper_token",
            "refresh_token": "loaded_paper_refresh",
            "expires_at": 9999999999,
        }
        token_file.write_text(json.dumps(token_data))

        # Mock TOKEN_FILE_PAPER path
        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_PAPER", token_file)
        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_LIVE", tmp_path / "tokens_live.json")
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")

        tokens = tm.get_tokens("PAPER")
        assert tokens["access_token"] == "loaded_paper_token"
        assert tokens["refresh_token"] == "loaded_paper_refresh"

    def test_token_loading_from_file_live(self, mocker, tmp_path):
        """Test token loading from file for LIVE mode."""
        token_file = tmp_path / "tokens_live.json"
        token_data = {
            "access_token": "loaded_live_token",
            "refresh_token": "loaded_live_refresh",
            "expires_at": 9999999999,
        }
        token_file.write_text(json.dumps(token_data))

        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_PAPER", tmp_path / "tokens_paper.json")
        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_LIVE", token_file)
        mocker.patch("config.secrets.secrets.trading_mode", "LIVE")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")

        tokens = tm.get_tokens("LIVE")
        assert tokens["access_token"] == "loaded_live_token"
        assert tokens["refresh_token"] == "loaded_live_refresh"

    def test_token_saving_to_file(self, mocker, tmp_path):
        """Test token saving to file."""
        token_file = tmp_path / "tokens_paper.json"

        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_PAPER", token_file)
        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_LIVE", tmp_path / "tokens_live.json")
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["access_token"] = "saved_token"
        tm._tokens["PAPER"]["refresh_token"] = "saved_refresh"
        tm._tokens["PAPER"]["token_expires_at"] = 9999999999

        tm._save_tokens("PAPER")

        # Verify file was created and contains correct data
        assert token_file.exists()
        saved_data = json.loads(token_file.read_text())
        assert saved_data["access_token"] == "saved_token"
        assert saved_data["refresh_token"] == "saved_refresh"

    def test_dual_mode_token_storage(self, mocker, tmp_path):
        """Test that PAPER and LIVE tokens are stored separately."""
        paper_file = tmp_path / "tokens_paper.json"
        live_file = tmp_path / "tokens_live.json"

        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_PAPER", paper_file)
        mocker.patch("src.lib.tradestation.session.TOKEN_FILE_LIVE", live_file)
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")

        # Set different tokens for each mode
        tm._tokens["PAPER"]["access_token"] = "paper_token"
        tm._tokens["LIVE"]["access_token"] = "live_token"

        tm._save_tokens("PAPER")
        tm._save_tokens("LIVE")

        # Verify both files exist with different tokens
        assert paper_file.exists()
        assert live_file.exists()

        paper_data = json.loads(paper_file.read_text())
        live_data = json.loads(live_file.read_text())

        assert paper_data["access_token"] == "paper_token"
        assert live_data["access_token"] == "live_token"

    def test_get_tokens_returns_correct_mode(self, mocker):
        """Test get_tokens returns tokens for specified mode."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["access_token"] = "paper_token"
        tm._tokens["LIVE"]["access_token"] = "live_token"

        paper_tokens = tm.get_tokens("PAPER")
        live_tokens = tm.get_tokens("LIVE")

        assert paper_tokens["access_token"] == "paper_token"
        assert live_tokens["access_token"] == "live_token"

    def test_get_tokens_uses_default_mode(self, mocker):
        """Test get_tokens uses secrets.trading_mode when mode is None."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["access_token"] = "paper_token"

        tokens = tm.get_tokens(None)
        assert tokens["access_token"] == "paper_token"


# ============================================================================
# TokenManager Authentication Tests
# ============================================================================


@pytest.mark.unit
class TestTokenManagerAuthentication:
    """Tests for TokenManager authentication (OAuth flow mocked)."""

    def test_authenticate_for_paper_mode(self, mocker):
        """Test authentication for PAPER mode."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")
        mocker.patch("webbrowser.open")
        mocker.patch("threading.Thread")
        mocker.patch("src.lib.tradestation.session.HTTPServer")

        # Mock OAuth callback handler to simulate receiving auth code
        from src.lib.tradestation.session import OAuthCallbackHandler

        OAuthCallbackHandler.auth_code = "mock_auth_code_123"

        # Mock httpx.post for token exchange
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = api_responses.MOCK_TOKEN_RESPONSE

        mocker.patch("httpx.post", return_value=mock_response)
        mocker.patch("time.time", return_value=1000)
        mocker.patch("src.lib.tradestation.session.TokenManager._save_tokens")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm.authenticate("PAPER")

        # Verify tokens were set
        tokens = tm.get_tokens("PAPER")
        assert tokens["access_token"] == "mock_access_token_12345"
        assert tokens["refresh_token"] == "mock_refresh_token_67890"
        assert tm._last_mode == "PAPER"

    def test_authenticate_for_live_mode(self, mocker):
        """Test authentication for LIVE mode."""
        mocker.patch("config.secrets.secrets.trading_mode", "LIVE")
        mocker.patch("webbrowser.open")
        mocker.patch("threading.Thread")
        mocker.patch("src.lib.tradestation.session.HTTPServer")

        from src.lib.tradestation.session import OAuthCallbackHandler

        OAuthCallbackHandler.auth_code = "mock_auth_code_456"

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = api_responses.MOCK_TOKEN_RESPONSE

        mocker.patch("httpx.post", return_value=mock_response)
        mocker.patch("time.time", return_value=1000)
        mocker.patch("src.lib.tradestation.session.TokenManager._save_tokens")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm.authenticate("LIVE")

        tokens = tm.get_tokens("LIVE")
        assert tokens["access_token"] == "mock_access_token_12345"
        assert tm._last_mode == "LIVE"

    def test_authenticate_token_exchange_failure(self, mocker):
        """Test authentication raises error when token exchange fails."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")
        mocker.patch("webbrowser.open")
        mocker.patch("threading.Thread")
        mocker.patch("src.lib.tradestation.session.HTTPServer")

        from src.lib.tradestation.session import OAuthCallbackHandler

        OAuthCallbackHandler.auth_code = "mock_auth_code"

        # Mock failed token exchange
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid grant"

        mocker.patch("httpx.post", return_value=mock_response)

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")

        with pytest.raises(AuthenticationError):
            tm.authenticate("PAPER")

    def test_ensure_authenticated_auto_refreshes_expired_tokens(self, mocker):
        """Test ensure_authenticated auto-refreshes expired tokens."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")
        mocker.patch("time.time", return_value=2000)  # Current time

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["access_token"] = "expired_token"
        tm._tokens["PAPER"]["token_expires_at"] = 1000  # Expired

        # Mock refresh_access_token
        mock_refresh = mocker.patch.object(tm, "refresh_access_token")

        tm.ensure_authenticated("PAPER")

        # Verify refresh was called
        mock_refresh.assert_called_once_with("PAPER")

    def test_ensure_authenticated_authenticates_if_no_token(self, mocker):
        """Test ensure_authenticated authenticates if no token exists."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["access_token"] = None

        # Mock authenticate
        mock_authenticate = mocker.patch.object(tm, "authenticate")

        tm.ensure_authenticated("PAPER")

        # Verify authenticate was called
        mock_authenticate.assert_called_once_with("PAPER")


# ============================================================================
# TokenManager Token Refresh Tests
# ============================================================================


@pytest.mark.unit
class TestTokenManagerTokenRefresh:
    """Tests for TokenManager token refresh."""

    def test_successful_token_refresh(self, mocker):
        """Test successful token refresh."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")
        mocker.patch("time.time", return_value=1000)
        mocker.patch("src.lib.tradestation.session.TokenManager._save_tokens")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["refresh_token"] = "old_refresh_token"

        # Mock successful refresh response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = api_responses.MOCK_TOKEN_REFRESH_RESPONSE

        mocker.patch("httpx.post", return_value=mock_response)

        tm.refresh_access_token("PAPER")

        # Verify tokens were updated
        tokens = tm.get_tokens("PAPER")
        assert tokens["access_token"] == "new_access_token_12345"
        assert tokens["refresh_token"] == "new_refresh_token_67890"
        assert tm._last_mode == "PAPER"

    def test_refresh_failure_triggers_re_authentication(self, mocker):
        """Test refresh failure triggers re-authentication."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["refresh_token"] = "invalid_refresh_token"

        # Mock failed refresh
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = "Invalid refresh token"

        mocker.patch("httpx.post", return_value=mock_response)

        # Mock authenticate
        mock_authenticate = mocker.patch.object(tm, "authenticate")

        tm.refresh_access_token("PAPER")

        # Verify authenticate was called
        mock_authenticate.assert_called_once_with("PAPER")

    def test_refresh_token_rotation(self, mocker):
        """Test refresh token rotation (new refresh token provided)."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")
        mocker.patch("time.time", return_value=1000)
        mocker.patch("src.lib.tradestation.session.TokenManager._save_tokens")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["refresh_token"] = "old_refresh_token"

        # Mock refresh response with new refresh token
        refresh_response = {
            "access_token": "new_access_token",
            "refresh_token": "new_refresh_token",  # New refresh token
            "token_type": "Bearer",
            "expires_in": 3600,
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = refresh_response

        mocker.patch("httpx.post", return_value=mock_response)

        tm.refresh_access_token("PAPER")

        # Verify new refresh token was saved
        tokens = tm.get_tokens("PAPER")
        assert tokens["refresh_token"] == "new_refresh_token"

    def test_refresh_without_refresh_token(self, mocker):
        """Test refresh without refresh token triggers authentication."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["refresh_token"] = None

        # Mock authenticate
        mock_authenticate = mocker.patch.object(tm, "authenticate")

        tm.refresh_access_token("PAPER")

        # Verify authenticate was called
        mock_authenticate.assert_called_once_with("PAPER")

    def test_token_expiration_handling(self, mocker):
        """Test token expiration is handled correctly."""
        mocker.patch("config.secrets.secrets.trading_mode", "PAPER")
        mocker.patch("time.time", return_value=2000)  # Current time

        tm = TokenManager("client_id", "client_secret", "http://localhost:8888")
        tm._tokens["PAPER"]["access_token"] = "token"
        tm._tokens["PAPER"]["token_expires_at"] = 1000  # Expired

        # Mock refresh
        mock_refresh = mocker.patch.object(tm, "refresh_access_token")

        # ensure_authenticated should detect expiration and refresh
        tm.ensure_authenticated("PAPER")

        mock_refresh.assert_called_once_with("PAPER")

import os
from unittest.mock import patch

import pytest

# Use relative import if running from package, or absolute if running from root with src in path
# Given the conftest issues, we will try to be robust
try:
    from tradestation.config import SDKConfig
except ImportError:
    from tradestation.config import SDKConfig


class TestSDKConfig:
    @pytest.fixture
    def mock_env(self):
        """Clean environment for each test."""
        with patch.dict(os.environ, {}, clear=True):
            yield

    def test_default_initialization(self, mock_env):
        """Test partial initialization with defaults."""
        config = SDKConfig()
        assert config.trading_mode == "PAPER"
        assert config.log_level == "INFO"
        assert config.use_async is False
        assert config.get_api_base_url() == "https://sim-api.tradestation.com/v3"

    def test_load_from_env_vars(self, mock_env):
        """Test loading configuration from environment variables."""
        env_vars = {
            "TRADESTATION_CLIENT_ID": "test_id",
            "TRADESTATION_CLIENT_SECRET": "test_secret",  # pragma: allowlist secret
            "TRADESTATION_REDIRECT_URI": "http://test.com",
            "TRADESTATION_ACCOUNT_ID": "123456",
            "TRADING_MODE": "LIVE",
            "LOG_LEVEL": "DEBUG",
            "TRADESTATION_USE_ASYNC": "true",
        }
        with patch.dict(os.environ, env_vars):
            config = SDKConfig()
            assert config.client_id == "test_id"
            assert config.client_secret == "test_secret"  # pragma: allowlist secret
            assert config.redirect_uri == "http://test.com"
            assert config.account_id == "123456"
            assert config.trading_mode == "LIVE"
            assert config.log_level == "DEBUG"
            assert config.use_async is True
            assert config.get_api_base_url() == "https://api.tradestation.com/v3"

    def test_invalid_trading_mode_fallback(self, mock_env):
        """Test fallback to PAPER when invalid mode is provided."""
        with patch.dict(os.environ, {"TRADING_MODE": "INVALID"}):
            config = SDKConfig()
            assert config.trading_mode == "PAPER"

    def test_validate_credentials_success(self, mock_env):
        """Test validation passes with secrets."""
        with patch.dict(
            os.environ, {"TRADESTATION_CLIENT_ID": "id", "TRADESTATION_CLIENT_SECRET": "secret"}
        ):  # pragma: allowlist secret
            config = SDKConfig()
            # Should not raise
            config.validate_credentials()

    def test_validate_credentials_missing_client_id(self, mock_env):
        """Test validation raises ValueError when Client ID is missing."""
        with patch.dict(os.environ, {"TRADESTATION_CLIENT_SECRET": "secret"}):  # pragma: allowlist secret
            config = SDKConfig()
            with pytest.raises(ValueError, match="TRADESTATION_CLIENT_ID"):
                config.validate_credentials()

    def test_validate_credentials_missing_client_secret(self, mock_env):
        """Test validation raises ValueError when Client Secret is missing."""
        with patch.dict(os.environ, {"TRADESTATION_CLIENT_ID": "id"}):
            config = SDKConfig()
            with pytest.raises(ValueError, match="TRADESTATION_CLIENT_SECRET"):
                config.validate_credentials()

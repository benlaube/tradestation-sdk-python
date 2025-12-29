"""
SDK Internal Configuration

Loads configuration from environment variables (including .env files).
This makes the SDK portable and self-contained.

Dependencies: python-dotenv (optional - will work without it)
"""

import os
from pathlib import Path

# Try to load .env file if python-dotenv is available
try:
    from dotenv import load_dotenv

    # Search for .env in SDK directory and parent directories
    current_dir = Path(__file__).parent
    env_paths = [
        current_dir / ".env",  # SDK directory
        current_dir.parent.parent.parent / ".env",  # Project root (if SDK is in src/lib/tradestation)
    ]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            break
except ImportError:
    # python-dotenv not installed, will use system environment variables only
    pass


class SDKConfig:
    """
    SDK configuration loaded from environment variables.

    If the SDK is used as a submodule, it will read from the parent project's .env.
    If the SDK is standalone, it will read from its own .env or system environment.
    """

    def __init__(self):
        # TradeStation API Credentials
        self.client_id = os.getenv("TRADESTATION_CLIENT_ID", "")
        self.client_secret = os.getenv("TRADESTATION_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("TRADESTATION_REDIRECT_URI", "http://localhost:8888/callback")
        self.account_id = os.getenv("TRADESTATION_ACCOUNT_ID", "")  # Optional - can query from API

        # Trading Mode (PAPER or LIVE)
        self.trading_mode = os.getenv("TRADING_MODE", "PAPER").upper()
        if self.trading_mode not in ["PAPER", "LIVE"]:
            # Don't raise, just default to PAPER for portability
            self.trading_mode = "PAPER"

        # Logging
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()

        # HTTP Client Configuration
        # Set TRADESTATION_USE_ASYNC=true to enable async HTTP client (httpx)
        # Default: False for backward compatibility
        self.use_async = os.getenv("TRADESTATION_USE_ASYNC", "").lower() in ("true", "1", "yes")

    def validate_credentials(self):
        """
        Validate that required credentials are set.
        Call this when initializing the SDK to ensure proper configuration.

        Raises:
            ValueError: If required credentials are missing
        """
        if not self.client_id:
            raise ValueError(
                "Missing required environment variable: TRADESTATION_CLIENT_ID\n"
                "Set this in your .env file or environment."
            )
        if not self.client_secret:
            raise ValueError(
                "Missing required environment variable: TRADESTATION_CLIENT_SECRET\n"
                "Set this in your .env file or environment."
            )

    def get_api_base_url(self, mode: str | None = None) -> str:
        """
        Returns the appropriate TradeStation API base URL based on trading mode.

        Args:
            mode: Override trading mode (PAPER or LIVE). If None, uses self.trading_mode

        Returns:
            API base URL string
        """
        effective_mode = (mode or self.trading_mode).upper()
        if effective_mode == "PAPER":
            return "https://sim-api.tradestation.com/v3"
        return "https://api.tradestation.com/v3"


# Global singleton instance
sdk_config = SDKConfig()

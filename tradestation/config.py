"""Runtime SDK configuration helpers."""

from __future__ import annotations

import os
from pathlib import Path


def _load_env_file() -> None:
    """Load the nearest relevant `.env` without requiring callers to do it first."""
    try:
        from dotenv import load_dotenv
    except ImportError:
        return

    current_dir = Path(__file__).resolve().parent
    env_paths = [current_dir / ".env", *(parent / ".env" for parent in current_dir.parents)]

    for env_path in env_paths:
        if env_path.exists():
            load_dotenv(dotenv_path=env_path)
            break


def _normalize_mode(mode: str | None) -> str:
    value = (mode or "PAPER").upper().strip()
    return value if value in {"PAPER", "LIVE"} else "PAPER"


class TradeStationSDKConfig:
    """Mutable SDK configuration that can be refreshed from env or explicit values."""

    def __init__(
        self,
        client_id: str = "",
        client_secret: str = "",
        redirect_uri: str = "http://localhost:8888/callback",
        account_id: str = "",
        trading_mode: str = "PAPER",
        log_level: str = "INFO",
        load_env: bool = False,
    ) -> None:
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.account_id = account_id
        self.trading_mode = _normalize_mode(trading_mode)
        self.log_level = log_level.upper()

        if load_env:
            self.refresh_from_env()

    def refresh_from_env(self) -> "TradeStationSDKConfig":
        """Reload configuration from the active environment."""
        _load_env_file()
        self.client_id = os.getenv("TRADESTATION_CLIENT_ID", "")
        self.client_secret = os.getenv("TRADESTATION_CLIENT_SECRET", "")
        self.redirect_uri = os.getenv("TRADESTATION_REDIRECT_URI", "http://localhost:8888/callback")
        self.account_id = os.getenv("TRADESTATION_ACCOUNT_ID", "")

        env_mode = os.getenv("TRADESTATION_MODE") or os.getenv("TRADING_MODE")
        self.trading_mode = _normalize_mode(env_mode)
        self.log_level = os.getenv("LOG_LEVEL", "INFO").upper()
        return self

    def apply(self, other: "TradeStationSDKConfig") -> "TradeStationSDKConfig":
        """Copy values from another config into this mutable instance."""
        self.client_id = other.client_id
        self.client_secret = other.client_secret
        self.redirect_uri = other.redirect_uri
        self.account_id = other.account_id
        self.trading_mode = _normalize_mode(other.trading_mode)
        self.log_level = other.log_level.upper()
        return self

    def clone(self) -> "TradeStationSDKConfig":
        """Return a detached copy for callers that need stable values."""
        return TradeStationSDKConfig(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            account_id=self.account_id,
            trading_mode=self.trading_mode,
            log_level=self.log_level,
        )

    def validate_credentials(self) -> None:
        """Validate that required credentials are present."""
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
        """Return the base URL for the requested or configured mode."""
        effective_mode = _normalize_mode(mode or self.trading_mode)
        if effective_mode == "PAPER":
            return "https://sim-api.tradestation.com/v3"
        return "https://api.tradestation.com/v3"


sdk_config = TradeStationSDKConfig(load_env=True)

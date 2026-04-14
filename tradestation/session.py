"""
TradeStation Session & OAuth Management

Handles OAuth2 flow, token storage, and token refresh for PAPER and LIVE modes.
Replaces external tastyware/tradestation SDK Session class.

Key responsibilities:
- Run the Authorization Code flow (local HTTP callback) to obtain tokens
- Persist tokens separately for PAPER and LIVE
- Refresh access tokens proactively before they expire
- Provide mode-aware token access to the HTTP client and streaming modules

Side effects:
- Starts a temporary local HTTP server on the redirect URI port during auth
- Writes token JSON files under `config/` (git-ignored)

Dependencies: requests, json, time, webbrowser, pathlib, http.server, urllib.parse, threading
"""

import builtins
import contextlib
import json
import os
import secrets as py_secrets
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
import jwt
from .logger import setup_logger

from .config import sdk_config
from .exceptions import AuthenticationError, TokenExpiredError

logger = setup_logger(__name__, sdk_config.log_level)

# OAuth endpoints
OAUTH_URL = "https://signin.tradestation.com"
OAUTH_SCOPES = [
    "MarketData",
    "ReadAccount",
    "Trade",
    "OptionSpreads",
    "Matrix",
    "openid",
    "offline_access",
    "profile",
    "email",
]

# API base URLs
API_URL_V3 = "https://api.tradestation.com/v3"
API_URL_SIM = "https://sim-api.tradestation.com/v3"

# Token storage paths (git-ignored) - separate files per mode
# Tokens stored in config/ directory for better organization (not in logs/)
TOKEN_DIR = Path(__file__).parent.parent.parent.parent / "config"
TOKEN_DIR.mkdir(exist_ok=True)  # Ensure config directory exists
TOKEN_FILE_PAPER = TOKEN_DIR / "tokens_paper.json"
TOKEN_FILE_LIVE = TOKEN_DIR / "tokens_live.json"


class OAuthCallbackHandler(BaseHTTPRequestHandler):
    """
    Minimal HTTP handler that captures the OAuth authorization code.

    Behavior:
    - Listens on the redirect URI path/port
    - Extracts `code` or `error` from the query string
    - Writes a simple HTML response for user feedback
    - Stores the auth code on the class attribute for retrieval by TokenManager
    """

    auth_code: str | None = None
    expected_state: str | None = None

    def do_GET(self):
        """Handle GET request with authorization code"""
        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)

        # TradeStation redirects to root path "/" (not "/callback")
        if "state" in params and self.expected_state and params["state"][0] != self.expected_state:
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Invalid state</h1><p>State mismatch detected.</p></body></html>")
            logger.error("❌ OAuth state mismatch - potential CSRF")
            return

        if "code" in params:
            OAuthCallbackHandler.auth_code = params["code"][0]
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                b"<html><body><h1>Authentication Successful!</h1>"
                b"<p>You can close this window and return to the bot.</p></body></html>"
            )
            logger.info("✅ Authorization code received successfully")
        elif "error" in params:
            error = params["error"][0]
            error_desc = params.get("error_description", ["Unknown"])[0]
            self.send_response(400)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(
                f"<html><body><h1>Authentication Failed</h1>"
                f"<p>Error: {error}</p><p>{error_desc}</p></body></html>".encode()
            )
            logger.error(f"❌ OAuth error: {error} - {error_desc}")
        else:
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><h1>Waiting for TradeStation...</h1></body></html>")

    def log_message(self, format, *args):
        """Suppress default HTTP server logging"""
        pass


class TokenManager:
    """
    Manages OAuth tokens for PAPER and LIVE modes.

    Handles token storage, loading, authentication, and refresh.

    Persistence:
    - Tokens are stored in JSON files under `config/`:
      - PAPER → tokens_paper.json
      - LIVE  → tokens_live.json

    Safety:
    - Files are git-ignored; do not store secrets in version control.
    - Callers should ensure file permissions are restricted (e.g., chmod 600).
    """

    def __init__(self, client_id: str, client_secret: str, redirect_uri: str):
        """
        Initialize token manager.

        Args:
            client_id: TradeStation API client ID
            client_secret: TradeStation API client secret
            redirect_uri: OAuth redirect URI
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri

        # OAuth endpoints (same for both PAPER and LIVE)
        self.auth_url = f"{OAUTH_URL}/authorize"
        self.token_url = f"{OAUTH_URL}/oauth/token"

        # Token storage per mode
        self._tokens: dict[str, dict[str, Any]] = {
            "PAPER": {"access_token": None, "refresh_token": None, "token_expires_at": 0},
            "LIVE": {"access_token": None, "refresh_token": None, "token_expires_at": 0},
        }

        # Track which mode was most recently authenticated/refreshed
        self._last_mode: str = sdk_config.trading_mode

        # Load tokens if they exist
        self._load_tokens()

    def _load_tokens(self) -> bool:
        """
        Load saved tokens from local files for both modes.

        Returns:
            True if any tokens loaded successfully, False otherwise
        """
        loaded = False
        TOKEN_DIR.mkdir(exist_ok=True)

        # Load PAPER tokens
        if TOKEN_FILE_PAPER.exists():
            try:
                with open(TOKEN_FILE_PAPER) as f:
                    data = json.load(f)
                    self._tokens["PAPER"]["access_token"] = data.get("access_token")
                    self._tokens["PAPER"]["refresh_token"] = data.get("refresh_token")
                    self._tokens["PAPER"]["token_expires_at"] = data.get("expires_at", 0)
                    logger.info("Loaded PAPER tokens from file")
                    loaded = True
            except Exception as e:
                logger.warning(f"Failed to load PAPER tokens: {e}")

        # Load LIVE tokens
        if TOKEN_FILE_LIVE.exists():
            try:
                with open(TOKEN_FILE_LIVE) as f:
                    data = json.load(f)
                    self._tokens["LIVE"]["access_token"] = data.get("access_token")
                    self._tokens["LIVE"]["refresh_token"] = data.get("refresh_token")
                    self._tokens["LIVE"]["token_expires_at"] = data.get("expires_at", 0)
                    logger.info("Loaded LIVE tokens from file")
                    loaded = True
            except Exception as e:
                logger.warning(f"Failed to load LIVE tokens: {e}")

        return loaded

    def _save_tokens(self, mode: str | None = None):
        """
        Save tokens to local file for persistence.

        Args:
            mode: "PAPER" or "LIVE". If None, saves tokens for the mode specified in sdk_config.trading_mode
        """
        if mode is None:
            mode = sdk_config.trading_mode

        TOKEN_DIR.mkdir(exist_ok=True)
        token_file = TOKEN_FILE_PAPER if mode == "PAPER" else TOKEN_FILE_LIVE

        with open(token_file, "w") as f:
            json.dump(
                {
                    "access_token": self._tokens[mode]["access_token"],
                    "refresh_token": self._tokens[mode]["refresh_token"],
                    "expires_at": self._tokens[mode]["token_expires_at"],
                },
                f,
                indent=2,
            )
        # Restrict file permissions to owner read/write (600) for token files
        try:
            os.chmod(token_file, 0o600)
        except Exception as e:
            logger.warning(f"Could not set permissions on token file {token_file}: {e}")

        logger.debug(f"Tokens saved to file for {mode} mode")

    def get_tokens(self, mode: str | None = None) -> dict[str, Any]:
        """
        Get tokens for specified mode.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Dictionary with access_token, refresh_token, token_expires_at
        """
        if mode is None:
            mode = sdk_config.trading_mode
        return self._tokens[mode]

    def authenticate(self, mode: str | None = None):
        """
        Perform OAuth2 Authorization Code flow authentication.

        Opens the browser for user login, runs a local callback server to capture
        the authorization code, exchanges it for tokens, and persists them.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Token payload dict with access_token, refresh_token, token_expires_at.

        Side Effects:
            - Launches browser window to the TradeStation consent page.
            - Starts a temporary HTTP server on the redirect URI port.
            - Writes token file for the chosen mode.

        Raises:
            AuthenticationError: if authentication fails.
        """
        if mode is None:
            mode = sdk_config.trading_mode
        logger.info("🔐 Starting TradeStation OAuth authentication...")
        logger.info("A browser window will open for you to log in")

        # Validate redirect URI host is loopback for security
        parsed_redirect = urlparse(self.redirect_uri)
        if parsed_redirect.hostname not in {"localhost", "127.0.0.1"}:
            raise AuthenticationError("Redirect URI must use localhost/127.0.0.1 for OAuth callback security")

        # Step 1: Build authorization URL with proper URL encoding
        state_token = py_secrets.token_urlsafe(24)
        OAuthCallbackHandler.expected_state = state_token

        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "audience": "https://api.tradestation.com",
            "scope": " ".join(OAUTH_SCOPES),
            "state": state_token,
        }

        # Use urlencode for proper URL encoding
        auth_request_url = f"{self.auth_url}?{urlencode(auth_params)}"

        logger.debug(f"Auth URL: {auth_request_url}")

        # Step 2: Start local server to capture callback
        redirect_port = 8888  # Default
        if ":" in self.redirect_uri:
            with contextlib.suppress(builtins.BaseException):
                redirect_port = int(self.redirect_uri.split(":")[2].split("/")[0])

        server_address = ("127.0.0.1", redirect_port)

        # Reset class variable before starting
        OAuthCallbackHandler.auth_code = None

        try:
            httpd = HTTPServer(server_address, OAuthCallbackHandler)
            logger.info(f"✅ Started OAuth callback server on http://localhost:{redirect_port}")
        except OSError as e:
            if "Address already in use" in str(e):
                logger.error(f"❌ Port {redirect_port} is already in use")
                logger.error(f"   Kill the process: lsof -ti :{redirect_port} | xargs kill -9")
                raise AuthenticationError(f"Port {redirect_port} in use. Cannot start OAuth server.") from e
            raise

        logger.info("🌐 Opening browser for TradeStation login...")

        # Start server in background thread
        server_thread = threading.Thread(target=httpd.handle_request, daemon=True)
        server_thread.start()

        # Open browser for user to authenticate
        webbrowser.open(auth_request_url)

        # Wait for authorization code (with timeout)
        timeout = 180  # 3 minutes
        start_time = time.time()
        logger.info("⏳ Waiting for you to complete login in browser...")

        while OAuthCallbackHandler.auth_code is None:
            if time.time() - start_time > timeout:
                raise AuthenticationError("Authentication timed out after 3 minutes. Please try again.")
            time.sleep(0.5)

        auth_code = OAuthCallbackHandler.auth_code
        logger.info("✅ Authorization code received from browser")

        # Step 3: Exchange authorization code for tokens
        token_payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "redirect_uri": self.redirect_uri,
        }

        try:
            logger.info("🔄 Exchanging authorization code for access token...")
            response = httpx.post(
                self.token_url,
                data=token_payload,
                headers={"Content-Type": "application/x-www-form-urlencoded"},
                timeout=30,
            )

            if response.status_code != 200:
                logger.error(f"Token exchange error response: {response.text}")
                raise AuthenticationError(f"Token exchange failed: {response.status_code} - {response.text}")

            token_data = response.json()

            self._tokens[mode]["access_token"] = token_data["access_token"]
            self._tokens[mode]["refresh_token"] = token_data.get("refresh_token")
            self._tokens[mode]["token_expires_at"] = (
                time.time() + token_data.get("expires_in", 86400) - 300
            )  # 5 min buffer
            self._last_mode = mode

            self._save_tokens(mode)
            logger.info(f"✅ Authentication successful for {mode} mode!")
            logger.info(f"   Access token expires in {token_data.get('expires_in', 0) // 3600} hours")

        except httpx.HTTPError as e:
            logger.error(f"❌ Token exchange failed: {e}")
            raise AuthenticationError(f"Failed to exchange authorization code for token: {e}") from e

    def refresh_access_token(self, mode: str | None = None):
        """
        Refresh the access token using the refresh token.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            Updated token payload dictionary with new expiry.

        Raises:
            TokenExpiredError: if refresh token is invalid or expired.
            AuthenticationError: for other authentication failures.
        """
        if mode is None:
            mode = sdk_config.trading_mode

        tokens = self.get_tokens(mode)
        if not tokens["refresh_token"]:
            logger.warning(f"No refresh token available for {mode} mode - need to re-authenticate")
            self.authenticate(mode)
            return

        logger.info(f"🔄 Refreshing access token for {mode} mode...")
        refresh_payload = {
            "grant_type": "refresh_token",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "refresh_token": tokens["refresh_token"],
        }

        try:
            response = httpx.post(self.token_url, data=refresh_payload, timeout=30)
            if response.status_code != 200:
                raise AuthenticationError(f"Token refresh failed: {response.status_code} - {response.text}")

            token_data = response.json()

            self._tokens[mode]["access_token"] = token_data["access_token"]
            self._tokens[mode]["refresh_token"] = token_data.get("refresh_token") or tokens["refresh_token"]
            self._tokens[mode]["token_expires_at"] = time.time() + token_data.get("expires_in", 86400) - 300
            self._last_mode = mode

            self._save_tokens(mode)
            logger.info(f"✅ Access token refreshed successfully for {mode} mode")

        except httpx.HTTPError as e:
            logger.warning(f"Token refresh failed for {mode} mode: {e}. Will re-authenticate.")
            self.authenticate(mode)

    def ensure_authenticated(self, mode: str | None = None):
        """
        Ensure we have a valid access token for specified mode.
        Refreshes if expired, or authenticates if no token exists.

        Args:
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            True when a valid token is present after any refresh/auth attempt.

        Raises:
            AuthenticationError: if authentication or refresh ultimately fails.
        """
        if mode is None:
            mode = sdk_config.trading_mode

        tokens = self.get_tokens(mode)
        if not tokens["access_token"]:
            logger.warning(f"No access token for {mode} mode - starting authentication")
            self.authenticate(mode)
        elif time.time() >= tokens["token_expires_at"]:
            logger.info(f"Access token expired for {mode} mode - refreshing")
            self.refresh_access_token(mode)
        else:
            self._last_mode = mode
        return True

    @property
    def last_mode(self) -> str:
        """Return the mode most recently used for authentication/refresh."""
        return self._last_mode


class Session:
    """
    TradeStation API Session

    Replaces external tastyware/tradestation SDK Session class.
    Provides HTTP clients and token management.

    Attributes:
        api_key: TradeStation client ID
        secret_key: TradeStation client secret
        refresh_token: Refresh token
        access_token: Access token
        id_token: ID token (optional)
        is_test: Whether using paper trading
        base_url: API base URL
        sync_client: httpx Client for sync requests
        async_client: httpx AsyncClient for async requests
    """

    def __init__(
        self,
        api_key: str,
        secret_key: str,
        refresh_token: str,
        access_token: str | None = None,
        id_token: str | None = None,
        token_lifetime: int = 1200,
        is_test: bool = False,
    ):
        """
        Initialize TradeStation Session.

        Args:
            api_key: TradeStation client ID
            secret_key: TradeStation client secret
            refresh_token: Refresh token
            access_token: Access token (optional, will refresh if not provided)
            id_token: ID token (optional)
            token_lifetime: Token lifetime in seconds (default: 1200 = 20 minutes)
            is_test: Whether using paper trading (default: False)
        """
        self.api_key = api_key
        self.secret_key = secret_key
        self.refresh_token = refresh_token
        self.access_token = access_token
        self.id_token = id_token
        self.token_lifetime = token_lifetime
        self.is_test = is_test

        # Set base URL based on mode
        if is_test:
            self.base_url = API_URL_SIM
        else:
            self.base_url = API_URL_V3

        # Initialize HTTP clients
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json",
        }
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        self.sync_client = httpx.Client(base_url=self.base_url, headers=headers, timeout=30.0)
        self.async_client = httpx.AsyncClient(base_url=self.base_url, headers=headers, timeout=30.0)

        # Refresh token if not provided
        if not self.access_token:
            self.refresh()

    def refresh(self) -> None:
        """
        Refresh the access token using the stored refresh token.
        """
        refresh_payload = {
            "grant_type": "refresh_token",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
            "refresh_token": self.refresh_token,
        }

        try:
            response = httpx.post(f"{OAUTH_URL}/oauth/token", data=refresh_payload, timeout=30)
            response.raise_for_status()
            token_data = response.json()

            # Update tokens
            self.access_token = token_data["access_token"]
            self.id_token = token_data.get("id_token", self.id_token)
            self.token_lifetime = int(token_data.get("expires_in", 1200))

            logger.debug(f"Refreshed token, expires in {self.token_lifetime} seconds.")

            # Update HTTP clients with new token
            auth_headers = {"Authorization": f"Bearer {self.access_token}"}
            self.sync_client.headers.update(auth_headers)
            self.async_client.headers.update(auth_headers)

        except httpx.HTTPError as e:
            logger.error(f"Token refresh failed: {e}")
            raise TokenExpiredError(f"Failed to refresh token: {e}") from e

    async def a_refresh(self) -> None:
        """
        Async version of refresh().
        """
        refresh_payload = {
            "grant_type": "refresh_token",
            "client_id": self.api_key,
            "client_secret": self.secret_key,
            "refresh_token": self.refresh_token,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(f"{OAUTH_URL}/oauth/token", data=refresh_payload, timeout=30)
                response.raise_for_status()
                token_data = response.json()

                # Update tokens
                self.access_token = token_data["access_token"]
                self.id_token = token_data.get("id_token", self.id_token)
                self.token_lifetime = int(token_data.get("expires_in", 1200))

                logger.debug(f"Refreshed token, expires in {self.token_lifetime} seconds.")

                # Update HTTP clients with new token
                auth_headers = {"Authorization": f"Bearer {self.access_token}"}
                self.sync_client.headers.update(auth_headers)
                self.async_client.headers.update(auth_headers)

        except httpx.HTTPError as e:
            logger.error(f"Token refresh failed: {e}")
            raise TokenExpiredError(f"Failed to refresh token: {e}") from e

    def revoke(self) -> None:
        """
        Revoke all valid refresh tokens.
        """
        try:
            response = httpx.post(
                f"{OAUTH_URL}/oauth/revoke",
                data={
                    "client_id": self.api_key,
                    "client_secret": self.secret_key,
                    "token": self.refresh_token,
                },
                timeout=30,
            )
            response.raise_for_status()
            logger.debug("Successfully revoked refresh tokens!")
        except httpx.HTTPError as e:
            logger.warning(f"Token revocation failed: {e}")

    async def a_revoke(self) -> None:
        """
        Async version of revoke().
        """
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{OAUTH_URL}/oauth/revoke",
                    data={
                        "client_id": self.api_key,
                        "client_secret": self.secret_key,
                        "token": self.refresh_token,
                    },
                    timeout=30,
                )
                response.raise_for_status()
                logger.debug("Successfully revoked refresh tokens!")
        except httpx.HTTPError as e:
            logger.warning(f"Token revocation failed: {e}")

    def _get(self, url: str, **kwargs) -> Any:
        """
        Make a GET request (internal method).

        Args:
            url: Endpoint URL (relative to base_url)
            **kwargs: Additional request arguments

        Returns:
            Parsed JSON response
        """
        response = self.sync_client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    async def _a_get(self, url: str, **kwargs) -> Any:
        """
        Make an async GET request (internal method).

        Args:
            url: Endpoint URL (relative to base_url)
            **kwargs: Additional request arguments

        Returns:
            Parsed JSON response
        """
        response = await self.async_client.get(url, **kwargs)
        response.raise_for_status()
        return response.json()

    @property
    def user_info(self) -> dict[str, str]:
        """
        Contains user info from ID token.

        Returns:
            Dictionary with user info (name, email, etc.) or empty dict if no ID token
        """
        if self.id_token is None:
            return {}
        try:
            return jwt.decode(self.id_token, options={"verify_signature": False})
        except Exception as e:
            logger.warning(f"Failed to decode ID token: {e}")
            return {}

    def serialize(self) -> str:
        """
        Serialize the session to a string for storage.

        Returns:
            JSON string representation of session
        """
        import json

        attrs = {
            "api_key": self.api_key,
            "secret_key": self.secret_key,
            "refresh_token": self.refresh_token,
            "access_token": self.access_token,
            "id_token": self.id_token,
            "token_lifetime": self.token_lifetime,
            "is_test": self.is_test,
        }
        return json.dumps(attrs)

    @classmethod
    def deserialize(cls, serialized: str) -> "Session":
        """
        Create a new Session object from a serialized string.

        Args:
            serialized: JSON string from serialize()

        Returns:
            New Session instance
        """
        import json

        deserialized = json.loads(serialized)
        return cls(**deserialized)

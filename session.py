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
import importlib.util
import json
import os
import platform
import secrets as py_secrets
import socket
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse

import httpx
import jwt

from .config import sdk_config
from .exceptions import AuthenticationError, TokenExpiredError
from .utils.logger import setup_logger

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
# Can be overridden via TRADESTATION_TOKEN_DIR environment variable
_token_dir_env = os.getenv("TRADESTATION_TOKEN_DIR")
if _token_dir_env:
    TOKEN_DIR = Path(_token_dir_env)
else:
    TOKEN_DIR = Path(__file__).parent.parent.parent.parent / "config"
TOKEN_DIR.mkdir(exist_ok=True, mode=0o700)  # Ensure config directory exists with restrictive permissions
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


def _find_available_port(start_port: int = 8888, end_port: int = 8898) -> int:
    """
    Find an available port in the specified range.

    Args:
        start_port: Starting port number (default: 8888)
        end_port: Ending port number (default: 8898)

    Returns:
        Available port number

    Raises:
        AuthenticationError: If no port is available in the range
    """
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                sock.bind(("127.0.0.1", port))
                return port
        except OSError:
            # Port is in use, try next
            continue

    raise AuthenticationError(
        f"No available port in range {start_port}-{end_port}. "
        f"Please free up a port or set TRADESTATION_REDIRECT_URI to use a different port."
    )


def _try_keychain_storage() -> bool:
    """
    Check if keychain/secret-service storage is available.

    Returns:
        True if keychain storage is available, False otherwise
    """
    # Check for keychain availability (optional dependency)
    try:
        system = platform.system()
        if system == "Darwin":  # macOS
            return importlib.util.find_spec("keyring") is not None
        elif system == "Linux":
            return (
                importlib.util.find_spec("keyring") is not None
                and importlib.util.find_spec("keyring.backends.SecretService") is not None
            )
        elif system == "Windows":
            return importlib.util.find_spec("keyring") is not None
    except Exception:
        pass
    return False


class TokenManager:
    """
    Manages OAuth tokens for PAPER and LIVE modes.

    Handles token storage, loading, authentication, and refresh.

    Persistence:
    - Tokens are stored in JSON files under `config/` (default) or keychain if available:
      - PAPER → tokens_paper.json or keychain entry
      - LIVE  → tokens_live.json or keychain entry
    - Token storage location can be configured via TRADESTATION_TOKEN_STORAGE env var:
      - "keychain" - Use system keychain (requires keyring package)
      - "file" - Use file storage (default, encrypted if keyring available)
      - "auto" - Auto-detect best option (default)

    Safety:
    - Files are git-ignored; do not store secrets in version control.
    - File permissions are automatically restricted (chmod 600).
    - Keychain storage is preferred when available for better security.
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

        # Token storage configuration
        storage_pref = os.getenv("TRADESTATION_TOKEN_STORAGE", "auto").lower()
        self._use_keychain = False
        if storage_pref == "keychain":
            if _try_keychain_storage():
                self._use_keychain = True
                logger.info("Using keychain storage for tokens (TRADESTATION_TOKEN_STORAGE=keychain)")
            else:
                logger.warning(
                    "Keychain storage requested but not available. Install 'keyring' package. "
                    "Falling back to file storage."
                )
        elif storage_pref == "auto":
            if _try_keychain_storage():
                self._use_keychain = True
                logger.debug("Auto-detected keychain storage available, using keychain")
            else:
                logger.debug("Keychain not available, using file storage")

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
        Load saved tokens from keychain or local files for both modes.

        Returns:
            True if any tokens loaded successfully, False otherwise
        """
        loaded = False

        if self._use_keychain:
            # Try loading from keychain
            try:
                import keyring

                service_name = "TradeStationSDK"
                for mode in ["PAPER", "LIVE"]:
                    try:
                        token_json = keyring.get_password(service_name, f"tokens_{mode.lower()}")
                        if token_json:
                            data = json.loads(token_json)
                            self._tokens[mode]["access_token"] = data.get("access_token")
                            self._tokens[mode]["refresh_token"] = data.get("refresh_token")
                            self._tokens[mode]["token_expires_at"] = data.get("expires_at", 0)
                            logger.info(f"Loaded {mode} tokens from keychain")
                            loaded = True
                    except Exception as e:
                        logger.debug(f"Failed to load {mode} tokens from keychain: {e}")
            except ImportError:
                logger.warning("keyring package not available, falling back to file storage")
                self._use_keychain = False

        # Fallback to file storage
        if not self._use_keychain:
            TOKEN_DIR.mkdir(exist_ok=True, mode=0o700)

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
        Save tokens to keychain or local file for persistence.

        Args:
            mode: "PAPER" or "LIVE". If None, saves tokens for the mode specified in sdk_config.trading_mode
        """
        if mode is None:
            mode = sdk_config.trading_mode

        token_data = {
            "access_token": self._tokens[mode]["access_token"],
            "refresh_token": self._tokens[mode]["refresh_token"],
            "expires_at": self._tokens[mode]["token_expires_at"],
        }

        if self._use_keychain:
            # Save to keychain
            try:
                import keyring

                service_name = "TradeStationSDK"
                keyring.set_password(service_name, f"tokens_{mode.lower()}", json.dumps(token_data))
                logger.debug(f"Tokens saved to keychain for {mode} mode")
                return
            except ImportError:
                logger.warning("keyring package not available, falling back to file storage")
                self._use_keychain = False
            except Exception as e:
                logger.warning(f"Failed to save tokens to keychain: {e}. Falling back to file storage.")
                self._use_keychain = False

        # Fallback to file storage
        TOKEN_DIR.mkdir(exist_ok=True, mode=0o700)
        token_file = TOKEN_FILE_PAPER if mode == "PAPER" else TOKEN_FILE_LIVE

        with open(token_file, "w") as f:
            json.dump(token_data, f, indent=2)

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

        # Step 1: Determine port for OAuth callback server
        # Extract port from redirect URI or use default
        redirect_port = 8888  # Default
        port_from_uri = None

        if ":" in self.redirect_uri:
            with contextlib.suppress(builtins.BaseException):
                port_from_uri = int(self.redirect_uri.split(":")[2].split("/")[0])

        # Check if port is explicitly set via environment variable
        env_port = os.getenv("TRADESTATION_OAUTH_PORT")
        if env_port:
            try:
                redirect_port = int(env_port)
                logger.info(f"Using OAuth port from TRADESTATION_OAUTH_PORT: {redirect_port}")
            except ValueError:
                logger.warning(f"Invalid TRADESTATION_OAUTH_PORT value: {env_port}, using auto-selection")
                redirect_port = None
        elif port_from_uri:
            redirect_port = port_from_uri
        else:
            # Auto-select port from range 8888-8898
            redirect_port = None

        # Reset class variable before starting
        OAuthCallbackHandler.auth_code = None

        # Step 2: Start local server to capture callback (with auto-port selection if needed)
        httpd = None
        port_was_auto_selected = False

        if redirect_port is not None:
            # Use specified port
            server_address = ("127.0.0.1", redirect_port)
            try:
                httpd = HTTPServer(server_address, OAuthCallbackHandler)
                logger.info(f"✅ Started OAuth callback server on http://localhost:{redirect_port}")
            except OSError as e:
                if "Address already in use" in str(e) or "already in use" in str(e).lower():
                    logger.warning(f"⚠️  Port {redirect_port} is in use, attempting auto-selection...")
                    redirect_port = None  # Fall through to auto-selection
                else:
                    raise

        if redirect_port is None:
            # Auto-select port from range
            redirect_port = _find_available_port(8888, 8898)
            server_address = ("127.0.0.1", redirect_port)
            httpd = HTTPServer(server_address, OAuthCallbackHandler)
            port_was_auto_selected = True
            logger.info(f"✅ Started OAuth callback server on http://localhost:{redirect_port} (auto-selected)")

        # If we still don't have a server, something went wrong
        if httpd is None:
            raise AuthenticationError(
                "Failed to start OAuth callback server. "
                "Please ensure ports 8888-8898 are available or set TRADESTATION_OAUTH_PORT."
            )

        # Step 3: Update redirect_uri if port was auto-selected or changed
        # This ensures the redirect_uri sent to TradeStation matches the port we're listening on
        if port_was_auto_selected or (port_from_uri is not None and redirect_port != port_from_uri):
            parsed = urlparse(self.redirect_uri)
            # Update redirect_uri to match the actual port being used
            self.redirect_uri = f"{parsed.scheme}://{parsed.hostname}:{redirect_port}{parsed.path}"

            if port_was_auto_selected:
                logger.warning(
                    f"⚠️  OAuth port auto-selected to {redirect_port} (original: {port_from_uri or 8888}). "
                    f"Ensure 'http://localhost:{redirect_port}/callback' is registered in TradeStation Developer Portal. "
                    f"See https://developer.tradestation.com for redirect URI configuration."
                )
            elif redirect_port != port_from_uri:
                logger.warning(
                    f"⚠️  OAuth port changed from {port_from_uri} to {redirect_port} due to port conflict. "
                    f"Ensure 'http://localhost:{redirect_port}/callback' is registered in TradeStation Developer Portal."
                )

        # Step 4: Build authorization URL with updated redirect_uri
        state_token = py_secrets.token_urlsafe(24)
        OAuthCallbackHandler.expected_state = state_token

        auth_params = {
            "response_type": "code",
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,  # Use updated redirect_uri that matches selected port
            "audience": "https://api.tradestation.com",
            "scope": " ".join(OAUTH_SCOPES),
            "state": state_token,
        }

        # Use urlencode for proper URL encoding
        auth_request_url = f"{self.auth_url}?{urlencode(auth_params)}"

        logger.debug(f"Auth URL: {auth_request_url}")

        logger.info("🌐 Opening browser for TradeStation login...")
        if port_was_auto_selected:
            logger.info(
                f"📝 Note: Using redirect URI '{self.redirect_uri}'. "
                f"If authentication fails, ensure this URI is registered in TradeStation Developer Portal."
            )

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

        # Step 5: Exchange authorization code for tokens
        # Use the same redirect_uri that was sent in the OAuth request (may have been updated)
        token_payload = {
            "grant_type": "authorization_code",
            "client_id": self.client_id,
            "client_secret": self.client_secret,
            "code": auth_code,
            "redirect_uri": self.redirect_uri,  # Must match what was sent in OAuth request
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

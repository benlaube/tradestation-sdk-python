"""
HTTP Client for TradeStation API

Centralizes HTTP concerns for the SDK: base URL selection (PAPER/LIVE), token
injection, structured logging, error parsing, retry/backoff, and NDJSON HTTP
streaming. All higher-level operation modules delegate network I/O to this
client to keep business logic clean.

Dependencies: requests, time, typing
"""

import asyncio
import json
import time
from typing import Any

import httpx
import requests

from ..config import sdk_config
from ..exceptions import (
    AuthenticationError,
    ErrorDetails,
    InvalidRequestError,
    NetworkError,
    NonRecoverableError,
    RateLimitError,
    RecoverableError,
    TradeStationAPIError,
)
from .logger import log_with_context, setup_logger
from ..session import TokenManager

logger = setup_logger(__name__, sdk_config.log_level)

# Base URLs for both modes
PAPER_BASE_URL = "https://sim-api.tradestation.com/v3"
LIVE_BASE_URL = "https://api.tradestation.com/v3"


def get_base_url(mode: str | None = None) -> str:
    """
    Get base URL for specified mode.

    Args:
        mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

    Returns:
        Base URL string
    """
    if mode is None:
        mode = sdk_config.trading_mode
    return PAPER_BASE_URL if mode == "PAPER" else LIVE_BASE_URL


def parse_api_error_response(response: requests.Response | Any) -> ErrorDetails:
    """
    Parse TradeStation API error response into structured ErrorDetails.

    Handles various error response formats:
    - {"Error": "message", "Code": "code"}
    - {"Errors": [{"Error": "...", "Code": "..."}]}
    - {"Message": "error message"}
    - {"error": "message", "error_description": "description"}
    - Standard HTTP error responses

    Args:
        response: requests.Response or httpx.Response-like object with error status

    Returns:
        ErrorDetails object with parsed error information
    """
    status_code = getattr(response, "status_code", 500)
    details = ErrorDetails(response_status=status_code, code=f"HTTP_{status_code}")

    # Try to parse JSON response body
    try:
        error_body = response.json()
        details.response_body = error_body

        # Format 1: {"Error": "message", "Code": "code"}
        if "Error" in error_body and "Code" in error_body:
            details.api_error_code = str(error_body.get("Code", ""))
            details.api_error_message = str(error_body.get("Error", ""))
            details.message = error_body.get("Error", "")

        # Format 2: {"Errors": [{"Error": "...", "Code": "..."}]}
        elif "Errors" in error_body and isinstance(error_body["Errors"], list):
            errors = error_body["Errors"]
            if errors:
                first_error = errors[0]
                if isinstance(first_error, dict):
                    details.api_error_code = str(first_error.get("Code", ""))
                    details.api_error_message = str(first_error.get("Error", ""))
                    details.message = first_error.get("Error", "")
                else:
                    details.message = str(first_error)

        # Format 3: {"Message": "error message"}
        elif "Message" in error_body:
            details.message = str(error_body.get("Message", ""))
            details.api_error_message = details.message

        # Format 4: OAuth-style {"error": "message", "error_description": "description"}
        elif "error" in error_body:
            details.api_error_code = str(error_body.get("error", ""))
            details.api_error_message = str(error_body.get("error_description", error_body.get("error", "")))
            details.message = details.api_error_message

        # Format 5: Generic message field
        elif "message" in error_body:
            details.message = str(error_body.get("message", ""))
            details.api_error_message = details.message

        # Format 6: Try to extract any string field as message
        else:
            # Look for common error message fields
            for key in ["error", "errorMessage", "error_message", "detail", "details"]:
                if key in error_body:
                    details.message = str(error_body[key])
                    details.api_error_message = details.message
                    break

            # If still no message, use the whole body as string representation
            if not details.message:
                details.message = f"API returned error: {error_body}"

    except (json.JSONDecodeError, ValueError):
        # Not JSON, try to get text
        try:
            error_text = getattr(response, "text", str(response))
            details.message = error_text[:500] if len(error_text) > 500 else error_text
            details.api_error_message = details.message
        except Exception:
            details.message = f"HTTP {status_code} error (unable to parse response)"

    # Set code based on status code if not set
    if not details.api_error_code:
        if status_code == 400:
            details.code = "INVALID_REQUEST"
        elif status_code == 401:
            details.code = "AUTHENTICATION_ERROR"
        elif status_code == 403:
            details.code = "FORBIDDEN"
        elif status_code == 404:
            details.code = "NOT_FOUND"
        elif status_code == 429:
            details.code = "RATE_LIMIT_ERROR"
        elif status_code >= 500:
            details.code = "SERVER_ERROR"
        else:
            details.code = "API_ERROR"

    return details


class HTTPClient:
    """
    HTTP client for TradeStation API requests.

    Handles authentication, request/response logging, and error handling.
    Supports both synchronous (requests) and asynchronous (httpx) operations.
    Renamed from BaseAPIClient for SDK clarity.

    By default, uses synchronous requests library for backward compatibility.
    Set use_async=True to enable async operations with httpx.
    """

    def __init__(
        self,
        token_manager: TokenManager,
        enable_full_logging: bool = False,
        max_retries: int = 3,
        retry_delay: float = 1.0,
        max_retry_delay: float = 60.0,
        enable_retry: bool = True,
        use_async: bool = False,
    ):
        """
        Initialize API client.

        Args:
            token_manager: TokenManager instance for authentication
            enable_full_logging: If True, logs full request/response bodies without truncation.
                               Can also be set via TRADESTATION_FULL_LOGGING environment variable.
            max_retries: Maximum number of retry attempts for recoverable errors (default: 3)
            retry_delay: Initial retry delay in seconds (default: 1.0)
            max_retry_delay: Maximum retry delay in seconds (default: 60.0)
            enable_retry: Enable automatic retry for recoverable errors (default: True)
            use_async: If True, use httpx for async operations. Default False for backward compatibility.
        """
        self.token_manager = token_manager
        self.use_async = use_async

        # Initialize async client if async mode is enabled
        self._async_client: httpx.AsyncClient | None = None
        if self.use_async:
            self._async_client = httpx.AsyncClient(timeout=30.0, limits=httpx.Limits(max_keepalive_connections=10))

        # Check environment variable as fallback
        import os

        env_full_logging = os.getenv("TRADESTATION_FULL_LOGGING", "").lower() in ("true", "1", "yes")
        prod_flag = os.getenv("ENVIRONMENT", "").lower() in ("prod", "production")
        self.enable_full_logging = False if prod_flag else (enable_full_logging or env_full_logging)

        # Retry configuration
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self.max_retry_delay = max_retry_delay
        self.enable_retry = enable_retry

    def _sanitize_data(self, data: dict[str, Any] | None) -> dict[str, Any] | None:
        """
        Sanitize sensitive fields in data dictionary.

        Args:
            data: Dictionary to sanitize

        Returns:
            Sanitized dictionary with sensitive fields redacted
        """
        if not data or not isinstance(data, dict):
            return data

        sanitized = data.copy()
        sensitive_keys = ["client_secret", "refresh_token", "code", "password", "access_token", "Authorization"]

        for key in sensitive_keys:
            if key in sanitized:
                sanitized[key] = "***REDACTED***"

        # Also check nested dicts
        for key, value in sanitized.items():
            if isinstance(value, dict):
                sanitized[key] = self._sanitize_data(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_data(item) if isinstance(item, dict) else item for item in value]

        return sanitized

    def _log_request(self, method: str, endpoint: str, params: dict | None = None, json_data: dict | None = None):
        """
        Log API request with optional full body logging.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: Request body
        """
        sanitized_params = self._sanitize_data(params) if params else params
        sanitized_json = self._sanitize_data(json_data) if json_data else json_data

        sensitive_endpoint = any(
            key in endpoint.lower() for key in ["oauth", "auth", "token", "orderexecution", "orders"]
        )

        if sensitive_endpoint:
            body_repr = "<redacted>"
        elif self.enable_full_logging:
            body_repr = sanitized_json
        else:
            body_str = str(sanitized_json) if sanitized_json else "None"
            if len(body_str) > 500:
                body_str = body_str[:500] + "... (truncated)"
            body_repr = body_str

        log_with_context(
            logger,
            "debug",
            f"API Request: {method} {endpoint} | Params: {sanitized_params} | Body: {body_repr}",
            source="bot",
            action="api_request",
            component="tradestation_api",
        )

    def _log_response(
        self, method: str, endpoint: str, response: requests.Response, elapsed_time: float, full: bool = False
    ):
        """
        Log API response with optional full body logging.

        Args:
            method: HTTP method
            endpoint: API endpoint
            response: Response object
            elapsed_time: Request execution time in seconds
            full: If True, log full response body (overrides enable_full_logging)
        """
        response_size = len(response.content) if response.content else 0
        log_full = full or self.enable_full_logging

        try:
            if log_full:
                # Full logging - try to parse and log complete JSON
                try:
                    response_json = response.json()
                    body_str = json.dumps(response_json, indent=2)
                except (json.JSONDecodeError, ValueError):
                    body_str = response.text
            else:
                # Standard logging - truncate
                body_str = response.text[:500] if response.text else "None"
                if response.text and len(response.text) > 500:
                    body_str += "... (truncated)"
        except Exception:
            body_str = "Unable to read response body"

        log_with_context(
            logger,
            "debug",
            f"API Response: {method} {endpoint} | "
            f"Status: {response.status_code} | "
            f"Time: {elapsed_time:.3f}s | "
            f"Size: {response_size} bytes | "
            f"Body: {body_str}",
            source="bot",
            action="api_response",
            component="tradestation_api",
        )

        # Log errors at warning level
        if response.status_code >= 400:
            try:
                error_body = response.json()
                log_with_context(
                    logger,
                    "warning",
                    f"API Error Response: {method} {endpoint} | "
                    f"Status: {response.status_code} | "
                    f"Error: {error_body if log_full else str(error_body)[:500]}",
                    source="bot",
                    action="api_error",
                    component="tradestation_api",
                )
            except Exception:
                error_text = response.text[:500] if not log_full else response.text
                log_with_context(
                    logger,
                    "warning",
                    f"API Error Response: {method} {endpoint} | Status: {response.status_code} | Body: {error_text}",
                    source="bot",
                    action="api_error",
                    component="tradestation_api",
                )

    def _build_error_context(
        self,
        method: str,
        endpoint: str,
        params: dict | None,
        json_data: dict | None,
        response: requests.Response | None,
        mode: str | None,
    ) -> ErrorDetails:
        """
        Build error context dictionary with request/response details.

        Args:
            method: HTTP method
            endpoint: API endpoint
            params: Query parameters
            json_data: Request body
            response: Response object (if available)
            mode: Trading mode (PAPER/LIVE)

        Returns:
            ErrorDetails object with context populated
        """
        details = ErrorDetails(
            request_method=method,
            request_endpoint=endpoint,
            request_params=self._sanitize_data(params) if params else None,
            request_body=self._sanitize_data(json_data) if json_data else None,
            mode=mode,
        )

        if response:
            details.response_status = response.status_code
            try:
                details.response_body = response.json()
            except (json.JSONDecodeError, ValueError):
                try:
                    details.response_body = {"text": response.text}
                except Exception:
                    pass

        return details

    def _make_request_internal(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_data: dict | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Internal method that performs a single API request without retry logic.

        This is the core request implementation that is wrapped by make_request()
        with retry logic for recoverable errors.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json_data: JSON body for POST requests
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            API response as dictionary

        Raises:
            RecoverableError: For errors that can be retried (network, rate limit, server errors)
            NonRecoverableError: For errors that should not be retried (auth, invalid request)
        """
        if mode is None:
            mode = sdk_config.trading_mode

        self.token_manager.ensure_authenticated(mode)

        base_url = get_base_url(mode)
        tokens = self.token_manager.get_tokens(mode)
        url = f"{base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Content-Type": "application/json",
        }

        # Log request using helper method
        self._log_request(method, endpoint, params, json_data)

        # Track execution time
        start_time = time.time()

        try:
            # Set timeout for API requests (30 seconds for order operations, 10 seconds for others)
            # Order operations may take longer due to TradeStation API processing
            timeout = 30 if endpoint.startswith("orderexecution") else 10
            response = requests.request(method, url, headers=headers, params=params, json=json_data, timeout=timeout)
            elapsed_time = time.time() - start_time

            # Log response using helper method
            self._log_response(method, endpoint, response, elapsed_time)

            # Check for errors and parse them
            if response.status_code >= 400:
                # Parse error response into ErrorDetails
                error_details = parse_api_error_response(response)

                # Merge with request context
                context_details = self._build_error_context(method, endpoint, params, json_data, response, mode)
                error_details.request_method = context_details.request_method
                error_details.request_endpoint = context_details.request_endpoint
                error_details.request_params = context_details.request_params
                error_details.request_body = context_details.request_body
                error_details.mode = context_details.mode

                # Determine exception type based on status code
                # Categorize as recoverable or non-recoverable for retry logic
                if response.status_code == 401:
                    raise NonRecoverableError(error_details)  # Auth errors are non-recoverable
                elif response.status_code == 403:
                    raise NonRecoverableError(error_details)  # Forbidden errors are non-recoverable
                elif response.status_code == 400:
                    raise NonRecoverableError(error_details)  # Invalid requests are non-recoverable
                elif response.status_code == 404:
                    raise NonRecoverableError(error_details)  # Not found errors are non-recoverable
                elif response.status_code == 429:
                    # Rate limit errors are recoverable (can retry after backoff)
                    raise RecoverableError(error_details)
                elif response.status_code >= 500:
                    # Server errors are recoverable (temporary failures)
                    raise RecoverableError(error_details)
                else:
                    # Other 4xx errors are non-recoverable
                    raise NonRecoverableError(error_details)

            # Log successful responses at info level for important operations
            if method in ["POST", "PUT", "DELETE"] or "order" in endpoint.lower():
                log_with_context(
                    logger,
                    "info",
                    f"API Success: {method} {endpoint} | Status: {response.status_code} | Time: {elapsed_time:.3f}s",
                    source="bot",
                    action="api_response",
                    component="tradestation_api",
                )

            return response.json()

        except (
            TradeStationAPIError,
            AuthenticationError,
            RateLimitError,
            InvalidRequestError,
            NetworkError,
            RecoverableError,
            NonRecoverableError,
        ):
            # Re-raise our custom exceptions as-is
            raise
        except requests.HTTPError as e:
            elapsed_time = time.time() - start_time

            # Build error context for HTTP errors
            error_details = self._build_error_context(
                method, endpoint, params, json_data, e.response if hasattr(e, "response") else None, mode
            )
            error_details.message = str(e)
            error_details.code = "HTTP_ERROR"

            # Determine exception type (categorize as recoverable or non-recoverable)
            if hasattr(e, "response") and e.response:
                if e.response.status_code == 401 or e.response.status_code == 403:
                    raise NonRecoverableError(error_details) from e  # Auth errors are non-recoverable
                elif e.response.status_code == 400:
                    raise NonRecoverableError(error_details) from e  # Invalid requests are non-recoverable
                elif e.response.status_code == 404:
                    raise NonRecoverableError(error_details) from e  # Not found errors are non-recoverable
                elif e.response.status_code == 429:
                    raise RecoverableError(error_details) from e  # Rate limit errors are recoverable
                elif e.response.status_code >= 500:
                    raise RecoverableError(error_details) from e  # Server errors are recoverable

            # Parse response if available
            if hasattr(e, "response") and e.response:
                parsed_details = parse_api_error_response(e.response)
                error_details.api_error_code = parsed_details.api_error_code
                error_details.api_error_message = parsed_details.api_error_message
                if parsed_details.message:
                    error_details.message = parsed_details.message

            log_with_context(
                logger,
                "error",
                f"API Request Failed: {method} {endpoint} | "
                f"Status: {e.response.status_code if hasattr(e, 'response') else 'Unknown'} | "
                f"Time: {elapsed_time:.3f}s | "
                f"Error: {error_details.to_human_readable()}",
                source="bot",
                action="api_error",
                component="tradestation_api",
            )

            raise NonRecoverableError(error_details) from e  # Default to non-recoverable for unknown errors
        except requests.exceptions.RequestException as e:
            elapsed_time = time.time() - start_time

            # Build error context for network errors
            error_details = self._build_error_context(method, endpoint, params, json_data, None, mode)
            error_details.message = f"Network error: {str(e)}"
            error_details.code = "NETWORK_ERROR"

            log_with_context(
                logger,
                "error",
                f"API Request Network Error: {method} {endpoint} | Time: {elapsed_time:.3f}s | Error: {str(e)}",
                source="bot",
                action="api_error",
                component="tradestation_api",
            )

            # Network errors are recoverable (can retry)
            raise RecoverableError(error_details) from e
        except Exception as e:
            elapsed_time = time.time() - start_time

            # Build error context for unexpected errors
            error_details = self._build_error_context(method, endpoint, params, json_data, None, mode)
            error_details.message = f"Unexpected error: {str(e)}"
            error_details.code = "UNEXPECTED_ERROR"

            log_with_context(
                logger,
                "error",
                f"API Request Exception: {method} {endpoint} | Time: {elapsed_time:.3f}s | Error: {str(e)}",
                source="bot",
                action="api_error",
                component="tradestation_api",
            )

            # Unexpected errors default to recoverable (may be transient)
            raise RecoverableError(error_details) from e

    def make_request(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_data: dict | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Make an authenticated API request with automatic retry logic and logging.

        Automatically retries recoverable errors (network failures, rate limits, server errors)
        with exponential backoff. Non-recoverable errors (authentication, invalid requests)
        are not retried and raised immediately.

        Automatically logs all API requests and responses including:
        - Request method, endpoint, parameters, and body (sensitive data redacted)
        - Response status code, execution time, and response size
        - Retry attempts with backoff delays
        - Errors and exceptions with full details

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json_data: JSON body for POST requests
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            API response as dictionary

        Raises:
            RecoverableError: For errors that can be retried (raised after max retries exceeded)
            NonRecoverableError: For errors that should not be retried (auth, invalid request)

        Dependencies: requests, time, logger
        """
        if not self.enable_retry:
            # Retry disabled, make single request
            return self._make_request_internal(method, endpoint, params, json_data, mode)

        # Retry logic with exponential backoff
        current_retry_delay = self.retry_delay
        attempt = 0

        while attempt <= self.max_retries:
            try:
                return self._make_request_internal(method, endpoint, params, json_data, mode)
            except NonRecoverableError:
                # Non-recoverable errors should not be retried
                raise
            except RecoverableError as e:
                attempt += 1

                if attempt > self.max_retries:
                    # Max retries exceeded, log and raise
                    log_with_context(
                        logger,
                        "error",
                        f"API Request Failed After {self.max_retries} Retries: {method} {endpoint} | "
                        f"Error: {e.details.to_human_readable()}",
                        source="bot",
                        action="api_retry_exhausted",
                        component="tradestation_api",
                    )
                    raise

                # Log retry attempt with context
                error_type = e.details.code or "UNKNOWN_ERROR"
                status_code = e.details.response_status or "N/A"
                retry_info = (
                    f"Retry {attempt}/{self.max_retries} for {method} {endpoint} | "
                    f"Error: {error_type} (Status: {status_code}) | "
                    f"Waiting {current_retry_delay:.1f}s before retry"
                )

                log_with_context(
                    logger,
                    "warning",
                    retry_info,
                    source="bot",
                    action="api_retry",
                    component="tradestation_api",
                )

                # Handle rate limit errors with special backoff
                if status_code == 429:
                    # Check for Retry-After header in response body
                    retry_after = None
                    if e.details.response_body and isinstance(e.details.response_body, dict):
                        retry_after = e.details.response_body.get("RetryAfter") or e.details.response_body.get(
                            "retry_after"
                        )

                    if retry_after:
                        # Use server-specified retry delay
                        wait_time = float(retry_after)
                        log_with_context(
                            logger,
                            "info",
                            f"Rate limit hit. Using server-specified Retry-After: {wait_time}s",
                            source="bot",
                            action="api_rate_limit",
                            component="tradestation_api",
                        )
                        time.sleep(wait_time)
                        current_retry_delay = self.retry_delay  # Reset to initial delay after server delay
                    else:
                        # Use exponential backoff for rate limits
                        time.sleep(current_retry_delay)
                        current_retry_delay = min(current_retry_delay * 2, self.max_retry_delay)
                else:
                    # Use exponential backoff for other recoverable errors
                    time.sleep(current_retry_delay)
                    current_retry_delay = min(current_retry_delay * 2, self.max_retry_delay)

                # Ensure authentication is still valid before retry
                if mode is None:
                    mode = sdk_config.trading_mode
                self.token_manager.ensure_authenticated(mode)

    def stream_data(self, endpoint: str, params: dict | None = None, mode: str | None = None):
        """
        Make an authenticated HTTP streaming request to TradeStation API.

        TradeStation API v3 supports HTTP Streaming (long-lived HTTP connections)
        for real-time data. This keeps the connection open and streams JSON objects
        as they arrive (newline-delimited JSON or chunked transfer).

        Args:
            endpoint: API endpoint (without base URL)
            params: Query parameters
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Yields:
            Dictionary objects as they arrive in the stream

        Dependencies: requests, json

        Example:
            for quote in client.stream_data("marketdata/stream/quotechanges", {"symbols": "MNQZ25"}):
                print(quote)
        """
        if mode is None:
            mode = sdk_config.trading_mode

        self.token_manager.ensure_authenticated(mode)

        base_url = get_base_url(mode)
        tokens = self.token_manager.get_tokens(mode)
        url = f"{base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Accept": "application/json",
        }

        logger.info(f"Starting HTTP stream: GET {endpoint} (mode: {mode})")

        try:
            # Use stream=True for HTTP streaming (long-lived connection, no timeout)
            response = requests.get(
                url,
                headers=headers,
                params=params,
                stream=True,
                timeout=None,  # No timeout for long-lived streams
            )
            response.raise_for_status()

            # Stream JSON objects as they arrive (newline-delimited JSON or chunked)
            buffer = ""
            for chunk in response.iter_content(chunk_size=8192, decode_unicode=False):
                if not chunk:
                    continue

                # Decode bytes to string if needed
                if isinstance(chunk, bytes):
                    chunk = chunk.decode("utf-8", errors="replace")

                buffer += chunk

                # Parse newline-delimited JSON (NDJSON)
                # TradeStation API sends one JSON object per line
                while "\n" in buffer:
                    line, buffer = buffer.split("\n", 1)
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        quote_data = json.loads(line)

                        # Handle StreamStatus messages (special control messages)
                        if isinstance(quote_data, dict) and "StreamStatus" in quote_data:
                            status = quote_data.get("StreamStatus")
                            if status == "EndSnapshot":
                                logger.debug("Received EndSnapshot - initial snapshot complete")
                                continue
                            elif status == "GoAway":
                                logger.warning("Received GoAway - stream ending, will reconnect")
                                break
                            elif status == "Error":
                                error_msg = quote_data.get("Message", "Unknown error")
                                logger.error(f"Stream error: {error_msg}")
                                raise Exception(f"Stream error: {error_msg}")

                        # Yield regular quote data
                        yield quote_data

                    except json.JSONDecodeError as e:
                        logger.debug(f"Failed to parse JSON line: {line[:100]} - {e}")
                        # Continue - might be incomplete or malformed
                        continue

        except requests.exceptions.RequestException as e:
            logger.error(f"HTTP stream error for {endpoint}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error in HTTP stream {endpoint}: {e}")
            raise

    async def make_request_async(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_data: dict | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Make an authenticated API request asynchronously using httpx.

        This method provides non-blocking I/O for high-concurrency applications.
        Automatically retries recoverable errors with exponential backoff.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json_data: JSON body for POST requests
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            API response as dictionary

        Raises:
            RecoverableError: For errors that can be retried (raised after max retries exceeded)
            NonRecoverableError: For errors that should not be retried (auth, invalid request)

        Note:
            This method requires use_async=True when initializing HTTPClient.
            For synchronous operations, use make_request() instead.

        Dependencies: httpx, asyncio
        """
        if not self.use_async or self._async_client is None:
            raise RuntimeError(
                "Async client not initialized. Set use_async=True when creating HTTPClient, "
                "or use make_request() for synchronous operations."
            )

        if not self.enable_retry:
            # Retry disabled, make single request
            return await self._make_request_async_internal(method, endpoint, params, json_data, mode)

        # Retry logic with exponential backoff
        current_retry_delay = self.retry_delay
        attempt = 0

        while attempt <= self.max_retries:
            try:
                return await self._make_request_async_internal(method, endpoint, params, json_data, mode)
            except NonRecoverableError:
                # Non-recoverable errors should not be retried
                raise
            except RecoverableError as e:
                attempt += 1

                if attempt > self.max_retries:
                    # Max retries exceeded, log and raise
                    log_with_context(
                        logger,
                        "error",
                        f"API Request Failed After {self.max_retries} Retries: {method} {endpoint} | "
                        f"Error: {e.details.to_human_readable()}",
                        source="bot",
                        action="api_retry_exhausted",
                        component="tradestation_api",
                    )
                    raise

                # Log retry attempt with context
                error_type = e.details.code or "UNKNOWN_ERROR"
                status_code = e.details.response_status or "N/A"
                retry_info = (
                    f"Retry {attempt}/{self.max_retries} for {method} {endpoint} | "
                    f"Error: {error_type} (Status: {status_code}) | "
                    f"Waiting {current_retry_delay:.1f}s before retry"
                )

                log_with_context(
                    logger,
                    "warning",
                    retry_info,
                    source="bot",
                    action="api_retry",
                    component="tradestation_api",
                )

                # Handle rate limit errors with special backoff
                if status_code == 429:
                    # Check for Retry-After header in response body
                    retry_after = None
                    if e.details.response_body and isinstance(e.details.response_body, dict):
                        retry_after = e.details.response_body.get("RetryAfter") or e.details.response_body.get(
                            "retry_after"
                        )

                    if retry_after:
                        # Use server-specified retry delay
                        wait_time = float(retry_after)
                        log_with_context(
                            logger,
                            "info",
                            f"Rate limit hit. Using server-specified Retry-After: {wait_time}s",
                            source="bot",
                            action="api_rate_limit",
                            component="tradestation_api",
                        )
                        await asyncio.sleep(wait_time)
                        current_retry_delay = self.retry_delay  # Reset to initial delay after server delay
                    else:
                        # Use exponential backoff for rate limits
                        await asyncio.sleep(current_retry_delay)
                        current_retry_delay = min(current_retry_delay * 2, self.max_retry_delay)
                else:
                    # Use exponential backoff for other recoverable errors
                    await asyncio.sleep(current_retry_delay)
                    current_retry_delay = min(current_retry_delay * 2, self.max_retry_delay)

                # Ensure authentication is still valid before retry
                if mode is None:
                    mode = sdk_config.trading_mode
                self.token_manager.ensure_authenticated(mode)

    async def _make_request_async_internal(
        self,
        method: str,
        endpoint: str,
        params: dict | None = None,
        json_data: dict | None = None,
        mode: str | None = None,
    ) -> dict[str, Any]:
        """
        Internal async method that performs a single API request without retry logic.

        Args:
            method: HTTP method (GET, POST, etc.)
            endpoint: API endpoint (without base URL)
            params: Query parameters
            json_data: JSON body for POST requests
            mode: "PAPER" or "LIVE". If None, uses sdk_config.trading_mode

        Returns:
            API response as dictionary

        Raises:
            RecoverableError: For errors that can be retried
            NonRecoverableError: For errors that should not be retried
        """
        if mode is None:
            mode = sdk_config.trading_mode

        self.token_manager.ensure_authenticated(mode)

        base_url = get_base_url(mode)
        tokens = self.token_manager.get_tokens(mode)
        url = f"{base_url}/{endpoint}"
        headers = {
            "Authorization": f"Bearer {tokens['access_token']}",
            "Content-Type": "application/json",
        }

        # Log request using helper method
        self._log_request(method, endpoint, params, json_data)

        # Track execution time
        start_time = time.time()

        if self._async_client is None:
            raise RuntimeError("Async client not initialized")

        try:
            # Set timeout for API requests (30 seconds for order operations, 10 seconds for others)
            timeout = 30.0 if endpoint.startswith("orderexecution") else 10.0

            # Make async request
            response = await self._async_client.request(
                method, url, headers=headers, params=params, json=json_data, timeout=timeout
            )
            elapsed_time = time.time() - start_time

            # Log response using helper method (convert httpx.Response to requests-like for logging)
            class ResponseAdapter:
                """Adapter to make httpx.Response compatible with logging method"""

                def __init__(self, httpx_response: httpx.Response):
                    self.status_code = httpx_response.status_code
                    self.text = httpx_response.text
                    self.content = httpx_response.content
                    self._json_cache = None

                def json(self):
                    if self._json_cache is None:
                        self._json_cache = json.loads(self.text)
                    return self._json_cache

            self._log_response(method, endpoint, ResponseAdapter(response), elapsed_time)

            # Check for errors and parse them
            if response.status_code >= 400:
                # Parse error response into ErrorDetails
                # Create a requests-like response for error parsing
                class ErrorResponseAdapter:
                    def __init__(self, httpx_response: httpx.Response):
                        self.status_code = httpx_response.status_code
                        self.text = httpx_response.text
                        self._json_cache = None

                    def json(self):
                        if self._json_cache is None:
                            try:
                                self._json_cache = json.loads(self.text)
                            except json.JSONDecodeError:
                                self._json_cache = {}
                        return self._json_cache

                error_details = parse_api_error_response(ErrorResponseAdapter(response))

                # Merge with request context
                context_details = self._build_error_context(method, endpoint, params, json_data, None, mode)
                error_details.request_method = context_details.request_method
                error_details.request_endpoint = context_details.request_endpoint
                error_details.request_params = context_details.request_params
                error_details.request_body = context_details.request_body
                error_details.mode = context_details.mode

                # Determine exception type based on status code
                if response.status_code == 401:
                    raise NonRecoverableError(error_details)
                elif response.status_code == 403:
                    raise NonRecoverableError(error_details)
                elif response.status_code == 400:
                    raise NonRecoverableError(error_details)
                elif response.status_code == 404:
                    raise NonRecoverableError(error_details)
                elif response.status_code == 429:
                    raise RecoverableError(error_details)
                elif response.status_code >= 500:
                    raise RecoverableError(error_details)
                else:
                    raise NonRecoverableError(error_details)

            # Log successful responses at info level for important operations
            if method in ["POST", "PUT", "DELETE"] or "order" in endpoint.lower():
                log_with_context(
                    logger,
                    "info",
                    f"API Success: {method} {endpoint} | Status: {response.status_code} | Time: {elapsed_time:.3f}s",
                    source="bot",
                    action="api_response",
                    component="tradestation_api",
                )

            return response.json()

        except (
            TradeStationAPIError,
            AuthenticationError,
            RateLimitError,
            InvalidRequestError,
            NetworkError,
            RecoverableError,
            NonRecoverableError,
        ):
            # Re-raise our custom exceptions as-is
            raise
        except httpx.HTTPError as e:
            elapsed_time = time.time() - start_time

            # Build error context for HTTP errors
            error_details = self._build_error_context(method, endpoint, params, json_data, None, mode)
            error_details.message = str(e)
            error_details.code = "HTTP_ERROR"

            log_with_context(
                logger,
                "error",
                f"API Request Failed: {method} {endpoint} | "
                f"Status: {getattr(e.response, 'status_code', 'Unknown') if hasattr(e, 'response') else 'Unknown'} | "
                f"Time: {elapsed_time:.3f}s | "
                f"Error: {error_details.to_human_readable()}",
                source="bot",
                action="api_error",
                component="tradestation_api",
            )

            # Network errors are recoverable
            raise RecoverableError(error_details) from e
        except Exception as e:
            elapsed_time = time.time() - start_time

            # Build error context for unexpected errors
            error_details = self._build_error_context(method, endpoint, params, json_data, None, mode)
            error_details.message = f"Unexpected error: {str(e)}"
            error_details.code = "UNEXPECTED_ERROR"

            log_with_context(
                logger,
                "error",
                f"API Request Exception: {method} {endpoint} | Time: {elapsed_time:.3f}s | Error: {str(e)}",
                source="bot",
                action="api_error",
                component="tradestation_api",
            )

            # Unexpected errors default to recoverable
            raise RecoverableError(error_details) from e

    async def aclose(self):
        """
        Close async HTTP client and release resources.

        Call this when done with async operations to properly clean up connections.
        """
        if self._async_client:
            await self._async_client.aclose()
            self._async_client = None

"""
TradeStation SDK Exceptions

Custom exceptions for TradeStation API operations with structured error details.

Dependencies: dataclasses, typing
"""

from dataclasses import dataclass
from typing import Any


@dataclass
class ErrorDetails:
    """
    Structured error information for TradeStation API errors.

    Provides both human-readable and machine-readable error representations.
    """

    code: str | None = None
    message: str = ""
    api_error_code: str | None = None
    api_error_message: str | None = None
    request_method: str | None = None
    request_endpoint: str | None = None
    request_params: dict[str, Any] | None = None
    request_body: dict[str, Any] | None = None
    response_status: int | None = None
    response_body: dict[str, Any] | None = None
    mode: str | None = None
    operation: str | None = None  # e.g., "place_order", "get_account_balances"

    def to_human_readable(self) -> str:
        """
        Generate human-readable error message.

        Returns:
            Formatted error message with context
        """
        lines = []

        # Main error message
        if self.operation:
            main_msg = f"{self.operation.replace('_', ' ').title()} failed"
        else:
            main_msg = "Operation failed"

        if self.message:
            main_msg += f": {self.message}"
        elif self.api_error_message:
            main_msg += f": {self.api_error_message}"
        elif self.api_error_code:
            main_msg += f": {self.api_error_code}"
        else:
            main_msg += ": Unknown error"

        lines.append(main_msg)

        # API error details
        if self.api_error_code or self.api_error_message:
            lines.append("")
            if self.api_error_code:
                lines.append(f"  - API Error Code: {self.api_error_code}")
            if self.api_error_message:
                lines.append(f"  - API Error Message: {self.api_error_message}")

        # Request details
        if self.request_method or self.request_endpoint:
            lines.append("")
            lines.append("  Request Details:")
            if self.request_method:
                lines.append(f"    - Method: {self.request_method}")
            if self.request_endpoint:
                lines.append(f"    - Endpoint: {self.request_endpoint}")
            if self.mode:
                lines.append(f"    - Mode: {self.mode}")
            if self.request_params:
                # Sanitize sensitive params
                sanitized = self._sanitize_dict(self.request_params)
                lines.append(f"    - Parameters: {sanitized}")
            if self.request_body:
                # Sanitize sensitive body fields
                sanitized = self._sanitize_dict(self.request_body)
                lines.append(f"    - Body: {sanitized}")

        # Response details
        if self.response_status:
            lines.append("")
            lines.append("  Response Details:")
            lines.append(f"    - Status: {self.response_status}")
            if self.response_body:
                sanitized = self._sanitize_dict(self.response_body)
                lines.append(f"    - Body: {sanitized}")

        return "\n".join(lines)

    def to_dict(self) -> dict[str, Any]:
        """
        Return structured error representation.

        Returns:
            Dictionary with all error details
        """
        return {
            "code": self.code,
            "message": self.message,
            "api_error_code": self.api_error_code,
            "api_error_message": self.api_error_message,
            "request_method": self.request_method,
            "request_endpoint": self.request_endpoint,
            "request_params": self._sanitize_dict(self.request_params) if self.request_params else None,
            "request_body": self._sanitize_dict(self.request_body) if self.request_body else None,
            "response_status": self.response_status,
            "response_body": self.response_body,
            "mode": self.mode,
            "operation": self.operation,
        }

    def _sanitize_dict(self, data: dict[str, Any]) -> dict[str, Any]:
        """Sanitize sensitive fields in dictionary."""
        if not isinstance(data, dict):
            return data

        sanitized = data.copy()
        sensitive_keys = ["client_secret", "refresh_token", "code", "password", "access_token", "Authorization"]

        for key in sensitive_keys:
            if key in sanitized:
                sanitized[key] = "***REDACTED***"

        # Also check nested dicts
        for key, value in sanitized.items():
            if isinstance(value, dict):
                sanitized[key] = self._sanitize_dict(value)
            elif isinstance(value, list):
                sanitized[key] = [self._sanitize_dict(item) if isinstance(item, dict) else item for item in value]

        return sanitized


class TradeStationAPIError(Exception):
    """
    Base exception for TradeStation API errors.

    Can be initialized with either a message string or ErrorDetails object.
    """

    def __init__(self, message: str | ErrorDetails = "", details: ErrorDetails | None = None):
        """
        Initialize exception.

        Args:
            message: Error message string or ErrorDetails object
            details: ErrorDetails object (if message is string)
        """
        if isinstance(message, ErrorDetails):
            self.details = message
            super().__init__(message.to_human_readable())
        elif details:
            self.details = details
            if message:
                self.details.message = message
            super().__init__(self.details.to_human_readable())
        else:
            # Create minimal ErrorDetails from message
            self.details = ErrorDetails(message=str(message))
            super().__init__(message)

    def __str__(self) -> str:
        """Return human-readable error message."""
        return self.details.to_human_readable()

    def to_dict(self) -> dict[str, Any]:
        """Return structured error representation."""
        return self.details.to_dict()


class AuthenticationError(TradeStationAPIError):
    """Raised when authentication fails."""

    pass


class RateLimitError(TradeStationAPIError):
    """Raised when rate limit is exceeded."""

    pass


class InvalidRequestError(TradeStationAPIError):
    """Raised when API request is invalid."""

    pass


class NetworkError(TradeStationAPIError):
    """Raised when network/connection errors occur."""

    pass


class TokenExpiredError(AuthenticationError):
    """Raised when access token has expired."""

    pass


class InvalidTokenError(AuthenticationError):
    """Raised when token is invalid or missing."""

    pass


class RecoverableError(TradeStationAPIError):
    """
    Errors that can be retried (network, temporary failures).

    These errors indicate transient issues that may resolve on retry:
    - Network errors (connection timeouts, DNS failures)
    - Server errors (500+ status codes)
    - Rate limit errors (429) - may resolve after backoff
    - Temporary service unavailability

    SDK streaming methods will automatically retry RecoverableError exceptions.
    """

    pass


class NonRecoverableError(TradeStationAPIError):
    """
    Errors that should not be retried (authentication, invalid request).

    These errors indicate permanent issues that won't resolve on retry:
    - Authentication errors (401, 403)
    - Invalid request errors (400)
    - Not found errors (404)

    SDK streaming methods will NOT retry NonRecoverableError exceptions.
    """

    pass

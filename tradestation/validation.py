"""Helpers for strict SDK request/response validation."""

from __future__ import annotations

from typing import Any

from pydantic import BaseModel, ValidationError

from .exceptions import ErrorDetails, SDKValidationError, TradeStationAPIError

SENSITIVE_KEYS = {
    "access_token",
    "refresh_token",
    "authorization",
    "client_secret",
    "password",
    "code",
}


def _payload_excerpt(payload: Any) -> dict[str, Any]:
    """Return a sanitized excerpt of a payload for error reporting."""
    if isinstance(payload, dict):
        items = list(payload.items())[:10]
        excerpt: dict[str, Any] = {}
        for key, value in items:
            key_str = str(key)
            if key_str.lower() in SENSITIVE_KEYS:
                excerpt[key_str] = "***REDACTED***"
            else:
                excerpt[key_str] = _payload_excerpt(value)
        return excerpt
    if isinstance(payload, list):
        return {"items": [_payload_excerpt(item) for item in payload[:5]], "count": len(payload)}
    return {"value": payload}


def validate_model(
    model_cls: type[BaseModel],
    payload: Any,
    *,
    operation: str,
    endpoint: str,
    mode: str | None = None,
    source: str,
) -> BaseModel:
    """Validate a payload against a Pydantic model and raise a rich SDK error on mismatch."""
    try:
        return model_cls.model_validate(payload)
    except ValidationError as exc:
        details = ErrorDetails(
            code="SDK_VALIDATION_ERROR",
            message=f"{source.title()} validation failed for {model_cls.__name__}",
            request_endpoint=endpoint,
            mode=mode,
            operation=operation,
            validation_errors=exc.errors(include_url=False),
        )
        excerpt = _payload_excerpt(payload)
        if source == "request":
            details.request_body = excerpt
        else:
            details.response_body = excerpt
        raise SDKValidationError(details) from exc


def dump_model(model: BaseModel) -> dict[str, Any]:
    """Serialize a validated model using the public SDK dict shape."""
    return model.model_dump(exclude_none=True)


def raise_unexpected_error(
    *,
    operation: str,
    endpoint: str,
    mode: str | None,
    exc: Exception,
) -> None:
    """Raise a structured SDK error for unexpected runtime failures."""
    details = ErrorDetails(
        code="SDK_RUNTIME_ERROR",
        message=f"Unexpected runtime error ({type(exc).__name__}): {exc}",
        request_endpoint=endpoint,
        mode=mode,
        operation=operation,
    )
    raise TradeStationAPIError(details) from exc

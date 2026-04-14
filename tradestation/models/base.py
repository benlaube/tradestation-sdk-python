"""Shared Pydantic model policy for TradeStation SDK contracts."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict


def strict_model_config(**overrides) -> ConfigDict:
    """Return the SDK-wide model config with strict extra-field handling."""
    return ConfigDict(extra="forbid", **overrides)


class TradeStationModel(BaseModel):
    """
    Base class for SDK request/response models.

    Policy:
    - outbound request payloads are validated before network calls
    - inbound response payloads are validated before public methods return
    - schema drift fails loud instead of silently dropping fields
    """

    model_config = strict_model_config()

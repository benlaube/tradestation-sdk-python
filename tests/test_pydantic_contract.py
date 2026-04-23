"""
Pydantic contract enforcement tests for the TradeStation SDK.

These tests ensure strict model policies and fail-loud validation behavior
cannot silently regress.
"""

from __future__ import annotations

import inspect
from types import UnionType
from typing import Any, Union, get_args, get_origin

import pytest
from pydantic import BaseModel

from tradestation.accounts import AccountOperations
from tradestation.market_data import MarketDataOperations
from tradestation.models import AccountsListResponse
from tradestation.models import __all__ as model_exports
from tradestation.models import accounts_list, accounts_rest
from tradestation.order_executions import OrderExecutionOperations
from tradestation.streaming import StreamingManager


APPROVED_RAW_FIELDS = {
    ("OrdersResponse", "Errors"),
    ("PositionsResponse", "Errors"),
    ("QuotesResponse", "Errors"),
    ("DetailedBalancesResponse", "Errors"),
    ("BODBalancesResponse", "Errors"),
    ("TradeStationOrderRequest", "TimeInForce"),
    ("TradeStationOrderResponse", "TimeInForce"),
    ("OrderStream", "TimeInForce"),
    ("BalanceStream", "BalanceDetail"),
    ("BalanceStream", "CurrencyDetails"),
}


def _iter_model_classes():
    import tradestation.models as models_module

    for name in model_exports:
        candidate = getattr(models_module, name, None)
        if inspect.isclass(candidate) and issubclass(candidate, BaseModel):
            yield candidate


def _contains_raw_dict_or_list(annotation: Any) -> bool:
    origin = get_origin(annotation)
    if origin is list:
        args = get_args(annotation)
        return not args or any(_contains_raw_dict_or_list(arg) for arg in args)
    if origin is dict:
        return True
    if origin in (tuple, set):
        return any(_contains_raw_dict_or_list(arg) for arg in get_args(annotation))
    if origin in (UnionType, Union):
        return any(_contains_raw_dict_or_list(arg) for arg in get_args(annotation))
    return False


@pytest.mark.unit
def test_all_sdk_models_forbid_extra_fields():
    """Every exported SDK model should fail on unknown fields."""
    for model_cls in _iter_model_classes():
        assert model_cls.model_config.get("extra") == "forbid", model_cls.__name__


@pytest.mark.unit
def test_no_duplicate_accounts_list_response_export():
    """The legacy accounts_rest shim must point to the canonical model object."""
    assert accounts_rest.AccountsListResponse is accounts_list.AccountsListResponse
    assert accounts_rest.AccountsListResponse is AccountsListResponse


@pytest.mark.unit
def test_models_do_not_regress_to_raw_dict_or_list_unions():
    """Nested typed fields should not be downgraded back to raw dict/list unions."""
    for model_cls in _iter_model_classes():
        for field_name, field_info in model_cls.model_fields.items():
            if (model_cls.__name__, field_name) in APPROVED_RAW_FIELDS:
                continue
            assert not _contains_raw_dict_or_list(field_info.annotation), f"{model_cls.__name__}.{field_name}"


@pytest.mark.unit
def test_account_info_validation_error_is_raised(mock_http_client, mocker):
    """Unknown broker fields in account responses should raise, not be dropped."""
    mocker.patch.object(
        mock_http_client,
        "make_request",
        return_value={"Accounts": [{"AccountID": "SIM123456", "Alias": "Paper", "UnexpectedField": "boom"}]},
    )

    account_ops = AccountOperations(mock_http_client, default_mode="PAPER")

    with pytest.raises(Exception):
        account_ops.get_account_info("PAPER")


@pytest.mark.unit
def test_quote_snapshot_validation_error_is_raised(mock_http_client, mocker):
    """Unknown quote fields should fail loud instead of being ignored."""
    mocker.patch.object(
        mock_http_client,
        "make_request",
        return_value={"Quotes": [{"Symbol": "MNQZ25", "Last": "25000.5", "UnexpectedField": "boom"}]},
    )

    market_data = MarketDataOperations(mock_http_client)

    with pytest.raises(Exception):
        market_data.get_quote_snapshots("MNQZ25", mode="PAPER")


@pytest.mark.unit
def test_order_request_validation_happens_before_http_call(mock_http_client, mocker):
    """If the synthesized order payload is invalid, no HTTP request should be sent."""
    mock_accounts = mocker.MagicMock()
    mock_accounts.get_account_info.return_value = {"account_id": 12345}
    mock_request = mocker.patch.object(mock_http_client, "make_request")

    order_exec = OrderExecutionOperations(mock_http_client, mock_accounts, default_mode="PAPER")

    with pytest.raises(Exception):
        order_exec.place_order("MNQZ25", "BUY", 2, "Market", mode="PAPER")

    mock_request.assert_not_called()


@pytest.mark.unit
def test_order_executions_validation_error_is_raised(mock_http_client, mocker):
    """Malformed execution payloads should raise instead of falling back to raw dicts."""
    mocker.patch.object(
        mock_http_client,
        "make_request",
        return_value={
            "Executions": [
                {
                    "ExecutionID": "EX123456",
                    "OrderID": "924243071",
                    "Symbol": "MNQZ25",
                    "TradeAction": "BUY",
                    "Quantity": "2",
                    "Price": "25000.00",
                    "Time": "2025-12-04T10:00:00-05:00",
                    "UnexpectedField": "boom",
                }
            ]
        },
    )

    order_exec = OrderExecutionOperations(mock_http_client, mocker.MagicMock(), default_mode="PAPER")

    with pytest.raises(Exception):
        order_exec.get_order_executions("924243071", mode="PAPER")


@pytest.mark.unit
@pytest.mark.asyncio
async def test_streaming_validation_error_is_raised(mock_token_manager, mock_http_client, mocker):
    """Malformed stream payloads should terminate with a validation error."""
    mocker.patch.object(
        mock_http_client,
        "stream_data",
        return_value=iter([{"Symbol": "MNQZ25", "Last": "25000.5", "UnexpectedField": "boom"}]),
    )

    streaming = StreamingManager(mock_token_manager, "client_id", "client_secret", mock_http_client)

    with pytest.raises(Exception):
        async for _ in streaming.stream_quotes("MNQZ25", mode="PAPER"):
            break

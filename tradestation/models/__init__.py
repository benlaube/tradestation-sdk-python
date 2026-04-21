"""
TradeStation API Models

Pydantic models for TradeStation API requests and responses.

Validation policy:
- request models validate outbound payloads before network calls
- response models validate inbound payloads before public methods return
- schema drift is treated as an error, not silently tolerated

Models are organized by domain:
- orders.py: Order requests, responses, and nested order components
- order_executions.py: Order execution (fill) models
- streaming.py: HTTP Streaming API models (quotes, orders, positions, balances)
- accounts.py: REST account models (single account, balances, BOD)
- accounts_list.py: REST account list response (GET /v3/brokerage/accounts)
- positions.py: REST position models
- quotes.py: REST quote models

Dependencies: pydantic
"""

from .accounts import (
    AccountBalancesResponse,
    AccountDetail,
    AccountSummary,
    BalanceDetail,
    BODBalance,
    BODBalancesResponse,
    DetailedBalancesResponse,
)
from .accounts_list import AccountsListResponse
from .order_executions import (
    TradeStationExecutionResponse,
)
from .orders import (
    OrdersResponse,
    TradeStationConditionalOrder,
    TradeStationMarketActivationRule,
    TradeStationOrderGroupRequest,
    TradeStationOrderGroupResponse,
    TradeStationOrderLeg,
    TradeStationOrderRequest,
    TradeStationOrderResponse,
    TradeStationTimeActivationRule,
    TradeStationTrailingStop,
)
from .positions import PositionResponse, PositionsResponse
from .quotes import QuoteSnapshot, QuotesResponse
from .streaming import (
    BalanceStream,
    Heartbeat,
    MarketFlags,
    OrderStream,
    PositionStream,
    QuoteStream,
    StreamErrorResponse,
    StreamStatus,
)

__all__ = [
    # Order Models
    "TradeStationOrderRequest",
    "TradeStationOrderGroupRequest",
    "OrdersResponse",
    "TradeStationOrderResponse",
    "TradeStationOrderGroupResponse",
    # Order Nested Models
    "TradeStationOrderLeg",
    "TradeStationConditionalOrder",
    "TradeStationMarketActivationRule",
    "TradeStationTimeActivationRule",
    "TradeStationTrailingStop",
    # Order Execution Models
    "TradeStationExecutionResponse",
    # Streaming Models (HTTP Streaming API)
    "QuoteStream",
    "OrderStream",
    "PositionStream",
    "BalanceStream",
    "StreamStatus",
    "Heartbeat",
    "StreamErrorResponse",
    "MarketFlags",
    # Accounts / Balances
    "AccountDetail",
    "AccountSummary",
    "BalanceDetail",
    "AccountBalancesResponse",
    "BODBalance",
    "BODBalancesResponse",
    "DetailedBalancesResponse",
    "AccountsListResponse",
    # Positions
    "PositionResponse",
    "PositionsResponse",
    # Quotes (REST)
    "QuoteSnapshot",
    "QuotesResponse",
]

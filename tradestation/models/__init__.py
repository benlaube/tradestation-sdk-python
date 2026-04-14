"""
TradeStation API Models

Pydantic models for TradeStation API requests and responses.
These models ensure we capture ALL data points from TradeStation API.

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
    AccountSummary,
    BalanceDetail,
    BODBalance,
    BODBalancesResponse,
)
from .accounts_list import AccountsListResponse
from .order_executions import (
    TradeStationExecutionResponse,
)
from .orders import (
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
    "AccountSummary",
    "BalanceDetail",
    "AccountBalancesResponse",
    "BODBalance",
    "BODBalancesResponse",
    "AccountsListResponse",
    # Positions
    "PositionResponse",
    "PositionsResponse",
    # Quotes (REST)
    "QuoteSnapshot",
    "QuotesResponse",
]

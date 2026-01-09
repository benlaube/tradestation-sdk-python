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
from .bars import BarResponse, BarsResponse
from .options import (
    OptionExpirationsResponse,
    OptionRiskRewardResponse,
    OptionSpreadType,
    OptionSpreadTypesResponse,
    OptionStrikesResponse,
)
from .order_executions import (
    TradeStationExecutionResponse,
)
from .order_wrappers import (
    CancelOrderResponse,
    ConfirmGroupOrderResponse,
    ConfirmOrderResponse,
    OrdersWrapper,
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
    BarStream,
    Heartbeat,
    MarketDepthAggregateStream,
    MarketDepthQuoteStream,
    MarketFlags,
    OptionChainStream,
    OptionQuoteStream,
    OrderStream,
    PositionStream,
    QuoteStream,
    StreamErrorResponse,
    StreamStatus,
)
from .symbols import SymbolDetail, SymbolDetailsResponse, SymbolSearchResponse

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
    # Bar Models
    "BarResponse",
    "BarsResponse",
    # Symbol Models
    "SymbolDetail",
    "SymbolDetailsResponse",
    "SymbolSearchResponse",
    # Option Models
    "OptionExpirationsResponse",
    "OptionStrikesResponse",
    "OptionRiskRewardResponse",
    "OptionSpreadType",
    "OptionSpreadTypesResponse",
    # Order Wrappers / Confirm
    "OrdersWrapper",
    "CancelOrderResponse",
    "ConfirmOrderResponse",
    "ConfirmGroupOrderResponse",
    # Streaming Models (HTTP Streaming API)
    "QuoteStream",
    "OrderStream",
    "PositionStream",
    "BalanceStream",
    "BarStream",
    "OptionChainStream",
    "OptionQuoteStream",
    "MarketDepthQuoteStream",
    "MarketDepthAggregateStream",
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

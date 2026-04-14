# TradeStation SDK Canonical Inventory

## About This Document

This is the **authoritative inventory** for the TradeStation SDK submodule.

It is derived from the current public façade in [`tradestation/__init__.py`](../tradestation/__init__.py), the exported operation modules, and the endpoint verification tests in [`tests/test_endpoints.py`](../tests/test_endpoints.py). When another document disagrees with this one, trust this inventory and the code.

**Use this if:** You need one current list of SDK methods, the endpoint families they map to, the available convenience functions, and the advanced accessors exposed by `TradeStationSDK`.

## Metadata

- **Status:** Active
- **Created:** 2026-04-14
- **Last Updated:** 2026-04-14 16:39:46 EDT
- **Version:** 1.0.0
- **Description:** Canonical inventory of the current TradeStation SDK public surface, endpoint families, convenience wrappers, and advanced accessors
- **Type:** Source-of-truth inventory
- **Applicability:** SDK usage, documentation maintenance, endpoint review, MCP/app integration work

---

## Source Of Truth

The authoritative sources are:

1. [`tradestation/__init__.py`](../tradestation/__init__.py) for the public `TradeStationSDK` façade
2. [`tests/test_endpoints.py`](../tests/test_endpoints.py) for endpoint assertions on the façade
3. [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json) for the vendored TradeStation v3 contract

Supporting docs such as [`API_REFERENCE.md`](./API_REFERENCE.md), [`API_ENDPOINT_MAPPING.md`](./API_ENDPOINT_MAPPING.md), and [`SDK_FUNCTIONS_LIST.md`](./SDK_FUNCTIONS_LIST.md) are maintained as navigational material and deeper explanation, but this file is the canonical inventory.

## Canonical Import

```python
from tradestation import TradeStationSDK
```

The current package import is `tradestation`, not `tradestation_sdk`.

## Public `TradeStationSDK` Façade

### Authentication

| Method | Purpose |
|--------|---------|
| `authenticate(mode=None)` | Run OAuth authentication for PAPER or LIVE mode |
| `refresh_access_token(mode=None)` | Refresh the active access token |
| `ensure_authenticated(mode=None)` | Ensure a valid token exists |
| `active_mode` | Return the currently active trading mode |

### Accounts

| Method | Purpose | Primary Endpoint |
|--------|---------|------------------|
| `get_account_info(mode=None)` | Resolve account metadata and working account selection | `GET /v3/brokerage/accounts` |
| `get_account_balances(mode=None, account_id=None)` | Fetch summarized balances for one account | `GET /v3/brokerage/accounts/{accountId}` |
| `get_account_balances_detailed(account_ids=None, mode=None)` | Fetch detailed balances for one or more accounts | `GET /v3/brokerage/accounts/{accounts}/balances` |
| `get_account_balances_bod(account_ids=None, mode=None)` | Fetch beginning-of-day balances | `GET /v3/brokerage/accounts/{accounts}/bodbalances` |

### Market Data

| Method | Purpose | Primary Endpoint |
|--------|---------|------------------|
| `get_bars(symbol, interval, unit, bars_back=200, mode=None)` | Fetch historical OHLCV bars | `GET /v3/marketdata/barcharts/{symbol}` |
| `search_symbols(pattern="", category="Future", asset_type=None, mode=None)` | Search the symbol catalog | `GET /v3/marketdata/symbols/search` |
| `get_futures_index_symbols(mode=None)` | Return common equity-index futures symbols | `GET /v3/marketdata/symbollists/futures/index/symbolnames` |
| `get_quote_snapshots(symbols, mode=None)` | Fetch quote snapshots | `GET /v3/marketdata/quotes/{symbols}` |
| `get_symbol_details(symbols, mode=None)` | Fetch symbol metadata and formatting details | `GET /v3/marketdata/symbols/{symbols}` |
| `get_crypto_symbol_names(mode=None)` | List supported crypto pair symbols | `GET /v3/marketdata/symbollists/cryptopairs/symbolnames` |
| `get_option_expirations(underlying, mode=None, strike_price=None)` | Fetch option expiration dates | `GET /v3/marketdata/options/expirations/{underlying}` |
| `get_option_risk_reward(request, mode=None)` | Run option risk/reward analysis | `POST /v3/marketdata/options/riskreward` |
| `get_option_spread_types(mode=None)` | Fetch supported option spread types | `GET /v3/marketdata/options/spreadtypes` |
| `get_option_strikes(underlying, expiration_date=None, min_strike=None, max_strike=None, mode=None, spread_type=None, strike_interval=None, expiration=None, expiration2=None)` | Fetch option strikes | `GET /v3/marketdata/options/strikes/{underlying}` |

### Streaming

| Method | Purpose | Primary Endpoint |
|--------|---------|------------------|
| `stream_quotes(symbols, mode=None)` | Stream quote updates | `GET /v3/marketdata/stream/quotes/{symbols}` |
| `stream_orders(account_id=None, mode=None)` | Stream order updates | `GET /v3/brokerage/stream/accounts/{accounts}/orders` |
| `stream_positions(account_id=None, mode=None)` | Stream position updates | `GET /v3/brokerage/stream/accounts/{accounts}/positions` |
| `stream_balances(account_id=None, mode=None)` | Stream balance updates | `GET /v3/brokerage/stream/accounts/{accounts}/balances` |

### Positions And P&L

| Method | Purpose | Primary Endpoint |
|--------|---------|------------------|
| `get_position(symbol, mode=None)` | Return net position quantity for one symbol | `GET /v3/brokerage/accounts/{accountId}/positions` |
| `get_all_positions(mode=None)` | Return all open positions | `GET /v3/brokerage/accounts/{accountId}/positions` |
| `flatten_position(symbol=None, mode=None)` | Flatten one symbol or all positions | Uses `place_order()` |
| `get_todays_profit_loss(mode=None)` | Sum today's P&L across positions | `GET /v3/brokerage/accounts/{accountId}/positions` |
| `get_todays_trades(mode=None)` | Return today's filled orders | Uses order history queries |
| `get_unrealized_profit_loss(mode=None)` | Sum unrealized P&L across positions | `GET /v3/brokerage/accounts/{accountId}/positions` |

### Order Execution And Queries

| Method | Purpose | Primary Endpoint |
|--------|---------|------------------|
| `cancel_all_orders_for_symbol(symbol, account_ids=None, mode=None)` | Cancel all open orders for one symbol | Composite convenience flow |
| `cancel_all_orders(account_ids=None, mode=None)` | Cancel all open orders | Composite convenience flow |
| `replace_order(old_order_id, symbol, side, quantity, order_type="Market", limit_price=None, stop_price=None, time_in_force="DAY", trail_amount=None, trail_percent=None, mode=None, account_id=None)` | Cancel and replace an order | Composite convenience flow |
| `place_order(symbol, side, quantity, order_type="Market", limit_price=None, stop_price=None, time_in_force="DAY", wait_for_fill=False, trail_amount=None, trail_percent=None, mode=None, account_id=None)` | Submit a single-leg order | `POST /v3/orderexecution/orders` |
| `cancel_order(order_id, mode=None)` | Cancel a single order | `DELETE /v3/orderexecution/orders/{orderID}` |
| `modify_order(order_id, quantity=None, limit_price=None, stop_price=None, mode=None)` | Modify a working order | `PUT /v3/orderexecution/orders/{orderID}` |
| `get_order_history(start_date=None, end_date=None, limit=100, mode=None)` | Return historical orders | `GET /v3/brokerage/accounts/{accounts}/historicalorders` |
| `get_current_orders(account_ids=None, next_token=None, mode=None)` | Return current orders | `GET /v3/brokerage/accounts/{accounts}/orders` |
| `get_orders_by_status(status, account_ids=None, next_token=None, mode=None)` | Filter current orders by status | Uses `get_current_orders()` |
| `get_open_orders(account_ids=None, next_token=None, mode=None)` | Convenience wrapper for working orders | Uses `get_orders_by_status()` |
| `get_filled_orders(account_ids=None, next_token=None, mode=None)` | Convenience wrapper for filled orders | Uses `get_orders_by_status()` |
| `get_canceled_orders(account_ids=None, next_token=None, mode=None)` | Convenience wrapper for canceled orders | Uses `get_orders_by_status()` |
| `get_rejected_orders(account_ids=None, next_token=None, mode=None)` | Convenience wrapper for rejected orders | Uses `get_orders_by_status()` |
| `get_orders_by_ids(order_ids, account_ids=None, mode=None)` | Fetch specific current orders by ID | `GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}` |
| `get_historical_orders_by_ids(order_ids, account_ids=None, start_date=None, end_date=None, mode=None)` | Fetch specific historical orders by ID | `GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}` |
| `get_order_executions(order_id, mode=None)` | Fetch execution fills for an order | `GET /v3/orderexecution/orders/{orderID}/executions` |
| `is_order_filled(order_id, mode=None)` | Return whether an order is filled | Composite query helper |
| `confirm_order(symbol, side, quantity, order_type="Market", limit_price=None, stop_price=None, time_in_force="DAY", mode=None)` | Validate an order before submission | `POST /v3/orderexecution/orderconfirm` |
| `get_activation_triggers(mode=None)` | List activation triggers | `GET /v3/orderexecution/activationtriggers` |
| `confirm_group_order(group_type, orders, mode=None)` | Validate an order group | `POST /v3/orderexecution/ordergroupconfirm` |
| `place_group_order(group_type, orders, mode=None)` | Submit an order group | `POST /v3/orderexecution/ordergroups` |
| `get_routes(mode=None)` | List order routing options | `GET /v3/orderexecution/routes` |

## Convenience Functions

These façade methods exist specifically to simplify common trading workflows:

| Method | Wraps |
|--------|-------|
| `place_bracket_order(...)` | `place_group_order("BRK", ...)` |
| `place_oco_order(orders, mode=None)` | `place_group_order("OCO", ...)` |
| `place_trailing_stop_order(...)` | `place_order(..., order_type="TrailingStop")` |
| `place_limit_order(...)` | `place_order(..., order_type="Limit")` |
| `place_stop_order(...)` | `place_order(..., order_type="Stop")` |
| `place_stop_limit_order(...)` | `place_order(..., order_type="StopLimit")` |
| `cancel_all_orders_for_symbol(...)` | `get_current_orders()` + `cancel_order()` |
| `cancel_all_orders(...)` | `get_current_orders()` + `cancel_order()` |
| `replace_order(...)` | `cancel_order()` + `place_order()` |
| `get_open_orders(...)` | `get_orders_by_status()` |
| `get_filled_orders(...)` | `get_orders_by_status()` |
| `get_canceled_orders(...)` | `get_orders_by_status()` |
| `get_rejected_orders(...)` | `get_orders_by_status()` |
| `is_order_filled(...)` | order query inspection |
| `flatten_position(...)` | position discovery + `place_order()` |
| `get_todays_trades(...)` | order history query + filled-status filtering |

## Advanced Accessors

The façade intentionally exposes lower-level modules and shared infrastructure for advanced use cases:

| Property | Type | Purpose |
|----------|------|---------|
| `streaming` | `StreamingManager` | Direct access to HTTP streaming helpers |
| `session` | `StreamingManager \| None` | Backward-compatible session alias |
| `client` | `HTTPClient` | Direct HTTP client access |
| `token_manager` | `TokenManager` | Direct token lifecycle access |
| `accounts` | `AccountOperations` | Lower-level account methods |
| `market_data` | `MarketDataOperations` | Lower-level market-data methods |
| `orders` | `OrderOperations` | Lower-level order-query methods |
| `positions` | `PositionOperations` | Lower-level position methods |
| `order_executions` | `OrderExecutionOperations` | Lower-level order-execution methods |
| `info()` | `dict[str, Any]` | SDK diagnostics and feature flags |

## Lower-Level Module Methods Exposed Through Accessors

These methods are part of the supported SDK surface because the corresponding operation modules are exposed as properties:

### `sdk.market_data`

- `stream_bars(...)`
- `stream_option_chains(...)`
- `stream_option_quotes(...)`
- `stream_market_depth_quotes(...)`
- `stream_market_depth_aggregates(...)`

### `sdk.orders`

- `stream_orders(...)`

### `sdk.positions`

- `stream_positions(...)`

For the complete implementation details of those lower-level methods, use the module source plus the endpoint mapping and examples docs.

## Endpoint Families Implemented

### Brokerage

- `GET /v3/brokerage/accounts`
- `GET /v3/brokerage/accounts/{accountId}`
- `GET /v3/brokerage/accounts/{accounts}/balances`
- `GET /v3/brokerage/accounts/{accounts}/bodbalances`
- `GET /v3/brokerage/accounts/{accounts}/orders`
- `GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}`
- `GET /v3/brokerage/accounts/{accounts}/historicalorders`
- `GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}`
- `GET /v3/brokerage/accounts/{accountId}/positions`
- `GET /v3/brokerage/stream/accounts/{accounts}/orders`
- `GET /v3/brokerage/stream/accounts/{accounts}/positions`
- `GET /v3/brokerage/stream/accounts/{accounts}/balances`

### Order Execution

- `POST /v3/orderexecution/orders`
- `PUT /v3/orderexecution/orders/{orderID}`
- `DELETE /v3/orderexecution/orders/{orderID}`
- `GET /v3/orderexecution/orders/{orderID}/executions`
- `POST /v3/orderexecution/orderconfirm`
- `POST /v3/orderexecution/ordergroupconfirm`
- `POST /v3/orderexecution/ordergroups`
- `GET /v3/orderexecution/activationtriggers`
- `GET /v3/orderexecution/routes`

### Market Data

- `GET /v3/marketdata/barcharts/{symbol}`
- `GET /v3/marketdata/quotes/{symbols}`
- `GET /v3/marketdata/symbols/search`
- `GET /v3/marketdata/symbols/{symbols}`
- `GET /v3/marketdata/symbollists/futures/index/symbolnames`
- `GET /v3/marketdata/symbollists/cryptopairs/symbolnames`
- `GET /v3/marketdata/options/expirations/{underlying}`
- `POST /v3/marketdata/options/riskreward`
- `GET /v3/marketdata/options/spreadtypes`
- `GET /v3/marketdata/options/strikes/{underlying}`
- `GET /v3/marketdata/stream/quotes/{symbols}`
- `GET /v3/marketdata/stream/barcharts/{symbol}`
- `GET /v3/marketdata/stream/options/chains/{underlying}`
- `GET /v3/marketdata/stream/options/quotes`
- `GET /v3/marketdata/stream/marketdepth/quotes/{symbol}`
- `GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}`

## Documentation Rules

- Use this file as the first stop when you need to know whether a method exists.
- Use [`API_REFERENCE.md`](./API_REFERENCE.md) for longer explanations and examples.
- Use [`API_ENDPOINT_MAPPING.md`](./API_ENDPOINT_MAPPING.md) when you need the HTTP path and request/response model context.
- Update this file whenever the façade in `tradestation/__init__.py` changes.

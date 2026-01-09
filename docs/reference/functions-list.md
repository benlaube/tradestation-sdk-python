---
status: Active
created: 12-05-2025 17:19:33 EST
lastUpdated: 12-29-2025 13:41:00 EST
version: 1.2.1
description: Quick reference list of all functions available in the TradeStation SDK across all modules and endpoints, organized by category for quick lookup
type: Function Index - Quick reference for developers looking up SDK functions
applicability: When quickly looking up available SDK functions, understanding function organization, or finding functions by category
howtouse: Use this document as a quick index to find available SDK functions by category, then reference detailed documentation for specific functions
---

# TradeStation SDK - Complete Functions List

## About This Document

This is a **quick reference index** of all functions available in the SDK, organized by category. Use this to quickly find function names, then refer to detailed documentation for parameters and usage.

**Use this if:** You want to see all available functions at a glance, find functions by category, or quickly look up function names.

**Related Documents:**
- 📚 **[API_REFERENCE.md](API_REFERENCE.md)** - Detailed function documentation with parameters
- 📝 **[ORDER_FUNCTIONS_REFERENCE.md](ORDER_FUNCTIONS_REFERENCE.md)** - Detailed order function documentation
- 💡 **[SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md)** - Usage examples for all functions
- 📋 **[CHEATSHEET.md](../CHEATSHEET.md)** - Quick code snippets
- 🎯 **[FEATURES.md](../FEATURES.md)** - Feature overview


## Table of Contents

- [New Functions](#new-functions)
- [Authentication Functions](#authentication-functions)
- [Account Functions](#account-functions)
- [Market Data Functions](#market-data-functions)
- [Position Functions](#position-functions)
- [Order Execution Functions](#order-execution-functions)
- [Order Execution Convenience Functions](#order-execution-convenience-functions)
- [Order Query Functions](#order-query-functions)
- [Order Status Convenience Functions](#order-status-convenience-functions)
- [Streaming Functions](#streaming-functions)
- [Utility Functions](#utility-functions)
- [Coverage Status](#coverage-status)
- [Summary](#summary)

---

## New Functions

The following functions were recently added to ensure all required trading operations are covered:

### 1. `is_order_filled()`

**Location:** `OrderExecutionOperations.is_order_filled()` / `TradeStationSDK.is_order_filled()`

**Purpose:** Convenience function to check if an order has been filled.

**Returns:** `bool` - True if order status is "FLL" (Filled) or "FLP" (Partial Fill)

**Example:**
```python
if sdk.is_order_filled("924243071", mode="PAPER"):
    print("Order is filled!")
```

### 2. `cancel_all_orders_for_symbol()`

**Location:** `OrderExecutionOperations.cancel_all_orders_for_symbol()` / `TradeStationSDK.cancel_all_orders_for_symbol()`

**Purpose:** Cancel all open orders for a specific symbol.

**Returns:** `list[dict[str, Any]]` - List of cancellation results with order_id, symbol, success, message

**Example:**
```python
results = sdk.cancel_all_orders_for_symbol("MNQZ25", mode="PAPER")
for result in results:
    print(f"Order {result['order_id']}: {result['success']}")
```

### 3. `cancel_all_orders()`

**Location:** `OrderExecutionOperations.cancel_all_orders()` / `TradeStationSDK.cancel_all_orders()`

**Purpose:** Cancel all open orders for account(s).

**Returns:** `list[dict[str, Any]]` - List of cancellation results with order_id, symbol, success, message

**Example:**
```python
results = sdk.cancel_all_orders(mode="PAPER")
print(f"Cancelled {len(results)} orders")
```

### 4. `replace_order()`

**Location:** `OrderExecutionOperations.replace_order()` / `TradeStationSDK.replace_order()`

**Purpose:** Replace an order by canceling the old one and placing a new one. Useful when you need to change symbol, side, or other parameters that cannot be modified with `modify_order()`.

**Returns:** `tuple[str | None, str]` - (new_order_id, status_message)

**Example:**
```python
new_order_id, status = sdk.replace_order(
    old_order_id="924243071",
    symbol="ESZ25",  # Different symbol
    side="SELL",     # Different side
    quantity=3,
    order_type="Limit",
    limit_price=25000.00,
    mode="PAPER"
)
```

### Enhanced: `place_bracket_order()` - Trailing Stop Support

**Location:** `OrderExecutionOperations.place_bracket_order()` / `TradeStationSDK.place_bracket_order()`

**New Parameters:**
- `stop_loss` (float | None): Now optional when using trailing stop
- `trail_amount` (float | None): Trail amount in price units (points)
- `trail_percent` (float | None): Trail percentage
- `use_trailing_stop` (bool): If True, use trailing stop instead of fixed stop-loss

**Example:**
```python
# Bracket order with trailing stop (NEW)
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    use_trailing_stop=True,
    trail_amount=1.5,  # $3.00 trail for MNQ
    mode="PAPER"
)
```

---

## Authentication Functions

**Module:** `TokenManager` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| `authenticate(mode)` | Perform OAuth2 authentication | None | OAuth2 flow (browser-based) |
| `refresh_access_token(mode)` | Refresh access token | None | `POST /v3/security/authorize` |
| `ensure_authenticated(mode)` | Ensure authenticated (auto-refresh if needed) | None | Depends on `refresh_access_token()` |
| `active_mode` (property) | Get most recent mode used | str | Internal state |

---

## Account Functions

**Module:** `AccountOperations` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| `get_account_info(mode)` | Get account information including account ID | dict | `GET /v3/brokerage/accounts` |
| `get_account_balances(mode, account_id)` | Get account balances (equity, buying power, margin, P&L) | dict[str, Any] | `GET /v3/brokerage/accounts/{accountId}` |
| `get_account_balances_detailed(account_ids, mode)` | Get detailed account balances with BalanceDetail | dict[str, Any] | `GET /v3/brokerage/accounts/{accounts}/balances` |
| `get_account_balances_bod(account_ids, mode)` | Get Beginning of Day balances | dict[str, Any] | `GET /v3/brokerage/accounts/{accounts}/bodbalances` |

---

## Market Data Functions

**Module:** `MarketDataOperations` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| `get_bars(symbol, interval, unit, bars_back, start_date, end_date, mode)` | Fetch historical bar data (OHLCV) | BarsResponse \| list[dict[str, Any]] | `GET /v3/marketdata/barcharts/{symbol}` |
| `search_symbols(pattern, category, asset_type, mode)` | Search for symbols matching criteria | SymbolSearchResponse \| list[dict[str, Any]] | `GET /v3/marketdata/symbols/search` |
| `get_futures_index_symbols(mode)` | Get list of available futures index symbols | list[dict[str, Any]] | `GET /v3/marketdata/symbollists/futures/index/symbolnames` |
| `get_quote_snapshots(symbols, mode)` | Get quote snapshots for one or more symbols | dict[str, Any] | `GET /v3/marketdata/quotes/{symbols}` |
| `get_symbol_details(symbols, mode)` | Get symbol details and formatting information | SymbolDetailsResponse \| dict[str, Any] | `GET /v3/marketdata/symbols/{symbols}` |
| `get_crypto_symbol_names(mode)` | Get list of available crypto symbol names | list[str] | `GET /v3/marketdata/symbollists/cryptopairs/symbolnames` |
| `get_option_expirations(underlying, mode)` | Get option expiration dates for an underlying | OptionExpirationsResponse \| list[str] | `GET /v3/marketdata/options/expirations/{underlying}` |
| `get_option_risk_reward(request, mode)` | Calculate option risk/reward analysis | OptionRiskRewardResponse \| dict[str, Any] | `POST /v3/marketdata/options/riskreward` |
| `get_option_spread_types(mode)` | Get available option spread types | OptionSpreadTypesResponse \| list[dict[str, Any]] | `GET /v3/marketdata/options/spreadtypes` |
| `get_option_strikes(underlying, expiration_date, min_strike, max_strike, mode)` | Get available strike prices for an underlying and expiration | OptionStrikesResponse \| list[float] | `GET /v3/marketdata/options/strikes/{underlying}` |
| `stream_quotes(symbols, mode)` | Stream quotes via HTTP Streaming (async) | AsyncGenerator[dict[str, Any], None] | `GET /v3/marketdata/stream/quotes/{symbols}` |
| `stream_bars(symbol, interval, unit, mode)` | Stream bars via HTTP Streaming (async) | AsyncGenerator[BarStream, None] | `GET /v3/marketdata/stream/barcharts/{symbol}` |
| `stream_option_chains(underlying, mode)` | Stream option chain data (async) | AsyncGenerator[OptionChainStream, None] | `GET /v3/marketdata/stream/options/chains/{underlying}` |
| `stream_option_quotes(legs, mode)` | Stream option quotes for specified legs (async) | AsyncGenerator[OptionQuoteStream, None] | `GET /v3/marketdata/stream/options/quotes` |
| `stream_market_depth_quotes(symbol, mode)` | Stream Level 2 market depth quotes (async) | AsyncGenerator[MarketDepthQuoteStream, None] | `GET /v3/marketdata/stream/marketdepth/quotes/{symbol}` |
| `stream_market_depth_aggregates(symbol, mode)` | Stream aggregated market depth data (async) | AsyncGenerator[MarketDepthAggregateStream, None] | `GET /v3/marketdata/stream/marketdepth/aggregates/{symbol}` |

---

## Position Functions

**Module:** `PositionOperations` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| `get_position(symbol, mode)` | Get current position quantity for a symbol | int | `GET /v3/brokerage/accounts/{accountId}/positions` |
| `get_all_positions(mode)` | Get all current positions across all symbols | list[dict[str, Any]] | `GET /v3/brokerage/accounts/{accountId}/positions` |
| `flatten_position(symbol, mode)` | Close all positions (or specific symbol) | list[dict[str, Any]] | Depends on `place_order()` |
| `get_todays_profit_loss(mode)` | Get today's profit and loss across all positions | float | `GET /v3/brokerage/accounts/{accountId}/positions` (sums TodaysProfitLoss) |
| `get_todays_trades(mode)` | Get today's filled trades (orders filled today) | list[dict[str, Any]] | Depends on `get_order_history()` filtered by today's date and FLL/FLP status |
| `get_unrealized_profit_loss(mode)` | Get unrealized profit and loss across all positions | float | `GET /v3/brokerage/accounts/{accountId}/positions` (sums UnrealizedProfitLoss) |
| `stream_positions(account_id, mode)` | Stream position updates via HTTP Streaming (async) | AsyncGenerator[dict[str, Any], None] | `GET /v3/brokerage/stream/accounts/{accounts}/positions` |

---

## Order Execution Functions

**Module:** `OrderExecutionOperations` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| [`place_order()`](./ORDER_FUNCTIONS_REFERENCE.md#1-place_order) | Place an order (Market, Limit, Stop, StopLimit, TrailingStop) | tuple[str \| None, str] | `POST /v3/orderexecution/orders` |
| [`cancel_order()`](./ORDER_FUNCTIONS_REFERENCE.md#2-cancel_order) | Cancel an order by order ID | tuple[bool, str] | `DELETE /v3/orderexecution/orders/{orderID}` |
| [`modify_order()`](./ORDER_FUNCTIONS_REFERENCE.md#3-modify_order) | Modify an existing order | tuple[bool, str] | `PUT /v3/orderexecution/orders/{orderID}` |
| [`get_order_executions()`](./ORDER_FUNCTIONS_REFERENCE.md#5-get_order_executions) | Get execution details (fills) for a specific order | list[dict[str, Any]] | `GET /v3/orderexecution/orders/{orderID}/executions` |
| [`is_order_filled()`](./ORDER_FUNCTIONS_REFERENCE.md#4-is_order_filled) | Check if an order has been filled (convenience function) | bool | `GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}` |
| [`confirm_order()`](./ORDER_FUNCTIONS_REFERENCE.md#6-confirm_order) | Pre-flight check to get estimated cost and commission | dict[str, Any] | `POST /v3/orderexecution/orderconfirm` |
| [`cancel_all_orders_for_symbol()`](./ORDER_FUNCTIONS_REFERENCE.md#11-cancel_all_orders_for_symbol) | Cancel all open orders for a specific symbol | list[dict[str, Any]] | Depends on `get_current_orders()` + `cancel_order()` |
| [`cancel_all_orders()`](./ORDER_FUNCTIONS_REFERENCE.md#12-cancel_all_orders) | Cancel all open orders for account(s) | list[dict[str, Any]] | Depends on `get_current_orders()` + `cancel_order()` |
| [`replace_order()`](./ORDER_FUNCTIONS_REFERENCE.md#13-replace_order) | Replace an order by canceling old and placing new | tuple[str \| None, str] | Depends on `cancel_order()` + `place_order()` |
| [`confirm_group_order()`](./ORDER_FUNCTIONS_REFERENCE.md#7-confirm_group_order) | Confirm a group order (OCO/Bracket) before placement | dict[str, Any] | `POST /v3/orderexecution/ordergroupconfirm` |
| [`place_group_order()`](./ORDER_FUNCTIONS_REFERENCE.md#8-place_group_order) | Place a group order (OCO/Bracket/NORMAL) | dict[str, Any] | `POST /v3/orderexecution/ordergroups` |
| [`get_activation_triggers()`](./ORDER_FUNCTIONS_REFERENCE.md#9-get_activation_triggers) | Get available activation trigger keys for conditional orders | list[dict[str, Any]] | `GET /v3/orderexecution/activationtriggers` |
| [`get_routes()`](./ORDER_FUNCTIONS_REFERENCE.md#10-get_routes) | Get available routing options for order execution | list[dict[str, Any]] | `GET /v3/orderexecution/routes` |

---

## Order Execution Convenience Functions

**Module:** `OrderExecutionOperations` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| [`place_limit_order()`](./ORDER_FUNCTIONS_REFERENCE.md#10-place_limit_order) | Place a limit order (convenience wrapper) | tuple[str \| None, str] | Depends on `place_order()` |
| [`place_stop_order()`](./ORDER_FUNCTIONS_REFERENCE.md#11-place_stop_order) | Place a stop order (convenience wrapper) | tuple[str \| None, str] | Depends on `place_order()` |
| [`place_stop_limit_order()`](./ORDER_FUNCTIONS_REFERENCE.md#12-place_stop_limit_order) | Place a stop-limit order (convenience wrapper) | tuple[str \| None, str] | Depends on `place_order()` |
| [`place_trailing_stop_order()`](./ORDER_FUNCTIONS_REFERENCE.md#13-place_trailing_stop_order) | Place a trailing stop order (convenience wrapper) | tuple[str \| None, str] | Depends on `place_order()` |
| [`place_oco_order()`](./ORDER_FUNCTIONS_REFERENCE.md#14-place_oco_order) | Place an OCO (One-Cancels-Other) order (convenience wrapper) | dict[str, Any] | Depends on `place_group_order("OCO", ...)` |
| [`place_bracket_order()`](./ORDER_FUNCTIONS_REFERENCE.md#15-place_bracket_order) | Place a bracket order (entry + profit target + stop-loss or trailing stop) | dict[str, Any] | Depends on `place_group_order("BRK", ...)` |

---

## Order Query Functions

**Module:** `OrderOperations` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| [`get_order_history()`](./ORDER_FUNCTIONS_REFERENCE.md#16-get_order_history) | Get historical orders with date filtering | list[dict[str, Any]] | `GET /v3/brokerage/accounts/{accounts}/historicalorders` |
| [`get_current_orders()`](./ORDER_FUNCTIONS_REFERENCE.md#17-get_current_orders) | Get current/open orders for account(s) | dict[str, Any] | `GET /v3/brokerage/accounts/{accounts}/orders` |
| [`get_orders_by_ids()`](./ORDER_FUNCTIONS_REFERENCE.md#18-get_orders_by_ids) | Get specific current orders by order ID(s) | dict[str, Any] | `GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}` |
| [`get_historical_orders_by_ids()`](./ORDER_FUNCTIONS_REFERENCE.md#19-get_historical_orders_by_ids) | Get specific historical orders by order ID(s) | dict[str, Any] | `GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}` |
| [`stream_orders()`](./ORDER_FUNCTIONS_REFERENCE.md#20-stream_orders) | Stream order updates via HTTP Streaming (async) | AsyncGenerator[dict[str, Any], None] | `GET /v3/brokerage/stream/accounts/{accounts}/orders` |

---

## Order Status Convenience Functions

**Module:** `OrderOperations` / `TradeStationSDK`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| `get_orders_by_status(status, account_ids, next_token, mode)` | Get orders filtered by status(es) - accepts single status or list | dict[str, Any] | Depends on `get_current_orders()` |
| `get_open_orders(account_ids, next_token, mode)` | Get open/working orders (OPN, ACK, PLA, FPR, RPD, RSN, UCN) | dict[str, Any] | Depends on `get_orders_by_status()` |
| `get_filled_orders(account_ids, next_token, mode)` | Get filled orders (FLL, FLP) | dict[str, Any] | Depends on `get_orders_by_status()` |
| `get_canceled_orders(account_ids, next_token, mode)` | Get canceled orders (CAN, EXP, OUT, TSC, UCH) | dict[str, Any] | Depends on `get_orders_by_status()` |
| `get_rejected_orders(account_ids, next_token, mode)` | Get rejected orders (REJ) | dict[str, Any] | Depends on `get_orders_by_status()` |

---

## Streaming Functions

**Module:** `StreamingManager` / `TradeStationSDK.streaming`

| Function | Description | Returns | API Endpoint / Dependency |
|----------|-------------|---------|--------------------------|
| `stream_quotes(symbols, mode)` | Stream quotes via HTTP Streaming (async, returns QuoteStream models) | AsyncGenerator[QuoteStream, None] | `GET /v3/marketdata/stream/quotes/{symbols}` |
| `stream_orders(account_id, mode)` | Stream order updates via HTTP Streaming (async, returns OrderStream models) | AsyncGenerator[OrderStream, None] | `GET /v3/brokerage/stream/accounts/{accounts}/orders` |
| `stream_positions(account_id, mode)` | Stream position updates via HTTP Streaming (async, returns PositionStream models) | AsyncGenerator[PositionStream, None] | `GET /v3/brokerage/stream/accounts/{accounts}/positions` |
| `stream_balances(account_id, mode)` | Stream real-time account balance updates (async, returns BalanceStream models) | AsyncGenerator[BalanceStream, None] | `GET /v3/brokerage/stream/accounts/{accounts}/balances` |
| `stream_orders_by_ids(account_ids, order_ids, mode)` | Stream specific orders by order ID(s) (async, returns OrderStream models) | AsyncGenerator[OrderStream, None] | `GET /v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}` |

---

## Utility Functions

**Module:** Various

| Function | Location | Description | Returns | API Endpoint / Dependency |
|----------|----------|-------------|---------|--------------------------|
| `normalize_order(order)` | `mappers.normalize_order()` | Normalize TradeStation order object to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `normalize_position(position)` | `mappers.normalize_position()` | Normalize TradeStation position object to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `normalize_quote(quote)` | `mappers.normalize_quote()` | Normalize TradeStation quote snapshot to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `normalize_execution(execution)` | `mappers.normalize_execution()` | Normalize execution/fill object to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `normalize_account(account)` | `mappers.normalize_account()` | Normalize account summary to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `normalize_balances(balances)` | `mappers.normalize_balances()` | Normalize balance detail to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `normalize_account_balances(response)` | `mappers.normalize_account_balances()` | Normalize account balances response to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `normalize_bod_balance(bod_balance)` | `mappers.normalize_bod_balance()` | Normalize beginning-of-day balance entry to consistent dictionary format | dict[str, Any] \| None | Internal utility function |
| `get_base_url(mode)` | `client.get_base_url()` | Get base URL for specified mode (PAPER/LIVE) | str | Internal utility function |
| `parse_api_error_response(response)` | `client.parse_api_error_response()` | Parse TradeStation API error response into structured ErrorDetails | ErrorDetails | Internal utility function |

---

## Coverage Status

All 9 required trading operations are now fully covered:

- ✅ **Replace an open order with a new one** - `replace_order()`
- ✅ **Cancel an order** - `cancel_order()`
- ✅ **Place a bracket order with trailing stop** - `place_bracket_order(..., use_trailing_stop=True)`
- ✅ **Confirm an order has been filled** - `is_order_filled()`, `get_order_executions()`
- ✅ **Cancel all orders (symbol)** - `cancel_all_orders_for_symbol()`
- ✅ **Cancel all orders on account** - `cancel_all_orders()`
- ✅ **Flatten position (symbol)** - `flatten_position(symbol)`
- ✅ **Flatten all positions** - `flatten_position()`
- ✅ **Trailing stop order** - `place_trailing_stop_order()`

---

## Summary

### Function Count by Category

| Category | Count | Functions |
|----------|-------|-----------|
| **Authentication** | 4 | authenticate, refresh_access_token, ensure_authenticated, active_mode |
| **Accounts** | 4 | get_account_info, get_account_balances, get_account_balances_detailed, get_account_balances_bod |
| **Market Data** | 16 | get_bars, search_symbols, get_futures_index_symbols, get_quote_snapshots, get_symbol_details, get_crypto_symbol_names, get_option_expirations, get_option_risk_reward, get_option_spread_types, get_option_strikes, stream_quotes, stream_bars, stream_option_chains, stream_option_quotes, stream_market_depth_quotes, stream_market_depth_aggregates |
| **Positions** | 7 | get_position, get_all_positions, flatten_position, get_todays_profit_loss, get_todays_trades, get_unrealized_profit_loss, stream_positions |
| **Order Execution** | 12 | place_order, cancel_order, modify_order, get_order_executions, is_order_filled, confirm_order, confirm_group_order, place_group_order, get_activation_triggers, get_routes, cancel_all_orders_for_symbol, cancel_all_orders, replace_order |
| **Order Convenience** | 6 | place_limit_order, place_stop_order, place_stop_limit_order, place_trailing_stop_order, place_oco_order, place_bracket_order |
| **Order Queries** | 5 | get_order_history, get_current_orders, get_orders_by_ids, get_historical_orders_by_ids, stream_orders |
| **Order Status Filters** | 5 | get_orders_by_status, get_open_orders, get_filled_orders, get_canceled_orders, get_rejected_orders |
| **Streaming** | 5 | stream_quotes, stream_orders, stream_positions, stream_balances, stream_orders_by_ids |
| **Utilities** | 10 | normalize_order, normalize_position, normalize_quote, normalize_execution, normalize_account, normalize_balances, normalize_account_balances, normalize_bod_balance, get_base_url, parse_api_error_response |
| **Total** | **78** | Unique functions across all modules |

### Access Patterns

All functions are accessible via:

1. **Main SDK Class (Recommended):**
   ```python
   sdk = TradeStationSDK()
   sdk.ensure_authenticated(mode="PAPER")
   result = sdk.get_account_info(mode="PAPER")
   ```

2. **Operation Classes (Direct Access):**
   ```python
   sdk = TradeStationSDK()
   result = sdk.accounts.get_account_info(mode="PAPER")
   result = sdk.market_data.get_bars(...)
   result = sdk.orders.get_current_orders(...)
   ```

3. **Streaming Manager:**
   ```python
   sdk = TradeStationSDK()
   async for quote in sdk.streaming.stream_quotes(["MNQZ25"], mode="PAPER"):
       print(quote)
   ```

### Dual-Mode Support

All functions support dual-mode operation (PAPER/LIVE) via the `mode` parameter:
- If `mode=None`, uses `secrets.trading_mode` (default from environment)
- If `mode="PAPER"`, uses paper trading API (`sim-api.tradestation.com`)
- If `mode="LIVE"`, uses live trading API (`api.tradestation.com`)

---

**Last Updated:** 12-05-2025 15:45:00 EST

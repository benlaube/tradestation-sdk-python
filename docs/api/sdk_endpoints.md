# TradeStation SDK API Endpoint Mapping

## About This Document

This document provides a **comprehensive mapping** between SDK functions and TradeStation API endpoints. It shows which SDK method calls which API endpoint, what HTTP methods are used, and what models are required.

**Use this if:** You need to understand the relationship between SDK functions and API endpoints, see what models are used, or debug API calls.

**Related Documents:**
- 📚 **[API_REFERENCE.md](API_REFERENCE.md)** - Complete SDK API reference
- 📝 **[ORDER_FUNCTIONS_REFERENCE.md](ORDER_FUNCTIONS_REFERENCE.md)** - Detailed order function documentation
- 💡 **[SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md)** - Usage examples
- 📊 **[API_COVERAGE.md](API_COVERAGE.md)** - API coverage analysis
- 🏗️ **[MODELS.md](MODELS.md)** - Pydantic model documentation

## Metadata

- **Status:** Active
- **Created:** 12-05-2025
- **Last Updated:** 12-29-2025 13:16:21 EST
- **Version:** 1.3
- **Description:** Comprehensive mapping between SDK functions and TradeStation API endpoints, including HTTP methods, request/response models, and usage examples organized by operation class
- **Type:** API Reference - Technical reference for developers implementing API integrations
- **Applicability:** When understanding which SDK method calls which API endpoint, what models are used, or how to use specific SDK functions
- **Dependencies:**
  - [`API_REFERENCE.md`](./API_REFERENCE.md) - Complete SDK API reference
  - [`ORDER_FUNCTIONS_REFERENCE.md`](./ORDER_FUNCTIONS_REFERENCE.md) - Detailed order function documentation
  - [`SDK_USAGE_EXAMPLES.md`](./SDK_USAGE_EXAMPLES.md) - Usage examples
  - [`tradestation-api-v3-openapi.json`](../reference/tradestation-api-v3-openapi.json) - Source OpenAPI specification
- **How to Use:** Use this document as a quick reference to find which SDK function maps to which API endpoint, what models are required, and see usage examples

---

## Overview

This document provides a comprehensive mapping between SDK functions and TradeStation API endpoints. It serves as a reference for understanding which SDK methods call which API endpoints, what models are used, and how to use each function.

**Organization:**
- Methods are grouped by operation class
- Each entry shows the SDK function, API endpoint, HTTP method, request/response models, and usage examples
- Convenience functions are clearly marked and show which low-level function they wrap

---

## Order Execution Operations (OrderExecutionOperations)

All methods in this class use the `/orderexecution/` API endpoints for order placement, modification, cancellation, and execution-related operations.

### Core Order Execution Methods

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `place_order()` | `/v3/orderexecution/orders` | POST | `TradeStationOrderRequest` (dict) | `TradeStationOrderResponse` | `sdk.place_order("MNQZ25", "BUY", 2, "Limit", limit_price=25000.00)` |
| `cancel_order()` | `/v3/orderexecution/orders/{orderID}` | DELETE | - | `dict` | `sdk.cancel_order("924243071")` |
| `modify_order()` | `/v3/orderexecution/orders/{orderID}` | PUT | `dict` | `TradeStationOrderResponse` | `sdk.modify_order("924243071", quantity=3, limit_price=25010.00)` |
| `get_order_executions()` | `/v3/orderexecution/orders/{orderID}/executions` | GET | - | `list[TradeStationExecutionResponse]` | `sdk.get_order_executions("924243071")` |

### Order Confirmation Methods

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `confirm_order()` | `/v3/orderexecution/orderconfirm` | POST | `TradeStationOrderRequest` (dict) | `dict` | `sdk.confirm_order("MNQZ25", "BUY", 2, "Limit", limit_price=25000.00)` |
| `confirm_group_order()` | `/v3/orderexecution/ordergroupconfirm` | POST | `TradeStationOrderGroupRequest` (dict) | `dict` | `sdk.confirm_group_order("BRK", orders)` |

### Group Order Methods

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `place_group_order()` | `/v3/orderexecution/ordergroups` | POST | `TradeStationOrderGroupRequest` (dict) | `TradeStationOrderGroupResponse` | `sdk.place_group_order("BRK", orders)` |

### Configuration Methods

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `get_activation_triggers()` | `/v3/orderexecution/activationtriggers` | GET | - | `list[dict]` | `sdk.get_activation_triggers()` |
| `get_routes()` | `/v3/orderexecution/routes` | GET | - | `list[dict]` | `sdk.get_routes()` |

### Convenience Functions

These convenience functions wrap the core methods above to simplify common use cases:

| SDK Function | Wraps | API Endpoint | Method | Example |
|--------------|-------|--------------|--------|---------|
| `place_limit_order()` | `place_order()` | `/v3/orderexecution/orders` | POST | `sdk.place_limit_order("MNQZ25", "BUY", 2, 25000.00)` |
| `place_stop_order()` | `place_order()` | `/v3/orderexecution/orders` | POST | `sdk.place_stop_order("MNQZ25", "SELL", 2, 24900.00)` |
| `place_stop_limit_order()` | `place_order()` | `/v3/orderexecution/orders` | POST | `sdk.place_stop_limit_order("MNQZ25", "SELL", 2, 24950.00, 24900.00)` |
| `place_trailing_stop_order()` | `place_order()` | `/v3/orderexecution/orders` | POST | `sdk.place_trailing_stop_order("MNQZ25", "SELL", 2, trail_amount=1.5)` |
| `place_bracket_order()` | `place_group_order("BRK", ...)` | `/v3/orderexecution/ordergroups` | POST | `sdk.place_bracket_order("MNQZ25", "BUY", 2, 25100.00, 24900.00)` |
| `place_oco_order()` | `place_group_order("OCO", ...)` | `/v3/orderexecution/ordergroups` | POST | `sdk.place_oco_order(orders)` |

**Note:** Convenience functions use the same underlying API endpoints as their wrapped methods but provide simpler interfaces for common order types.

---

## Order Query Operations (OrderOperations)

All methods in this class use the `/brokerage/accounts/.../orders` API endpoints for querying order information.

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `get_order_history()` | `/v3/brokerage/accounts/{accounts}/historicalorders` | GET | - | `list[TradeStationOrderResponse]` | `sdk.get_order_history(start_date="2025-12-01", limit=100)` |
| `get_current_orders()` | `/v3/brokerage/accounts/{accounts}/orders` | GET | - | `dict` with `Orders` list | `sdk.get_current_orders()` |
| `get_orders_by_ids()` | `/v3/brokerage/accounts/{accounts}/orders/{orderIds}` | GET | - | `dict` with `Orders` list | `sdk.get_orders_by_ids("924243071,924243072")` |
| `get_historical_orders_by_ids()` | `/v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}` | GET | - | `dict` with `Orders` list | `sdk.get_historical_orders_by_ids("924243071", start_date="2025-12-01")` |
| `stream_orders()` | `/v3/brokerage/stream/accounts/{accounts}/orders` | GET (stream) | - | `OrderStream` | `async for order in sdk.streaming.stream_orders("SIM123456"):` |

**Note:** `stream_orders()` is accessed via `sdk.streaming.stream_orders()` for consistency with other streaming methods.

---

## Account Operations (AccountOperations)

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `get_account_info()` | `/v3/brokerage/accounts` | GET | - | `AccountsListResponse` | `sdk.get_account_info()` |
| `get_account_balances()` | `/v3/brokerage/accounts/{accountId}` | GET | - | `AccountBalancesResponse` | `sdk.get_account_balances()` |
| `get_account_balances_detailed()` | `/v3/brokerage/accounts/{accounts}/balances` | GET | - | `dict` | `sdk.get_account_balances_detailed("SIM123456")` |
| `get_account_balances_bod()` | `/v3/brokerage/accounts/{accounts}/bodbalances` | GET | - | `BODBalancesResponse` | `sdk.get_account_balances_bod("SIM123456")` |

---

## Market Data Operations (MarketDataOperations)

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `get_bars()` | `/v3/marketdata/barcharts/{symbol}` | GET | - | `BarsResponse` | `sdk.get_bars("MNQZ25", "1", "Minute", bars_back=100)` |
| `get_quote_snapshots()` | `/v3/marketdata/quotes/{symbols}` | GET | - | `QuotesResponse` | `sdk.get_quote_snapshots("MNQZ25,ESZ25")` |
| `search_symbols()` | `/v3/marketdata/symbols/search` | GET | - | `SymbolSearchResponse` | `sdk.search_symbols(pattern="MNQ", category="Future")` |
| `get_symbol_details()` | `/v3/marketdata/symbols/{symbols}` | GET | - | `SymbolDetailsResponse` | `sdk.get_symbol_details("MNQZ25")` |
| `stream_quotes()` | `/v3/marketdata/stream/quotes/{symbols}` | GET (stream) | - | `QuoteStream` | `async for quote in sdk.streaming.stream_quotes(["MNQZ25"]):` |
| `stream_bars()` | `/v3/marketdata/stream/barcharts/{symbol}` | GET (stream) | - | `BarStream` | `async for bar in sdk.market_data.stream_bars("MNQZ25", "1", "Minute"):` |
| `get_option_expirations()` | `/v3/marketdata/options/expirations/{underlying}` | GET | - | `OptionExpirationsResponse` |  |
| `get_option_strikes()` | `/v3/marketdata/options/strikes/{underlying}` | GET | - | `OptionStrikesResponse` |  |
| `get_option_risk_reward()` | `/v3/marketdata/options/riskreward` | POST | `dict` | `OptionRiskRewardResponse` |  |
| `get_option_spread_types()` | `/v3/marketdata/options/spreadtypes` | GET | - | `OptionSpreadTypesResponse` |  |
| `stream_option_chains()` | `/v3/marketdata/stream/options/chains/{underlying}` | GET (stream) | - | `OptionChainStream` |  |
| `stream_option_quotes()` | `/v3/marketdata/stream/options/quotes` | GET (stream) | - | `OptionQuoteStream` |  |
| `stream_market_depth_quotes()` | `/v3/marketdata/stream/marketdepth/quotes/{symbol}` | GET (stream) | - | `MarketDepthQuoteStream` |  |
| `stream_market_depth_aggregates()` | `/v3/marketdata/stream/marketdepth/aggregates/{symbol}` | GET (stream) | - | `MarketDepthAggregateStream` |  |

---

## Order Execution Operations (OrderExecutionOperations)

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `cancel_order()` | `/v3/orderexecution/orders/{orderID}` | DELETE | - | `CancelOrderResponse` | `sdk.cancel_order("924243071")` |
| `confirm_order()` | `/v3/orderexecution/orderconfirm` | POST | `TradeStationOrderRequest` (dict) | `ConfirmOrderResponse` | `sdk.confirm_order("MNQZ25", "BUY", 1, "Limit", limit_price=25000.0)` |
| `confirm_group_order()` | `/v3/orderexecution/ordergroupconfirm` | POST | `TradeStationOrderGroupRequest` (dict) | `ConfirmGroupOrderResponse` | `sdk.confirm_group_order("OCO", orders)` |

---

## Order Query Operations (OrderOperations)

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `get_order_history()` | `/v3/brokerage/accounts/{accountId}/historicalorders` | GET | - | `OrdersWrapper` | `sdk.orders.get_order_history(mode="PAPER")` |
| `get_current_orders()` | `/v3/brokerage/accounts/{accounts}/orders` | GET | - | `OrdersWrapper` | `sdk.orders.get_current_orders(account_ids="SIM123456")` |
| `get_orders_by_ids()` | `/v3/brokerage/accounts/{accounts}/orders/{orderIds}` | GET | - | `OrdersWrapper` | `sdk.orders.get_orders_by_ids("123,456")` |
| `get_historical_orders_by_ids()` | `/v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}` | GET | - | `OrdersWrapper` | `sdk.orders.get_historical_orders_by_ids("123,456")` |

---

## Position Operations (PositionOperations)

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `get_position()` | `/v3/brokerage/accounts/{accountId}/positions` | GET | - | `PositionsResponse` | `sdk.get_position("MNQZ25")` |
| `get_all_positions()` | `/v3/brokerage/accounts/{accountId}/positions` | GET | - | `PositionsResponse` | `sdk.get_all_positions()` |
| `stream_positions()` | `/v3/brokerage/stream/accounts/{accounts}/positions` | GET (stream) | - | `PositionStream` | `async for position in sdk.streaming.stream_positions("SIM123456"):` |

---

## Streaming Operations (StreamingManager)

| SDK Function | API Endpoint | Method | Request Model | Response Model | Example |
|--------------|--------------|--------|---------------|----------------|---------|
| `stream_quotes()` | `/v3/marketdata/stream/quotes/{symbols}` | GET (stream) | - | `QuoteStream` | `async for quote in sdk.streaming.stream_quotes(["MNQZ25"]):` |
| `stream_orders()` | `/v3/brokerage/stream/accounts/{accounts}/orders` | GET (stream) | - | `OrderStream` | `async for order in sdk.streaming.stream_orders("SIM123456"):` |
| `stream_positions()` | `/v3/brokerage/stream/accounts/{accounts}/positions` | GET (stream) | - | `PositionStream` | `async for position in sdk.streaming.stream_positions("SIM123456"):` |
| `stream_balances()` | `/v3/brokerage/stream/accounts/{accounts}/balances` | GET (stream) | - | `BalanceStream` | `async for balance in sdk.streaming.stream_balances("SIM123456"):` |

---

## Usage Patterns

### When to Use Convenience Functions

**Use convenience functions when:**
- You want simpler, more readable code
- You're placing common order types (limit, stop, trailing stop, bracket, OCO)
- You want built-in validation and error handling
- You want type-safe parameters

**Use low-level functions when:**
- You need advanced order configurations
- You're building custom order types
- You need direct access to all API parameters
- You're implementing complex conditional orders

### Examples

**Convenience Function (Recommended):**
```python
# Simple bracket order
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,
    mode="PAPER"
)
```

**Low-Level Function (Advanced):**
```python
# Custom group order with conditional activation
orders = [
    {
        "AccountID": "SIM123456",
        "Symbol": "MNQZ25",
        "TradeAction": "Buy",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": "25000.00",
        "MarketActivationRules": [
            {
                "RuleType": "Price",
                "Symbol": "MNQZ25",
                "Predicate": "gte",
                "TriggerKey": "STT",
                "Price": "25010.00"
            }
        ],
        "TimeInForce": {"Duration": "DAY"}
    }
]
result = sdk.place_group_order("NORMAL", orders, mode="PAPER")
```

---

## Endpoint Path Patterns

### Order Execution Endpoints (`/orderexecution/`)
- `POST /v3/orderexecution/orders` - Place order
- `PUT /v3/orderexecution/orders/{orderID}` - Modify order
- `DELETE /v3/orderexecution/orders/{orderID}` - Cancel order
- `GET /v3/orderexecution/orders/{orderID}/executions` - Get executions
- `POST /v3/orderexecution/orderconfirm` - Confirm order
- `POST /v3/orderexecution/ordergroupconfirm` - Confirm group order
- `POST /v3/orderexecution/ordergroups` - Place group order
- `GET /v3/orderexecution/activationtriggers` - Get activation triggers
- `GET /v3/orderexecution/routes` - Get routing options

### Brokerage Endpoints (`/brokerage/`)
- `GET /v3/brokerage/accounts` - List accounts
- `GET /v3/brokerage/accounts/{accountId}` - Get account details
- `GET /v3/brokerage/accounts/{accounts}/balances` - Get detailed balances
- `GET /v3/brokerage/accounts/{accounts}/bodbalances` - Get BOD balances
- `GET /v3/brokerage/accounts/{accounts}/orders` - Get current orders
- `GET /v3/brokerage/accounts/{accounts}/orders/{orderIds}` - Get orders by IDs
- `GET /v3/brokerage/accounts/{accounts}/historicalorders` - Get order history
- `GET /v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}` - Get historical orders by IDs
- `GET /v3/brokerage/accounts/{accountId}/positions` - Get positions
- `GET /v3/brokerage/stream/accounts/{accounts}/orders` - Stream orders
- `GET /v3/brokerage/stream/accounts/{accounts}/positions` - Stream positions
- `GET /v3/brokerage/stream/accounts/{accounts}/balances` - Stream balances

### Market Data Endpoints (`/marketdata/`)
- `GET /v3/marketdata/barcharts/{symbol}` - Get historical bars
- `GET /v3/marketdata/quotes/{symbols}` - Get quote snapshots
- `GET /v3/marketdata/symbols/search` - Search symbols
- `GET /v3/marketdata/symbols/{symbols}` - Get symbol details
- `GET /v3/marketdata/stream/quotes/{symbols}` - Stream quotes
- `GET /v3/marketdata/stream/barcharts/{symbol}` - Stream bars

---

## Model Usage Summary

### Request Models
- `TradeStationOrderRequest` - Used internally by `place_order()` and convenience functions
- `TradeStationOrderGroupRequest` - Used internally by `place_group_order()` and bracket/OCO functions

### Response Models
- `TradeStationOrderResponse` - Returned from order placement, modification, queries
- `TradeStationOrderGroupResponse` - Returned from group order placement
- `TradeStationExecutionResponse` - Returned from `get_order_executions()`
- `AccountsListResponse` - Returned from `get_account_info()`
- `AccountBalancesResponse` - Returned from `get_account_balances()`
- `BODBalancesResponse` - Returned from `get_account_balances_bod()`
- `PositionsResponse` - Returned from position queries
- `QuotesResponse` - Returned from `get_quote_snapshots()`
- `QuoteStream` - Yielded from `stream_quotes()`
- `OrderStream` - Yielded from `stream_orders()`
- `PositionStream` - Yielded from `stream_positions()`
- `BalanceStream` - Yielded from `stream_balances()`

---

## Quick Reference

### Most Common Operations

**Place Orders:**
- `sdk.place_order()` - Generic order placement
- `sdk.place_limit_order()` - Limit order (convenience)
- `sdk.place_stop_order()` - Stop order (convenience)
- `sdk.place_trailing_stop_order()` - Trailing stop (convenience)
- `sdk.place_bracket_order()` - Bracket order (convenience)
- `sdk.place_oco_order()` - OCO order (convenience)

**Query Orders:**
- `sdk.get_current_orders()` - Current/open orders
- `sdk.get_order_history()` - Historical orders
- `sdk.get_order_executions()` - Order fills/executions

**Stream Data:**
- `sdk.streaming.stream_quotes()` - Real-time quotes
- `sdk.streaming.stream_orders()` - Real-time order updates
- `sdk.streaming.stream_positions()` - Real-time position updates
- `sdk.streaming.stream_balances()` - Real-time balance updates

---

**Last Updated:** 2025-12-05

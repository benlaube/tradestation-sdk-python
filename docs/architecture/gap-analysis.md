# TradeStation SDK Gap Analysis

## About This Document

This document provides **comprehensive gap analysis** identifying missing endpoints, functionality gaps, code quality improvements, and documentation gaps. It's useful for planning SDK enhancements and prioritizing improvements.

**Use this if:** You're planning SDK enhancements, want to identify missing features, or reviewing code quality improvements.

**Related Documents:**
- 📊 **[API_COVERAGE.md](API_COVERAGE.md)** - Current API coverage status
- 🗺️ **[ROADMAP.md](ROADMAP.md)** - Planned improvements and timeline
- 🎯 **[FEATURES.md](../FEATURES.md)** - Current feature overview
- 📖 **[README.md](../README.md)** - SDK documentation
- ⚠️ **[LIMITATIONS.md](../LIMITATIONS.md)** - Known limitations

## Metadata

- **Status:** Active
- **Created:** 12-05-2025
- **Last Updated:** 12-05-2025 14:21:15 EST
- **Version:** 1.0.0
- **Description:** Comprehensive analysis of functionality gaps, missing endpoints, code quality gaps, documentation gaps, and recommendations for SDK improvements
- **Type:** Analysis Report - Technical reference for developers and AI agents planning SDK enhancements
- **Applicability:** When planning SDK enhancements, identifying missing features, or reviewing code quality improvements
- **Dependencies:**
  - [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json) - Source OpenAPI specification for gap comparison
  - [`API_COVERAGE.md`](./API_COVERAGE.md) - Current API coverage status
  - [`SUMMARY.md`](./SUMMARY.md) - SDK enhancement summary
- **How to Use:** Review this document to identify gaps between API capabilities and SDK implementation, prioritize improvements, and plan enhancement work

---

---

## Table of Contents

- [Overview](#overview)
- [Implemented Features](#implemented-features)
- [Missing Endpoints](#missing-endpoints)
- [Code Quality Gaps](#code-quality-gaps)
- [Documentation Gaps](#documentation-gaps)
- [Model Gaps](#model-gaps)
- [Functionality Gaps](#functionality-gaps)
- [Recommendations](#recommendations)

---

## Overview

This document identifies gaps between:
1. **TradeStation API v3 Capabilities** (from [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json))
2. **Current SDK Implementation** (from `src/lib/tradestation/`)
3. **Code Quality Standards** (commenting, error handling, etc.)

**Note:** The OpenAPI specification contains **33 v3 endpoints** organized into 3 main tags:
- **Brokerage** (11 endpoints) - Account, position, and order management
- **MarketData** (14 endpoints) - Market data, quotes, symbols, streaming
- **Order Execution** (8 endpoints) - Order placement, modification, cancellation

---

## OpenAPI Specification Analysis

**Source:** [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json)

### Complete Endpoint Inventory

The OpenAPI specification defines **33 v3 endpoints** across 3 main categories:

#### Brokerage (11 endpoints)

| Method | Path | Operation ID | SDK Implementation |
|--------|------|--------------|-------------------|
| GET | `/v3/brokerage/accounts` | `GetAccounts` | ✅ `accounts.py#get_account_info` |
| GET | `/v3/brokerage/accounts/{accounts}/balances` | `GetBalances` | ✅ `accounts.py#get_detailed_balances` |
| GET | `/v3/brokerage/accounts/{accounts}/bodbalances` | `GetBalancesBOD` | ✅ `accounts.py#get_account_balances_bod` |
| GET | `/v3/brokerage/accounts/{accounts}/historicalorders` | `GetHistoricalOrders` | ✅ `orders.py#get_historical_orders` |
| GET | `/v3/brokerage/accounts/{accounts}/historicalorders/{orderIds}` | `GetHistoricalOrdersByOrderID` | ✅ `orders.py#get_historical_orders_by_ids` |
| GET | `/v3/brokerage/accounts/{accounts}/orders` | `GetOrders` | ✅ `orders.py#get_current_orders` |
| GET | `/v3/brokerage/accounts/{accounts}/orders/{orderIds}` | `GetOrdersByOrderID` | ✅ `orders.py#get_orders_by_ids` |
| GET | `/v3/brokerage/accounts/{accounts}/positions` | `GetPositions` | ✅ `positions.py#get_positions` |
| GET | `/v3/brokerage/stream/accounts/{accounts}/orders` | `StreamOrders` | ✅ `streaming.py#stream_orders` |
| GET | `/v3/brokerage/stream/accounts/{accounts}/orders/{ordersIds}` | `StreamOrdersByOrderId` | ✅ `streaming.py#stream_orders_by_ids` |
| GET | `/v3/brokerage/stream/accounts/{accounts}/positions` | `StreamPositions` | ✅ `streaming.py#stream_positions` |

**Note:** Missing from OpenAPI but implemented: `/v3/brokerage/stream/accounts/{accounts}/balances` (Balance streaming)

#### MarketData (14 endpoints)

| Method | Path | Operation ID | SDK Implementation |
|--------|------|--------------|-------------------|
| GET | `/v3/marketdata/barcharts/{symbol}` | `GetBars` | ✅ `market_data.py#get_bars` |
| GET | `/v3/marketdata/options/expirations/{underlying}` | `GetOptionExpirations` | ✅ `market_data.py#get_option_expirations` |
| POST | `/v3/marketdata/options/riskreward` | `GetOptionRiskReward` | ✅ `market_data.py#get_option_risk_reward` |
| GET | `/v3/marketdata/options/spreadtypes` | `GetOptionSpreadTypes` | ✅ `market_data.py#get_option_spread_types` |
| GET | `/v3/marketdata/options/strikes/{underlying}` | `GetOptionStrikes` | ✅ `market_data.py#get_option_strikes` |
| GET | `/v3/marketdata/quotes/{symbols}` | `GetQuoteSnapshots` | ✅ `market_data.py#get_quote_snapshots` |
| GET | `/v3/marketdata/stream/barcharts/{symbol}` | `StreamBars` | ✅ `market_data.py#stream_bars` |
| GET | `/v3/marketdata/stream/marketdepth/aggregates/{symbol}` | `StreamMarketDepthAggregates` | ✅ `market_data.py#stream_market_depth_aggregates` |
| GET | `/v3/marketdata/stream/marketdepth/quotes/{symbol}` | `StreamMarketDepthQuotes` | ✅ `market_data.py#stream_market_depth_quotes` |
| GET | `/v3/marketdata/stream/options/chains/{underlying}` | `GetOptionChain` | ✅ `market_data.py#stream_option_chains` |
| GET | `/v3/marketdata/stream/options/quotes` | `GetOptionQuotes` | ✅ `market_data.py#stream_option_quotes` |
| GET | `/v3/marketdata/stream/quotes/{symbols}` | `GetQuoteChangeStream` | ✅ `streaming.py#stream_quotes` |
| GET | `/v3/marketdata/symbollists/cryptopairs/symbolnames` | `GetCryptoSymbolNames` | ✅ `market_data.py#get_crypto_symbol_names` |
| GET | `/v3/marketdata/symbols/{symbols}` | `GetSymbolDetails` | ✅ `market_data.py#get_symbol_details` |

**Note:** Missing from OpenAPI: Symbol search endpoint (implemented via v2 endpoint)

#### Order Execution (8 endpoints)

| Method | Path | Operation ID | SDK Implementation |
|--------|------|--------------|-------------------|
| GET | `/v3/orderexecution/activationtriggers` | `GetActivationTriggers` | ✅ `orders.py#get_activation_triggers` |
| POST | `/v3/orderexecution/orderconfirm` | `ConfirmOrder` | ✅ `orders.py#confirm_order` |
| POST | `/v3/orderexecution/ordergroupconfirm` | `ConfirmGroupOrder` | ✅ `orders.py#confirm_group_order` |
| POST | `/v3/orderexecution/ordergroups` | `PlaceGroupOrder` | ✅ `orders.py#place_group_order` |
| POST | `/v3/orderexecution/orders` | `PlaceOrder` | ✅ `orders.py#place_order` |
| PUT | `/v3/orderexecution/orders/{orderID}` | `ReplaceOrder` | ✅ `orders.py#modify_order` |
| DELETE | `/v3/orderexecution/orders/{orderID}` | `CancelOrder` | ✅ `orders.py#cancel_order` |
| GET | `/v3/orderexecution/routes` | `Routes` | ✅ `orders.py#get_routing_options` |

**Note:** Missing from OpenAPI but implemented: `/v3/orderexecution/orders/{orderID}/executions` (Get order executions)

### Coverage Summary

- **Total v3 Endpoints in OpenAPI:** 33
- **Endpoints Implemented in SDK:** 33 (100%)
- **Additional Endpoints Implemented:** 2 (balance streaming, order executions)
- **Overall Coverage:** ✅ **100% of OpenAPI v3 endpoints + 2 additional endpoints**

### Code Examples

The OpenAPI specification contains **190 code examples** across multiple languages:
- **Shell (curl)** - 33 examples
- **Node.js** - 33 examples  
- **Python** - 33 examples
- **C#** - 33 examples
- **JSON (requestBody examples)** - 58 examples

See [`OPENAPI_CODE_EXAMPLES.md`](./OPENAPI_CODE_EXAMPLES.md) for complete list.

### Mermaid Diagrams

Visual representations of the API structure:
- [`API_STRUCTURE.md`](./API_STRUCTURE.md) - High-level structure diagram (embedded Mermaid)
- [`API_STRUCTURE_DETAILED.md`](./API_STRUCTURE_DETAILED.md) - Detailed endpoint diagram (embedded Mermaid)

**How to View:** These diagrams render automatically in:
- **Cursor/VS Code:** Open the `.md` file and use markdown preview (Cmd+Shift+V / Ctrl+Shift+V)
- **GitHub:** Navigate to the file - diagrams render automatically
- **Online:** Copy the Mermaid code block to [Mermaid Live Editor](https://mermaid.live)

---

## Implemented Features

### ✅ Fully Implemented

**Authentication:**
- ✅ OAuth2 Authorization Code flow
- ✅ Token refresh (automatic)
- ✅ Token storage (PAPER and LIVE separate)
- ✅ Token revocation

**Accounts:**
- ✅ List accounts (`brokerage/accounts`)
- ✅ Get account details (`brokerage/accounts/{accountId}`)
- ✅ Get account balances (basic via account details)
- ✅ Get detailed balances (`brokerage/accounts/{accounts}/balances`)
- ✅ Get BOD balances (`brokerage/accounts/{accounts}/bodbalances`)

**Market Data - REST:**
- ✅ Historical bars (`marketdata/barcharts/{symbol}`)
- ✅ Symbol search (`marketdata/symbols/search`)
- ✅ Quote snapshots (`marketdata/quotes/{symbols}`)
- ✅ Symbol details (`marketdata/symbols/{symbols}`)
- ✅ Futures index symbols (via search)
- ✅ Crypto symbol names (`marketdata/symbollists/cryptopairs/symbolnames`)
- ✅ Option expirations (`marketdata/options/expirations/{underlying}`)
- ✅ Option risk/reward (`marketdata/options/riskreward`)
- ✅ Option spread types (`marketdata/options/spreadtypes`)
- ✅ Option strikes (`marketdata/options/strikes/{underlying}`)

**Market Data - Streaming:**
- ✅ Real-time quotes (`marketdata/stream/quotes/{symbols}`)
- ✅ Real-time bars (`marketdata/stream/barcharts/{symbol}`) - Available but not used
- ✅ Option chains streaming (`marketdata/stream/options/chains/{underlying}`) - Available but not used
- ✅ Option quotes streaming (`marketdata/stream/options/quotes`) - Available but not used
- ✅ Market depth quotes (`marketdata/stream/marketdepth/quotes/{symbol}`) - Available but not used
- ✅ Market depth aggregates (`marketdata/stream/marketdepth/aggregates/{symbol}`) - Available but not used

**Orders - REST:**
- ✅ Place order (`orderexecution/orders`)
- ✅ Cancel order (`orderexecution/orders/{orderId}`)
- ✅ Modify order (`orderexecution/orders/{orderId}`)
- ✅ Order history (`brokerage/accounts/{accounts}/historicalorders`)
- ✅ Order executions (`orderexecution/orders/{orderId}/executions`)
- ✅ Confirm order (`orderexecution/orderconfirm`) - Available but not used
- ✅ Get current orders (`brokerage/accounts/{accounts}/orders`) - Available but not used
- ✅ Get orders by IDs (`brokerage/accounts/{accounts}/orders/{orderIds}`) - Available but not used
- ✅ Get historical orders by IDs (`brokerage/accounts/{accounts}/historicalorders/{orderIds}`) - Available but not used
- ✅ Activation triggers (`orderexecution/activationtriggers`)
- ✅ Group order confirm (`orderexecution/ordergroupconfirm`)
- ✅ Group order place (`orderexecution/ordergroups`)
- ✅ Routing options (`orderexecution/routes`)

**Orders - Streaming:**
- ✅ Order updates (`brokerage/stream/accounts/{accountId}/orders`)
- ✅ Orders by IDs streaming (`brokerage/stream/accounts/{accounts}/orders/{ordersIds}`)

**Positions - REST:**
- ✅ Get positions (`brokerage/accounts/{accountId}/positions`)

**Positions - Streaming:**
- ✅ Position updates (`brokerage/stream/accounts/{accountId}/positions`)

---

## Missing Endpoints

### ❌ Not Implemented

**Account Streaming:**
- ✅ `brokerage/stream/accounts/{accountId}/balances` - Real-time balance updates
  - **Status:** Implemented in `streaming.py` as `stream_balances()`
  - **Priority:** Medium
  - **Complexity:** Low (similar to positions streaming)

**Market Data - REST:**
- ❌ `marketdata/symbollists/*` - Other symbol list endpoints (beyond crypto)
  - **Impact:** Limited symbol discovery
  - **Priority:** Low
  - **Complexity:** Low

**Market Data - Streaming:**
- ⚠️ All streaming endpoints are implemented but some are not actively used
  - `stream_bars()` - Implemented but not used
  - `stream_option_chains()` - Implemented but not used
  - `stream_option_quotes()` - Implemented but not used
  - `stream_market_depth_quotes()` - Implemented but not used
  - `stream_market_depth_aggregates()` - Implemented but not used

**Orders - REST:**
- ⚠️ Several endpoints implemented but not actively used:
  - `get_current_orders()` - Implemented but not used
  - `get_orders_by_ids()` - Implemented but not used
  - `get_historical_orders_by_ids()` - Implemented but not used
  - `confirm_order()` - Implemented but not used

---

## Code Quality Gaps

### Commenting Gaps

**Issues Found:**
1. **Inconsistent Dependencies Documentation:**
   - Some functions reference `BaseAPIClient` instead of `HTTPClient` in docstrings
   - **Files Affected:** `orders.py` (7 occurrences)
   - **Status:** ⚠️ Needs fixing

2. **Missing Function-Level Comments:**
   - All functions have docstrings ✅
   - All functions have "Dependencies" sections ✅
   - Some complex functions could use more inline comments

3. **Missing Class-Level Documentation:**
   - All classes have docstrings ✅
   - Some classes could benefit from usage examples

4. **Missing Module-Level Documentation:**
   - All modules have docstrings ✅
   - Some modules could use architecture diagrams

### Error Handling Gaps

**Issues Found:**
1. **Inconsistent Error Handling:**
   - Some methods return tuples `(success, message)`
   - Some methods raise exceptions
   - Some methods return `None` on error
   - **Recommendation:** Standardize on exception-based error handling with custom exceptions

2. **Missing Retry Logic:**
   - HTTP client has basic error handling
   - No automatic retry for transient failures
   - **Recommendation:** Add retry logic with exponential backoff

3. **Missing Rate Limit Handling:**
   - No explicit rate limit detection
   - No rate limit backoff
   - **Recommendation:** Add `RateLimitError` handling with backoff

### Type Safety Gaps

**Issues Found:**
1. **Streaming Responses Not Validated:**
   - Streaming methods return `dict[str, Any]` instead of Pydantic models
   - **Recommendation:** Use `QuoteStream`, `OrderStream`, `PositionStream` models
   - **Status:** ⚠️ Models created but not used in streaming methods

2. **Request Validation:**
   - Some methods accept raw dictionaries instead of Pydantic models
   - **Recommendation:** Use `TradeStationOrderRequest` for order placement

---

## Documentation Gaps

### Missing Documentation

1. **API Reference Documentation:**
   - ✅ README.md created
   - ❌ Detailed API reference per module
   - ❌ Method signature documentation
   - ❌ Parameter descriptions
   - ❌ Return value descriptions
   - ❌ Exception documentation

2. **Usage Examples:**
   - ✅ Basic examples in README
   - ❌ Advanced usage examples
   - ❌ Error handling examples
   - ❌ Streaming examples with error handling
   - ❌ Multi-account examples

3. **Migration Guide:**
   - ✅ Migration guide in README
   - ❌ Detailed migration examples
   - ❌ Breaking changes documentation

4. **Architecture Documentation:**
   - ✅ High-level architecture in README
   - ❌ Detailed component diagrams
   - ❌ Data flow diagrams
   - ❌ Sequence diagrams for common operations

5. **Testing Documentation:**
   - ❌ Unit test examples
   - ❌ Integration test examples
   - ❌ Mocking examples

---

## Model Gaps

### Missing Models

1. **Account Models:**
   - ❌ `AccountResponse` - REST API account response
   - ❌ `BalanceResponse` - REST API balance response
   - ❌ `BalanceDetail` - Detailed balance information
   - ❌ `CurrencyDetail` - Currency-specific balance details
   - ❌ `BODBalance` - Beginning of Day balance
   - ❌ `StreamBalance` - Streaming balance update

2. **Market Data Models:**
   - ❌ `BarResponse` - Historical bar response
   - ❌ `SymbolSearchResponse` - Symbol search response
   - ❌ `QuoteSnapshotResponse` - Quote snapshot response
   - ❌ `SymbolDetailsResponse` - Symbol details response
   - ❌ `OptionChainResponse` - Option chain response
   - ❌ `OptionQuoteResponse` - Option quote response
   - ❌ `MarketDepthQuote` - Market depth quote
   - ❌ `MarketDepthAggregate` - Market depth aggregate

3. **Order Models:**
   - ✅ `TradeStationOrderRequest` - Order placement request
   - ✅ `TradeStationOrderResponse` - REST order response
   - ✅ `OrderStream` - Streaming order update
   - ❌ `OrderHistoryResponse` - Order history response wrapper
   - ❌ `OrderExecutionResponse` - Order execution response (different from `TradeStationExecutionResponse`)

4. **Position Models:**
   - ✅ `PositionStream` - Streaming position update
   - ❌ `PositionResponse` - REST position response (simple: Symbol, Quantity)

### Model Completeness

**QuoteStream Model:**
- ✅ All major fields from API v3 spec
- ✅ MarketFlags nested model
- ⚠️ Some optional fields may be missing (need to verify against API spec)

**OrderStream Model:**
- ✅ Same structure as REST order response
- ✅ All fields captured
- ✅ Conditional orders, activation rules, trailing stops

**PositionStream Model:**
- ✅ All fields from API v3 spec
- ✅ Deleted flag for position closures
- ✅ P&L fields (TodaysProfitLoss, UnrealizedProfitLoss, etc.)

---

## Functionality Gaps

### Missing Features

1. **Account Balance Streaming:**
   - ❌ Real-time balance updates
   - **Impact:** Can't track balance changes in real-time
   - **Priority:** Medium

2. **Order Status Polling:**
   - ⚠️ Streaming available but no polling fallback
   - **Impact:** If streaming fails, no way to check order status
   - **Priority:** Low (streaming is reliable)

3. **Batch Operations:**
   - ❌ Batch order placement
   - ❌ Batch order cancellation
   - **Impact:** Can't efficiently manage multiple orders
   - **Priority:** Low

4. **Order Modification Validation:**
   - ⚠️ Modify order doesn't validate current order state
   - **Impact:** May attempt to modify orders that can't be modified
   - **Priority:** Low

5. **Connection Pooling:**
   - ❌ No connection pooling for HTTP requests
   - **Impact:** Slower performance for high-frequency requests
   - **Priority:** Low (current performance is acceptable)

6. **Request Caching:**
   - ❌ No caching for read-only requests (symbol details, etc.)
   - **Impact:** Unnecessary API calls
   - **Priority:** Low

7. **Webhook Support:**
   - ❌ No webhook endpoint support
   - **Impact:** Can't receive TradeStation webhooks
   - **Priority:** Low (not part of API v3)

---

## Recommendations

### High Priority

1. **Fix Docstring References:**
   - Update all `BaseAPIClient` references to `HTTPClient` in docstrings
   - **Files:** `orders.py` (7 occurrences)

2. **Use Streaming Models:**
   - Update streaming methods to return Pydantic models instead of raw dicts
   - **Files:** `streaming.py`, `market_data.py`, `orders.py`, `positions.py`

3. **Add Account Balance Streaming:**
   - Implement `stream_balances()` method
   - **Location:** `accounts.py` or `streaming.py`

### Medium Priority

1. **Standardize Error Handling:**
   - Use custom exceptions consistently
   - Remove tuple return patterns
   - **Files:** `orders.py`, `positions.py`

2. **Add Retry Logic:**
   - Implement automatic retry for transient failures
   - **Location:** `client.py`

3. **Create Missing Models:**
   - Add account response models
   - Add market data response models
   - **Location:** `models/responses.py`

4. **Enhance Documentation:**
   - Create detailed API reference
   - Add more usage examples
   - **Location:** `docs/API_REFERENCE.md`

### Low Priority

1. **Add Request Validation:**
   - Use Pydantic models for all requests
   - **Location:** All operation modules

2. **Add Connection Pooling:**
   - Use `httpx.AsyncClient` with connection pooling
   - **Location:** `client.py`

3. **Add Request Caching:**
   - Cache read-only requests (symbol details, etc.)
   - **Location:** `client.py` or operation modules

---

## Summary

### Implementation Status

- **Total API Endpoints:** ~30
- **Implemented:** ~25 (83%)
- **Actively Used:** ~18 (60%)
- **Missing:** ~5 (17%)

### Code Quality Status

- **Docstrings:** ✅ Complete (minor fixes needed)
- **Type Hints:** ✅ Complete
- **Error Handling:** ⚠️ Needs standardization
- **Models:** ⚠️ Streaming models created but not used

### Documentation Status

- **README:** ✅ Complete
- **API Reference:** ❌ Missing
- **Examples:** ⚠️ Basic examples only
- **Architecture:** ⚠️ High-level only

---

**Next Steps:**
1. Fix docstring references (High Priority)
2. Use streaming models in streaming methods (High Priority)
3. Add account balance streaming (High Priority)
4. Standardize error handling (Medium Priority)
5. Create detailed API reference (Medium Priority)

---

**Last Updated:** 2025-12-05


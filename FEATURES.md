# TradeStation SDK - Feature Overview

## About This Document

This document provides a **visual overview of all SDK features and capabilities**. It's organized by feature category with tables showing function names, descriptions, and mode support. Use this as a quick reference to see what the SDK can do.

**Use this if:** You want to see all available features at a glance, compare capabilities, or find specific functions.

**Related Documents:**
- 📖 **[README.md](README.md)** - Complete SDK documentation
- 📚 **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - Detailed API reference for all functions
- 📋 **[CHEATSHEET.md](CHEATSHEET.md)** - Quick code snippets
- 💡 **[docs/SDK_USAGE_EXAMPLES.md](docs/SDK_USAGE_EXAMPLES.md)** - Usage examples
- 🎯 **[docs/FEATURE_COMPARISON.md](docs/FEATURE_COMPARISON.md)** - Comparison with other SDKs

---

Visual overview of all SDK features and capabilities.

---

## 🎯 Core Features

### Authentication & Security

| Feature | Status | Description |
|---------|--------|-------------|
| OAuth2 Authorization Code Flow | ✅ | Automatic browser-based authentication |
| Automatic Token Refresh | ✅ | Tokens refresh automatically when expired |
| PAPER/LIVE Mode Support | ✅ | Seamless switching between simulator and live |
| Dual-Mode Token Storage | ✅ | Separate tokens for PAPER and LIVE |
| Credential Sanitization | ✅ | Sensitive data redacted from logs |
| Token Encryption | 📋 v1.1 | System keychain integration (planned) |

---

### Account Operations (4 functions)

| Function | Description | Mode Support |
|----------|-------------|--------------|
| `get_account_info()` | Get account details, ID, name, type | PAPER ✅ LIVE ✅ |
| `get_account_balances()` | Get equity, buying power, margin, P&L | PAPER ✅ LIVE ✅ |
| `get_account_balances_detailed()` | Detailed balances with BalanceDetail | PAPER ✅ LIVE ✅ |
| `get_account_balances_bod()` | Beginning of Day balances | PAPER ✅ LIVE ✅ |

---

### Market Data (16+ functions)

| Function | Description | Mode Support |
|----------|-------------|--------------|
| `get_bars()` | Historical OHLCV bars | PAPER ✅ LIVE ✅ |
| `search_symbols()` | Search stocks, futures, options | PAPER ✅ LIVE ✅ |
| `get_quote_snapshots()` | Current bid/ask/last prices | PAPER ✅ LIVE ✅ |
| `get_symbol_details()` | Symbol metadata (exchange, category) | PAPER ✅ LIVE ✅ |
| `get_futures_index_symbols()` | List of futures symbols | PAPER ✅ LIVE ✅ |
| `get_crypto_symbol_names()` | List of crypto symbols | PAPER ✅ LIVE ✅ |
| **Options Data** | Expirations, strikes, spreads | PAPER ✅ LIVE ✅ |
| **More...** | See [API_REFERENCE.md](docs/API_REFERENCE.md) | |

---

### Order Execution (18+ functions)

#### Basic Order Types

| Order Type | Function | Description |
|------------|----------|-------------|
| Market | `place_order(order_type="Market")` | Execute immediately at market price |
| Limit | `place_limit_order()` | Execute at specified price or better |
| Stop | `place_stop_order()` | Trigger at stop price |
| Stop-Limit | `place_stop_limit_order()` | Stop + Limit combination |
| Trailing Stop | `place_trailing_stop_order()` | Stop that trails price |

#### Advanced Order Types

| Order Type | Function | Description |
|------------|----------|-------------|
| Bracket (BRK) | `place_bracket_order()` | Entry + Profit Target + Stop Loss |
| OCO | `place_oco_order()` | One-Cancels-Other orders |
| Conditional | `place_group_order()` | Market/time activation rules |

#### Order Management

| Function | Description |
|----------|-------------|
| `cancel_order()` | Cancel specific order |
| `cancel_all_orders()` | Cancel all open orders |
| `cancel_all_orders_for_symbol()` | Cancel all orders for symbol |
| `modify_order()` | Modify quantity, price |
| `replace_order()` | Cancel + place new order |
| `confirm_order()` | Pre-flight check (dry-run) |
| `get_activation_triggers()` | List activation triggers |
| `get_routes()` | List routing options |

---

### Order Queries (10+ functions)

| Function | Description |
|----------|-------------|
| `get_order_history()` | Historical orders (date range) |
| `get_current_orders()` | All current/open orders |
| `get_orders_by_ids()` | Get specific orders by ID |
| `get_orders_by_status()` | Filter by status |
| `get_open_orders()` | Convenience: all open orders |
| `get_filled_orders()` | Convenience: all filled orders |
| `get_canceled_orders()` | Convenience: all canceled orders |
| `get_rejected_orders()` | Convenience: all rejected orders |
| `get_order_executions()` | Get fills for order |
| `is_order_filled()` | Check if order filled |

---

### Position Management (6 functions)

| Function | Description |
|----------|-------------|
| `get_position()` | Get position for symbol (quantity) |
| `get_all_positions()` | Get all positions |
| `flatten_position()` | Close position (specific or all) |
| `get_todays_profit_loss()` | Today's P&L |
| `get_unrealized_profit_loss()` | Unrealized P&L |
| `get_todays_trades()` | Today's filled trades |

---

### Streaming (5+ functions)

| Function | Description | Features |
|----------|-------------|----------|
| `streaming.stream_quotes()` | Real-time quote updates | Auto-reconnect ✅, REST fallback ✅ |
| `streaming.stream_orders()` | Real-time order updates | Auto-reconnect ✅, REST fallback ✅ |
| `streaming.stream_positions()` | Real-time position updates | Auto-reconnect ✅, REST fallback ✅ |
| `streaming.stream_balances()` | Real-time balance updates | Auto-reconnect ✅ |
| `streaming.get_stream_health()` | Stream health metrics | Health tracking ✅ |

**Streaming Features:**
- ✅ Automatic reconnection (exponential backoff)
- ✅ REST polling fallback (if streaming fails)
- ✅ Session auto-recovery (token refresh)
- ✅ Stream health tracking
- ✅ Configurable retry logic (max retries, delays)
- ✅ Error categorization (recoverable vs non-recoverable)

**REST API Features:**
- ✅ Built-in retry logic with exponential backoff (v1.0.0)
- ✅ Automatic retry for recoverable errors (network, rate limits, server errors)
- ✅ Configurable retry parameters (max_retries, retry_delay, max_retry_delay)
- ✅ Rate limit handling with server Retry-After header support
- ✅ Comprehensive retry attempt logging
- ✅ Error categorization (recoverable vs non-recoverable)

---

### Error Handling

#### Exception Types

| Exception | When Raised | Recoverable? |
|-----------|-------------|--------------|
| `TradeStationAPIError` | Base exception | N/A |
| `AuthenticationError` | Auth failure (401, 403) | ❌ No |
| `TokenExpiredError` | Token expired | ✅ Yes (auto-refresh) |
| `InvalidTokenError` | Invalid token | ❌ No |
| `RateLimitError` | Rate limit (429) | ✅ Yes (backoff) |
| `InvalidRequestError` | Bad request (400) | ❌ No |
| `NetworkError` | Network failure | ✅ Yes (retry - REST & Streaming) |
| `RecoverableError` | Transient failure | ✅ Yes (retry - REST & Streaming) |
| `NonRecoverableError` | Permanent failure | ❌ No |

#### Error Details

All exceptions include `ErrorDetails` with:
- ✅ Human-readable error message
- ✅ API error code and message
- ✅ Full request context (method, endpoint, params, body)
- ✅ Response details (status, body)
- ✅ Operation context (which SDK method failed)
- ✅ Trading mode (PAPER/LIVE)
- ✅ Structured dict export (`to_dict()`)

---

### Type Safety

| Model Type | Count | Purpose |
|------------|-------|---------|
| **Request Models** | 2 | Type-safe API requests |
| **REST Response Models** | 10+ | Type-safe API responses |
| **Streaming Models** | 7 | Type-safe streaming data |
| **Total Models** | 19+ | Complete type coverage |

**Features:**
- ✅ Pydantic validation
- ✅ IDE autocomplete
- ✅ Type hints everywhere
- ✅ Runtime validation
- ✅ Self-documenting

---

### Utilities & Helpers

| Feature | Description |
|---------|-------------|
| `info()` | SDK diagnostics and status |
| `normalize_order()` | Order data normalization |
| `normalize_position()` | Position data normalization |
| `get_base_url()` | Get API base URL for mode |

---

## 📊 API Coverage

### TradeStation API v3 Coverage

| Category | Coverage | Status |
|----------|----------|--------|
| **Accounts** | 100% (4/4) | ✅ Complete |
| **Market Data** | 90% (16/18) | ✅ Excellent |
| **Orders** | 95% (28/30) | ✅ Excellent |
| **Positions** | 100% (4/4) | ✅ Complete |
| **Streaming** | 80% (5/7) | ✅ Good |
| **Overall** | **92% (57/62)** | ✅ Production Ready |

**Missing:**
- OptionChain variations (low priority)
- BarCharts streaming (low priority)

See [API_COVERAGE.md](docs/API_COVERAGE.md) for details.

---

## 🔧 Developer Experience

### Quick Start Metrics

| Metric | Time | Difficulty |
|--------|------|------------|
| **Install SDK** | 30 seconds | ⭐ Trivial |
| **First authentication** | 2 minutes | ⭐ Easy |
| **First API call** | 3 minutes | ⭐ Easy |
| **First order** | 5 minutes | ⭐⭐ Moderate |
| **First stream** | 8 minutes | ⭐⭐ Moderate |
| **Production deploy** | 3-7 days | ⭐⭐⭐ Advanced |

### Documentation Completeness

| Type | Status | Count |
|------|--------|-------|
| **Quick Starts** | ✅ | 3 guides (2min, 5min, 15min) |
| **API Reference** | ✅ | Complete (all functions) |
| **Code Examples** | ✅ | 100+ examples |
| **Interactive Notebooks** | ✅ | 3 notebooks |
| **CLI Tools** | ✅ | 2 tools |
| **Troubleshooting** | ✅ | 8+ common issues |
| **Security** | ✅ | Comprehensive guide |
| **Deployment** | ✅ | 4 cloud platforms |

---

## 🎓 Learning Resources

### For Beginners

- 📖 [QUICKSTART.md](QUICKSTART.md) - 2-minute setup
- 📓 [01_authentication.ipynb](examples/01_authentication.ipynb) - Interactive auth
- 🔧 [test_connection.py](cli/test_connection.py) - Verify setup
- 📋 [CHEATSHEET.md](CHEATSHEET.md) - Quick reference

### For Developers

- 📚 [README.md](README.md) - Complete guide
- 💡 [SDK_USAGE_EXAMPLES.md](docs/SDK_USAGE_EXAMPLES.md) - Code examples
- 🏗️ [ARCHITECTURE.md](docs/ARCHITECTURE.md) - Architecture deep-dive
- 📖 [API_REFERENCE.md](docs/API_REFERENCE.md) - Function reference

### For Production

- 🔒 [SECURITY.md](SECURITY.md) - Security best practices
- 🚀 [DEPLOYMENT.md](DEPLOYMENT.md) - Deployment guide
- ⚠️ [LIMITATIONS.md](LIMITATIONS.md) - Know the constraints
- 📊 [ROADMAP.md](ROADMAP.md) - Future plans

---

## 📚 Documentation Quick Links

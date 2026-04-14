# TradeStation SDK

**Version:** 1.0.0  
**Status:** Production Ready  
**Python:** 3.10+  
**License:** MIT

## About This Document

This is the **main entry point** for the TradeStation Python SDK documentation. It provides:
- Complete SDK overview and feature list
- Quick start guide (5 minutes)
- Comprehensive API reference links
- FAQ and troubleshooting
- Links to all other documentation

**Start here if:** You're new to the SDK or want a complete overview.

**Related Documents:**
- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Get started in 2 minutes (even faster than this guide)
- 📋 **[CHEATSHEET.md](CHEATSHEET.md)** - Quick reference for common operations
- 📦 **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation instructions for all platforms
- 📖 **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** - 15-minute comprehensive tutorial
- 📚 **[docs/INDEX.md](docs/INDEX.md)** - Complete documentation index and navigation
- ⚠️ **[LIMITATIONS.md](LIMITATIONS.md)** - Known constraints and workarounds
- 🔒 **[SECURITY.md](SECURITY.md)** - Security best practices
- 🚀 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment guide
- 🔄 **[MIGRATION.md](MIGRATION.md)** - Migrate from other SDKs
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- 🎯 **[FEATURES.md](FEATURES.md)** - Complete feature overview
- 🗺️ **[docs/ROADMAP.md](docs/ROADMAP.md)** - Future development plans

---

A comprehensive, self-contained Python SDK for TradeStation API v3. This SDK provides complete access to TradeStation's REST API and HTTP Streaming endpoints without external dependencies.

[![PyPI](https://img.shields.io/badge/pypi-tradestation--python--sdk-blue)](https://pypi.org/project/tradestation-python-sdk/)
[![Python](https://img.shields.io/badge/python-3.10+-blue)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Tests](https://img.shields.io/badge/tests-90%25%2B-brightgreen)](tests/)

---

## 🚀 Quick Links

| New to SDK? | Documentation | Tools & Examples |
|------------|---------------|------------------|
| [2-Min Quick Start](QUICKSTART.md) | [Complete README](README.md) | [Jupyter Notebooks](examples/) |
| [15-Min Tutorial](docs/GETTING_STARTED.md) | [API Reference](docs/API_REFERENCE.md) | [CLI Tools](cli/) |
| [Installation Guide](INSTALLATION.md) | [Usage Examples](docs/SDK_USAGE_EXAMPLES.md) | [Cheat Sheet](CHEATSHEET.md) |

| Need Help? | Going Live? | Contributing? |
|------------|-------------|---------------|
| [FAQ & Troubleshooting](README.md#faq--troubleshooting) | [Security Guide](SECURITY.md) | [Contributing Guide](CONTRIBUTING.md) |
| [Known Limitations](LIMITATIONS.md) | [Deployment Guide](DEPLOYMENT.md) | [Roadmap](docs/ROADMAP.md) |
| [Migration Guide](MIGRATION.md) | [Production Checklist](DEPLOYMENT.md#checklist-before-going-live) | [GitHub Issues](https://github.com/benlaube/tradestation-python-sdk/issues) |

---

## 📚 Documentation Hub

- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Get started in 2 minutes
- 📋 **[CHEATSHEET.md](CHEATSHEET.md)** - Quick reference (print and keep!)
- 📦 **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation guide
- 🔄 **[MIGRATION.md](MIGRATION.md)** - Migrate from other SDKs
- ⚠️ **[LIMITATIONS.md](LIMITATIONS.md)** - Known constraints and workarounds
- 🔒 **[SECURITY.md](SECURITY.md)** - Security best practices
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history
- 🗺️ **[docs/ROADMAP.md](docs/ROADMAP.md)** - Future plans

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Quick Start (5 Minutes)](#quick-start-5-minutes)
- [FAQ & Troubleshooting](#faq--troubleshooting)
- [API Rate Limits](#api-rate-limits)
- [Known Limitations](#known-limitations)
- [Architecture](#architecture)
- [API Reference](#api-reference)
- [Streaming](#streaming)
- [Error Handling](#error-handling)
- [Models](#models)
- [Examples](#examples)
- [Migration Guide](#migration-guide)
- [Contributing](#contributing)
- [Security](#security)
- [License](#license)

---

## Overview

The TradeStation SDK is a complete implementation of TradeStation API v3 functionality, including:

- **OAuth2 Authentication** - Automated token management for PAPER and LIVE modes
- **REST API Operations** - Accounts, market data, orders, positions
- **HTTP Streaming** - Real-time quotes, orders, positions, market depth, options
- **Advanced Orders** - Bracket orders, OCO orders, conditional orders, trailing stops
- **Type Safety** - Pydantic models for all requests and responses
- **Error Handling** - Custom exceptions with detailed error information

### Why Internal SDK?

This SDK was created to:
- **Remove External Dependencies** - No reliance on `tastyware/tradestation` or other external packages
- **Complete Data Capture** - Ensures all 30+ fields from TradeStation API are captured
- **Full Control** - Complete control over API integration and error handling
- **Better Maintainability** - Self-contained, easier to extend and maintain

---

## Features

### ✅ Core Features

- **Dual-Mode Support** - Seamless switching between PAPER and LIVE trading modes
- **Automatic Token Refresh** - Handles OAuth token refresh automatically
- **Comprehensive API Coverage** - All major TradeStation API v3 endpoints
- **HTTP Streaming** - Real-time data via HTTP Streaming (NDJSON)
- **Type-Safe Models** - Pydantic models for all API requests and responses
- **Streaming Models** - Separate models for streaming responses (different from REST)
- **Error Handling** - Custom exceptions with automatic retry logic and error categorization
- **Data Normalization** - Mappers to normalize API responses to consistent format

### ✅ Supported Operations

**Accounts:**
- List accounts
- Get account details
- Get account balances (basic and detailed)
- Get Beginning of Day (BOD) balances

**Market Data:**
- Historical bars
- Symbol search
- Quote snapshots
- Symbol details
- Futures index symbols
- Crypto symbol names
- Option expirations, strikes, risk/reward
- Option spread types

**Orders:**
- Place orders (Market, Limit, Stop, StopLimit, TrailingStop)
- Cancel orders
- Modify orders
- Get order history
- Get current orders
- Get order executions
- Confirm orders (pre-flight check)
- Bracket orders (BRK)
- OCO orders (One-Cancels-Other)
- Conditional orders (market/time activation)
- Get activation triggers
- Get routing options

**Positions:**
- Get position for symbol
- Get all positions
- Flatten positions (close all or specific symbol)

**Streaming:**
- Real-time quotes
- Real-time order updates
- Real-time position updates
- Real-time bars
- Option chains streaming
- Option quotes streaming
- Market depth quotes
- Market depth aggregates

---

## Installation

### Via pip (Recommended for Standalone Use)
```bash
pip install tradestation-python-sdk
```

### From Source
```bash
git clone https://github.com/benlaube/tradestation-python-sdk.git
cd tradestation-python-sdk
pip install -e .
```

### Development Installation
```bash
pip install -e ".[dev]"
```

### As Part of Existing Project
If you're using this SDK as part of the trading bot project, dependencies are managed via `requirements.txt`:

```bash
pip install -r requirements.txt
```

### Use as Git Submodule (Vendored)
For monorepos or to pin the SDK to a specific commit without publishing to PyPI:

```bash
git submodule add -b main git@github.com:<your-org>/tradestation-python-sdk.git libs/tradestation-sdk
pip install -e ./libs/tradestation-sdk
```

See [docs/SUBMODULE_INTEGRATION.md](docs/SUBMODULE_INTEGRATION.md) for the full workflow, CI tips, and update/rollback steps.

**Required Dependencies:**
- `httpx>=0.27.2` - HTTP client for API requests and streaming
- `PyJWT>=2.8.0` - JWT token parsing
- `pydantic>=2.12.5` - Data validation and models
- `python-dotenv>=1.0.0` - Environment variable management

---

## Quick Start (5 Minutes)

### Step 1: Set Up Credentials

Create a `.env` file in your project directory:

```env
TRADESTATION_CLIENT_ID=your_client_id_here
TRADESTATION_CLIENT_SECRET=your_client_secret_here
TRADESTATION_REDIRECT_URI=http://localhost:8888/callback
TRADESTATION_MODE=PAPER
```

`TRADESTATION_MODE` is the canonical mode variable. `TRADING_MODE` is still accepted as a deprecated fallback for compatibility.

**Get your credentials:**
1. Go to [TradeStation Developer Portal](https://developer.tradestation.com)
2. Create an application
3. Copy your Client ID and Client Secret
4. Set Redirect URI to `http://localhost:8888/callback`

### Step 2: First Script (Hello TradeStation!)

```python
from tradestation import TradeStationSDK

# Initialize SDK
sdk = TradeStationSDK()

# Authenticate (opens browser for first-time login)
sdk.authenticate(mode="PAPER")

# Get account info
account = sdk.get_account_info(mode="PAPER")
print(f"✅ Connected to account: {account['account_id']}")

# Get account balance
balances = sdk.get_account_balances(mode="PAPER")
print(f"💰 Buying Power: ${balances['buying_power']:.2f}")
print(f"📊 Equity: ${balances['equity']:.2f}")
```

**Run it:**
```bash
python my_first_script.py
```

Your browser will open for TradeStation login (first time only). After that, tokens are saved and authentication is automatic!

### Step 3: Place Your First Order

```python
# Place a limit order for AAPL stock
order_id, status = sdk.place_limit_order(
    symbol="AAPL",
    side="BUY",
    quantity=10,
    limit_price=150.00,
    mode="PAPER"
)
print(f"✅ Order placed: {order_id}")

# Check order status
orders = sdk.get_current_orders(mode="PAPER")
print(f"📝 Open orders: {len(orders['Orders'])}")
```

### Step 4: Stream Real-Time Data

```python
import asyncio

async def stream_quotes():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")
    
    async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
        print(f"📈 AAPL: Last=${quote.Last}, Bid=${quote.Bid}, Ask=${quote.Ask}")

asyncio.run(stream_quotes())
```

**That's it!** You're now trading with TradeStation API. 🎉

---

## Next Steps

- 📖 [Complete API Reference](docs/API_REFERENCE.md)
- 💡 [Usage Examples](docs/SDK_USAGE_EXAMPLES.md)
- 🔧 [Advanced Features](#streaming)
- ❓ [FAQ & Troubleshooting](#faq--troubleshooting)
- 📊 [Interactive Examples (Jupyter Notebooks)](#examples)

---

## FAQ & Troubleshooting

### Common Issues

#### ❌ "Port 8888 already in use"

**Problem:** OAuth callback server can't bind to port 8888.

**Solution:**

**Option 1:** Kill the process using port 8888
```bash
# macOS/Linux:
lsof -ti:8888 | xargs kill -9

# Windows:
netstat -ano | findstr :8888
taskkill /PID <PID> /F
```

**Option 2:** Change redirect URI in `.env`
```env
TRADESTATION_REDIRECT_URI=http://localhost:9999/callback
```

#### ❌ "Authentication failed: Invalid credentials"

**Problem:** Client ID or secret is incorrect.

**Solution:**
1. Verify credentials in [TradeStation Developer Portal](https://developer.tradestation.com)
2. Ensure `.env` file is in the same directory as your script
3. Check for typos or extra spaces in credentials
4. Make sure redirect URI matches exactly (including `http://` and `/callback`)

#### ❌ "Token expired"

**Problem:** Access token has expired (20-minute lifespan).

**Solution:** SDK automatically refreshes tokens. If refresh fails:
```python
# Re-authenticate
sdk.authenticate(mode="PAPER")
```

#### ❌ "Symbol 'MNQZ25' not found"

**Problem:** Futures contract has expired or symbol is incorrect.

**Solution:** Search for the current contract month:
```python
# Find current MNQ contract
symbols = sdk.search_symbols(pattern="MNQ", category="Future", mode="PAPER")
current_contract = symbols[0]['Symbol']  # e.g., "MNQH26" (March 2026)
print(f"Current contract: {current_contract}")
```

#### ❌ "Rate limit exceeded (429)"

**Problem:** Too many API requests in a short time.

**Solution:**
```python
import time

# Add delay between requests
for symbol in ["AAPL", "MSFT", "GOOGL"]:
    data = sdk.get_bars(symbol, "1", "Minute", 100, mode="PAPER")
    time.sleep(0.5)  # 500ms delay

# OR use batching for quotes
quotes = sdk.get_quote_snapshots("AAPL,MSFT,GOOGL", mode="PAPER")
```

#### ❌ "ModuleNotFoundError: No module named 'config'"

**Problem:** When using SDK standalone, it tries to import project-specific modules.

**Solution:** Use environment variables directly:
```python
import os
os.environ['TRADESTATION_CLIENT_ID'] = 'your_client_id'
os.environ['TRADESTATION_CLIENT_SECRET'] = 'your_client_secret'

from tradestation_sdk import TradeStationSDK
sdk = TradeStationSDK()
```

#### ❌ "Streaming connection closed unexpectedly"

**Problem:** HTTP streaming connection dropped.

**Solution:** SDK has automatic reconnection (v1.0.0+):
```python
# Automatic reconnection is enabled by default
async for quote in sdk.streaming.stream_quotes(
    ["AAPL"],
    mode="PAPER",
    auto_reconnect=True,       # Enabled by default
    max_retries=10,            # Retry up to 10 times
    fallback_to_polling=True   # Fall back to REST polling if streaming fails
):
    print(quote.Last)
```

### Getting Help

- 📖 **Documentation:** Check [docs/](docs/) for detailed guides
- 🐛 **Bug Reports:** [Open an issue](https://github.com/benlaube/tradestation-python-sdk/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)
- 📧 **Email:** benlaube@example.com

---

## API Rate Limits

TradeStation API v3 has rate limits to prevent abuse:

- **General Endpoints:** ~120 requests per minute
- **Market Data:** ~60 requests per minute
- **Streaming:** 10 concurrent streams per account
- **Order Placement:** ~60 orders per minute

### Best Practices for Rate Limit Management

**1. Add Delays Between Requests**
```python
import time

for symbol in symbols:
    data = sdk.get_bars(symbol, "1", "Minute", 100, mode="PAPER")
    time.sleep(0.5)  # 500ms delay = ~120 requests/minute max
```

**2. Batch Requests When Possible**
```python
# ❌ Bad: Individual requests for each symbol (3 API calls)
for symbol in ["AAPL", "MSFT", "GOOGL"]:
    quote = sdk.get_quote_snapshots(symbol, mode="PAPER")

# ✅ Good: Batch request (1 API call)
quotes = sdk.get_quote_snapshots("AAPL,MSFT,GOOGL", mode="PAPER")
```

**3. Use Streaming for Real-Time Data**
```python
# ❌ Bad: Polling quotes every second (60+ API calls/minute)
while True:
    quote = sdk.get_quote_snapshots("AAPL", mode="PAPER")
    time.sleep(1)

# ✅ Good: Use streaming (1 connection, unlimited updates)
async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
    print(f"Last: {quote.Last}")
```

**4. Retry Logic (Built-in)**
```python
# Retry logic is now built-in! All REST API methods automatically retry recoverable errors.
# No manual retry wrapper needed for most cases.

# Default: 3 retries with exponential backoff (1s, 2s, 4s)
order_id, status = sdk.place_order("MNQZ25", "BUY", 2, mode="PAPER")
# Automatically retries on network errors, rate limits, server errors

# Custom retry configuration (if needed)
sdk._client.max_retries = 5  # Increase max retries
sdk._client.retry_delay = 2.0  # Start with 2s delay
sdk._client.max_retry_delay = 120.0  # Allow up to 2min delay
```

### Rate Limit Errors

When you exceed rate limits, the SDK raises `RateLimitError`:

```python
from tradestation_sdk import RateLimitError

try:
    order_id, status = sdk.place_order(...)
except RateLimitError as e:
    # Check response for retry-after header
    retry_after = e.details.response_body.get('RetryAfter', 60)
    print(f"Rate limit exceeded. Retry after: {retry_after}s")
    time.sleep(retry_after)
```

---

## Known Limitations

### Current Constraints

1. **Token Storage Security**
   - **Issue:** Tokens stored as plain JSON in `logs/tokens_*.json`
   - **Not encrypted at rest**
   - **Risk:** Local file access = token access
   - **Mitigation:** Planned for v1.1 (system keychain encryption)
   - **Workaround:** Secure file permissions on Linux/macOS:
     ```bash
     chmod 600 logs/tokens_*.json
     ```

2. **OAuth Port Conflicts**
   - **Issue:** OAuth callback requires port 8888 (or configured port)
   - **Manual intervention needed if port in use**
   - **Mitigation:** Planned for v1.1 (auto-port selection)
   - **Workaround:** Change port in `.env` or kill process on port 8888

3. **Built-in Retry Logic for REST API** ✅ **Implemented in v1.0.0**
   - **Status:** All REST API methods now have automatic retry with exponential backoff
   - **Features:** Retries recoverable errors (network, rate limits, server errors)
   - **Configuration:** Customizable max_retries, retry_delay, max_retry_delay
   - **Note:** Streaming methods already had retry logic; now REST API methods match

4. **Streaming Reconnection Improvements**
   - **Status:** Automatic reconnection added in v1.0.0 ✅
   - **Includes:** Exponential backoff, REST polling fallback, health tracking
   - **Future:** v1.2 will add circuit breaker pattern

5. **Synchronous HTTP Client**
   - **Issue:** Uses `requests` library (blocking I/O)
   - **Not ideal for high-concurrency applications**
   - **Mitigation:** Planned for v2.0 (native async with `httpx`)
   - **Workaround:** Use thread pools for concurrent requests

6. **Bar Data Interval Limits**
   - **Issue:** Only minute-based intervals supported (1, 2, 5, etc.)
   - **Second-based intervals (30S, 60S) return API errors**
   - **Limitation:** TradeStation API v3 constraint (cannot be fixed by SDK)
   - **Workaround:** Use minute intervals and resample data locally

7. **Account ID Resolution**
   - **Issue:** If not set in `.env`, SDK selects first futures account
   - **Multi-account scenarios may need explicit IDs**
   - **Mitigation:** Always set `TRADESTATION_ACCOUNT_ID` in `.env` for production

8. **Trailing Stop Units**
   - **Issue:** `trail_amount` is in price points, not dollars
   - **For MNQ:** 1 point = $2.00 (can be confusing)
   - **Mitigation:** v1.1 will add `trail_amount_dollars` parameter
   - **Workaround:** Convert manually (e.g., $3 stop = 1.5 points)

### Dependency Constraints

- **Python Version:** Requires Python 3.10+ (type hints, async support)
- **Operating System:** Cross-platform (Windows, macOS, Linux)
- **Network:** Requires stable internet connection for OAuth and streaming

### Planned Improvements

See [CHANGELOG.md](CHANGELOG.md) and [GitHub Issues](https://github.com/benlaube/tradestation-python-sdk/issues) for planned enhancements.

**Roadmap:**
- **v1.1:** Token encryption, auto-port selection, improved error messages
- **v1.2:** Circuit breaker pattern, request caching, rate limit tracking
- **v2.0:** Native async support, WebSocket implementation, connection pooling

---

## Error Handling

The SDK provides comprehensive error handling with descriptive error messages and structured error details.

### Exception Types

- **`TradeStationAPIError`** - Base exception for all API errors
- **`AuthenticationError`** - Authentication failures (401, 403)
- **`TokenExpiredError`** - Access token has expired
- **`InvalidTokenError`** - Token is invalid or missing
- **`RateLimitError`** - Rate limit exceeded (429)
- **`InvalidRequestError`** - Invalid API request (400)
- **`SDKValidationError`** - Request/response payload failed SDK contract validation
- **`NetworkError`** - Network/connection errors (500+)
- **`RecoverableError`** - Errors that can be retried (network, temporary failures)
- **`NonRecoverableError`** - Errors that should not be retried (authentication, invalid request)

### Error Details

All exceptions include structured `ErrorDetails` with:
- Human-readable error messages
- API error codes and messages
- Full request context (method, endpoint, params, body)
- Response details (status, body)
- Operation context (which SDK method failed)
- Trading mode (PAPER/LIVE)
- Validation details for schema drift or malformed payloads

### Validation Contract

- Exported Pydantic request/response models use `extra="forbid"` by default.
- Unknown broker fields are treated as schema drift and raise `SDKValidationError`.
- Validation errors include sanitized payload excerpts and Pydantic error details.
- Audited SDK boundaries now fail loud instead of silently returning `{}`, `[]`, or raw fallback payloads on parse failures.

### Example Error Handling

```python
from tradestation import (
    TradeStationSDK,
    TradeStationAPIError,
    AuthenticationError,
    InvalidRequestError,
    SDKValidationError,
)

sdk = TradeStationSDK()

try:
    order_id, status = sdk.place_order(
        symbol="INVALID_SYMBOL",
        side="BUY",
        quantity=1,
        mode="PAPER"
    )
except InvalidRequestError as e:
    # Human-readable error message
    print(f"Error: {e}")
    
    # Structured error details
    details = e.to_dict()
    print(f"API Error Code: {details['api_error_code']}")
    print(f"Request: {details['request_method']} {details['request_endpoint']}")
    print(f"Operation: {details['operation']}")
except SDKValidationError as e:
    details = e.to_dict()
    print(f"Validation failed: {details['message']}")
    print(f"Validation Errors: {details['validation_errors']}")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    sdk.authenticate(mode="PAPER")
except TradeStationAPIError as e:
    print(f"API error: {e}")
```

### Error Message Format

Errors provide both human-readable and structured formats:

**Human-Readable:**
```
Order placement failed: Invalid symbol 'INVALID_SYMBOL'
  - API Error Code: INVALID_SYMBOL
  - Request: POST orderexecution/orders
  - Mode: PAPER
```

Validation failures use the same structured style:

```
Get Quote Snapshots failed: Response validation failed for QuotesResponse

  Request Details:
    - Endpoint: marketdata/quotes/MNQZ25
    - Mode: PAPER

  Validation Errors:
    - {'type': 'extra_forbidden', 'loc': ('Quotes', 0, 'UnexpectedField'), 'msg': 'Extra inputs are not permitted'}
```

**Structured (via `to_dict()`):**
```python
{
    "code": "SDK_VALIDATION_ERROR",
    "message": "Response validation failed for QuotesResponse",
    "api_error_code": None,
    "request_method": None,
    "request_endpoint": "marketdata/quotes/MNQZ25",
    "mode": "PAPER",
    "operation": "get_quote_snapshots",
    "validation_errors": [...]
}
```

---

## Logging Configuration

The SDK provides comprehensive logging of all API requests and responses.

### Standard Logging

By default, the SDK logs:
- Request method, endpoint, and parameters
- Response status, timing, and size
- Response body (truncated to 500 characters)
- Errors with full context

### Full Request/Response Logging

Enable full logging to capture complete request and response bodies (useful for debugging):

```python
# Enable via SDK initialization
sdk = TradeStationSDK(enable_full_logging=True)

# Or via environment variable
# export TRADESTATION_FULL_LOGGING=true
sdk = TradeStationSDK()  # Reads from environment
```

When enabled:
- Complete request bodies are logged (no truncation)
- Complete response bodies are logged (no truncation)
- All sensitive data (tokens, passwords) is automatically redacted

### Logging Levels

The SDK respects the project's logging configuration:
- **DEBUG** - Full request/response details
- **INFO** - Important operations (orders, authentication)
- **WARNING** - API errors (400+ status codes)
- **ERROR** - Exceptions and failures

### Log Output

Logs are written to:
- **Console** - Colorized output with categories
- **File** - Session-based log files (`logs/session_YYYYMMDD_HHMMSS.log`)
- **Database** - Optional Supabase logging (if configured)

### Example Log Output

**Standard Logging:**
```
[bot|api_request|tradestation_api] - API Request: POST orderexecution/orders | Params: None | Body: {'AccountID': 'SIM123456', 'Symbol': 'MNQZ25', ...} (truncated)
[bot|api_response|tradestation_api] - API Response: POST orderexecution/orders | Status: 200 | Time: 0.234s | Size: 456 bytes
```

**Full Logging:**
```
[bot|api_request|tradestation_api] - API Request: POST orderexecution/orders | Params: None | Body: {'AccountID': 'SIM123456', 'Symbol': 'MNQZ25', 'TradeAction': 'BUY', 'OrderType': 'Market', 'Quantity': '1', 'TimeInForce': {'Duration': 'DAY'}}
[bot|api_response|tradestation_api] - API Response: POST orderexecution/orders | Status: 200 | Time: 0.234s | Size: 456 bytes | Body: {"Orders": [{"OrderID": "924243071", "Status": "REC", ...}]}
```

---
print(f"Order placed: {order_id}")

# Get positions
positions = sdk.get_all_positions(mode="PAPER")
for pos in positions:
    print(f"{pos['Symbol']}: {pos['Quantity']}")
```

### Streaming Example

```python
import asyncio
from src.lib.tradestation import TradeStationSDK

async def stream_quotes():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")
    
    # SDK handles reconnection, retry, and fallback automatically
    async for quote in sdk.streaming.stream_quotes(
        ["MNQZ25"],
        mode="PAPER",
        auto_reconnect=True,      # Automatic reconnection on errors
        fallback_to_polling=True  # REST polling fallback if streaming fails
    ):
        print(f"{quote.Symbol}: Last={quote.Last}, Bid={quote.Bid}, Ask={quote.Ask}")

asyncio.run(stream_quotes())
```

### Convenience Functions Example

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Place a bracket order using convenience function (recommended)
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,
    entry_price=None,  # Market entry
    mode="PAPER"
)

# Extract order IDs from result
entry_order_id = result["Orders"][0]["OrderID"]
profit_order_id = result["Orders"][1]["OrderID"]
stop_order_id = result["Orders"][2]["OrderID"]
print(f"Bracket order placed: Entry={entry_order_id}, Profit={profit_order_id}, Stop={stop_order_id}")

# Place limit order (convenience)
order_id, status = sdk.place_limit_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    limit_price=25000.00,
    mode="PAPER"
)

# Place trailing stop (convenience)
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # $3.00 trail for MNQ
    mode="PAPER"
)
```

### Advanced Orders Example (Low-Level)

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Place a bracket order using low-level API (for advanced configurations)
bracket_orders = [
    {
        "AccountID": "SIM123456",
        "Symbol": "MNQZ25",
        "TradeAction": "Buy",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": "25000.00",
        "TimeInForce": {"Duration": "DAY"}
    },
    {
        "AccountID": "SIM123456",
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": "25050.00",  # Profit target
        "TimeInForce": {"Duration": "GTC"}
    },
    {
        "AccountID": "SIM123456",
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "StopMarket",
        "Quantity": "2",
        "StopPrice": "24950.00",  # Stop loss
        "TimeInForce": {"Duration": "GTC"}
    }
]

result = sdk.place_group_order(
    group_type="BRK",
    orders=bracket_orders,
    mode="PAPER"
)
print(f"Bracket order placed: {result}")
```

---

## Architecture

### Directory Structure

```
src/lib/tradestation/
├── __init__.py              # Main SDK class and exports
├── session.py               # OAuth authentication and token management
├── client.py                # HTTP client for API requests
├── exceptions.py            # Custom SDK exceptions
├── accounts.py              # Account operations
├── market_data.py           # Market data operations
├── orders.py                # Order operations
├── positions.py             # Position operations
├── streaming.py              # HTTP streaming manager
├── mappers.py                # Data normalization functions
├── models/                  # Pydantic models
│   ├── __init__.py
│   ├── requests.py          # Request models (order placement, etc.)
│   ├── responses.py         # REST API response models
│   └── streaming.py         # Streaming API response models
└── docs/                    # SDK documentation
    ├── README.md            # This file
    ├── API_COVERAGE.md      # API endpoint coverage analysis
    └── MODELS.md            # Model documentation
```

### Core Components

**TradeStationSDK** (`__init__.py`)
- Main SDK class that composes all modules
- Provides unified interface for all operations
- Manages authentication and mode switching

**TokenManager** (`session.py`)
- OAuth2 token management
- Automatic token refresh
- Separate token storage for PAPER and LIVE modes

**HTTPClient** (`client.py`)
- HTTP request handling
- Authentication header injection
- Request/response logging
- HTTP Streaming support (NDJSON)

**Operation Modules** (`accounts.py`, `order_executions.py`, `orders.py`, `positions.py`, `market_data.py`)
- Domain-specific API operations
- Type-safe method signatures
- Comprehensive error handling
- **OrderExecutionOperations** - Order placement, modification, cancellation, executions (uses `/orderexecution/` endpoints)
- **OrderOperations** - Order queries and streaming (uses `/brokerage/accounts/.../orders` endpoints)

**StreamingManager** (`streaming.py`)
- HTTP Streaming session management
- Real-time data streaming
- Automatic reconnection with exponential backoff
- Session auto-recovery
- REST polling fallback
- Stream health tracking

**Models** (`models/`)
- Pydantic models for type safety
- Request models (order placement, etc.)
- Response models (REST API)
- Streaming models (HTTP Streaming API)

**Mappers** (`mappers.py`)
- Data normalization functions
- Handles attribute name variations (PascalCase, camelCase)
- Converts API responses to consistent format

---

## API Reference

### TradeStationSDK Class

Main SDK class providing access to all operations.

#### Initialization

```python
sdk = TradeStationSDK()
```

#### Authentication Methods

```python
# Authenticate (opens browser for first-time login)
sdk.authenticate(mode="PAPER")

# Refresh access token
sdk.refresh_access_token(mode="PAPER")

# Ensure authenticated (auto-refreshes if needed)
sdk.ensure_authenticated(mode="PAPER")

# Get active mode
mode = sdk.active_mode  # Returns "PAPER" or "LIVE"
```

#### Account Methods

```python
# Get account information
account = sdk.get_account_info(mode="PAPER")

# Get account balances (basic)
balances = sdk.get_account_balances(mode="PAPER", account_id="SIM123456")

# Get detailed account balances
detailed = sdk.get_account_balances_detailed(account_ids="SIM123456", mode="PAPER")

# Get Beginning of Day balances
bod = sdk.get_account_balances_bod(account_ids="SIM123456", mode="PAPER")
```

#### Market Data Methods

```python
# Get historical bars
bars = sdk.get_bars(
    symbol="MNQZ25",
    interval="1",
    unit="Minute",
    bars_back=200,
    mode="PAPER"
)

# Search symbols
symbols = sdk.search_symbols(
    pattern="MNQ",
    category="Future",
    asset_type="Index",
    mode="PAPER"
)

# Get quote snapshots
quotes = sdk.get_quote_snapshots("MNQZ25,ESZ25", mode="PAPER")

# Get symbol details
details = sdk.get_symbol_details("MNQZ25", mode="PAPER")
```

#### Order Execution Methods

**Core Order Execution:**
```python
# Place order (generic - supports all order types)
order_id, status = sdk.place_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    order_type="Market",
    mode="PAPER"
)

# Cancel order
success, message = sdk.cancel_order(order_id="924243071", mode="PAPER")

# Modify order
success, message = sdk.modify_order(
    order_id="924243071",
    quantity=3,
    limit_price=25000.00,
    mode="PAPER"
)

# Get order executions (fills)
executions = sdk.get_order_executions(order_id="924243071", mode="PAPER")

# Confirm order (pre-flight check)
confirmation = sdk.confirm_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    order_type="Limit",
    limit_price=25000.00,
    mode="PAPER"
)
```

**Convenience Functions (Recommended):**
```python
# Place limit order (convenience wrapper)
order_id, status = sdk.place_limit_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    limit_price=25000.00,
    mode="PAPER"
)

# Place stop order (convenience wrapper)
order_id, status = sdk.place_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    stop_price=24900.00,
    mode="PAPER"
)

# Place stop-limit order (convenience wrapper)
order_id, status = sdk.place_stop_limit_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    limit_price=24950.00,
    stop_price=24900.00,
    mode="PAPER"
)

# Place trailing stop order (convenience wrapper)
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # $3.00 trail for MNQ (1.5 points = $3.00)
    mode="PAPER"
)

# Place bracket order (convenience - uses proper group order API)
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,
    entry_price=None,  # Market entry
    mode="PAPER"
)
# Returns: {"GroupID": "...", "Orders": [entry, profit, stop], ...}

# Place OCO order (convenience wrapper)
oco_orders = [
    {"AccountID": "SIM123456", "Symbol": "MNQZ25", "TradeAction": "Buy", ...},
    {"AccountID": "SIM123456", "Symbol": "MNQZ25", "TradeAction": "SellShort", ...}
]
result = sdk.place_oco_order(oco_orders, mode="PAPER")
```

**Group Orders (Low-Level):**
```python
# Place group order (low-level - for advanced use cases)
result = sdk.place_group_order(
    group_type="BRK",  # or "OCO", "NORMAL"
    orders=[...],  # List of order dictionaries
    mode="PAPER"
)

# Confirm group order
confirmation = sdk.confirm_group_order(
    group_type="BRK",
    orders=[...],
    mode="PAPER"
)
```

**Configuration:**
```python
# Get activation triggers (for conditional orders)
triggers = sdk.get_activation_triggers(mode="PAPER")

# Get routing options
routes = sdk.get_routes(mode="PAPER")
```

#### Order Query Methods

```python
# Get order history
history = sdk.get_order_history(
    start_date="2025-12-01",
    end_date="2025-12-05",
    limit=100,
    mode="PAPER"
)

# Get current orders
current = sdk.get_current_orders(account_ids="SIM123456", mode="PAPER")

# Get orders by IDs
orders = sdk.get_orders_by_ids(
    order_ids="924243071,924243072",
    account_ids="SIM123456",
    mode="PAPER"
)

# Get historical orders by IDs
historical = sdk.get_historical_orders_by_ids(
    order_ids="924243071",
    account_ids="SIM123456",
    start_date="2025-12-01",
    mode="PAPER"
)
```

**Note:** Order execution methods (placement, modification, cancellation) are in `OrderExecutionOperations`, while order query methods (history, current orders) are in `OrderOperations`. Both are accessible via the main SDK class for backward compatibility.

#### Position Methods

```python
# Get position for symbol
quantity = sdk.get_position(symbol="MNQZ25", mode="PAPER")

# Get all positions
positions = sdk.get_all_positions(mode="PAPER")

# Flatten position (close all or specific symbol)
flattened = sdk.flatten_position(symbol="MNQZ25", mode="PAPER")
```

### StreamingManager

Access streaming operations via `sdk.streaming`:

```python
# Stream quotes (returns QuoteStream models)
async for quote in sdk.streaming.stream_quotes(["MNQZ25"], mode="PAPER"):
    print(f"{quote.Symbol}: Last={quote.Last}, Bid={quote.Bid}, Ask={quote.Ask}")

# Stream orders (returns OrderStream models)
async for order in sdk.streaming.stream_orders(account_id="SIM123456", mode="PAPER"):
    print(f"Order {order.OrderID}: {order.Status} - {order.Symbol}")

# Stream positions (returns PositionStream models)
async for position in sdk.streaming.stream_positions(account_id="SIM123456", mode="PAPER"):
    print(f"{position.Symbol}: {position.Quantity} @ {position.AveragePrice}")

# Stream balances (returns dict - no model yet)
async for balance in sdk.streaming.stream_balances(account_id="SIM123456", mode="PAPER"):
    print(balance)
```

---

## Streaming

### HTTP Streaming vs WebSockets

TradeStation API v3 uses **HTTP Streaming** (long-lived HTTP connections with NDJSON), not true WebSockets. The SDK's `StreamingManager` handles HTTP Streaming endpoints.

### Streaming Endpoints

**Quotes:**
- Endpoint: `GET /v3/marketdata/stream/quotes/{symbols}`
- Returns: `QuoteStream` objects
- Fields: Last, Bid, Ask, Volume, VWAP, High52Week, Low52Week, MarketFlags, etc.

**Orders:**
- Endpoint: `GET /v3/brokerage/stream/accounts/{accountId}/orders`
- Returns: `OrderStream` objects
- Fields: Same as REST order responses, delivered in real-time

**Positions:**
- Endpoint: `GET /v3/brokerage/stream/accounts/{accountId}/positions`
- Returns: `PositionStream` objects
- Fields: AveragePrice, Last, Bid, Ask, TodaysProfitLoss, UnrealizedProfitLoss, etc.

**Balances:**
- Endpoint: `GET /v3/brokerage/stream/accounts/{accountId}/balances`
- Returns: Balance update dictionaries
- Fields: AccountID, Equity, BuyingPower, CashBalance, TodaysProfitLoss, etc.

### Control Messages

Streams include control messages:
- **StreamStatus** - `"EndSnapshot"` (initial snapshot complete), `"GoAway"` (server shutdown)
- **Heartbeat** - Sent every 5 seconds on idle streams
- **StreamErrorResponse** - Error messages

### Example: Streaming Quotes

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, QuoteStream

async def main():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")
    
    async for quote in sdk.streaming.stream_quotes(["MNQZ25"], mode="PAPER"):
        # Streaming methods now return QuoteStream models directly
        # Control messages (StreamStatus, Heartbeat) are filtered automatically
        print(f"{quote.Symbol}: Last={quote.Last}, Bid={quote.Bid}, Ask={quote.Ask}")
        print(f"  Volume: {quote.Volume}, VWAP: {quote.VWAP}")
        print(f"  52W High: {quote.High52Week}, 52W Low: {quote.Low52Week}")

asyncio.run(main())
```

---

## Error Handling

The SDK provides custom exceptions for better error handling:

```python
from src.lib.tradestation import (
    TradeStationSDK,
    TradeStationAPIError,
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    NetworkError,
    TokenExpiredError,
    InvalidTokenError
)

try:
    sdk = TradeStationSDK()
    sdk.place_order(...)
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    # Re-authenticate
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # Implement backoff
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
    # Fix request parameters
except NetworkError as e:
    print(f"Network error: {e}")
    # Retry with backoff
except TokenExpiredError as e:
    print(f"Token expired: {e}")
    # Refresh token
except TradeStationAPIError as e:
    print(f"API error: {e}")
    # Handle generic API error
```

### Exception Hierarchy

```
TradeStationAPIError (base)
├── AuthenticationError
│   ├── TokenExpiredError
│   └── InvalidTokenError
├── RateLimitError
├── InvalidRequestError
└── NetworkError
```

---

## Models

### Request Models

All exported request/response models now inherit a strict SDK base that forbids unknown fields by default.

**TradeStationOrderRequest**
- Used for placing single orders
- Fields: AccountID, Symbol, TradeAction, OrderType, Quantity, LimitPrice, StopPrice, TimeInForce, TrailAmount, TrailPercent

**TradeStationOrderGroupRequest**
- Used for placing group orders (OCO/Bracket)
- Fields: Type (OCO/BRK/NORMAL), Orders (list of TradeStationOrderRequest)

### Response Models (REST API)

**TradeStationOrderResponse**
- Complete order response with all 30+ fields
- Includes: OrderID, Status, Legs, ConditionalOrders, MarketActivationRules, etc.

**TradeStationOrderGroupResponse**
- Group order response
- Fields: GroupID, GroupName, Type, Orders

**TradeStationExecutionResponse**
- Order execution (fill) response
- Fields: ExecutionID, Symbol, TradeAction, Quantity, Price, Commission, ExecutionTime

### Streaming Models

**QuoteStream**
- Streaming quote response
- Additional fields: High52Week, Low52Week, MarketFlags, Restrictions, DailyOpenInterest, etc.

**OrderStream**
- Streaming order update
- Same structure as TradeStationOrderResponse, delivered in real-time

**PositionStream**
- Streaming position update
- Detailed fields: AveragePrice, Last, Bid, Ask, TodaysProfitLoss, UnrealizedProfitLoss, MarkToMarketPrice, etc.

**StreamStatus**
- Control message: "EndSnapshot", "GoAway"

**Heartbeat**
- Keep-alive message: Heartbeat (int), Timestamp

**StreamErrorResponse**
- Error message: Error, Message, AccountID, Symbol

### Using Models

```python
from tradestation import (
    TradeStationSDK,
    TradeStationOrderRequest,
    QuoteStream,
    OrderStream,
    PositionStream
)

# Create request model
order_request = TradeStationOrderRequest(
    AccountID="SIM123456",
    Symbol="MNQZ25",
    TradeAction="Buy",
    OrderType="Limit",
    Quantity="2",
    LimitPrice="25000.00",
    TimeInForce={"Duration": "DAY"}
)

# Parse streaming response
async for data in sdk.streaming.stream_quotes(["MNQZ25"]):
    quote = QuoteStream(**data)
    print(f"52-week high: {quote.High52Week}")
```

---

## Examples

### Example 1: Basic Trading Flow

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Check account balance
balances = sdk.get_account_balances(mode="PAPER")
print(f"Buying Power: ${balances['buying_power']:.2f}")

# Check current position
position = sdk.get_position("MNQZ25", mode="PAPER")
print(f"Current position: {position}")

# Place order if no position
if position == 0:
    order_id, status = sdk.place_order(
        symbol="MNQZ25",
        side="BUY",
        quantity=1,
        mode="PAPER"
    )
    print(f"Order placed: {order_id}")
```

### Example 2: Streaming Quotes with Processing

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, QuoteStream

async def process_quotes():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")
    
    async for data in sdk.streaming.stream_quotes(["MNQZ25"], mode="PAPER"):
        # Skip control messages
        if "StreamStatus" in data or "Heartbeat" in data:
            continue
        
        try:
            quote = QuoteStream(**data)
            
            # Process quote
            if quote.Last and quote.Bid and quote.Ask:
                spread = float(quote.Ask) - float(quote.Bid)
                print(f"{quote.Symbol}: Last={quote.Last}, Spread={spread:.2f}")
        except Exception as e:
            print(f"Error processing quote: {e}")

asyncio.run(process_quotes())
```

### Example 3: Order Status Monitoring

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, OrderStream

async def monitor_orders():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")
    
    account_id = sdk.get_account_info(mode="PAPER")["account_id"]
    
    async for data in sdk.streaming.stream_orders(account_id, mode="PAPER"):
        # Skip control messages
        if "StreamStatus" in data or "Heartbeat" in data:
            continue
        
        try:
            order = OrderStream(**data)
            print(f"Order {order.OrderID}: {order.Status} - {order.StatusDescription}")
            
            if order.Status == "FLL":
                print(f"Order filled at {order.FilledPrice}")
        except Exception as e:
            print(f"Error processing order: {e}")

asyncio.run(monitor_orders())
```

### Example 4: Position P&L Tracking

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, PositionStream

async def track_pnl():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")
    
    account_id = sdk.get_account_info(mode="PAPER")["account_id"]
    
    async for data in sdk.streaming.stream_positions(account_id, mode="PAPER"):
        # Skip control messages
        if "StreamStatus" in data or "Heartbeat" in data:
            continue
        
        try:
            position = PositionStream(**data)
            
            if position.Deleted:
                print(f"Position {position.PositionID} closed")
                continue
            
            print(f"{position.Symbol}: {position.Quantity} @ {position.AveragePrice}")
            print(f"  Unrealized P&L: ${position.UnrealizedProfitLoss}")
            print(f"  Today's P&L: ${position.TodaysProfitLoss}")
        except Exception as e:
            print(f"Error processing position: {e}")

asyncio.run(track_pnl())
```

### Example 5: Bracket Order

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

account_id = sdk.get_account_info(mode="PAPER")["account_id"]
entry_price = 25000.00
profit_target = entry_price + 50.00  # $50 profit target
stop_loss = entry_price - 25.00      # $25 stop loss

bracket_orders = [
    # Entry order
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Buy",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": str(entry_price),
        "TimeInForce": {"Duration": "DAY"}
    },
    # Profit target
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": str(profit_target),
        "TimeInForce": {"Duration": "GTC"}
    },
    # Stop loss
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "StopMarket",
        "Quantity": "2",
        "StopPrice": str(stop_loss),
        "TimeInForce": {"Duration": "GTC"}
    }
]

result = sdk.place_group_order(
    group_type="BRK",
    orders=bracket_orders,
    mode="PAPER"
)
print(f"Bracket order placed: {result}")
```

---

## Migration Guide

### From External SDK (`tastyware/tradestation`)

If you were using the external SDK, here's how to migrate:

**Before:**
```python
from tradestation import Session

session = Session(
    api_key=client_id,
    secret_key=client_secret,
    refresh_token=refresh_token
)
```

**After:**
```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")
```

**Before:**
```python
from src.services.tradestation import TradeStationAPI

api = TradeStationAPI()
```

**After:**
```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
# Or use compatibility alias:
from src.services.tradestation import TradeStationAPI
api = TradeStationAPI()  # Still works, wraps SDK
```

### Key Differences

1. **No External Dependency** - Remove `tradestation==0.2` from requirements.txt
2. **Import Path** - Use `src.lib.tradestation` instead of `tradestation`
3. **Class Name** - Use `TradeStationSDK` instead of `Session` (for main class)
4. **Streaming** - Use `sdk.streaming.stream_quotes()` instead of `session.stream_quotes()`
5. **Models** - Use `QuoteStream`, `OrderStream`, `PositionStream` for streaming responses

---

## Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines.

### Quick Contribution Guide

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Run tests: `pytest`
6. Format code: `black .`
7. Submit a pull request

See [CONTRIBUTING.md](CONTRIBUTING.md) for complete guidelines including:
- Code style and formatting
- Testing requirements
- Documentation standards
- Pull request process

---

## Documentation

### SDK Documentation Files

- **[README.md](README.md)** - This file (main documentation)
- **[QUICKSTART.md](QUICKSTART.md)** - 2-minute quick start guide
- **[CHEATSHEET.md](CHEATSHEET.md)** - Quick reference for common operations
- **[MIGRATION.md](MIGRATION.md)** - Migration guide from other SDKs
- **[LIMITATIONS.md](LIMITATIONS.md)** - Known limitations and constraints
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - Contribution guidelines
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and changes
- **[LICENSE](LICENSE)** - MIT License

### Detailed Documentation (docs/)

- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API reference
- **[SDK_USAGE_EXAMPLES.md](docs/SDK_USAGE_EXAMPLES.md)** - Usage examples
- **[ORDER_FUNCTIONS_REFERENCE.md](docs/ORDER_FUNCTIONS_REFERENCE.md)** - Order functions
- **[API_COVERAGE.md](docs/API_COVERAGE.md)** - API endpoint coverage
- **[MODELS.md](docs/MODELS.md)** - Model documentation
- **[API_STRUCTURE.md](docs/API_STRUCTURE.md)** - API structure analysis

### Interactive Examples (examples/)

- **[01_authentication.ipynb](examples/01_authentication.ipynb)** - Authentication tutorial
- **[03_market_data.ipynb](examples/03_market_data.ipynb)** - Market data with charts
- **[04_placing_orders.ipynb](examples/04_placing_orders.ipynb)** - Order placement
- **[quick_start.py](examples/quick_start.py)** - Standalone quick start script

### CLI Tools (cli/)

- **[test_auth.py](cli/test_auth.py)** - Test authentication
- **[test_connection.py](cli/test_connection.py)** - Comprehensive connection test

### External Resources

For complete TradeStation API v3 documentation, see:
- [TradeStation Developer Portal](https://developer.tradestation.com)
- [API v3 Reference](https://developer.tradestation.com/webapi)
- OpenAPI Spec: [`tradestation-api-v3-openapi.json`](./tradestation-api-v3-openapi.json)

---

## License

MIT License - See [LICENSE](LICENSE) file for details.

Copyright (c) 2025 Ben Laube

---

## Security

**Security is critical when trading real money.** Follow these best practices:

- ✅ **Never commit credentials** - Use .env files (excluded from git)
- ✅ **Secure token files** - Set restrictive permissions (chmod 600)
- ✅ **Start with PAPER mode** - Test thoroughly before LIVE mode
- ✅ **Validate inputs** - Check all order parameters before placing
- ✅ **Implement limits** - Max orders/day, max position size
- ✅ **Log everything** - Maintain audit trail of all operations
- ✅ **Monitor activity** - Watch for unexpected orders or balance changes

**Read the complete security guide:** [SECURITY.md](SECURITY.md)

**Report security issues:** security@example.com (not GitHub issues!)

---

## Support & Community

### Getting Help

- 📖 **Documentation:** Check [docs/](docs/) for detailed guides
- 🚀 **Quick Start:** See [QUICKSTART.md](QUICKSTART.md) for 2-minute setup
- 📋 **Cheat Sheet:** Keep [CHEATSHEET.md](CHEATSHEET.md) handy for quick reference
- 📦 **Installation:** See [INSTALLATION.md](INSTALLATION.md) for platform-specific guides
- ❓ **FAQ:** Read [FAQ & Troubleshooting](#faq--troubleshooting) section above
- 🔄 **Migration:** See [MIGRATION.md](MIGRATION.md) to switch from other SDKs
- ⚠️ **Limitations:** Check [LIMITATIONS.md](LIMITATIONS.md) for known constraints
- 🐛 **Bug Reports:** [Open an issue](https://github.com/benlaube/tradestation-python-sdk/issues)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)
- 📧 **Email:** benlaube@example.com

### Contributing

Want to improve the SDK? See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Changelog

See [CHANGELOG.md](CHANGELOG.md) for version history and release notes.

---

---

## 📊 SDK at a Glance

**📦 Installation:** `pip install tradestation-sdk`  
**⏱️ Time to First Order:** 2-5 minutes  
**📈 API Coverage:** 92% (57/62 endpoints)  
**🧪 Test Coverage:** 90%+  
**🐍 Python Version:** 3.10+  
**📝 Documentation:** 30,000+ words across 23 files  
**💡 Examples:** 3 Jupyter notebooks + CLI tools  
**🔒 Security:** Comprehensive security guide  
**🚀 Production Ready:** Full deployment guide  

**See [docs/FEATURE_COMPARISON.md](docs/FEATURE_COMPARISON.md) for complete feature comparison.**

---

**Last Updated:** 2025-12-07  
**SDK Version:** 1.0.0

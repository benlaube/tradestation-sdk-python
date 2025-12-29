# TradeStation SDK - Known Limitations

## About This Document

This document outlines **current limitations, constraints, and known issues** in the TradeStation SDK. Understanding these limitations helps you build more robust applications and avoid common pitfalls. Each limitation includes workarounds and planned fixes.

**Use this if:** You're experiencing issues, planning production deployment, or want to understand SDK constraints.

**Related Documents:**
- 📖 **[README.md](README.md)** - Complete SDK documentation
- 🔒 **[SECURITY.md](SECURITY.md)** - Security considerations (related to token storage limitations)
- 🚀 **[DEPLOYMENT.md](DEPLOYMENT.md)** - Production deployment (important to review limitations first)
- 🗺️ **[docs/ROADMAP.md](docs/ROADMAP.md)** - Planned fixes and future versions
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history and fixes
- ❓ **[README.md#faq--troubleshooting](README.md#faq--troubleshooting)** - FAQ and troubleshooting

---

This document outlines current limitations, constraints, and known issues in the TradeStation SDK. Understanding these limitations helps you build more robust applications and avoid common pitfalls.

---

## Security Limitations

### 1. Token Storage (✅ Improved in v1.0.1)

**Status:** ✅ **Enhanced with optional keychain support and improved file security**

**Previous Issue:** OAuth tokens were stored as plain JSON in `config/tokens_paper.json` and `config/tokens_live.json`.

**Current Implementation (v1.0.1):**
- **Keychain Storage (Optional):** System keychain integration available when `keyring` package is installed
  - macOS: Keychain Services
  - Linux: Secret Service API / gnome-keyring
  - Windows: Windows Credential Manager
- **File Storage (Fallback):** Secure file storage with automatic permission restrictions (chmod 600)
- **Configurable:** Set `TRADESTATION_TOKEN_STORAGE=keychain` to prefer keychain, or `auto` for auto-detection

**Configuration:**
```bash
# Use keychain storage (requires: pip install keyring)
export TRADESTATION_TOKEN_STORAGE=keychain

# Use file storage (default)
export TRADESTATION_TOKEN_STORAGE=file

# Auto-detect best option (default)
export TRADESTATION_TOKEN_STORAGE=auto

# Custom token directory (optional)
export TRADESTATION_TOKEN_DIR=/path/to/secure/location
```

**File Permissions:**
- Token files are automatically set to `chmod 600` (owner read/write only)
- Token directory is set to `chmod 700` (owner access only)
- Works on macOS, Linux, and Windows

**Keychain Usage:**
```python
# Install keyring package
# pip install keyring

# SDK will automatically use keychain if available
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")  # Tokens stored in keychain
```

**Note:** Keychain storage requires the `keyring` package. If not installed, SDK falls back to secure file storage.

---

## Network & Connection Limitations

### 2. OAuth Port Conflicts (✅ Fixed in v1.0.1)

**Status:** ✅ **Automatic port selection implemented**

**Previous Issue:** OAuth callback server required a specific port (default: 8888), causing authentication failures if port was in use.

**Current Implementation (v1.0.1):**
- **Automatic Port Selection:** SDK automatically finds an available port in range 8888-8898
- **Redirect URI Synchronization:** SDK automatically updates redirect_uri to match selected port
- **Environment Override:** Can specify exact port via `TRADESTATION_OAUTH_PORT`
- **Redirect URI Support:** Port is extracted from `TRADESTATION_REDIRECT_URI` if specified
- **Improved Error Messages:** Clear guidance when all ports are unavailable
- **Warnings:** SDK warns if auto-selected port may not be registered in Developer Portal

**⚠️ IMPORTANT: Port Registration Requirements**

**TradeStation API v3 requires that redirect URIs be EXACTLY registered in the Developer Portal.**

If the SDK auto-selects a port (e.g., 8889 when 8888 is busy), you must ensure that port is registered:

1. **Register ALL ports in range (recommended):**
   - Go to [TradeStation Developer Portal](https://developer.tradestation.com)
   - Add redirect URIs for all ports: `http://localhost:8888/callback`, `http://localhost:8889/callback`, etc. (through 8898)
   - This allows the SDK to auto-select any available port

2. **Or use a fixed port:**
   - Set `TRADESTATION_OAUTH_PORT=8888` (or your preferred port)
   - Register only that specific port in Developer Portal
   - SDK will use that port or fail with a clear error if unavailable

**Configuration:**
```bash
# Auto-select port from range 8888-8898 (default behavior)
# IMPORTANT: Register all ports 8888-8898 in Developer Portal
# No configuration needed

# Specify exact port (recommended if you only register one port)
export TRADESTATION_OAUTH_PORT=8888

# Or specify in redirect URI
export TRADESTATION_REDIRECT_URI=http://localhost:8888/callback
```

**Behavior:**
1. If `TRADESTATION_OAUTH_PORT` is set, use that port
2. If port is in redirect URI, extract and use that port
3. If port is in use, automatically try next port in range 8888-8898
4. **SDK updates redirect_uri to match selected port** (ensures TradeStation redirects correctly)
5. SDK warns if port was auto-selected (reminds you to register it)
6. If all ports unavailable, provide clear error message

**Example:**
```python
# SDK automatically handles port conflicts
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")  
# If port 8888 is busy, SDK will:
# 1. Auto-select port 8889
# 2. Update redirect_uri to http://localhost:8889/callback
# 3. Warn you to register this port in Developer Portal
# 4. Send OAuth request with updated redirect_uri
```

**Troubleshooting:**

**Error: "redirect_uri_mismatch"**
- **Cause:** Selected port is not registered in TradeStation Developer Portal
- **Solution:** Register the port being used (check SDK logs for the actual port)
- **Prevention:** Register all ports 8888-8898 in Developer Portal

**Manual Override (if needed):**
```bash
# Kill process using port (if auto-selection fails)
lsof -ti:8888 | xargs kill -9  # macOS/Linux
```

---

### 3. Synchronous HTTP Client (✅ Async Support Added in v1.0.1)

**Status:** ✅ **Async HTTP client support added (optional)**

**Previous Issue:** SDK used `requests` library (blocking I/O), limiting high-concurrency applications.

**Current Implementation (v1.0.1):**
- **Async Support (Optional):** Enable async HTTP client with `httpx` for non-blocking I/O
- **Backward Compatible:** Default behavior unchanged (synchronous `requests` library)
- **Connection Pooling:** Async client includes connection pooling for better performance
- **Same API:** Retry logic, error handling, and logging work identically in async mode

**When to Use Async:**
- Building high-frequency trading systems
- Processing hundreds of symbols simultaneously
- Running multiple trading strategies in parallel
- High-concurrency applications requiring non-blocking I/O

**Configuration:**
```python
# Enable async mode
sdk = TradeStationSDK(use_async=True)

# Or via environment variable
export TRADESTATION_USE_ASYNC=true
sdk = TradeStationSDK()
```

**Async Usage:**
```python
import asyncio

async def fetch_multiple_quotes():
    sdk = TradeStationSDK(use_async=True)
    await sdk.ensure_authenticated(mode="PAPER")

    # Use async client directly
    quotes = await sdk.client.make_request_async(
        "GET",
        "marketdata/quotes/MNQZ25,ESZ25",
        mode="PAPER"
    )

    # Clean up when done
    await sdk.aclose()
    return quotes

# Run async function
quotes = asyncio.run(fetch_multiple_quotes())
```

**Performance Comparison:**
- **Synchronous (default):** ~120 requests/minute (rate limit), 2-5 seconds per batch
- **Async:** Better concurrency, non-blocking I/O, connection pooling
- **Thread Pool (workaround):** Still supported, but async is more efficient

**Note:** Async support is opt-in. Existing synchronous code continues to work unchanged.

---

### 4. Built-in Request Retry Logic (✅ Implemented in v1.0.0)

**Status:** ✅ **REST API methods now have built-in retry logic with exponential backoff**

**Features:**
- Automatic retry for recoverable errors (network failures, rate limits, server errors)
- Exponential backoff (1s initial, up to 60s max)
- Configurable retry parameters (max_retries, retry_delay, max_retry_delay)
- Smart error categorization (RecoverableError vs NonRecoverableError)
- Comprehensive logging for retry attempts
- Rate limit handling with server-specified Retry-After header support

**Default Configuration:**
- Max retries: 3 attempts
- Initial retry delay: 1.0 seconds
- Max retry delay: 60.0 seconds
- Retry enabled: True (can be disabled)

**Custom Configuration:**
```python
from tradestation_sdk import TradeStationSDK

# Custom retry configuration
sdk = TradeStationSDK()
sdk._client.max_retries = 5  # Increase max retries
sdk._client.retry_delay = 2.0  # Start with 2s delay
sdk._client.max_retry_delay = 120.0  # Allow up to 2min delay
sdk._client.enable_retry = True  # Enable/disable retry
```

**What Gets Retried:**
- ✅ Network errors (connection timeouts, DNS failures)
- ✅ Rate limit errors (429) - with server Retry-After header support
- ✅ Server errors (500+) - temporary failures
- ❌ Authentication errors (401, 403) - not retried
- ❌ Invalid requests (400) - not retried
- ❌ Not found errors (404) - not retried

**Logging:**
All retry attempts are logged with context:
- Retry attempt number and max retries
- Error type and status code
- Backoff delay duration
- Final failure after max retries

**Note:** Streaming methods have always had retry logic (via `_with_retry()`). This implementation adds the same robust retry logic to REST API methods.

---

## API & Data Limitations

### 5. Bar Data Interval Constraints

**Issue:** TradeStation API only supports minute-based intervals.

**Supported:** `1, 2, 3, 5, 10, 15, 30, 60` (minutes)
**Not Supported:** Second-based intervals (`30S`, `60S`)

**Impact:**
- Cannot get sub-minute bars from API
- Need to use streaming for second-level data
- Backtesting limited to minute granularity

**Example Error:**
```python
# This FAILS
bars = sdk.get_bars("AAPL", "30", "Second", 100, mode="PAPER")
# Error: "Invalid interval for unit"
```

**Correct Usage:**
```python
# This WORKS
bars = sdk.get_bars("AAPL", "1", "Minute", 100, mode="PAPER")
```

**Workaround for Sub-Minute Data:**
```python
# Use streaming to collect second-level data
import asyncio

async def collect_second_data():
    quotes = []
    async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
        quotes.append({
            'timestamp': quote.Timestamp,
            'last': quote.Last,
            'bid': quote.Bid,
            'ask': quote.Ask
        })
        # Build your own second-level bars from tick data
```

**Note:** This is a TradeStation API constraint, not an SDK limitation.

---

### 6. Trailing Stop Units (Points, Not Dollars)

**Issue:** `trail_amount` parameter is in price points, not dollar amounts.

**Confusing Example (MNQ Futures):**
- MNQ point value: $2.00 per point
- Want $3.00 trailing stop
- Must use `trail_amount=1.5` (not `trail_amount=3.0`)

**Impact:**
- Easy to set incorrect stop distances
- Different for each instrument type
- Documentation can be misleading

**Correct Usage:**
```python
# MNQ futures: 1 point = $2.00
# For $3.00 trailing stop: 3.0 / 2.0 = 1.5 points
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # = $3.00 for MNQ
    mode="PAPER"
)

# AAPL stock: 1 point = $1.00
# For $3.00 trailing stop: 3.0 points
order_id, status = sdk.place_trailing_stop_order(
    symbol="AAPL",
    side="SELL",
    quantity=10,
    trail_amount=3.0,  # = $3.00 for stocks
    mode="PAPER"
)
```

**Planned Fix:** v1.1 will add `trail_amount_dollars` parameter for convenience.

---

### 7. Account ID Resolution

**Issue:** If `TRADESTATION_ACCOUNT_ID` not set, SDK auto-selects first futures account.

**Impact:**
- Wrong account may be selected in multi-account scenarios
- Production deployments should always set account ID explicitly
- Account switching isn't intuitive

**Best Practice:**
```env
# Always set in production
TRADESTATION_ACCOUNT_ID=SIM123456
```

**Multi-Account Workaround:**
```python
# Get all accounts
account = sdk.get_account_info(mode="PAPER")
all_accounts = account.get('accounts', [])

# Select specific account
for acc in all_accounts:
    if acc['AccountType'] == 'Futures':
        selected_account_id = acc['AccountID']
        break

# Use explicit account ID
balances = sdk.get_account_balances(
    mode="PAPER",
    account_id=selected_account_id
)
```

**Planned Fix:** v1.2 will add better multi-account support with account selection API.

---

## Streaming Limitations

### 8. HTTP Streaming vs WebSocket

**Issue:** TradeStation API v3 uses HTTP Streaming, not true WebSockets.

**Differences:**
- HTTP Streaming: Long-lived HTTP connection with NDJSON
- WebSocket: True bidirectional socket connection
- HTTP Streaming has higher latency

**Impact:**
- Slightly higher latency than WebSockets (~10-50ms)
- Connection management is more complex
- Requires newline-delimited JSON parsing

**Current Status:** SDK handles HTTP Streaming automatically with:
- Automatic reconnection (v1.0.0+)
- REST polling fallback
- Stream health tracking

**Future:** TradeStation may add native WebSocket support in future API versions.

---

### 9. Concurrent Stream Limit

**Issue:** TradeStation limits concurrent streams per account.

**Limit:** ~10 concurrent streams per account

**Impact:**
- Cannot stream 100+ symbols simultaneously
- Need to batch symbols per stream
- Multi-strategy systems may hit limits

**Best Practice:**
```python
# ❌ Bad: Too many streams
for symbol in 100_symbols:
    asyncio.create_task(sdk.streaming.stream_quotes([symbol]))

# ✅ Good: Batch symbols
chunks = [symbols[i:i+10] for i in range(0, len(symbols), 10)]
for chunk in chunks:
    asyncio.create_task(sdk.streaming.stream_quotes(chunk))
```

---

## Rate Limiting

### 10. API Rate Limits

**Limits:**
- General endpoints: ~120 requests/minute
- Market data: ~60 requests/minute
- Order placement: ~60 orders/minute
- Streaming: ~10 concurrent streams

**Impact:**
- High-frequency strategies may hit limits
- Bulk operations need throttling
- No built-in rate limit tracking

**Workaround:** Implement rate limiting
```python
import time
from collections import deque

class RateLimiter:
    def __init__(self, max_calls, period):
        self.max_calls = max_calls
        self.period = period
        self.calls = deque()

    def __call__(self, func):
        def wrapper(*args, **kwargs):
            now = time.time()
            # Remove old calls
            while self.calls and self.calls[0] < now - self.period:
                self.calls.popleft()
            # Check rate limit
            if len(self.calls) >= self.max_calls:
                sleep_time = self.period - (now - self.calls[0])
                time.sleep(sleep_time)
            self.calls.append(time.time())
            return func(*args, **kwargs)
        return wrapper

@RateLimiter(max_calls=60, period=60)
def rate_limited_place_order(*args, **kwargs):
    return sdk.place_order(*args, **kwargs)
```

**Planned Fix:** v1.2 will add built-in rate limit tracking and throttling.

---

## Dependency Constraints

### 11. Python Version Requirement

**Requirement:** Python 3.10+

**Reason:**
- Type hints with `|` operator (PEP 604)
- Structural pattern matching (used in error handling)
- Async generator improvements

**Impact:**
- Cannot use with Python 3.9 or earlier
- Some legacy systems may need Python upgrade

**Workaround:** Use Docker with Python 3.10+
```dockerfile
FROM python:3.10-slim
RUN pip install tradestation-sdk
```

---

### 12. Operating System Compatibility

**Supported:** Windows, macOS, Linux

**Known Issues:**
- **Windows:** OAuth browser launch may fail on some systems
- **macOS:** Keychain integration not yet implemented (v1.1)
- **Linux:** Depends on browser availability for OAuth

**Workaround for Headless Systems:**
```python
# Manual token management for headless servers
# 1. Authenticate on local machine first
# 2. Copy tokens to server
# 3. Use tokens on server
import shutil
shutil.copy('logs/tokens_paper.json', '/server/path/')
```

---

## Error Handling Gaps

### 13. Error Message Inconsistency

**Issue:** TradeStation API returns errors in multiple formats.

**Impact:**
- SDK may not parse all error formats correctly
- Some edge-case errors have generic messages
- Debugging can be challenging

**Known Error Formats:**
1. `{"Error": "message", "Code": "code"}`
2. `{"Errors": [{"Error": "...", "Code": "..."}]}`
3. `{"Message": "message"}`
4. `{"error": "...", "error_description": "..."}`

**Current:** SDK handles all known formats (as of v1.0.0).

**If You Encounter Unknown Format:**
```python
try:
    order_id, status = sdk.place_order(...)
except TradeStationAPIError as e:
    # Get full error details
    error_dict = e.to_dict()
    print(f"Full error: {error_dict}")
    # Report to GitHub issues for SDK improvement
```

---

## Roadmap & Planned Fixes

### v1.0.1 (December 2025) ✅ Released
- ✅ Token storage: Optional keychain integration with secure file fallback
- ✅ OAuth port: Automatic port selection (8888-8898 range)
- ✅ HTTP client: Async support with httpx (optional, backward compatible)
- ✅ Improved error messages and logging

### v1.1 (Q1 2026)
- `trail_amount_dollars` parameter for convenience
- Additional keychain storage improvements

### v1.2 (Q2 2026)
- ✅ Built-in retry logic with backoff (✅ **Implemented in v1.0.0**)
- ✅ Rate limit tracking and throttling
- ✅ Circuit breaker pattern for streaming
- ✅ Request/response caching
- ✅ Multi-account API improvements

### v2.0 (Q3 2026)
- ✅ Native async support (httpx/aiohttp)
- ✅ Connection pooling
- ✅ Native WebSocket support (if TradeStation adds it)
- ✅ Performance optimizations

---

## Getting Help

If you encounter limitations not listed here:
- 📖 [Check FAQ & Troubleshooting](README.md#faq--troubleshooting)
- 🐛 [Open an Issue](https://github.com/benlaube/tradestation-python-sdk/issues)
- 💬 [GitHub Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)

---

**Last Updated:** 2025-12-28
**SDK Version:** 1.0.1

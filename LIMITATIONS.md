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

### 1. Token Storage (No Encryption at Rest)

**Issue:** OAuth tokens are stored as plain JSON in `config/tokens_paper.json` and `config/tokens_live.json`.

**Impact:**
- Anyone with file system access can read tokens
- Tokens grant full API access until expiration
- Risk on shared systems or compromised machines

**Mitigation (Current):**
```bash
# Set restrictive file permissions (macOS/Linux)
chmod 600 config/tokens_*.json

# Ensure config/ directory is in .gitignore if you relocate tokens
echo "config/" >> .gitignore
```

**Planned Fix:** v1.1 will add system keychain integration:
- macOS: Keychain Services
- Linux: Secret Service API / gnome-keyring
- Windows: Windows Credential Manager

**Workaround:** Implement custom token storage:
```python
class SecureTokenManager(TokenManager):
    def save_tokens(self, mode, tokens):
        # Your encryption logic here
        encrypted = encrypt_tokens(tokens)
        super().save_tokens(mode, encrypted)
```

---

## Network & Connection Limitations

### 2. OAuth Port Conflicts

**Issue:** OAuth callback server requires a specific port (default: 8888).

**Impact:**
- Authentication fails if port is in use
- Manual intervention required
- Process restart doesn't fix it

**Common Causes:**
- Multiple SDK instances running
- Other applications using port 8888
- Zombie processes from previous crashes

**Solutions:**

**Option 1:** Kill process using the port
```bash
# macOS/Linux
lsof -ti:8888 | xargs kill -9

# Windows
netstat -ano | findstr :8888
taskkill /PID <PID> /F
```

**Option 2:** Use a different port
```env
# .env
TRADESTATION_REDIRECT_URI=http://localhost:9999/callback
```

**Planned Fix:** v1.1 will add automatic port selection (8888-8898 range).

---

### 3. Synchronous HTTP Client

**Issue:** SDK uses `requests` library (blocking I/O).

**Impact:**
- Not ideal for high-concurrency applications
- Blocks thread during API calls
- Cannot handle thousands of concurrent requests efficiently

**When This Matters:**
- Building high-frequency trading systems
- Processing hundreds of symbols simultaneously
- Running multiple trading strategies in parallel

**Current Performance:**
- ~120 requests/minute (rate limit)
- Single-threaded: 2-5 seconds per batch
- Multi-threaded: Better, but thread overhead

**Workaround:** Use thread pools
```python
from concurrent.futures import ThreadPoolExecutor

def get_quote(symbol):
    return sdk.get_quote_snapshots(symbol, mode="PAPER")

with ThreadPoolExecutor(max_workers=10) as executor:
    quotes = list(executor.map(get_quote, symbols))
```

**Planned Fix:** v2.0 will add native async support with `httpx` or `aiohttp`.

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

### v1.1 (Q1 2026)
- ✅ Token encryption (keychain integration)
- ✅ Auto-port selection for OAuth
- ✅ `trail_amount_dollars` parameter
- ✅ Improved error messages

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
**SDK Version:** 1.0.0

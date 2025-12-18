# TradeStation SDK - Migration Guide

## About This Document

This guide helps you **migrate to TradeStation SDK** from other libraries (like `tastyware/tradestation`) or upgrade between SDK versions. It provides step-by-step migration instructions, code comparison examples, and common pitfalls.

**Use this if:** You're switching from another TradeStation library or upgrading the SDK version.

**Related Documents:**
- 📖 **[README.md](README.md)** - Complete SDK documentation
- 📦 **[INSTALLATION.md](INSTALLATION.md)** - Installation instructions
- 📚 **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API reference
- 💡 **[docs/SDK_USAGE_EXAMPLES.md](docs/SDK_USAGE_EXAMPLES.md)** - Usage examples
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Version history and breaking changes

---

This guide helps you migrate to TradeStation SDK from other libraries or upgrade between SDK versions.

---

## Table of Contents

- [From External SDK (tastyware/tradestation)](#from-external-sdk-tastywaretradestation)
- [From Direct API Calls](#from-direct-api-calls)
- [From Other Trading Libraries](#from-other-trading-libraries)
- [Version Upgrades](#version-upgrades)

---

## From External SDK (tastyware/tradestation)

If you were using the external `tradestation` package (tastyware/tradestation), here's how to migrate.

### Installation Changes

**Before:**
```bash
pip install tradestation
```

**After:**
```bash
pip uninstall tradestation  # Remove old package
pip install tradestation-python-sdk
```

Update `requirements.txt`:
```diff
- tradestation==0.2
+ tradestation-sdk>=1.0.0
```

### Import Changes

**Before:**
```python
from tradestation import Session
```

**After:**
```python
from tradestation_sdk import TradeStationSDK
```

### Initialization Changes

**Before:**
```python
session = Session(
    api_key=client_id,
    secret_key=client_secret,
    refresh_token=refresh_token
)
```

**After:**
```python
# SDK reads from environment variables (.env file)
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")  # Opens browser for OAuth
```

### Authentication Changes

**Before:**
```python
# Manual token management
session = Session(
    api_key=client_id,
    secret_key=client_secret,
    refresh_token=refresh_token
)
```

**After:**
```python
# Automatic token management
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")  # OAuth flow
# Tokens saved automatically, refresh automatically
```

### API Method Changes

**Before:**
```python
# Get account
account = session.get_accounts()

# Get bars
bars = session.get_bars(symbol="AAPL", interval="1min", count=100)

# Place order
order = session.place_order(
    account_id=account_id,
    symbol="AAPL",
    quantity=10,
    side="BUY",
    order_type="Market"
)
```

**After:**
```python
# Get account
account = sdk.get_account_info(mode="PAPER")

# Get bars
bars = sdk.get_bars(
    symbol="AAPL",
    interval="1",
    unit="Minute",
    bars_back=100,
    mode="PAPER"
)

# Place order (convenience function)
order_id, status = sdk.place_order(
    symbol="AAPL",
    side="BUY",
    quantity=10,
    order_type="Market",
    mode="PAPER"
)
```

### Streaming Changes

**Before:**
```python
# WebSocket streaming
for quote in session.stream_quotes(["AAPL"]):
    print(quote)
```

**After:**
```python
# HTTP streaming with async/await
import asyncio

async def stream():
    async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
        print(f"{quote.Symbol}: {quote.Last}")

asyncio.run(stream())
```

### Mode Support

**New Feature:** SDK supports both PAPER and LIVE modes seamlessly:

```python
# PAPER mode (simulator)
sdk.authenticate(mode="PAPER")
sdk.place_order(..., mode="PAPER")

# LIVE mode (real money)
sdk.authenticate(mode="LIVE")
sdk.place_order(..., mode="LIVE")
```

### Error Handling Changes

**Before:**
```python
try:
    order = session.place_order(...)
except Exception as e:
    print(f"Error: {e}")
```

**After:**
```python
from tradestation_sdk import (
    TradeStationAPIError,
    AuthenticationError,
    RateLimitError
)

try:
    order_id, status = sdk.place_order(...)
except AuthenticationError:
    sdk.authenticate(mode="PAPER")
except RateLimitError:
    time.sleep(60)
except TradeStationAPIError as e:
    print(f"API Error: {e}")
    # Get structured error details
    error_dict = e.to_dict()
```

### Complete Migration Example

**Before (External SDK):**
```python
from tradestation import Session

session = Session(
    api_key="client_id",
    secret_key="client_secret",
    refresh_token="refresh_token"
)

accounts = session.get_accounts()
account_id = accounts[0]['account_id']

bars = session.get_bars(symbol="AAPL", interval="1min", count=100)

order = session.place_order(
    account_id=account_id,
    symbol="AAPL",
    quantity=10,
    side="BUY",
    order_type="Market"
)

for quote in session.stream_quotes(["AAPL"]):
    print(quote)
```

**After (This SDK):**
```python
from tradestation_sdk import TradeStationSDK
import asyncio

# Initialize (reads from .env)
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")

# Get account
account = sdk.get_account_info(mode="PAPER")

# Get bars
bars = sdk.get_bars("AAPL", "1", "Minute", 100, mode="PAPER")

# Place order
order_id, status = sdk.place_order(
    symbol="AAPL",
    side="BUY",
    quantity=10,
    order_type="Market",
    mode="PAPER"
)

# Stream quotes
async def stream():
    async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
        print(f"{quote.Symbol}: {quote.Last}")

asyncio.run(stream())
```

---

## From Direct API Calls

If you were making direct HTTP requests to TradeStation API, the SDK simplifies your code significantly.

### Authentication

**Before (Manual OAuth):**
```python
import requests

# Step 1: Get authorization code
auth_url = f"https://signin.tradestation.com/authorize?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code"
# Manual: Open browser, get code from callback

# Step 2: Exchange code for tokens
token_response = requests.post(
    "https://signin.tradestation.com/oauth/token",
    data={
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "redirect_uri": redirect_uri
    }
)
tokens = token_response.json()
access_token = tokens['access_token']

# Step 3: Use token in requests
headers = {"Authorization": f"Bearer {access_token}"}
```

**After (SDK Handles Everything):**
```python
from tradestation_sdk import TradeStationSDK

sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")
# Done! SDK handles OAuth flow, token storage, and refresh
```

### API Requests

**Before (Manual):**
```python
import requests

headers = {"Authorization": f"Bearer {access_token}"}
response = requests.get(
    "https://sim-api.tradestation.com/v3/brokerage/accounts",
    headers=headers
)
accounts = response.json()
```

**After (SDK):**
```python
account = sdk.get_account_info(mode="PAPER")
```

### Streaming

**Before (Manual NDJSON Parsing):**
```python
import requests
import json

response = requests.get(
    "https://sim-api.tradestation.com/v3/marketdata/stream/quotes/AAPL",
    headers=headers,
    stream=True
)

buffer = ""
for chunk in response.iter_content(chunk_size=8192):
    buffer += chunk.decode('utf-8')
    while '\n' in buffer:
        line, buffer = buffer.split('\n', 1)
        if line.strip():
            quote = json.loads(line)
            print(quote)
```

**After (SDK):**
```python
import asyncio

async def stream():
    async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
        print(f"{quote.Symbol}: {quote.Last}")

asyncio.run(stream())
```

---

## From Other Trading Libraries

### From Alpaca API

**Alpaca:**
```python
from alpaca.trading.client import TradingClient

client = TradingClient(api_key, secret_key)
account = client.get_account()
order = client.submit_order(
    symbol="AAPL",
    qty=10,
    side="buy",
    type="market"
)
```

**TradeStation SDK:**
```python
from tradestation_sdk import TradeStationSDK

sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")
account = sdk.get_account_info(mode="PAPER")
order_id, status = sdk.place_order(
    symbol="AAPL",
    side="BUY",
    quantity=10,
    order_type="Market",
    mode="PAPER"
)
```

### From Interactive Brokers (ib_insync)

**Interactive Brokers:**
```python
from ib_insync import IB, MarketOrder

ib = IB()
ib.connect('127.0.0.1', 7497, clientId=1)

contract = Stock('AAPL', 'SMART', 'USD')
order = MarketOrder('BUY', 10)
trade = ib.placeOrder(contract, order)
```

**TradeStation SDK:**
```python
from tradestation_sdk import TradeStationSDK

sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")

order_id, status = sdk.place_order(
    symbol="AAPL",
    side="BUY",
    quantity=10,
    order_type="Market",
    mode="PAPER"
)
```

### Key Differences

| Feature | Alpaca | IB | TradeStation SDK |
|---------|--------|-------|------------------|
| Auth | API Key | TWS/Gateway | OAuth2 |
| Async | Native | Native | HTTP Streaming |
| Paper Trading | Yes | Yes (Simulator) | Yes (PAPER mode) |
| Futures | No | Yes | Yes |
| Options | Limited | Yes | Yes |
| Streaming | WebSocket | Native | HTTP Streaming |

---

## Version Upgrades

### From v0.x to v1.0

**Breaking Changes:**
- None (v1.0 is first public release)

**New Features:**
- Automatic stream reconnection
- REST polling fallback
- Stream health tracking
- Convenience functions for orders
- Enhanced error handling

**Recommended Actions:**
1. Update to v1.0: `pip install --upgrade tradestation-sdk`
2. Enable automatic reconnection in streaming (enabled by default)
3. Use convenience functions for cleaner code
4. Review new error handling patterns

### Future Versions

Check [CHANGELOG.md](CHANGELOG.md) for version-specific migration notes.

---

## Migration Checklist

Use this checklist when migrating:

- [ ] Update dependencies (remove old, install new)
- [ ] Update imports (`from tradestation_sdk import ...`)
- [ ] Set up `.env` file with credentials
- [ ] Change authentication code (OAuth flow)
- [ ] Update API method calls (see examples above)
- [ ] Add mode parameter to all calls (`mode="PAPER"`)
- [ ] Update streaming code (async/await)
- [ ] Update error handling (new exception types)
- [ ] Test in PAPER mode first
- [ ] Update documentation and comments
- [ ] Run tests to verify migration
- [ ] Deploy to production after validation

---

## Need Help?

- 📖 [README](README.md) - Full documentation
- 💡 [Examples](docs/SDK_USAGE_EXAMPLES.md) - Code examples
- ❓ [FAQ](README.md#faq--troubleshooting) - Common issues
- 🐛 [Issues](https://github.com/benlaube/tradestation-python-sdk/issues) - Report problems

---

**Migration taking longer than expected?** Open a discussion on GitHub and we'll help!

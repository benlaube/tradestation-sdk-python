---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:32 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - Cheat Sheet

## About This Document

This is a **quick reference guide** for common SDK operations. Print this out or keep it open in a tab for fast lookups.

**Use this if:** You know the SDK basics and need quick code snippets.

**For more detail, see:**

- 📖 **[README.md](../../README.md)** - Complete SDK documentation
- 📚 **[API Reference](../api/reference.md)** - Complete API reference with all parameters
- 💡 **[Usage Examples](usage-examples.md)** - Detailed examples with explanations
- 🚀 **[docs/getting-started/quickstart.md](../getting-started/quickstart.md)** - 2-minute getting started guide
- 📦 **[INSTALLATION.md](../getting-started/installation.md)** - Installation instructions

---

Quick reference for common operations. Keep this handy!

---

## Setup

```python
from tradestation_sdk import TradeStationSDK
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")
```

---

## Account Operations

```python
# Get account info
account = sdk.get_account_info(mode="PAPER")
# → {'account_id': 'SIM123456', 'name': '...', ...}

# Get balances
balances = sdk.get_account_balances(mode="PAPER")
# → {'equity': 100000.0, 'buying_power': 50000.0, ...}
```

---

## Market Data

```python
# Historical bars (OHLCV)
bars = sdk.get_bars("AAPL", "1", "Minute", bars_back=100, mode="PAPER")
# → [{'Open': 150.0, 'High': 150.5, 'Low': 149.5, 'Close': 150.0, ...}, ...]

# Search symbols
symbols = sdk.search_symbols(pattern="MNQ", category="Future", mode="PAPER")
# → [{'Symbol': 'MNQZ25', 'Description': 'E-mini Nasdaq...', ...}, ...]

# Get quotes
quotes = sdk.get_quote_snapshots("AAPL,MSFT", mode="PAPER")
# → {'Quotes': [{'Symbol': 'AAPL', 'Last': 150.0, 'Bid': 149.9, ...}], ...}
```

---

## Order Placement

### Market Order

```python
order_id, status = sdk.place_order(
    symbol="AAPL",
    side="BUY",
    quantity=10,
    order_type="Market",
    mode="PAPER"
)
```

### Limit Order

```python
order_id, status = sdk.place_limit_order(
    symbol="AAPL",
    side="BUY",
    quantity=10,
    limit_price=150.00,
    mode="PAPER"
)
```

### Stop Order

```python
order_id, status = sdk.place_stop_order(
    symbol="AAPL",
    side="SELL",
    quantity=10,
    stop_price=145.00,
    mode="PAPER"
)
```

### Trailing Stop

```python
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # 1.5 points = $3.00 for MNQ
    mode="PAPER"
)
```

### Bracket Order (Entry + Profit + Stop)

```python
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,
    entry_price=None,  # Market entry
    mode="PAPER"
)
# → {'GroupID': '...', 'Orders': [entry, profit, stop]}
```

---

## Order Management

```python
# Cancel order
success, msg = sdk.cancel_order("924243071", mode="PAPER")

# Modify order
success, msg = sdk.modify_order(
    order_id="924243071",
    quantity=20,
    limit_price=151.00,
    mode="PAPER"
)

# Get order history
orders = sdk.get_order_history(
    start_date="2025-12-01",
    limit=100,
    mode="PAPER"
)

# Get current orders
current = sdk.get_current_orders(mode="PAPER")
# → {'Orders': [...], 'Errors': []}
```

---

## Position Management

```python
# Get position for symbol
position = sdk.get_position("AAPL", mode="PAPER")
# → 10 (long), -10 (short), 0 (flat)

# Get all positions
positions = sdk.get_all_positions(mode="PAPER")
# → [{'Symbol': 'AAPL', 'Quantity': 10, ...}, ...]

# Flatten position
flattened = sdk.flatten_position(symbol="AAPL", mode="PAPER")
# → [{'symbol': 'AAPL', 'order_id': '...', ...}]

# Flatten all positions
flattened = sdk.flatten_position(mode="PAPER")
```

---

## Streaming (Real-Time Data)

```python
import asyncio

async def stream_example():
    # Stream quotes
    async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
        print(f"{quote.Symbol}: ${quote.Last}")

    # Stream orders
    async for order in sdk.streaming.stream_orders(account_id, mode="PAPER"):
        print(f"Order {order.OrderID}: {order.Status}")

    # Stream positions
    async for pos in sdk.streaming.stream_positions(account_id, mode="PAPER"):
        print(f"{pos.Symbol}: {pos.Quantity} @ ${pos.AveragePrice}")

asyncio.run(stream_example())
```

---

## Error Handling

```python
from tradestation_sdk import (
    TradeStationAPIError,
    AuthenticationError,
    RateLimitError,
    InvalidRequestError
)

try:
    order_id, status = sdk.place_order(...)
except AuthenticationError:
    sdk.authenticate(mode="PAPER")
except RateLimitError:
    time.sleep(60)  # Wait 1 minute
except InvalidRequestError as e:
    print(f"Invalid: {e}")
except TradeStationAPIError as e:
    print(f"API Error: {e}")
```

---

## Common Patterns

### Retry with Backoff

```python
import time
for attempt in range(3):
    try:
        return sdk.place_order(...)
    except RateLimitError:
        if attempt < 2:
            time.sleep(2 ** attempt)
        else:
            raise
```

### Check Before Trading

```python
# Check position first
position = sdk.get_position("AAPL", mode="PAPER")
if position == 0:
    # Flat - safe to buy
    sdk.place_order("AAPL", "BUY", 10, mode="PAPER")
```

### Monitor Order Fill

```python
import asyncio

async def wait_for_fill(order_id):
    account_id = sdk.get_account_info(mode="PAPER")["account_id"]
    async for order in sdk.streaming.stream_orders(account_id, mode="PAPER"):
        if order.OrderID == order_id and order.Status == "FLL":
            print(f"✅ Filled at ${order.FilledPrice}")
            break
```

---

## SDK Info

```python
# Get SDK diagnostics
info = sdk.info()
print(f"Version: {info['version']}")
print(f"Authenticated: {info['authenticated_modes']}")
print(f"Features: {info['features']}")
```

---

## Modes

```python
# PAPER mode (simulator - safe for testing)
sdk.authenticate(mode="PAPER")
sdk.place_order(..., mode="PAPER")

# LIVE mode (real money - use with caution!)
sdk.authenticate(mode="LIVE")
sdk.place_order(..., mode="LIVE")
```

---

## Rate Limits

- **General:** ~120 req/min
- **Market Data:** ~60 req/min
- **Orders:** ~60 orders/min
- **Streams:** ~10 concurrent

**Add delays:**

```python
import time
time.sleep(0.5)  # Between requests
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Port 8888 in use | `lsof -ti:8888 \| xargs kill -9` |
| Auth failed | Check credentials in `.env` |
| Token expired | SDK auto-refreshes (or `sdk.authenticate()`) |
| Symbol not found | Search: `sdk.search_symbols("MNQ", "Future")` |
| Rate limit | Add delays or batch requests |

---

## Resources

- 📖 [Full Documentation](README.md)
- 💡 [Examples](usage-examples.md)
- 🐛 [Issues](https://github.com/benlaube/tradestation-python-sdk/issues)
- 💬 [Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)

---

**Print this and keep it next to your monitor!** 📄

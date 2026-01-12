---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:25 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - Quick Start (2 Minutes)

## About This Document

This is the **fastest way to get started** with the TradeStation SDK. This guide gets you from zero to your first API call in under 2 minutes.

**Use this if:** You want to get started immediately and see results fast.

**If you need more detail, see:**

- 📖 **[README.md](README.md)** - Complete SDK overview and documentation
- 📦 **[INSTALLATION.md](installation.md)** - Detailed installation for all platforms
- 📚 **[README.md](README.md)** - 15-minute comprehensive tutorial
- 📋 **[CHEATSHEET.md](../guides/cheatsheet.md)** - Quick reference for common operations
- 💡 **[../guides/usage-examples.md](../guides/usage-examples.md)** - More code examples
- ⚠️ **[docs/architecture/limitations.md](../architecture/limitations.md)** - Important constraints to know

---

The absolute fastest way to get started with TradeStation SDK.

## Step 1: Install (30 seconds)

```bash
pip install tradestation-python-sdk
```

## Step 2: Get Credentials (60 seconds)

1. Go to <https://developer.tradestation.com>
2. Create an application
3. Copy your **Client ID** and **Client Secret**
4. **Set Redirect URI(s):**
   - **Recommended:** Register all ports 8888-8898: `http://localhost:8888/callback`, `http://localhost:8889/callback`, etc.
   - **Or:** Register only `http://localhost:8888/callback` and set `TRADESTATION_OAUTH_PORT=8888` in `.env`
   - **Why:** SDK may auto-select a different port if 8888 is busy

## Step 3: Configure (30 seconds)

Create `.env` file:

```env
TRADESTATION_CLIENT_ID=paste_your_client_id_here
TRADESTATION_CLIENT_SECRET=paste_your_client_secret_here
TRADESTATION_REDIRECT_URI=http://localhost:8888/callback
TRADING_MODE=PAPER
```

## Step 4: Run Your First Script (30 seconds)

Copy-paste this into `test.py`:

```python
from tradestation_sdk import TradeStationSDK

# Initialize
sdk = TradeStationSDK()

# Authenticate (browser opens - login once)
sdk.authenticate(mode="PAPER")

# Get account
account = sdk.get_account_info(mode="PAPER")
print(f"✅ Connected: {account['account_id']}")

# Get balance
balances = sdk.get_account_balances(mode="PAPER")
print(f"💰 Buying Power: ${balances['buying_power']:,.2f}")

# Place order (example - commented for safety)
# order_id, status = sdk.place_limit_order(
#     symbol="AAPL",
#     side="BUY",
#     quantity=10,
#     limit_price=150.00,
#     mode="PAPER"
# )
# print(f"✅ Order: {order_id}")
```

Run it:

```bash
python test.py
```

**Done!** 🎉

---

## Common Issues

### "Port 8888 in use"

**v1.0.1+:** SDK will auto-select an available port. Ensure the selected port is registered in Developer Portal.

**Or manually:**

```bash
# Kill process on port 8888
lsof -ti:8888 | xargs kill -9
```

### "redirect_uri_mismatch"

**Cause:** Selected port not registered in TradeStation Developer Portal
**Solution:** Register the port shown in SDK logs (or register all ports 8888-8898)

### "Module not found"

```bash
# Reinstall SDK
pip install --upgrade tradestation-python-sdk
```

### "Authentication failed"

- Double-check credentials in `.env`
- Ensure redirect URI is exactly: `http://localhost:8888/callback`

---

## Next Steps

- 📖 [Full README](README.md)
- 💡 [Usage Examples](../guides/usage-examples.md)
- 📊 [Jupyter Notebooks](../../examples/)
- 🔧 [CLI Tools](../../tradestation/cli/)
- ❓ [FAQ & Troubleshooting](README.md#faq--troubleshooting)

---

**Need help?** Open an issue: <https://github.com/benlaube/tradestation-python-sdk/issues>

# TradeStation SDK - Quick Start (2 Minutes)

## About This Document

This is the **fastest way to get started** with the TradeStation SDK. This guide gets you from zero to your first API call in under 2 minutes.

**Use this if:** You want to get started immediately and see results fast.

**If you need more detail, see:**
- 📖 **[README.md](README.md)** - Complete SDK overview and documentation
- 📦 **[INSTALLATION.md](INSTALLATION.md)** - Detailed installation for all platforms
- 📚 **[docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)** - 15-minute comprehensive tutorial
- 📋 **[CHEATSHEET.md](CHEATSHEET.md)** - Quick reference for common operations
- 💡 **[docs/SDK_USAGE_EXAMPLES.md](docs/SDK_USAGE_EXAMPLES.md)** - More code examples
- ⚠️ **[LIMITATIONS.md](LIMITATIONS.md)** - Important constraints to know

---

The absolute fastest way to get started with TradeStation SDK.

## Step 1: Install (30 seconds)

```bash
pip install tradestation-python-sdk
```

## Step 2: Get Credentials (60 seconds)

1. Go to https://developer.tradestation.com
2. Create an application
3. Copy your **Client ID** and **Client Secret**

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
from tradestation import TradeStationSDK

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
```bash
# Kill process on port 8888
lsof -ti:8888 | xargs kill -9
```

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
- 💡 [Usage Examples](docs/SDK_USAGE_EXAMPLES.md)
- 📊 [Jupyter Notebooks](examples/)
- 🔧 [CLI Tools](tradestation/cli/)
- ❓ [FAQ & Troubleshooting](README.md#faq--troubleshooting)

---

**Need help?** Open an issue: https://github.com/benlaube/tradestation-python-sdk/issues

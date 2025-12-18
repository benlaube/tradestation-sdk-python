# TradeStation SDK - Complete Getting Started Guide

## About This Document

This is a **comprehensive 15-minute tutorial** that takes you from zero to a working trading bot. It includes step-by-step instructions, code examples, explanations, and best practices.

**Use this if:** You want a thorough introduction with explanations, not just quick code snippets.

**Related Documents:**
- 🚀 **[QUICKSTART.md](../QUICKSTART.md)** - Faster 2-minute version (if you just want to run code)
- 📖 **[README.md](../README.md)** - Complete SDK documentation
- 📋 **[CHEATSHEET.md](../CHEATSHEET.md)** - Quick reference after you learn the basics
- 💡 **[SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md)** - More detailed examples
- 📚 **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API reference
- 📊 **[examples/README.md](../examples/README.md)** - Interactive Jupyter notebooks

---

Everything you need to go from zero to trading in 15 minutes.

---

## What You'll Build

By the end of this guide, you'll have a working trading bot that can:
- ✅ Authenticate with TradeStation API
- ✅ Get real-time market data
- ✅ Place and manage orders
- ✅ Track positions and P&L
- ✅ Stream real-time quotes

All in PAPER mode (simulator) for safe learning!

---

## Prerequisites (5 minutes)

### 1. TradeStation Account

**Need an account?**
1. Go to https://www.tradestation.com
2. Sign up for account (can take 1-2 days for approval)
3. For testing only: Use PAPER mode (no account needed)

### 2. Developer Credentials

**Get API credentials:**
1. Go to https://developer.tradestation.com
2. Sign in with your TradeStation account
3. Create a new application
4. Copy your **Client ID** and **Client Secret**
5. Set **Redirect URI** to: `http://localhost:8888/callback`

### 3. Python Environment

**Check Python version:**
```bash
python --version
# Should be 3.10 or higher
```

**If too old:**
- **macOS:** `brew install python@3.10`
- **Ubuntu:** `sudo apt install python3.10`
- **Windows:** Download from https://python.org

---

## Installation (2 minutes)

### Step 1: Install SDK

```bash
pip install tradestation-python-sdk
```

### Step 2: Verify Installation

```bash
python -c "import tradestation_sdk; print(tradestation_sdk.__version__)"
# Should print: 1.0.0
```

---

## Configuration (3 minutes)

### Step 1: Create Project Directory

```bash
mkdir my-trading-bot
cd my-trading-bot
```

### Step 2: Create .env File

```bash
# Create .env file with your credentials
cat > .env << EOF
TRADESTATION_CLIENT_ID=your_client_id_here
TRADESTATION_CLIENT_SECRET=your_client_secret_here
TRADESTATION_REDIRECT_URI=http://localhost:8888/callback
TRADING_MODE=PAPER
EOF
```

**Replace** `your_client_id_here` and `your_client_secret_here` with your actual credentials!

### Step 3: Install python-dotenv

```bash
pip install python-dotenv
```

---

## Your First Script (5 minutes)

### Create main.py

```python
"""
My First Trading Bot - TradeStation SDK

This bot:
1. Authenticates with TradeStation
2. Gets account information and balances
3. Fetches market data
4. Places a test order (commented out for safety)
"""

from tradestation_sdk import TradeStationSDK, TradeStationAPIError
from dotenv import load_dotenv

# Load credentials from .env
load_dotenv()

def main():
    print("🤖 Starting My First Trading Bot...")
    print()
    
    # Initialize SDK
    print("📦 Initializing SDK...")
    sdk = TradeStationSDK()
    
    # Show SDK info
    info = sdk.info()
    print(f"✅ SDK v{info['version']} ready")
    print()
    
    # Authenticate
    print("🔐 Authenticating with TradeStation...")
    print("   (Browser will open for login - first time only)")
    try:
        sdk.authenticate(mode="PAPER")
        print("✅ Authentication successful!")
    except Exception as e:
        print(f"❌ Authentication failed: {e}")
        return
    print()
    
    # Get account info
    print("👤 Getting account information...")
    account = sdk.get_account_info(mode="PAPER")
    print(f"✅ Account: {account['account_id']}")
    print(f"   Name: {account['name']}")
    print(f"   Type: {account['type']}")
    print()
    
    # Get balances
    print("💰 Getting account balances...")
    balances = sdk.get_account_balances(mode="PAPER")
    print(f"✅ Equity: ${balances['equity']:,.2f}")
    print(f"   Buying Power: ${balances['buying_power']:,.2f}")
    print(f"   Open P&L: ${balances['open_pnl']:,.2f}")
    print()
    
    # Get market data
    print("📊 Getting market data for AAPL...")
    quotes = sdk.get_quote_snapshots("AAPL", mode="PAPER")
    if quotes.get("Quotes"):
        quote = quotes["Quotes"][0]
        print(f"✅ AAPL Quote:")
        print(f"   Last: ${quote.get('Last', 'N/A')}")
        print(f"   Bid: ${quote.get('Bid', 'N/A')}")
        print(f"   Ask: ${quote.get('Ask', 'N/A')}")
    print()
    
    # Check current position
    print("📍 Checking AAPL position...")
    position = sdk.get_position("AAPL", mode="PAPER")
    print(f"✅ Current position: {position} shares")
    print()
    
    # Example: Place order (commented for safety)
    print("📝 Order Placement Example:")
    print("   (Commented out for safety - uncomment to place actual order)")
    print()
    print("   # Place a limit order")
    print("   order_id, status = sdk.place_limit_order(")
    print("       symbol='AAPL',")
    print("       side='BUY',")
    print("       quantity=10,")
    print("       limit_price=150.00,")
    print("       mode='PAPER'")
    print("   )")
    print("   print(f'✅ Order placed: {order_id}')")
    print()
    
    # Summary
    print("=" * 60)
    print("🎉 Success! Your first trading bot is working!")
    print("=" * 60)
    print()
    print("What's next?")
    print("  1. Uncomment the order placement code to place a test order")
    print("  2. Try streaming real-time data (see examples/)")
    print("  3. Build your own trading strategy")
    print("  4. Read the documentation in docs/")
    print()

if __name__ == "__main__":
    main()
```

### Run Your Bot

```bash
python main.py
```

**What happens:**
1. Browser opens for TradeStation login (first time only)
2. Script gets account info and balances
3. Fetches AAPL quote
4. Shows example order code (commented out)

**Success!** 🎉 You now have a working trading bot!

---

## Next Steps (Choose Your Path)

### Path A: Learn More (Interactive)

**Use Jupyter notebooks for hands-on learning:**

```bash
# Install Jupyter
pip install jupyter notebook pandas matplotlib

# Go to examples directory
cd examples/

# Start Jupyter
jupyter notebook
```

**Then open:**
1. `01_authentication.ipynb` - Authentication tutorial
2. `03_market_data.ipynb` - Market data with charts
3. `04_placing_orders.ipynb` - Order placement

---

### Path B: Build a Real Strategy

**Create a simple moving average strategy:**

```python
# strategy.py
from tradestation_sdk import TradeStationSDK
import pandas as pd

sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")

# Get historical data
bars = sdk.get_bars("AAPL", "1", "Minute", bars_back=100, mode="PAPER")
df = pd.DataFrame(bars)

# Calculate moving averages
df['SMA_20'] = df['Close'].rolling(20).mean()
df['SMA_50'] = df['Close'].rolling(50).mean()

# Get latest values
current_sma_20 = df['SMA_20'].iloc[-1]
current_sma_50 = df['SMA_50'].iloc[-1]

# Get current position
position = sdk.get_position("AAPL", mode="PAPER")

# Trading logic
if current_sma_20 > current_sma_50 and position == 0:
    # Buy signal - SMA crossed up
    print("📈 Buy signal detected!")
    order_id, status = sdk.place_order(
        symbol="AAPL",
        side="BUY",
        quantity=10,
        order_type="Market",
        mode="PAPER"
    )
    print(f"✅ Order placed: {order_id}")

elif current_sma_20 < current_sma_50 and position > 0:
    # Sell signal - SMA crossed down
    print("📉 Sell signal detected!")
    order_id, status = sdk.place_order(
        symbol="AAPL",
        side="SELL",
        quantity=10,
        order_type="Market",
        mode="PAPER"
    )
    print(f"✅ Order placed: {order_id}")

else:
    print("⏸️  No signal - holding position")
```

---

### Path C: Stream Real-Time Data

**Create a real-time quote monitor:**

```python
# stream_monitor.py
import asyncio
from tradestation_sdk import TradeStationSDK

async def monitor_quotes():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")
    
    print("📊 Streaming AAPL quotes (Ctrl+C to stop)...")
    print()
    
    async for quote in sdk.streaming.stream_quotes(["AAPL"], mode="PAPER"):
        print(f"AAPL: Last=${quote.Last:>8}, Bid=${quote.Bid:>8}, Ask=${quote.Ask:>8}", end='\r')

if __name__ == "__main__":
    asyncio.run(monitor_quotes())
```

**Run it:**
```bash
python stream_monitor.py
```

---

## Going to Production

### Before LIVE Mode

**Complete this checklist:**

- [ ] **Tested thoroughly in PAPER mode** (at least 1 week)
- [ ] **Implemented error handling** for all operations
- [ ] **Added position limits** (max size, max orders/day)
- [ ] **Set up logging** and monitoring
- [ ] **Implemented stop-losses** and risk management
- [ ] **Created backup** and disaster recovery plan
- [ ] **Read [SECURITY.md](SECURITY.md)** - Security best practices
- [ ] **Read [LIMITATIONS.md](LIMITATIONS.md)** - Known constraints
- [ ] **Tested with small positions** in LIVE mode first

### Switching to LIVE Mode

**⚠️ WARNING: LIVE mode uses real money!**

**When ready:**

```python
# Change in .env file
TRADING_MODE=LIVE
```

Or in code:

```python
# Authenticate with LIVE mode
sdk.authenticate(mode="LIVE")

# Place order in LIVE mode
order_id, status = sdk.place_order(..., mode="LIVE")
```

**Best practice:**
1. Start with small position sizes
2. Monitor closely for 24-48 hours
3. Gradually increase position sizes
4. Always have stop-losses in place

---

## Troubleshooting

### Common Issues

See [FAQ & Troubleshooting](README.md#faq--troubleshooting) for solutions to:
- Port 8888 already in use
- Authentication failed
- Token expired
- Symbol not found
- Rate limit exceeded
- Module import errors

### Still Having Issues?

1. **Run diagnostic test:**
   ```bash
   python cli/test_connection.py
   ```

2. **Check SDK info:**
   ```python
   info = sdk.info()
   print(info)
   ```

3. **Enable full logging:**
   ```python
   sdk = TradeStationSDK(enable_full_logging=True)
   ```

4. **Get help:**
   - [Open an issue](https://github.com/benlaube/tradestation-python-sdk/issues)
   - [GitHub Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)

---

## Resources

### Documentation
- 📖 [README.md](README.md) - Main documentation
- 📋 [CHEATSHEET.md](CHEATSHEET.md) - Quick reference
- 💡 [docs/SDK_USAGE_EXAMPLES.md](docs/SDK_USAGE_EXAMPLES.md) - Code examples
- 📚 [docs/INDEX.md](docs/INDEX.md) - Documentation index

### Learning
- 📓 [examples/](examples/) - Jupyter notebooks
- 🔧 [cli/](cli/) - CLI testing tools
- 🎓 [TradeStation API Docs](https://developer.tradestation.com/webapi)

### Community
- 🐛 [Issues](https://github.com/benlaube/tradestation-python-sdk/issues)
- 💬 [Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)
- 📧 Email: benlaube@example.com

---

## Congratulations! 🎉

You're now ready to build sophisticated trading systems with TradeStation SDK.

**Remember:**
- Start with PAPER mode
- Test thoroughly before LIVE
- Implement risk management
- Monitor your bot closely
- Read the security guide

**Happy trading!** 📈

---

**Last Updated:** 2025-12-07  
**SDK Version:** 1.0.0

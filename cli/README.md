---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:34 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - CLI Tools

## About This Document

This directory contains **command-line diagnostic tools** for testing and verifying SDK functionality. These tools help you quickly verify your setup, test authentication, and diagnose connection issues.

**Use this if:** You want to quickly test your SDK setup, verify credentials, or diagnose connection problems.

**Related Documents:**
- 📖 **[README.md](../README.md)** - Complete SDK documentation
- 🚀 **[QUICKSTART.md](../QUICKSTART.md)** - Getting started guide
- ⚠️ **[LIMITATIONS.md](../LIMITATIONS.md)** - Known issues and troubleshooting
- ❓ **[README.md#faq--troubleshooting](../README.md#faq--troubleshooting)** - FAQ and troubleshooting

---

Command-line tools for testing and verifying SDK functionality.

## Available Tools

### test_auth.py
Test SDK authentication and token management.

```bash
python cli/test_auth.py PAPER
python cli/test_auth.py LIVE
```

### test_connection.py
Comprehensive connection test (auth, account, balances, market data).

```bash
python cli/test_connection.py
```

### test_orders.py
Test order placement and management (PAPER mode recommended).

```bash
python cli/test_orders.py --mode PAPER --symbol AAPL --side BUY --quantity 10
```

### test_streaming.py
Test real-time data streaming.

```bash
python cli/test_streaming.py --symbols AAPL,MSFT --duration 30
```

## Setup

Install SDK with dev dependencies:

```bash
pip install -e ".[dev]"
```

Create `.env` file:

```env
TRADESTATION_CLIENT_ID=your_client_id
TRADESTATION_CLIENT_SECRET=your_client_secret
TRADESTATION_REDIRECT_URI=http://localhost:8888/callback
TRADING_MODE=PAPER
```

## Usage Tips

- **Always test with PAPER mode first**
- **Use test_connection.py** to verify your setup
- **Use test_streaming.py** to check real-time data
- **Use test_orders.py** to test order placement (PAPER mode!)

## Exit Codes

- `0` - Success
- `1` - Error (check output for details)

## Support

See [main README](../README.md) for troubleshooting and support options.

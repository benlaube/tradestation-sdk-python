---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:34 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK Examples

## About This Document

This directory contains **interactive examples** demonstrating SDK usage patterns, from basic authentication to advanced streaming and trading strategies. Includes Jupyter notebooks for learning and Python scripts for quick reference.

**Use this if:** You want to learn by example, experiment interactively, or see working code you can copy.

**Related Documents:**
- 🚀 **[QUICKSTART.md](../QUICKSTART.md)** - 2-minute getting started
- 📚 **[docs/GETTING_STARTED.md](../docs/GETTING_STARTED.md)** - 15-minute comprehensive tutorial
- 💡 **[docs/SDK_USAGE_EXAMPLES.md](../docs/SDK_USAGE_EXAMPLES.md)** - More detailed examples with explanations
- 📋 **[CHEATSHEET.md](../CHEATSHEET.md)** - Quick code snippets
- 📖 **[README.md](../README.md)** - Complete SDK documentation

---

Interactive examples demonstrating SDK usage patterns, from basic authentication to advanced streaming and trading strategies.

## Jupyter Notebooks

Interactive notebooks for learning and experimentation:

1. **01_authentication.ipynb** - Authentication setup and token management
2. **02_account_balances.ipynb** - Retrieving account information and balances
3. **03_market_data.ipynb** - Historical bars, quotes, and symbol search
4. **04_placing_orders.ipynb** - Order placement (market, limit, stop, trailing stop)
5. **05_streaming_data.ipynb** - Real-time quotes, orders, and positions
6. **06_bracket_orders.ipynb** - Advanced bracket orders with profit targets and stop losses
7. **07_position_management.ipynb** - Managing positions and P&L tracking
8. **08_error_handling.ipynb** - Handling errors and implementing retry logic

## Python Scripts

Standalone Python scripts for common use cases:

- **quick_start.py** - Basic SDK setup and first order
- **stream_quotes.py** - Real-time quote streaming example
- **bracket_order_example.py** - Complete bracket order workflow
- **position_tracker.py** - Track positions and P&L in real-time

## Installation

Install Jupyter and required dependencies:

```bash
pip install -e ".[examples]"
```

Or manually:

```bash
pip install jupyter notebook matplotlib pandas
```

## Running Notebooks

```bash
cd examples/
jupyter notebook
```

Then open any `.ipynb` file in your browser.

## Environment Setup

Before running examples, create a `.env` file in the project root:

```env
TRADESTATION_CLIENT_ID=your_client_id
TRADESTATION_CLIENT_SECRET=your_client_secret
TRADESTATION_REDIRECT_URI=http://localhost:8888/callback
TRADING_MODE=PAPER
```

## Tips

- **Always use PAPER mode** for testing and learning
- **Start with notebooks 01-03** to understand basics
- **Notebooks are interactive** - modify and experiment!
- **Check SDK documentation** for complete API reference

## Support

- 📖 [SDK Documentation](../docs/)
- 💡 [Usage Examples](../docs/SDK_USAGE_EXAMPLES.md)
- 🐛 [Report Issues](https://github.com/benlaube/tradestation-python-sdk/issues)

# TradeStation SDK - Documentation Index

## About This Document

This is the **complete navigation hub** for all SDK documentation. It organizes all documentation files by category and provides learning paths for different use cases.

**Use this if:** You're looking for specific documentation, want to understand the documentation structure, or need guidance on what to read next.

**Related Documents:**
- 📖 **[README.md](../README.md)** - Main SDK documentation (start here)
- 🧭 **[CANONICAL_SDK_INVENTORY.md](CANONICAL_SDK_INVENTORY.md)** - Authoritative SDK method and endpoint inventory
- 🚀 **[QUICKSTART.md](../QUICKSTART.md)** - 2-minute getting started guide
- 📚 **[GETTING_STARTED.md](GETTING_STARTED.md)** - 15-minute comprehensive tutorial
- 📋 **[CHEATSHEET.md](../CHEATSHEET.md)** - Quick reference guide

---

Complete guide to all SDK documentation. Start here to find what you need!

---

## 🚀 Getting Started (New Users)

**Start here if you're new to the SDK:**

1. **[QUICKSTART.md](../QUICKSTART.md)** - 2-minute setup guide (copy-paste and go!)
2. **[README.md](../README.md#quick-start-5-minutes)** - 5-minute tutorial with explanations
3. **[examples/01_authentication.ipynb](../examples/01_authentication.ipynb)** - Interactive authentication tutorial
4. **[tradestation/cli/test_connection.py](../tradestation/cli/test_connection.py)** - Verify your setup works

**Recommended Path:**
```
QUICKSTART.md → README.md → Jupyter Notebooks → API Reference
```

---

## 📚 Core Documentation

### Main Documentation Files

| File | Purpose | When to Use |
|------|---------|-------------|
| [README.md](../README.md) | Main SDK documentation | Starting point, feature overview |
| [CANONICAL_SDK_INVENTORY.md](CANONICAL_SDK_INVENTORY.md) | Source-of-truth SDK inventory | Verify the current public surface and endpoints |
| [QUICKSTART.md](../QUICKSTART.md) | 2-minute setup guide | Fastest path to running code |
| [CHEATSHEET.md](../CHEATSHEET.md) | Quick reference | Keep handy while coding |
| [FAQ & Troubleshooting](../README.md#faq--troubleshooting) | Common issues | When something doesn't work |

### Specialized Guides

| File | Purpose | When to Use |
|------|---------|-------------|
| [MIGRATION.md](../MIGRATION.md) | Migration guide | Switching from other SDKs |
| [LIMITATIONS.md](../LIMITATIONS.md) | Known constraints | Understanding SDK boundaries |
| [CONTRIBUTING.md](../CONTRIBUTING.md) | Contribution guide | Adding features/fixing bugs |
| [CHANGELOG.md](../CHANGELOG.md) | Version history | Tracking changes, upgrade notes |
| [ROADMAP.md](ROADMAP.md) | Future plans | Upcoming features and timeline |
| [SUBMODULE_INTEGRATION.md](SUBMODULE_INTEGRATION.md) | Git submodule usage | Embedding the SDK into other repos |

---

## 📖 Technical Documentation (docs/)

### API Reference

| File | Description | Use For |
|------|-------------|---------|
| [CANONICAL_SDK_INVENTORY.md](CANONICAL_SDK_INVENTORY.md) | Canonical method inventory | Current SDK façade, convenience functions, endpoint families |
| [API_REFERENCE.md](API_REFERENCE.md) | Complete API reference | Function signatures, parameters |
| [SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md) | Code examples | Working code patterns |
| [ORDER_FUNCTIONS_REFERENCE.md](ORDER_FUNCTIONS_REFERENCE.md) | Order functions | Order placement details |
| [API_ENDPOINT_MAPPING.md](API_ENDPOINT_MAPPING.md) | SDK → API mapping | Understanding internals |

### Architecture & Design

| File | Description | Use For |
|------|-------------|---------|
| [API_STRUCTURE.md](API_STRUCTURE.md) | API organization | Understanding TradeStation API |
| [API_STRUCTURE_DETAILED.md](API_STRUCTURE_DETAILED.md) | Detailed API analysis | Deep dive into API design |
| [README.md](README.md) | Service overview | Architecture decisions |

### Models & Data

| File | Description | Use For |
|------|-------------|---------|
| [MODELS.md](MODELS.md) | Pydantic models | Type definitions, field descriptions |
| [TRAILING_STOP_VARIATIONS.md](TRAILING_STOP_VARIATIONS.md) | Trailing stop details | Advanced order types |

### Coverage & Analysis

| File | Description | Use For |
|------|-------------|---------|
| [API_COVERAGE.md](API_COVERAGE.md) | Endpoint coverage | Feature completeness |
| [OPERATION_COVERAGE.md](OPERATION_COVERAGE.md) | Operation analysis | What's implemented |
| [GAP_ANALYSIS.md](GAP_ANALYSIS.md) | Missing features | Future roadmap |

---

## 💡 Examples & Tutorials

### Interactive Notebooks (examples/)

**Learn by doing with Jupyter notebooks:**

| Notebook | Topic | Difficulty |
|----------|-------|------------|
| [01_authentication.ipynb](../examples/01_authentication.ipynb) | Authentication & setup | Beginner |
| [GETTING_STARTED.md](GETTING_STARTED.md) | 15-minute tutorial | Beginner |
| [03_market_data.ipynb](../examples/03_market_data.ipynb) | Market data & charts | Beginner |
| [04_placing_orders.ipynb](../examples/04_placing_orders.ipynb) | Order placement | Intermediate |

**Setup:**
```bash
cd examples/
pip install -r requirements.txt
jupyter notebook
```

### Python Scripts (examples/)

**Standalone scripts you can run directly:**

- [quick_start.py](../examples/quick_start.py) - Complete quick start example

---

## 🔧 CLI Tools (`tradestation/cli/`)

**Command-line tools for testing and debugging:**

| Tool | Purpose | Command |
|------|---------|---------|
| [test_auth.py](../tradestation/cli/test_auth.py) | Test authentication | `python tradestation/cli/test_auth.py PAPER` |
| [test_connection.py](../tradestation/cli/test_connection.py) | Full connection test | `python tradestation/cli/test_connection.py` |

See the scripts in [`tradestation/cli/`](../tradestation/cli/) for complete CLI coverage.

---

## 🧪 Testing Documentation

### Test Suite

| File | Description | Use For |
|------|-------------|---------|
| [tests/README.md](../tests/README.md) | Test suite overview | Running tests, coverage |
| [tests/conftest.py](../tests/conftest.py) | Test fixtures | Understanding test setup |
| [tests/fixtures/api_responses.py](../tests/fixtures/api_responses.py) | Mock data | Test data reference |

**Run tests:**
```bash
pytest                          # All tests
pytest --cov                    # With coverage
pytest tests/test_accounts.py   # Specific module
```

---

## 📊 Learning Paths

### Path 1: Beginner (Never used trading APIs)

1. [QUICKSTART.md](../QUICKSTART.md) - Get started in 2 minutes
2. [01_authentication.ipynb](../examples/01_authentication.ipynb) - Learn authentication
3. [GETTING_STARTED.md](GETTING_STARTED.md) - Complete 15-minute tutorial
4. [03_market_data.ipynb](../examples/03_market_data.ipynb) - Get market data
5. [04_placing_orders.ipynb](../examples/04_placing_orders.ipynb) - Place your first order
6. [CHEATSHEET.md](../CHEATSHEET.md) - Keep this handy!

### Path 2: Intermediate (Used other trading APIs)

1. [MIGRATION.md](../MIGRATION.md) - Compare with other SDKs
2. [README.md](../README.md) - Understand SDK features
3. [SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md) - See code patterns
4. [API_REFERENCE.md](API_REFERENCE.md) - Deep dive into API

### Path 3: Advanced (Building production systems)

1. [LIMITATIONS.md](../LIMITATIONS.md) - Understand constraints
2. [API_COVERAGE.md](API_COVERAGE.md) - Know what's available
3. [ORDER_FUNCTIONS_REFERENCE.md](ORDER_FUNCTIONS_REFERENCE.md) - Master order execution
4. [MODELS.md](MODELS.md) - Understand data structures
5. [CONTRIBUTING.md](../CONTRIBUTING.md) - Extend the SDK

---

## 🔍 Quick Lookup

**Need to find something specific?**

| I want to... | Go to... |
|--------------|----------|
| Verify whether a method or endpoint exists right now | [CANONICAL_SDK_INVENTORY.md](CANONICAL_SDK_INVENTORY.md) |
| Set up SDK in 2 minutes | [QUICKSTART.md](../QUICKSTART.md) |
| Learn authentication | [01_authentication.ipynb](../examples/01_authentication.ipynb) |
| Place my first order | [04_placing_orders.ipynb](../examples/04_placing_orders.ipynb) |
| Fix port conflict | [FAQ & Troubleshooting](../README.md#faq--troubleshooting) |
| See code examples | [SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md) |
| Find a function | [CANONICAL_SDK_INVENTORY.md](CANONICAL_SDK_INVENTORY.md) |
| Quick reference | [CHEATSHEET.md](../CHEATSHEET.md) |
| Understand errors | [README.md](../README.md#error-handling) |
| Stream real-time data | [SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md#streaming) |
| Migrate from other SDK | [MIGRATION.md](../MIGRATION.md) |
| Know SDK limits | [LIMITATIONS.md](../LIMITATIONS.md) |
| See future plans | [ROADMAP.md](ROADMAP.md) |
| Contribute code | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| Check version changes | [CHANGELOG.md](../CHANGELOG.md) |

---

## 📁 Documentation Structure

```
tradestation/
├── README.md                    # Main documentation
├── QUICKSTART.md                # 2-minute setup
├── CHEATSHEET.md                # Quick reference
├── MIGRATION.md                 # Migration guide
├── LIMITATIONS.md               # Known limitations
├── CONTRIBUTING.md              # Contribution guide
├── CHANGELOG.md                 # Version history
├── LICENSE                      # MIT License
│
├── docs/                        # Technical documentation
│   ├── INDEX.md                 # This file
│   ├── API_REFERENCE.md         # Complete API reference
│   ├── SDK_USAGE_EXAMPLES.md    # Code examples
│   ├── ORDER_FUNCTIONS_REFERENCE.md
│   ├── MODELS.md
│   ├── API_COVERAGE.md
│   └── ...
│
├── examples/                    # Interactive examples
│   ├── README.md
│   ├── 01_authentication.ipynb
│   ├── 03_market_data.ipynb
│   ├── 04_placing_orders.ipynb
│   ├── quick_start.py
│   └── requirements.txt
│
├── tradestation/cli/            # CLI testing tools
│   ├── README.md
│   ├── test_auth.py
│   └── test_connection.py
│
└── tests/                       # Test suite
    ├── README.md
    └── ...
```

---

## 🆘 Need Help?

### First Steps

1. **Check [QUICKSTART.md](../QUICKSTART.md)** - Maybe you just need the quick start
2. **Read [FAQ](../README.md#faq--troubleshooting)** - Common issues are documented
3. **Run [test_connection.py](../tradestation/cli/test_connection.py)** - Diagnose connection issues
4. **Check [LIMITATIONS.md](../LIMITATIONS.md)** - Your issue might be a known limitation

### Still Stuck?

- 🐛 [Open an Issue](https://github.com/benlaube/tradestation-python-sdk/issues) - Bug reports
- 💬 [GitHub Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions) - Questions
- 📧 [Email](mailto:benlaube@example.com) - Direct support

---

## 🗺️ Navigation Tips

**Use your text editor's search** (Ctrl+F / Cmd+F) to find topics across all documentation files.

**Common search terms:**
- "authentication" - Auth setup and token management
- "order" - Order placement and management
- "streaming" - Real-time data streaming
- "error" - Error handling and troubleshooting
- "rate limit" - API rate limits and throttling
- "bracket" - Bracket order examples
- "position" - Position management

---

**Happy coding!** 🚀

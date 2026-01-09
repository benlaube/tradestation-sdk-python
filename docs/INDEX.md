---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:33 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - Documentation Index

## About This Document

This is the **complete navigation hub** for all SDK documentation. It organizes all documentation files by category and provides learning paths for different use cases.

**Use this if:** You're looking for specific documentation, want to understand the documentation structure, or need guidance on what to read next.

**Note:** Documentation has been reorganized. See [README.md](README.md) for the new structure.

**Related Documents:**
- 📖 **[README.md](../README.md)** - Main SDK documentation (start here)
- 🚀 **[QUICKSTART.md](../QUICKSTART.md)** - 2-minute getting started guide
- 📚 **[Getting Started Tutorial](getting-started/README.md)** - 15-minute comprehensive tutorial
- 📋 **[CHEATSHEET.md](../CHEATSHEET.md)** - Quick reference guide

---

**⚠️ Documentation Structure Updated**

The documentation has been reorganized into a hierarchical structure. See [README.md](README.md) for the new organization.

**Quick Links:**
- [Getting Started](getting-started/README.md) - Installation and tutorials
- [API Reference](api/reference.md) - Complete API documentation
- [Models Documentation](models/README.md) - Model documentation
- [Guides & Examples](guides/README.md) - How-to guides
- [Architecture](architecture/README.md) - System architecture
- [Reference Materials](reference/README.md) - Quick references
- [Analysis & Research](analysis/README.md) - Analysis documents

---

Complete guide to all SDK documentation. Start here to find what you need!

---

## 🚀 Getting Started (New Users)

**Start here if you're new to the SDK:**

1. **[QUICKSTART.md](../QUICKSTART.md)** - 2-minute setup guide (copy-paste and go!)
2. **[README.md](../README.md#quick-start-5-minutes)** - 5-minute tutorial with explanations
3. **[examples/01_authentication.ipynb](../examples/01_authentication.ipynb)** - Interactive authentication tutorial
4. **[cli/test_connection.py](../cli/test_connection.py)** - Verify your setup works

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
| [api/reference.md](api/reference.md) | Complete API reference | Function signatures, parameters |
| [api/endpoints.md](api/endpoints.md) | SDK → API mapping | Understanding internals |
| [api/coverage.md](api/coverage.md) | Endpoint coverage | Feature completeness |
| [api/operations.md](api/operations.md) | Operation analysis | What's implemented |
| [api/structure.md](api/structure.md) | API organization | Understanding TradeStation API |

### Architecture & Design

| File | Description | Use For |
|------|-------------|---------|
| [architecture/overview.md](architecture/overview.md) | SDK architecture | Architecture decisions |
| [architecture/feature-comparison.md](architecture/feature-comparison.md) | Feature comparison | Comparing with other SDKs |
| [architecture/gap-analysis.md](architecture/gap-analysis.md) | Missing features | Future roadmap |

### Models & Data

| File | Description | Use For |
|------|-------------|---------|
| [models/README.md](models/README.md) | Pydantic models | Type definitions, field descriptions |
| [reference/trailing-stops.md](reference/trailing-stops.md) | Trailing stop details | Advanced order types |

### Guides & Examples

| File | Description | Use For |
|------|-------------|---------|
| [guides/usage-examples.md](guides/usage-examples.md) | Code examples | Working code patterns |
| [guides/order-functions.md](guides/order-functions.md) | Order functions | Order placement details |
| [guides/code-examples.md](guides/code-examples.md) | OpenAPI examples | Code patterns |
| [guides/submodule-integration.md](guides/submodule-integration.md) | Git submodule | Embedding SDK |

### Reference Materials

| File | Description | Use For |
|------|-------------|---------|
| [reference/functions-list.md](reference/functions-list.md) | Function list | Complete function reference |
| [reference/new-functions.md](reference/new-functions.md) | New functions | Recently added features |
| [reference/audit-references.md](reference/audit-references.md) | Audit files | Audit documentation |

### Analysis & Research

| File | Description | Use For |
|------|-------------|---------|
| [analysis/openapi-analysis.md](analysis/openapi-analysis.md) | OpenAPI analysis | API specification analysis |
| [analysis/roadmap.md](analysis/roadmap.md) | Development roadmap | Future plans |

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

## 🔧 CLI Tools (cli/)

**Command-line tools for testing and debugging:**

| Tool | Purpose | Command |
|------|---------|---------|
| [test_auth.py](../cli/test_auth.py) | Test authentication | `python cli/test_auth.py PAPER` |
| [test_connection.py](../cli/test_connection.py) | Full connection test | `python cli/test_connection.py` |

See [cli/README.md](../cli/README.md) for complete CLI documentation.

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
3. [Getting Started Tutorial](getting-started/README.md) - Complete 15-minute tutorial
4. [03_market_data.ipynb](../examples/03_market_data.ipynb) - Get market data
5. [04_placing_orders.ipynb](../examples/04_placing_orders.ipynb) - Place your first order
6. [CHEATSHEET.md](../CHEATSHEET.md) - Keep this handy!

### Path 2: Intermediate (Used other trading APIs)

1. [MIGRATION.md](../MIGRATION.md) - Compare with other SDKs
2. [README.md](../README.md) - Understand SDK features
3. [Usage Examples](guides/usage-examples.md) - See code patterns
4. [API Reference](api/reference.md) - Deep dive into API

### Path 3: Advanced (Building production systems)

1. [LIMITATIONS.md](../LIMITATIONS.md) - Understand constraints
2. [API Coverage](api/coverage.md) - Know what's available
3. [Order Functions](guides/order-functions.md) - Master order execution
4. [Models Documentation](models/README.md) - Understand data structures
5. [CONTRIBUTING.md](../CONTRIBUTING.md) - Extend the SDK

---

## 🔍 Quick Lookup

**Need to find something specific?**

| I want to... | Go to... |
|--------------|----------|
| Set up SDK in 2 minutes | [QUICKSTART.md](../QUICKSTART.md) |
| Learn authentication | [01_authentication.ipynb](../examples/01_authentication.ipynb) |
| Place my first order | [04_placing_orders.ipynb](../examples/04_placing_orders.ipynb) |
| Fix port conflict | [FAQ & Troubleshooting](../README.md#faq--troubleshooting) |
| See code examples | [Usage Examples](guides/usage-examples.md) |
| Find a function | [API Reference](api/reference.md) |
| Quick reference | [CHEATSHEET.md](../CHEATSHEET.md) |
| Understand errors | [README.md](../README.md#error-handling) |
| Stream real-time data | [Usage Examples](guides/usage-examples.md) |
| Migrate from other SDK | [MIGRATION.md](../MIGRATION.md) |
| Know SDK limits | [LIMITATIONS.md](../LIMITATIONS.md) |
| See future plans | [Roadmap](analysis/roadmap.md) |
| Contribute code | [CONTRIBUTING.md](../CONTRIBUTING.md) |
| Check version changes | [CHANGELOG.md](../CHANGELOG.md) |

---

## 📁 Documentation Structure

```
tradestation-sdk/
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
│   ├── README.md                # Documentation index (new structure)
│   ├── INDEX.md                 # This file (legacy index)
│   ├── getting-started/         # Getting started guides
│   ├── api/                     # API documentation
│   ├── models/                  # Model documentation
│   ├── guides/                  # How-to guides
│   ├── architecture/            # Architecture docs
│   ├── reference/               # Reference materials
│   └── analysis/                # Analysis & research
│
├── examples/                    # Interactive examples
│   ├── README.md
│   ├── 01_authentication.ipynb
│   ├── 03_market_data.ipynb
│   ├── 04_placing_orders.ipynb
│   ├── quick_start.py
│   └── requirements.txt
│
├── cli/                         # CLI testing tools
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
3. **Run [test_connection.py](../cli/test_connection.py)** - Diagnose connection issues
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

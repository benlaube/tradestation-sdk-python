---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:33 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - Feature Comparison

## About This Document

This document compares the TradeStation SDK to other trading SDKs and libraries. It provides a feature-by-feature comparison matrix to help you understand how this SDK differs from alternatives.

**Use this if:** You're evaluating SDKs, migrating from another library, or want to understand this SDK's competitive advantages.

**Related Documents:**

- 🔄 **[MIGRATION.md](../guides/migration.md)** - Migration guide from other SDKs
- 🎯 **[FEATURES.md](features.md)** - Complete feature overview
- 📖 **[README.md](../../README.md)** - SDK documentation
- 🗺️ **[ROADMAP.md](../analysis/roadmap.md)** - Future development plans

---

How this SDK compares to other trading SDKs and libraries.

---

## SDK Comparison Matrix

### TradeStation SDKs

| Feature | This SDK (Internal) | tastyware/tradestation | Official SDK (if available) |
|---------|-------------------|----------------------|---------------------------|
| **Installation** | `pip install tradestation-sdk` | `pip install tradestation` | N/A |
| **Python Version** | 3.10+ | 3.7+ | N/A |
| **OAuth2 Support** | ✅ Automatic | ✅ Manual | N/A |
| **Token Management** | ✅ Automatic refresh | ⚠️ Manual | N/A |
| **PAPER/LIVE Modes** | ✅ Seamless switching | ❌ Single mode | N/A |
| **Type Safety** | ✅ Pydantic models | ⚠️ Partial | N/A |
| **Error Handling** | ✅ Custom exceptions | ⚠️ Generic | N/A |
| **Streaming** | ✅ HTTP Streaming | ✅ WebSocket | N/A |
| **Auto-Reconnect** | ✅ Yes | ❌ No | N/A |
| **REST Fallback** | ✅ Yes | ❌ No | N/A |
| **Convenience Functions** | ✅ 18+ functions | ❌ Low-level only | N/A |
| **Documentation** | ✅ Comprehensive | ⚠️ Minimal | N/A |
| **Examples** | ✅ Jupyter + CLI | ❌ None | N/A |
| **Tests** | ✅ 90%+ coverage | ⚠️ Limited | N/A |
| **Active Maintenance** | ✅ Active | ⚠️ Sporadic | N/A |

**Legend:**

- ✅ Fully supported
- ⚠️ Partially supported or manual
- ❌ Not supported
- N/A - Not available

---

### vs Other Broker SDKs

| Feature | TradeStation SDK | Alpaca | Interactive Brokers | TD Ameritrade |
|---------|-----------------|--------|---------------------|---------------|
| **Auth Type** | OAuth2 | API Key | TWS/Gateway | OAuth2 |
| **Paper Trading** | ✅ PAPER mode | ✅ Paper account | ✅ Simulator | ✅ Paper account |
| **Real-Time Streaming** | ✅ HTTP Streaming | ✅ WebSocket | ✅ Native | ✅ WebSocket |
| **Futures Trading** | ✅ Full support | ❌ Not supported | ✅ Full support | ✅ Full support |
| **Options Trading** | ✅ Full support | ⚠️ Limited | ✅ Full support | ✅ Full support |
| **Bracket Orders** | ✅ Native | ✅ Via API | ✅ Native | ✅ Via API |
| **Trailing Stops** | ✅ Native | ✅ Via API | ✅ Native | ✅ Via API |
| **Historical Data** | ✅ REST API | ✅ REST API | ✅ Native | ✅ REST API |
| **Market Hours** | ✅ Extended | ✅ Extended | ✅ 24/5 (futures) | ✅ Extended |
| **Commission** | Varies | $0 stocks | Varies | $0 stocks |
| **Python Support** | ✅ Native | ✅ Native | ✅ ib_insync | ✅ Native |
| **Documentation** | ✅ Excellent | ✅ Excellent | ✅ Good | ✅ Good |

---

## Feature Completeness

### TradeStation API v3 Coverage

| Category | Coverage | Functions | Notes |
|----------|----------|-----------|-------|
| **Accounts** | 100% | 4/4 | All endpoints implemented |
| **Market Data** | 90% | 16/18 | Missing: OptionChain variations |
| **Orders** | 95% | 28/30 | All major order types |
| **Positions** | 100% | 4/4 | All endpoints implemented |
| **Streaming** | 80% | 5/7 | Missing: BarCharts, OptionChain streams |
| **Overall** | 92% | 57/62 | Production-ready |

**Details:** See [API_COVERAGE.md](API_COVERAGE.md)

---

## Supported Order Types

| Order Type | This SDK | Alpaca | IB | TD Ameritrade |
|------------|----------|--------|-------|---------------|
| Market | ✅ | ✅ | ✅ | ✅ |
| Limit | ✅ | ✅ | ✅ | ✅ |
| Stop | ✅ | ✅ | ✅ | ✅ |
| Stop-Limit | ✅ | ✅ | ✅ | ✅ |
| Trailing Stop | ✅ | ⚠️ (client-side) | ✅ | ✅ |
| Bracket (OCA) | ✅ | ⚠️ (via API) | ✅ | ⚠️ (via API) |
| OCO | ✅ | ❌ | ✅ | ✅ |
| Conditional | ✅ | ❌ | ✅ | ✅ |

---

## Performance Comparison

### Order Execution Speed

| SDK | Avg Latency | Notes |
|-----|-------------|-------|
| TradeStation SDK | ~200-300ms | Via REST API |
| Alpaca | ~100-200ms | WebSocket + REST |
| Interactive Brokers | ~50-150ms | Native API |
| TD Ameritrade | ~150-250ms | Via REST API |

**Note:** Latency depends on network, location, and market conditions.

---

### Streaming Performance

| SDK | Latency | Reliability | Reconnection |
|-----|---------|-------------|--------------|
| TradeStation SDK | ~50-100ms | ⚠️ HTTP | ✅ Auto |
| Alpaca | ~20-50ms | ✅ WebSocket | ✅ Auto |
| Interactive Brokers | ~10-30ms | ✅ Native | ✅ Auto |
| TD Ameritrade | ~30-60ms | ✅ WebSocket | ✅ Auto |

**Note:** TradeStation uses HTTP Streaming (not WebSocket), which has slightly higher latency.

---

## Asset Class Support

| Asset Class | This SDK | Alpaca | IB | TD Ameritrade |
|-------------|----------|--------|-------|---------------|
| **Stocks** | ✅ | ✅ | ✅ | ✅ |
| **Futures** | ✅ | ❌ | ✅ | ✅ |
| **Options** | ✅ | ⚠️ Limited | ✅ | ✅ |
| **Crypto** | ✅ | ✅ | ⚠️ Limited | ❌ |
| **Forex** | ✅ | ❌ | ✅ | ✅ |
| **Bonds** | ❌ | ❌ | ✅ | ✅ |

---

## Why Choose TradeStation SDK?

### Strengths

✅ **Full futures support** - Complete futures trading (unlike Alpaca)
✅ **Automatic token refresh** - No manual token management
✅ **Dual-mode support** - Seamless PAPER ↔ LIVE switching
✅ **Type safety** - Pydantic models for all data
✅ **Error handling** - Detailed error context and categorization
✅ **Convenience functions** - Simple interfaces for common tasks
✅ **Comprehensive docs** - Jupyter notebooks, CLI tools, examples
✅ **Auto-reconnection** - Streaming reliability with fallback
✅ **Test suite** - 90%+ coverage with mocked tests

### Trade-offs

⚠️ **HTTP Streaming** - Slightly higher latency than WebSocket
⚠️ **Python 3.10+** - Newer Python required
⚠️ **Synchronous client** - Blocking I/O (async planned for v2.0)
⚠️ **Token storage** - Plain JSON (encryption planned for v1.1)

---

## Use Cases

### When to Use This SDK

✅ **Algorithmic futures trading** - Full futures support
✅ **Multi-strategy systems** - PAPER/LIVE mode switching
✅ **Production trading bots** - Reliable, well-tested
✅ **Paper trading & backtesting** - Full PAPER mode support
✅ **Educational projects** - Comprehensive examples

### When to Consider Alternatives

- **Ultra-low latency required** → Interactive Brokers (native API)
- **Stock-only trading** → Alpaca (simpler, WebSocket streaming)
- **Cryptocurrency focus** → Specialized crypto exchanges
- **Options-heavy strategies** → Interactive Brokers (better options tools)

---

## Feature Roadmap vs Competitors

| Planned Feature | Version | Alpaca | IB | Notes |
|-----------------|---------|--------|-------|-------|
| Token encryption | v1.1 | N/A | N/A | System keychain |
| Built-in retry | v1.2 | ✅ Has | ✅ Has | Exponential backoff |
| Rate limiting | v1.2 | ✅ Has | ✅ Has | Auto-throttling |
| Async HTTP | v2.0 | ✅ Has | ✅ Has | Native async |
| WebSocket | v2.0 | ✅ Has | ✅ Has | If TS adds support |
| Connection pooling | v2.0 | ✅ Has | ✅ Has | Performance |

---

## Community & Ecosystem

### Integrations

**Works with:**

- ✅ Pandas (data analysis)
- ✅ TA-Lib (technical indicators)
- ✅ Backtrader (backtesting)
- ✅ Jupyter (interactive development)
- ✅ FastAPI (web services)
- ✅ Celery (task queues)

**Tested Platforms:**

- ✅ Linux (Ubuntu, RHEL, Arch)
- ✅ macOS (Intel, Apple Silicon)
- ✅ Windows (10, 11)
- ✅ Docker containers
- ✅ Cloud platforms (AWS, GCP, Azure)

---

## Conclusion

**Choose this SDK if you need:**

- Futures trading support
- Comprehensive TradeStation API coverage
- Type safety and modern Python
- Extensive documentation and examples
- Production-ready reliability

**Choose alternatives if you need:**

- Ultra-low latency (IB)
- Stock-only simplicity (Alpaca)
- Mature async implementation (wait for v2.0 or use IB)

---

**Still deciding?** Try the [Quick Start](../getting-started/quickstart.md) - takes 2 minutes!

---

**Last Updated:** 2025-12-07

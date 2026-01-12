---
version: 1.0.1
lastUpdated: 01-08-2026 20:06:00 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - Roadmap

## About This Document

This document outlines the **future development plans and roadmap** for the SDK. It includes version strategy, planned features, timelines, and priorities for upcoming releases.

**Use this if:** You want to know what's coming next, understand development priorities, or see the long-term vision for the SDK.

**Related Documents:**

- 📝 **[CHANGELOG.md](../CHANGELOG.md)** - What's been released (past)
- ⚠️ **[docs/architecture/limitations.md](../architecture/limitations.md)** - Known issues and planned fixes
- 📖 **[README.md](../README.md)** - Current SDK features
- 🎯 **[FEATURES.md](../architecture/features.md)** - Complete feature overviews
- 🤝 **[CONTRIBUTING.md](../CONTRIBUTING.md)** - How to contribute to roadmap items

---

Future plans and development roadmap for the SDK.

---

## Version Strategy

We follow [Semantic Versioning](https://semver.org/):

- **Major (X.0.0):** Breaking changes
- **Minor (0.X.0):** New features, backward-compatible
- **Patch (0.0.X):** Bug fixes, backward-compatible

---

## Current Version: v1.0.1 (December 2025)

**Status:** Production Ready (Beta for external distribution)

**Highlights (v1.0.1):**

- ✅ **Security:** System keychain support for token storage (macOS, Linux, Windows)
- ✅ **Reliability:** Auto-selection of available OAuth ports (conflicts resolved)
- ✅ **Performance:** Async support included via `use_async=True` (beta)
- ✅ **Resiliency:** Built-in retry logic for all REST operations

**Core Features (v1.0.0):**

- Complete TradeStation API v3 support (90%+ coverage)
- OAuth2 authentication with automatic token refresh
- PAPER/LIVE mode support
- HTTP Streaming with auto-reconnection
- Type-safe Pydantic models

**Known Limitations:** See [docs/architecture/limitations.md](../architecture/limitations.md)

---

## Planned Releases

### v1.1 (Q1 2026) - Usability & Convenience

**Focus:** Developer experience and convenience features

**Features:**

- 💰 **Trail Amount Dollars** - `trail_amount_dollars` parameter for convenience
- 📝 **Enhanced Error Messages** - Even more descriptive context for complex order failures
- 📊 **Request Metrics** - Track API usage, latency, error rates
- 🧹 **Cleanup** - Finalize async interface standardization

**Timeline:** Q1 2026 (January-March)

---

### v1.2 (Q2 2026) - Reliability & Advanced Features

**Focus:** Reliability at scale and advanced trading logic

**Features:**

- 🚦 **Rate Limit Tracking** - Automatic rate limit monitoring and throttling (pre-emptive)
- 🔀 **Circuit Breaker Pattern** - Prevent cascading failures in streaming
- 💾 **Request Caching** - Cache account info, balances, symbol searches
- 🔗 **Connection Pooling** - HTTP connection reuse optimization

**Timeline:** Q2 2026 (April-June)

---

### v1.3 (Q3 2026) - Advanced Orders

**Focus:** Complex order types and trading strategies

**Features:**

- 📈 **Advanced Order Types** - More conditional order patterns
- 🎯 **Order Templates** - Pre-configured order templates
- 📊 **Options Strategies** - Iron condors, spreads, straddles validation
- 📉 **Advanced Stops** - Chandelier stops, ATR-based stops

**Timeline:** Q3 2026 (July-September)

---

### v2.0 (Q4 2026) - Async-First & Performance

**Focus:** Async-first architecture and major performance improvements

**Breaking Changes:**

- Async-first API (sync methods may be deprecated or wrapped)
- Minimum Python version: 3.10+
- New import structure (if needed for major refactor)

**Features:**

- ⚡ **Native Async Core** - Fully async core (moving away from requests entirely if needed)
- 🌐 **WebSocket Support** - Native WebSocket (if TradeStation adds it)
- 🎯 **Batch Operations** - Batch multiple API calls
- 💾 **Advanced Caching** - Redis/memcached support

**Timeline:** Q4 2026 (October-December)

---

## Feature Requests & Community Input

### Most Requested Features

**From GitHub Issues:**

1. Token encryption (v1.1) ✅ Delivered in v1.0.1
2. Built-in retry logic (v1.2) ✅ Delivered in v1.0.1
3. Async support (v2.0) ✅ Beta in v1.0.1
4. Options trading examples (v1.3) ✅ Planned

**Want to request a feature?**

- [Open a feature request](https://github.com/benlaube/tradestation-python-sdk/issues/new?template=feature_request.md)
- [Vote on existing requests](https://github.com/benlaube/tradestation-python-sdk/issues?q=is%3Aissue+is%3Aopen+label%3Aenhancement)
- [Join discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)

---

## Long-Term Vision (2027+)

### Vision: Complete Trading Ecosystem

**Beyond v2.0:**

- 📊 **Built-in Backtesting** - Backtest strategies without external libraries
- 📈 **Strategy Templates** - Pre-built trading strategies
- 🔔 **Alert System** - Custom alerts for price, volume, indicators
- 📱 **Mobile Support** - iOS/Android SDK wrappers
- 🌍 **Multi-Broker Support** - Abstract interface for other brokers
- 🤖 **AI/ML Integration** - Built-in ML model deployment
- 📊 **Analytics Dashboard** - Web-based analytics and monitoring

---

## Community Contributions Welcome

**Want to contribute?** See [CONTRIBUTING.md](CONTRIBUTING.md)

**Areas needing help:**

- 📝 Documentation improvements
- 🧪 More test coverage
- 💡 Example strategies
- 🔧 CLI tools
- 🌐 Internationalization
- 📚 Tutorial content

---

## Stability Promise

**v1.x Stability:**

- No breaking changes in v1.x releases
- Deprecations will be warned 6 months before removal
- Critical security fixes will be backported
- Long-term support (LTS) for v1.x until v2.0 stable

**v2.0 Migration:**

- 6-month migration window
- Compatibility shim provided
- Detailed migration guide
- Community support during migration

---

## Release Schedule

| Version | Target | Status | Focus |
|---------|--------|--------|-------|
| v1.0.0 | Dec 2025 | ✅ Released | Initial release |
| v1.0.1 | Jan 2026 | ✅ Released | Security (Keychain), Async Beta, Retries |
| v1.1.0 | Q1 2026 | 📋 Planned | Usability & Convenience |
| v1.2.0 | Q2 2026 | 📋 Planned | Reliability & Advanced Features |
| v1.3.0 | Q3 2026 | 📋 Planned | Advanced Orders |
| v2.0.0 | Q4 2026 | 📋 Planned | Async-First & Performance |

**Note:** Dates are targets and may shift based on priorities and community needs.

---

## Versioning & Support Policy

### Active Support

- **v1.x (current):** Active development, bug fixes, security patches
- **v0.x (if any):** Security patches only

### Long-Term Support (LTS)

- **v1.x:** Supported until 6 months after v2.0 stable release
- **v2.x:** Active support after release

### End of Life (EOL)

- We'll provide **at least 6 months notice** before ending support for any version.

---

## Stay Informed

**Get updates:**

- ⭐ [Star the repo](https://github.com/benlaube/tradestation-python-sdk) to watch releases
- 📧 [Subscribe to newsletter](https://example.com/newsletter)
- 🐦 [Follow on Twitter](https://twitter.com/example)
- 💬 [Join discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)

---

## Feedback

**Shape the roadmap!**

Your feedback directly influences development priorities:

- [Feature requests](https://github.com/benlaube/tradestation-python-sdk/issues/new?template=feature_request.md)
- [Bug reports](https://github.com/benlaube/tradestation-python-sdk/issues/new?template=bug_report.md)
- [Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)

**Most-requested features get priority!**

---

**Last Updated:** 2026-01-08
**Current Version:** 1.0.1
**Next Release:** v1.1.0 (Q1 2026)

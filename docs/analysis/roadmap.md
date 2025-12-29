# TradeStation SDK - Roadmap

## About This Document

This document outlines the **future development plans and roadmap** for the SDK. It includes version strategy, planned features, timelines, and priorities for upcoming releases.

**Use this if:** You want to know what's coming next, understand development priorities, or see the long-term vision for the SDK.

**Related Documents:**
- 📝 **[CHANGELOG.md](../CHANGELOG.md)** - What's been released (past)
- ⚠️ **[LIMITATIONS.md](../LIMITATIONS.md)** - Known issues and planned fixes
- 📖 **[README.md](../README.md)** - Current SDK features
- 🎯 **[FEATURES.md](../FEATURES.md)** - Complete feature overview
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

## Current Version: v1.0.0 (December 2025)

**Status:** Production Ready (Beta for external distribution)

**Highlights:**
- Complete TradeStation API v3 support (90%+ coverage)
- OAuth2 authentication with automatic token refresh
- PAPER/LIVE mode support
- HTTP Streaming with auto-reconnection
- Type-safe Pydantic models
- Comprehensive error handling
- 90%+ test coverage

**Known Limitations:** See [LIMITATIONS.md](LIMITATIONS.md)

---

## Planned Releases

### v1.1 (Q1 2026) - Security & Reliability

**Focus:** Security enhancements and reliability improvements

**Features:**
- 🔒 **Token Encryption** - System keychain integration (macOS, Linux, Windows)
- 🔌 **Auto-Port Selection** - Automatic OAuth callback port selection (8888-8898)
- 💰 **Trail Amount Dollars** - `trail_amount_dollars` parameter for convenience
- 📝 **Improved Error Messages** - More descriptive error messages with solutions
- 🔄 **Proactive Token Refresh** - Refresh tokens before expiration
- 📊 **Request Metrics** - Track API usage, latency, error rates

**Security:**
- Encrypted token storage (no plain JSON)
- Secure credential management
- Token rotation helpers

**Developer Experience:**
- Better error messages
- More CLI diagnostic tools
- Enhanced logging options

**Timeline:** Q1 2026 (January-March)

---

### v1.2 (Q2 2026) - Performance & Features

**Focus:** Performance optimizations and advanced features

**Features:**
- ♻️ **Built-in Retry Logic** - Configurable retry with exponential backoff
- 🚦 **Rate Limit Tracking** - Automatic rate limit monitoring and throttling
- 🔀 **Circuit Breaker Pattern** - Prevent cascading failures in streaming
- 💾 **Request Caching** - Cache account info, balances, symbol searches
- 🔗 **Connection Pooling** - HTTP connection reuse for better performance
- 📊 **Stream Health Metrics** - Enhanced stream monitoring and diagnostics
- 🎯 **Multi-Account API** - Better multi-account management

**Performance:**
- 30-50% faster for repeated requests (caching)
- Smarter retry logic (saves API quota)
- Better connection management

**Reliability:**
- Circuit breaker prevents runaway errors
- Rate limit auto-throttling
- Enhanced stream recovery

**Timeline:** Q2 2026 (April-June)

---

### v1.3 (Q3 2026) - Advanced Orders

**Focus:** Advanced order types and trading features

**Features:**
- 📈 **Advanced Order Types** - More conditional order patterns
- 🎯 **Order Templates** - Pre-configured order templates
- 📊 **Options Strategies** - Iron condors, spreads, straddles
- 📉 **Advanced Stops** - Chandelier stops, ATR-based stops
- 🔄 **Order Modification Enhancements** - Easier order updates
- 📱 **Notification System** - Order fills, position changes

**Timeline:** Q3 2026 (July-September)

---

### v2.0 (Q4 2026) - Async & Performance

**Focus:** Native async support and major performance improvements

**Breaking Changes:**
- Async-first API (sync methods deprecated)
- Minimum Python version: 3.10
- New import structure (backward compatibility maintained)

**Features:**
- ⚡ **Native Async Support** - httpx or aiohttp for async I/O
- 🌐 **WebSocket Support** - Native WebSocket (if TradeStation adds it)
- 🔗 **Connection Pooling** - Persistent connections
- 📊 **Performance Metrics** - Built-in performance monitoring
- 🎯 **Batch Operations** - Batch multiple API calls
- 💾 **Advanced Caching** - Redis/memcached support

**Performance Targets:**
- 3-5x faster API calls (connection pooling)
- 10x better concurrency (native async)
- 50% lower latency (WebSocket)

**Migration:**
- Detailed migration guide from v1.x
- Compatibility shim for gradual migration
- Deprecation warnings 6 months before removal

**Timeline:** Q4 2026 (October-December)

---

## Feature Requests & Community Input

### Most Requested Features

**From GitHub Issues:**
1. Token encryption (v1.1) ✅ Planned
2. Built-in retry logic (v1.2) ✅ Planned
3. Async support (v2.0) ✅ Planned
4. Better error messages (v1.1) ✅ Planned
5. Options trading examples (v1.3) ✅ Planned

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
| v1.1.0 | Q1 2026 | 📋 Planned | Security & reliability |
| v1.2.0 | Q2 2026 | 📋 Planned | Performance & features |
| v1.3.0 | Q3 2026 | 📋 Planned | Advanced orders |
| v2.0.0 | Q4 2026 | 📋 Planned | Async & performance |

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

We'll provide **at least 6 months notice** before ending support for any version.

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

**Last Updated:** 2025-12-07  
**Current Version:** 1.0.0  
**Next Release:** v1.1.0 (Q1 2026)

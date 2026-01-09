---
version: 1.2
lastUpdated: 12-29-2025 12:52:55 EST
type: Model Reference
status: Active
description: Complete documentation for all Pydantic models used in the SDK
---

# Models Documentation


## Model Documentation

This section contains complete documentation for all Pydantic models used in the TradeStation SDK.

### Model Overview

All models are documented in the [Models Overview](README.md) which includes:
- Model coverage analysis
- Field mapping documentation
- Data collection status
- Missing fields identification

### Model Categories

Models are organized by domain:
- **Order Models** - Order requests, responses, and nested components
- **Streaming Models** - HTTP Streaming API response models
  - `QuoteStream`, `OrderStream`, `PositionStream`, `BalanceStream`, `BarStream`
- **Market Data Models (REST)** - Historical/lookup responses
  - `BarResponse`, `BarsResponse` (GET /v3/marketdata/barcharts/{symbol}`)
- **Symbol Models** - Symbol metadata/search
  - `SymbolDetail`, `SymbolDetailsResponse`, `SymbolSearchResponse`
- **Option Models** - Option metadata/analytics
  - `OptionExpirationsResponse`, `OptionStrikesResponse`, `OptionRiskRewardResponse`, `OptionSpreadType`, `OptionSpreadTypesResponse`
- **Account Models** - Account and balance models
- **Position Models** - Position models
- **Quote Models** - Quote snapshot models

### Quick Reference

**Looking for a specific model?**
- See [Models Overview](README.md) - Complete model list and field coverage

**Understanding model structure?**
- Review [Models Source Code](../../models/) - Implementation with docstrings

**Using models in code?**
- Check [API Reference](../api/reference.md) - Methods that return/accept models
- See [Usage Examples](../guides/usage-examples.md) - Code examples

---

## Related Documentation

- [Models Source Code](../../models/) - Complete model implementations
- [Models README](../../models/README.md) - Models directory overview with usage examples
- [API Reference](../api/reference.md) - API methods using these models

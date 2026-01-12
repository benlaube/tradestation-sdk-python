---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:33 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK Models

Pydantic models for TradeStation API requests and responses. These models ensure type safety, validation, and complete data capture from the TradeStation API.

## Overview

This directory contains Pydantic models organized by domain:

- **Orders** (`orders.py`) - Order requests, responses, and nested order components
- **Order Executions** (`order_executions.py`) - Order execution (fill) models
- **Streaming** (`streaming.py`) - HTTP Streaming API models (quotes, orders, positions, balances)
- **Accounts** (`accounts.py`, `accounts_list.py`, `accounts_rest.py`) - Account models and balances
- **Positions** (`positions.py`) - Position models
- **Quotes** (`quotes.py`) - Quote snapshot models

## Model Categories

### Order Models

**File:** `orders.py`

Models for placing and managing orders:

- `TradeStationOrderRequest` - Single order placement request
- `TradeStationOrderGroupRequest` - Group order request (OCO/Bracket orders)
- `TradeStationOrderResponse` - Complete order response (30+ fields)
- `TradeStationOrderGroupResponse` - Group order response
- `TradeStationOrderLeg` - Multi-leg order components
- `TradeStationConditionalOrder` - Conditional order relationships
- `TradeStationTrailingStop` - Trailing stop parameters
- `TradeStationMarketActivationRule` - Market-based activation rules
- `TradeStationTimeActivationRule` - Time-based activation rules

**Usage:**
```python
from models.orders import TradeStationOrderRequest, TradeStationOrderResponse

# Create order request
order = TradeStationOrderRequest(
    AccountID="SIM123456",
    Symbol="MNQZ25",
    Quantity=2,
    OrderType="Market",
    BuyOrSell="Buy"
)

# Parse order response
response = TradeStationOrderResponse(**api_response)
```

### Order Execution Models

**File:** `order_executions.py`

Models for order executions (fills):

- `TradeStationExecutionResponse` - Execution details including price, quantity, fees

**Usage:**
```python
from models.order_executions import TradeStationExecutionResponse

execution = TradeStationExecutionResponse(**execution_data)
print(f"Filled {execution.Quantity} at {execution.Price}")
```

### Streaming Models

**File:** `streaming.py`

Models for HTTP Streaming API responses (NDJSON format):

- `QuoteStream` - Real-time quote data with 50+ fields
- `OrderStream` - Real-time order updates
- `PositionStream` - Real-time position updates
- `BalanceStream` - Real-time balance updates
- `StreamStatus` - Stream connection status
- `Heartbeat` - Keep-alive messages
- `StreamErrorResponse` - Error messages from stream
- `MarketFlags` - Market-specific flags (halted, delayed, etc.)

**Usage:**
```python
from models.streaming import QuoteStream, OrderStream

# Parse streaming quote
quote = QuoteStream(**quote_data)
print(f"{quote.Symbol}: {quote.Last}")

# Parse streaming order update
order_update = OrderStream(**order_data)
```

### Account Models

**Files:** `accounts.py`, `accounts_list.py`, `accounts_rest.py`

Models for account information and balances:

- `AccountSummary` - Account summary information
- `BalanceDetail` - Detailed balance information
- `AccountBalancesResponse` - Account balances response
- `BODBalance` - Beginning of day balance
- `BODBalancesResponse` - BOD balances response
- `AccountsListResponse` - List of all accounts

**Usage:**
```python
from models.accounts import AccountSummary, AccountBalancesResponse
from models.accounts_list import AccountsListResponse

# Get account summary
summary = AccountSummary(**account_data)

# Get balances
balances = AccountBalancesResponse(**balances_data)

# List all accounts
accounts = AccountsListResponse(**accounts_list_data)
```

### Position Models

**File:** `positions.py`

Models for position information:

- `PositionResponse` - Single position details
- `PositionsResponse` - Multiple positions response

**Usage:**
```python
from models.positions import PositionResponse, PositionsResponse

# Single position
position = PositionResponse(**position_data)

# Multiple positions
positions = PositionsResponse(**positions_data)
```

### Quote Models

**File:** `quotes.py`

Models for quote snapshots (REST API):

- `QuoteSnapshot` - Single quote snapshot
- `QuotesResponse` - Multiple quotes response

**Usage:**
```python
from models.quotes import QuoteSnapshot, QuotesResponse

# Single quote
quote = QuoteSnapshot(**quote_data)

# Multiple quotes
quotes = QuotesResponse(**quotes_data)
```

## Complete Model List

### Exported Models

All models are exported from `models/__init__.py`:

**Order Models:**
- `TradeStationOrderRequest`
- `TradeStationOrderGroupRequest`
- `TradeStationOrderResponse`
- `TradeStationOrderGroupResponse`
- `TradeStationOrderLeg`
- `TradeStationConditionalOrder`
- `TradeStationMarketActivationRule`
- `TradeStationTimeActivationRule`
- `TradeStationTrailingStop`

**Order Execution Models:**
- `TradeStationExecutionResponse`

**Streaming Models:**
- `QuoteStream`
- `OrderStream`
- `PositionStream`
- `BalanceStream`
- `StreamStatus`
- `Heartbeat`
- `StreamErrorResponse`
- `MarketFlags`

**Account Models:**
- `AccountSummary`
- `BalanceDetail`
- `AccountBalancesResponse`
- `BODBalance`
- `BODBalancesResponse`
- `AccountsListResponse`

**Position Models:**
- `PositionResponse`
- `PositionsResponse`

**Quote Models:**
- `QuoteSnapshot`
- `QuotesResponse`

## Data Coverage

### Complete Field Capture

These models are designed to capture **ALL** fields from the TradeStation API:

- ✅ **Order Response:** 30+ fields (including group_id, conditional_orders, commission_fee, etc.)
- ✅ **Quote Stream:** 50+ fields (including 52-week highs/lows, market flags, restrictions)
- ✅ **Order Stream:** Complete order state with all nested components
- ✅ **Position Stream:** Full position details with P&L, unrealized gains, etc.

### Missing Fields Detection

If you find missing fields:
1. Check `docs/models/README.md` for field coverage analysis
2. Add the field to the appropriate model
3. Update `docs/models/README.md` with the new field
4. Test with real API responses

## Dependencies

- **pydantic** - Model validation and serialization
- **typing** - Type hints for optional fields

## Related Documentation

- 📚 **[docs/models/README.md](../../docs/models/README.md)** - Complete model documentation and field coverage analysis
- 📖 **[docs/api/reference.md](../../docs/api/reference.md)** - API reference with model usage examples
- 💡 **[docs/guides/usage-examples.md](../../docs/guides/usage-examples.md)** - Code examples using models
- 🏗️ **[models/__init__.py](__init__.py)** - Model exports and organization

## Model Design Principles

1. **Complete Field Capture** - Models include all fields from TradeStation API responses
2. **Type Safety** - All fields are typed with Pydantic for validation
3. **Optional Fields** - Fields that may be missing are marked as optional (`| None`)
4. **Field Descriptions** - All fields have descriptions for documentation
5. **Nested Models** - Complex structures use nested Pydantic models
6. **API Alignment** - Field names match TradeStation API exactly (PascalCase)

## Version

- **Version:** 1.0.0
- **Last Updated:** 2025-12-28
- **SDK Version:** See [README.md](../../README.md)

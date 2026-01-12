---
version: 1.0.0
lastUpdated: 12-29-2025 17:14:49 EST
type: Reference Material
status: Active
description: Domain-specific operation modules for TradeStation API v3
---

# Operations Subpackage

## Overview

The `operations/` subpackage contains domain-specific operation modules that implement TradeStation API v3 endpoints. Each module provides typed, mode-aware (PAPER/LIVE) methods for interacting with specific API domains.

## Module Organization

### Core Operation Modules

| Module | Purpose | Key Classes |
|--------|---------|-------------|
| `accounts.py` | Account management and balances | `AccountOperations` |
| `market_data.py` | Market data, quotes, bars, options | `MarketDataOperations` |
| `orders.py` | Order queries and history | `OrderOperations` |
| `order_executions.py` | Order placement, modification, cancellation | `OrderExecutionOperations` |
| `positions.py` | Position queries and management | `PositionOperations` |
| `streaming.py` | HTTP streaming (quotes, orders, positions) | `StreamingManager`, `WebSocketManager` |

## Module Structure

Each operation module follows a consistent pattern:

1. **Operation Class**: Main class containing domain-specific methods
2. **Mode Awareness**: All methods support `mode` parameter (PAPER/LIVE)
3. **Type Safety**: Methods use Pydantic models for request/response validation
4. **Error Handling**: Methods raise typed exceptions (`TradeStationAPIError`, etc.)
5. **HTTP Client**: All modules use `HTTPClient` from `utils.client` for network I/O

## Dependencies

### Internal Dependencies

All operation modules depend on:

- `utils.client.HTTPClient` - HTTP client for API requests
- `utils.logger.setup_logger` - Structured logging
- `config.sdk_config` - SDK configuration
- `exceptions` - Typed exception classes
- `models` - Pydantic request/response models
- `session.TokenManager` - OAuth token management (via HTTPClient)

### External Dependencies

- `requests` - HTTP library (synchronous)
- `httpx` - HTTP library (async, optional)
- `typing` - Type hints

## Usage Examples

### Direct Import (Internal Use)

```python
from operations.accounts import AccountOperations
from utils.client import HTTPClient
from session import TokenManager

# Create operation instance
token_manager = TokenManager()
client = HTTPClient(token_manager=token_manager)
account_ops = AccountOperations(client=client)

# Use operation methods
accounts = account_ops.get_accounts_list(mode="PAPER")
```

### Via SDK Class (Recommended)

```python
from tradestation_sdk import TradeStationSDK

# SDK class composes all operations
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")

# Access operations through SDK
accounts = sdk.get_accounts_list(mode="PAPER")
```

## Module Details

### `accounts.py` - Account Operations

**Purpose:** Account management, balances, and account metadata

**Key Methods:**
- `get_accounts_list()` - List all accounts
- `get_account_info()` - Get account summary
- `get_account_balances()` - Get account balances
- `get_bod_balances()` - Get beginning-of-day balances

**Dependencies:**
- `models.accounts` - Account models (AccountSummary, AccountBalancesResponse, etc.)

### `market_data.py` - Market Data Operations

**Purpose:** Market data, quotes, bars, options, and symbol information

**Key Methods:**
- `get_symbol_details()` - Get symbol information
- `get_futures_index_symbols()` - Get futures index symbols
- `get_crypto_symbol_names()` - Get crypto symbol names
- `stream_quotes()` - Stream real-time quotes
- `stream_bars()` - Stream real-time bars
- `get_option_expirations()` - Get option expiration dates
- `get_option_strikes()` - Get option strike prices
- `stream_option_chains()` - Stream option chain data

**Dependencies:**
- `models.quotes` - Quote models
- `models.symbols` - Symbol models
- `models.options` - Option models

### `orders.py` - Order Queries

**Purpose:** Query existing orders and order history

**Key Methods:**
- `get_orders()` - Get orders for account
- `get_order_by_id()` - Get specific order by ID
- `get_order_history()` - Get order history

**Dependencies:**
- `models.orders` - Order models (TradeStationOrderResponse, etc.)

### `order_executions.py` - Order Execution

**Purpose:** Place, modify, cancel, and confirm orders

**Key Methods:**
- `place_order()` - Place a new order
- `place_group_order()` - Place bracket/OCO orders
- `modify_order()` - Modify existing order
- `cancel_order()` - Cancel an order
- `confirm_order()` - Confirm order placement

**Dependencies:**
- `models.orders` - Order request/response models
- `models.order_executions` - Execution models

### `positions.py` - Position Operations

**Purpose:** Query and manage positions

**Key Methods:**
- `get_positions()` - Get all positions for account
- `get_position_by_symbol()` - Get position for specific symbol

**Dependencies:**
- `models.positions` - Position models (PositionResponse, PositionsResponse)

### `streaming.py` - HTTP Streaming

**Purpose:** Real-time data streaming via HTTP Streaming (NDJSON)

**Key Classes:**
- `StreamingManager` - Manages streaming connections
- `WebSocketManager` - WebSocket support (if available)

**Key Methods:**
- `stream_quotes()` - Stream quotes
- `stream_orders()` - Stream order updates
- `stream_positions()` - Stream position updates
- `stream_bars()` - Stream bar updates

**Dependencies:**
- `models.streaming` - Streaming models (QuoteStream, OrderStream, etc.)

## Module Dependencies Graph

```
operations/
├── accounts.py
│   └── depends on: utils.client, models.accounts
├── market_data.py
│   └── depends on: utils.client, models.quotes, models.symbols, models.options
├── orders.py
│   └── depends on: utils.client, models.orders
├── order_executions.py
│   └── depends on: utils.client, models.orders, models.order_executions
├── positions.py
│   └── depends on: utils.client, models.positions
└── streaming.py
    └── depends on: utils.client, models.streaming
```

## Adding New Operations

When adding a new operation module:

1. **Create Module File**: `operations/new_domain.py`
2. **Create Operation Class**: `class NewDomainOperations:`
3. **Add HTTPClient Dependency**: `def __init__(self, client: HTTPClient):`
4. **Implement Methods**: Follow existing pattern (mode parameter, typed exceptions)
5. **Add to Exports**: Update `operations/__init__.py`
6. **Add to SDK**: Update `__init__.py` to compose new operations
7. **Add Tests**: Create tests in `tests/test_new_domain.py`
8. **Update Documentation**: Add to API reference and function lists

## Related Documentation

- [Main README](../../README.md) - SDK overview
- [API Reference](../../docs/api/reference.md) - Complete API documentation
- [Functions List](../../docs/reference/functions-list.md) - All SDK functions
- [Utils README](../utils/README.md) - Utility modules documentation

---

## Maintenance

- Keep module structure consistent across all operations
- Document all public methods with docstrings
- Use typed exceptions for error handling
- Follow mode-aware pattern (PAPER/LIVE support)
- Update this README when adding new modules

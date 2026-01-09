---
version: 1.0.0
lastUpdated: 12-29-2025 17:18:15 EST
type: Reference Material
status: Active
description: Shared utility modules for TradeStation SDK
---

# Utils Subpackage

## Overview

The `utils/` subpackage contains shared utility modules used across the SDK. These modules provide core functionality for HTTP communication, logging, and data transformation.

## Module Organization

### Core Utility Modules

| Module | Purpose | Key Components |
|--------|---------|----------------|
| `client.py` | HTTP client for API requests | `HTTPClient`, `get_base_url()` |
| `logger.py` | Structured logging | `setup_logger()` |
| `mappers.py` | Data normalization | `normalize_*()` functions |

## Module Details

### `client.py` - HTTP Client

**Purpose:** Centralized HTTP client for all TradeStation API requests

**Key Components:**
- `HTTPClient` - Main HTTP client class
- `get_base_url()` - Get base URL for PAPER/LIVE mode

**Features:**
- Mode-aware base URL selection (PAPER vs LIVE)
- Automatic token injection from TokenManager
- Structured request/response logging
- Error parsing and typed exception raising
- Retry logic with exponential backoff
- Rate limit handling
- NDJSON HTTP streaming support
- Optional async support via httpx

**Usage:**
```python
from utils.client import HTTPClient, get_base_url
from session import TokenManager

token_manager = TokenManager()
client = HTTPClient(token_manager=token_manager)

# Make API request
response = client.get("/accounts", mode="PAPER")
```

**Dependencies:**
- `requests` - Synchronous HTTP library
- `httpx` - Async HTTP library (optional)
- `session.TokenManager` - OAuth token management
- `config.sdk_config` - SDK configuration
- `exceptions` - Typed exception classes

### `logger.py` - Logging Utilities

**Purpose:** Structured logging setup for SDK modules

**Key Components:**
- `setup_logger()` - Configure logger for module

**Features:**
- Structured logging with colorlog
- Configurable log levels
- Module-specific loggers
- Consistent log format across SDK

**Usage:**
```python
from utils.logger import setup_logger
from config import sdk_config

logger = setup_logger(__name__, sdk_config.log_level)
logger.info("Operation completed")
logger.error("Error occurred", exc_info=True)
```

**Dependencies:**
- `colorlog` - Colored logging output
- `config.sdk_config` - Log level configuration

### `mappers.py` - Data Normalization

**Purpose:** Normalize TradeStation API responses to consistent dictionary format

**Key Functions:**
- `normalize_order()` - Normalize order data
- `normalize_position()` - Normalize position data
- `normalize_quote()` - Normalize quote data
- `normalize_execution()` - Normalize execution/fill data
- `normalize_account()` - Normalize account summary
- `normalize_balances()` - Normalize balance detail
- `normalize_account_balances()` - Normalize account balances response
- `normalize_bod_balance()` - Normalize BOD balance data

**Features:**
- Converts PascalCase/camelCase to snake_case
- Handles missing/null fields gracefully
- Type conversion (string to float/int)
- Consistent output format across all data types

**Usage:**
```python
from utils.mappers import normalize_order, normalize_quote

# Normalize API response
order_data = {
    "OrderID": "12345",
    "Symbol": "MNQZ25",
    "Quantity": 2
}
normalized = normalize_order(order_data)
# Result: {"order_id": "12345", "symbol": "MNQZ25", "quantity": 2}
```

**Helper Functions:**
- `_get_value()` - Safely extract value from object (handles dict/object)
- `_to_float()` - Convert value to float safely
- `_to_int()` - Convert value to int safely

**Dependencies:**
- `config.sdk_config` - SDK configuration
- `logger` - Logging for errors

## Module Dependencies

### Internal Dependencies

```
utils/
├── client.py
│   ├── depends on: config, session, exceptions
│   └── used by: all operations modules
├── logger.py
│   ├── depends on: config
│   └── used by: all SDK modules
└── mappers.py
    ├── depends on: config, logger
    └── used by: operations modules (optional)
```

### External Dependencies

- `requests` - HTTP library (required)
- `httpx` - Async HTTP library (optional)
- `colorlog` - Colored logging (required)

## Usage Patterns

### HTTP Client Pattern

All operation modules use HTTPClient:

```python
from utils.client import HTTPClient
from session import TokenManager

class MyOperations:
    def __init__(self, client: HTTPClient):
        self.client = client

    def my_method(self, mode: str = "PAPER"):
        response = self.client.get("/endpoint", mode=mode)
        return response.json()
```

### Logging Pattern

All modules use structured logging:

```python
from utils.logger import setup_logger
from config import sdk_config

logger = setup_logger(__name__, sdk_config.log_level)

def my_function():
    logger.info("Starting operation")
    try:
        # ... operation code ...
        logger.info("Operation completed")
    except Exception as e:
        logger.error(f"Operation failed: {e}", exc_info=True)
        raise
```

### Normalization Pattern

Optional normalization for consistent data format:

```python
from utils.mappers import normalize_order

def get_order(order_id: str):
    response = self.client.get(f"/orders/{order_id}")
    order_data = response.json()

    # Optional: normalize to snake_case
    normalized = normalize_order(order_data)
    return normalized
```

## Adding New Utilities

When adding a new utility module:

1. **Create Module File**: `utils/new_utility.py`
2. **Follow Patterns**: Use existing patterns (logging, error handling)
3. **Add to Exports**: Update `utils/__init__.py`
4. **Document Dependencies**: List all dependencies in docstring
5. **Add Tests**: Create tests in `tests/test_new_utility.py`
6. **Update Documentation**: Add to this README

## Related Documentation

- [Main README](../README.md) - SDK overview
- [Operations README](../operations/README.md) - Operation modules
- [Data Transformation Guide](../docs/guides/data-transformation.md) - Mapper usage
- [API Reference](../docs/api/reference.md) - Complete API documentation

---

## Maintenance

- Keep utilities focused and reusable
- Document all public functions/classes
- Use consistent error handling patterns
- Follow logging standards across all utilities
- Update this README when adding new utilities

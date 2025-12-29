# Test Fixtures

## Metadata
- **Version:** 1.0.0
- **Last Updated:** 2025-12-29 16:26:28 EST
- **Type:** Reference Material
- **Status:** Active
- **Description:** Test fixtures and mock data for TradeStation SDK tests

---

## Overview

The `tests/fixtures/` directory contains mock data and utilities for testing the TradeStation SDK. These fixtures provide realistic mock responses matching TradeStation API v3 structure, allowing tests to run without making actual API calls.

## Module Organization

### Fixture Modules

| Module | Purpose | Key Components |
|--------|---------|----------------|
| `api_responses.py` | Mock API response data | `MOCK_*` constants |
| `mock_requests.py` | Request mocking utilities | Mock request helpers |

## Module Details

### `api_responses.py` - Mock API Responses

**Purpose:** Provides realistic mock API responses matching TradeStation API v3 structure

**Key Fixtures:**
- `MOCK_ACCOUNTS_LIST` - Mock accounts list response
- `MOCK_ACCOUNT_BALANCES` - Mock account balances response
- `MOCK_ORDER_RESPONSE` - Mock order response
- `MOCK_POSITION_RESPONSE` - Mock position response
- `MOCK_QUOTE_SNAPSHOT` - Mock quote snapshot
- `MOCK_EXECUTION_RESPONSE` - Mock execution response
- Additional mocks for all major API endpoints

**Structure:**
All mock responses are dictionaries matching actual TradeStation API v3 response formats:
- PascalCase field names (matching API)
- Realistic data values
- Complete response structures
- Error response formats

**Usage:**
```python
from tests.fixtures.api_responses import MOCK_ACCOUNTS_LIST, MOCK_ORDER_RESPONSE

def test_get_accounts():
    # Use mock response in test
    accounts = MOCK_ACCOUNTS_LIST
    assert len(accounts["Accounts"]) == 2
    assert accounts["Accounts"][0]["AccountID"] == "SIM123456"
```

### `mock_requests.py` - Request Mocking Utilities

**Purpose:** Utilities for mocking HTTP requests in tests

**Key Components:**
- Mock request helpers
- Response patching utilities
- Error simulation helpers

**Usage:**
```python
from tests.fixtures.mock_requests import mock_get_response

def test_api_call(mocker):
    # Mock API response
    mock_response = mock_get_response(MOCK_ACCOUNTS_LIST)
    mocker.patch('requests.get', return_value=mock_response)
    
    # Test code that makes API call
    result = sdk.get_accounts_list()
    assert result is not None
```

## Fixture Organization

### Response Types

Fixtures are organized by API domain:

1. **Account Fixtures**
   - Account lists
   - Account balances
   - BOD balances

2. **Order Fixtures**
   - Order responses
   - Order groups
   - Order confirmations

3. **Position Fixtures**
   - Position responses
   - Position lists

4. **Market Data Fixtures**
   - Quote snapshots
   - Bar data
   - Symbol details

5. **Execution Fixtures**
   - Execution responses
   - Fill data

6. **Streaming Fixtures**
   - Stream messages
   - Heartbeat messages
   - Error responses

## Adding New Fixtures

When adding new fixtures:

1. **Match API Structure**: Ensure mock data matches actual API response format
2. **Use Realistic Data**: Use realistic values (not "test", "123", etc.)
3. **Include All Fields**: Include all fields from actual API responses
4. **Document Purpose**: Add docstring explaining what the fixture represents
5. **Update Tests**: Use new fixtures in relevant tests

**Example:**
```python
# In api_responses.py
MOCK_NEW_ENDPOINT_RESPONSE = {
    "Field1": "value1",
    "Field2": 123,
    "Field3": {
        "NestedField": "nested_value"
    }
}
"""
Mock response for /new/endpoint endpoint.

Matches TradeStation API v3 response structure.
Used in tests/test_new_feature.py
"""
```

## Fixture Usage Patterns

### Direct Import

```python
from tests.fixtures.api_responses import MOCK_ACCOUNTS_LIST

def test_function():
    data = MOCK_ACCOUNTS_LIST
    # Use mock data
```

### With Patching

```python
import pytest
from unittest.mock import Mock
from tests.fixtures.api_responses import MOCK_ORDER_RESPONSE

def test_order_placement(mocker):
    mock_response = Mock()
    mock_response.json.return_value = MOCK_ORDER_RESPONSE
    mock_response.status_code = 200
    
    mocker.patch('requests.post', return_value=mock_response)
    
    # Test order placement
    result = sdk.place_order(...)
    assert result is not None
```

### With Pydantic Models

```python
from tests.fixtures.api_responses import MOCK_ORDER_RESPONSE
from models.orders import TradeStationOrderResponse

def test_order_model():
    # Create model from mock data
    order = TradeStationOrderResponse(**MOCK_ORDER_RESPONSE)
    assert order.OrderID == MOCK_ORDER_RESPONSE["OrderID"]
```

## Best Practices

1. **Keep Fixtures Realistic**: Use realistic data that matches production API responses
2. **Update When API Changes**: Update fixtures when API structure changes
3. **Document Complex Fixtures**: Add docstrings for complex or non-obvious fixtures
4. **Organize by Domain**: Group related fixtures together
5. **Use Constants**: Export fixtures as module-level constants for easy import
6. **Test Fixtures**: Consider adding tests to verify fixture structure matches models

## Related Documentation

- [Tests README](../README.md) - Test suite overview
- [Models Documentation](../../docs/models/README.md) - Pydantic models
- [API Reference](../../docs/api/reference.md) - API response structures

---

## Maintenance

- Keep fixtures synchronized with actual API responses
- Update fixtures when API structure changes
- Add new fixtures for new API endpoints
- Remove obsolete fixtures when endpoints are deprecated
- Document fixture purpose and usage

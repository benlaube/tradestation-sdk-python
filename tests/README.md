# TradeStation SDK Test Suite

## About This Document

This document describes the **comprehensive test suite** for the TradeStation SDK. It covers test structure, running tests, coverage goals, and how to write new tests. All tests use mocked HTTP requests for fast, reliable execution.

**Use this if:** You want to run tests, understand test coverage, contribute tests, or verify SDK functionality.

**Related Documents:**
- 📖 **[README.md](../README.md)** - Complete SDK documentation
- 🤝 **[CONTRIBUTING.md](../CONTRIBUTING.md)** - Contribution guidelines (includes testing requirements)
- 📝 **[CHANGELOG.md](../CHANGELOG.md)** - Version history
- 🧪 **[docs/API_REFERENCE.md](../docs/API_REFERENCE.md)** - API reference (what's being tested)

---

## Overview

Comprehensive test suite for TradeStation SDK covering all 72 functions across 6 modules. All tests use mocked HTTP requests (no real API calls) for fast, reliable execution.

## Test Structure

### SDK Unit Tests (`src/lib/tradestation/tests/`)

Self-contained test suite that will travel with SDK when extracted to separate repo.

**Test Files:**
- `test_client.py` - HTTPClient tests (request/response logging, error handling, mode support)
- `test_session.py` - TokenManager/Session tests (token management, authentication, refresh)
- `test_accounts.py` - AccountOperations tests (4 functions)
- `test_market_data.py` - MarketDataOperations tests (16 functions)
- `test_orders.py` - OrderOperations tests (10 functions)
- `test_order_executions.py` - OrderExecutionOperations tests (18 functions)
- `test_positions.py` - PositionOperations tests (4 functions)
- `test_streaming.py` - StreamingManager tests (5 functions, async)
- `test_sdk.py` - TradeStationSDK integration tests
- `test_exceptions.py` - Exception handling tests
- `test_logging.py` - Logging verification tests
- `test_endpoints.py` - Endpoint verification tests (parametrized)

**Fixtures:**
- `conftest.py` - Pytest fixtures (token manager, HTTP client, SDK instances)
- `fixtures/api_responses.py` - Mock API response data
- `fixtures/mock_requests.py` - Request mocking utilities

### Integration Tests (`tests/lib/tradestation/`)

Tests for SDK integration with bot services.

**Test Files:**
- `test_sdk_integration.py` - SDK + bot integration tests
- `test_sdk_usage.py` - Real-world usage scenarios

## Running Tests

### Run All SDK Unit Tests
```bash
pytest src/lib/tradestation/tests/
```

### Run Integration Tests
```bash
pytest tests/lib/tradestation/
```

### Run All SDK Tests (Unit + Integration)
```bash
pytest src/lib/tradestation/tests/ tests/lib/tradestation/
```

### Run with Coverage
```bash
pytest src/lib/tradestation/tests/ --cov=src/lib/tradestation --cov-report=html
```

### Run Specific Test File
```bash
pytest src/lib/tradestation/tests/test_client.py -v
```

### Run by Marker
```bash
pytest src/lib/tradestation/tests/ -m accounts
pytest src/lib/tradestation/tests/ -m orders
pytest src/lib/tradestation/tests/ -m market_data
pytest src/lib/tradestation/tests/ -m streaming
pytest src/lib/tradestation/tests/ -m unit
pytest src/lib/tradestation/tests/ -m integration
```

### Run Specific Test
```bash
pytest src/lib/tradestation/tests/ -k "test_place_order"
```

### Skip Slow Tests
```bash
pytest src/lib/tradestation/tests/ -m "not slow"
```

## Test Markers

- `@pytest.mark.unit` - Unit tests (mocked, in SDK directory)
- `@pytest.mark.integration` - Integration tests (in root tests directory)
- `@pytest.mark.slow` - Slow tests (streaming, etc.)
- `@pytest.mark.accounts` - Account module tests
- `@pytest.mark.orders` - Order module tests
- `@pytest.mark.market_data` - Market data tests
- `@pytest.mark.streaming` - Streaming tests
- `@pytest.mark.sdk` - SDK-specific tests

## Test Coverage Goals

- ✅ 90%+ code coverage for SDK modules
- ✅ 100% function coverage (all 72 functions tested)
- ✅ 100% endpoint verification (all endpoints verified)
- ✅ 100% error path coverage (all exception types tested)
- ✅ 100% logging verification (all log paths tested)

## Features Tested

### Core Components
- ✅ HTTPClient: Request/response logging, error handling, mode support
- ✅ TokenManager: Token management, authentication, refresh
- ✅ Session: OAuth flow (mocked), token storage

### Operation Modules
- ✅ AccountOperations: Account info, balances (4 functions)
- ✅ MarketDataOperations: Historical bars, quotes, symbols (16 functions)
- ✅ OrderOperations: Order queries, history (10 functions)
- ✅ OrderExecutionOperations: Order placement, modification, cancellation (18 functions)
- ✅ PositionOperations: Position queries, flattening (4 functions)
- ✅ StreamingManager: HTTP streaming for quotes, orders, positions (5 functions)

### SDK Integration
- ✅ TradeStationSDK: Initialization, function delegation, workflows
- ✅ Exception Handling: All exception types, error details, error parsing
- ✅ Logging: Request/response logging, log context, sanitization

### Endpoint Verification
- ✅ All 72 functions verify correct endpoint is called
- ✅ HTTP method verification (GET, POST, PUT, DELETE)
- ✅ Request/response validation

## Mock Responses

All mock responses are in `fixtures/api_responses.py` and match TradeStation API v3 structure:
- Account responses (list, balances, BOD)
- Market data responses (bars, quotes, symbols)
- Order responses (placement, cancellation, modification)
- Position responses
- Streaming responses (newline-delimited JSON)
- Error responses (401, 429, 400, 500)

## Writing New Tests

### Example Test Structure

```python
@pytest.mark.unit
@pytest.mark.accounts
class TestAccountOperationsGetAccountInfo:
    """Tests for get_account_info method."""
    
    def test_get_account_info_success(self, mock_http_client, mocker):
        """Test get_account_info returns account information."""
        mock_request = mocker.patch.object(
            mock_http_client,
            "make_request",
            return_value=api_responses.MOCK_ACCOUNTS_LIST
        )
        
        account_ops = AccountOperations(mock_http_client, default_mode="PAPER")
        result = account_ops.get_account_info("PAPER")
        
        # Verify endpoint was called
        mock_request.assert_called_once_with("GET", "brokerage/accounts", mode="PAPER")
        
        # Verify result structure
        assert "account_id" in result
```

### Using Fixtures

- `mock_http_client` - HTTPClient with mocked requests
- `mock_token_manager` - TokenManager with valid tokens
- `sdk_instance` - TradeStationSDK with all dependencies mocked
- `sample_account_data` - Sample account response
- `sample_order_data` - Sample order response
- Trading mode fixtures: `paper_mode`, `live_mode`, `trading_mode` (parametrized)

### Mocking HTTP Requests

```python
mocker.patch.object(
    mock_http_client,
    "make_request",
    return_value=api_responses.MOCK_ACCOUNTS_LIST
)
```

### Verifying Endpoints

```python
call_args = mock_http_client.make_request.call_args
assert "brokerage/accounts" in call_args[0][1]  # Endpoint
assert call_args[0][0] == "GET"  # Method
```

## Notes

- All tests use mocked HTTP requests (no real API calls)
- OAuth flow is mocked to avoid browser interaction
- Streaming tests use async/await with `@pytest.mark.asyncio`
- Tests run in < 30 seconds (all mocked)
- Coverage reports available via `--cov` flag

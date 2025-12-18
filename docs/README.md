# TradeStation SDK - Technical Documentation

## About This Document

This document provides **comprehensive technical documentation** for the TradeStation SDK service layer. It covers architecture, module descriptions, data flow, limitations, and usage examples from a technical implementation perspective.

**Use this if:** You want to understand the SDK's internal architecture, module structure, or technical implementation details.

**Related Documents:**
- 📖 **[README.md](../README.md)** - Main SDK documentation (user-facing)
- 🏗️ **[docs/TRADESTATIONSDK_ARCHITECTURE.md](TRADESTATIONSDK_ARCHITECTURE.md)** - SDK architecture diagrams
- 📚 **[docs/API_REFERENCE.md](API_REFERENCE.md)** - Complete API reference
- 💡 **[docs/SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md)** - Usage examples
- ⚠️ **[LIMITATIONS.md](../LIMITATIONS.md)** - Known constraints

## Metadata

- **Status:** Active
- **Created:** 11-26-2025
- **Last Updated:** 12-05-2025 14:21:15 EST
- **Version:** 1.0.0
- **Description:** Comprehensive documentation for the TradeStation API Service, including overview, limitations, technical breakdown, usage examples, and future improvements
- **Type:** Service Documentation - Technical reference for developers using the TradeStation API Service
- **Applicability:** When understanding service capabilities, limitations, technical architecture, or implementing TradeStation API integrations
- **Dependencies:**
  - [`../README.md`](../README.md) - Main SDK README
  - [`API_REFERENCE.md`](./API_REFERENCE.md) - Complete API reference
  - [`SDK_USAGE_EXAMPLES.md`](./SDK_USAGE_EXAMPLES.md) - Usage examples
- **How to Use:** Reference this document to understand service architecture, limitations, technical details, and usage patterns

---

## A. Overview

The TradeStation API Service is a comprehensive Python client for interacting with the TradeStation REST API v3. It provides a unified interface for authentication, account management, market data retrieval, position tracking, order execution, and real-time streaming.

### Core Responsibilities

- **Authentication**: OAuth2 Authorization Code flow with automatic token refresh for both PAPER and LIVE trading modes
- **Account Operations**: Retrieve account information, balances, and multi-account support
- **Market Data**: Fetch historical bars, search symbols, and stream real-time quotes
- **Position Management**: Query positions and flatten positions (close all or specific symbol)
- **Order Execution**: Place, cancel, modify orders with support for Market, Limit, Stop, StopLimit, and TrailingStop order types
- **Real-Time Streaming**: HTTP streaming for quotes, orders, and positions (with optional WebSocket SDK support)

### Inputs

- **Configuration**: OAuth credentials (client_id, client_secret, redirect_uri) from environment variables
- **Trading Mode**: PAPER (simulator) or LIVE (production) - defaults from `TRADING_MODE` environment variable
- **API Requests**: Symbol strings, order parameters, account IDs, date ranges, etc.

### Outputs

- **Account Data**: Account information, balances, equity, buying power, P&L
- **Market Data**: Historical bars (OHLCV), symbol search results, real-time quotes
- **Position Data**: Current positions, position quantities, position updates
- **Order Data**: Order IDs, order status, execution details, order history
- **Streaming Data**: Real-time quote updates, order updates, position updates

## B. Out-of-Scope

This service does **NOT** handle:

- **Strategy Logic**: Trading strategies, signal generation, or entry/exit rules (handled by `src/strategy/`)
- **Risk Management**: Stop-loss calculations, position sizing, risk limits (handled by `config/risk_config.py`)
- **Data Persistence**: Database operations, trade logging, historical data storage (handled by `src/services/supabase/`)
- **Bot Orchestration**: Main trading loop, decision-making, state management (handled by `src/core/bot.py`)
- **UI/Dashboard**: Web interfaces, visualization, user interactions (handled by `frontend/` and `src/api/`)
- **Order Validation**: Pre-trade checks, margin validation, symbol validation (handled by `src/services/trade_service.py`)
- **Webhook Handling**: External webhook endpoints, callback processing (handled by `src/api/`)
- **Backtesting**: Historical strategy testing, performance analysis (not implemented)

## C. Limitations

### Current Constraints

1. **Token Storage**: Tokens are stored in plain JSON files (`logs/tokens_paper.json`, `logs/tokens_live.json`). Not encrypted at rest.

2. **OAuth Port Conflicts**: OAuth callback server requires port 8888 (or configured redirect URI port). If port is in use, authentication fails. Manual port cleanup may be required.

3. **HTTP Streaming Limitations**:
   - No automatic reconnection on stream failures
   - Stream errors may not be gracefully handled in all edge cases
   - No backpressure handling for high-frequency quote streams

4. **WebSocket SDK Dependency**: WebSocket features require optional `tradestation` SDK installation. Service degrades gracefully if SDK unavailable, but streaming methods may be limited.

5. **Account ID Resolution**: If `TRADESTATION_ACCOUNT_ID` not set, service queries API and selects first account (or first futures account). Multi-account scenarios may need explicit account IDs.

6. **Order History Date Requirements**: TradeStation API requires `startDate` parameter. Service defaults to last 7 days if not provided. Maximum 1000 orders per request.

7. **Bar Data Intervals**: TradeStation API only supports minute-based intervals (1, 2, 5, etc.). Second-based intervals (30S, 60S) return "Invalid interval for unit" errors.

8. **Trailing Stop Units**: `trail_amount` for TrailingStop orders is in price units (points), not dollar amounts. For MNQ: 1 point = $2.00. This may be confusing for users.

9. **Error Handling**: Some API errors return generic messages. Detailed error parsing may be incomplete for edge cases.

10. **Mode Switching**: Switching between PAPER and LIVE modes requires separate authentication. Tokens are stored separately but mode switching mid-session may cause confusion.

### Dependency Risks

- **requests Library**: Required for all HTTP operations. Network timeouts default to 10s (30s for orders). No retry logic built-in.
- **tradestation SDK**: Optional dependency. If missing, WebSocket session creation fails silently.
- **Python Version**: Requires Python 3.10+ (based on type hints and async support).

### Required Configuration

**Environment Variables** (via `config/secrets.py`):
- `TRADESTATION_CLIENT_ID` (required)
- `TRADESTATION_CLIENT_SECRET` (required)
- `TRADESTATION_REDIRECT_URI` (defaults to `http://localhost:8888/callback`)
- `TRADESTATION_ACCOUNT_ID` (optional - will query API if not provided)
- `TRADING_MODE` (required: `PAPER` or `LIVE`, defaults to `PAPER`)
- `LOG_LEVEL` (optional, defaults to `INFO`)

**Token Files** (auto-created):
- `logs/tokens_paper.json` (PAPER mode tokens)
- `logs/tokens_live.json` (LIVE mode tokens)

## D. Future Improvements

Based on current architecture patterns:

1. **Token Encryption**: Encrypt tokens at rest using system keychain or encrypted storage.

2. **Automatic Reconnection**: Implement exponential backoff and automatic reconnection for HTTP streaming connections.

3. **Request Retry Logic**: Add configurable retry logic with exponential backoff for transient API failures.

4. **Rate Limiting**: Implement rate limit tracking and throttling to respect TradeStation API limits.

5. **Connection Pooling**: Use `requests.Session` for connection pooling and improved performance.

6. **Async HTTP Client**: Migrate to `httpx` or `aiohttp` for native async support (currently uses threading for async streaming).

7. **WebSocket Native Implementation**: Implement native WebSocket support without SDK dependency for better control.

8. **Multi-Account Management**: Add explicit account selection and multi-account operation support.

9. **Order State Machine**: Implement order state tracking and status polling for better order lifecycle management.

10. **Streaming Backpressure**: Add buffering and backpressure handling for high-frequency quote streams.

11. **Error Classification**: Categorize API errors (authentication, rate limit, validation, server) for better error handling.

12. **Token Refresh Proactive**: Refresh tokens proactively before expiration (currently refreshes on-demand).

13. **Request/Response Caching**: Add optional caching for account info, symbol search, and other read-heavy operations.

14. **Streaming Metrics**: Add metrics for stream health (latency, message rate, reconnection count).

## E. Technical Breakdown

### Directory Structure

```
src/services/tradestation/
├── __init__.py          # Main TradeStationAPI orchestrator class
├── auth.py              # TokenManager, OAuthCallbackHandler
├── client.py            # BaseAPIClient, HTTP request handling
├── accounts.py          # AccountOperations
├── market_data.py       # MarketDataOperations
├── orders.py            # OrderOperations
├── positions.py         # PositionOperations
└── streaming.py        # StreamingManager (HTTP streaming + SDK Session support)
```

### Module Descriptions

#### `__init__.py` - TradeStationAPI
Main orchestrator class that composes all modules. Provides unified interface for all TradeStation operations. Maintains backward compatibility with existing code.

**Key Methods**:
- `authenticate(mode)` - OAuth authentication
- `get_account_info(mode)` - Account information
- `get_bars(symbol, interval, unit, bars_back, mode)` - Historical bars
- `place_order(...)` - Place order
- `get_position(symbol, mode)` - Get position
- `flatten_position(symbol, mode)` - Close positions

#### `auth.py` - TokenManager & OAuthCallbackHandler
Handles OAuth2 Authorization Code flow, token storage, and token refresh for both PAPER and LIVE modes.

**Key Classes**:
- `TokenManager`: Manages tokens, authentication, refresh
- `OAuthCallbackHandler`: HTTP server handler for OAuth callback

**Key Methods**:
- `authenticate(mode)` - Perform OAuth flow
- `refresh_access_token(mode)` - Refresh expired tokens
- `ensure_authenticated(mode)` - Ensure valid tokens

#### `client.py` - BaseAPIClient
Base HTTP client for all API requests. Handles authentication, request/response logging, error handling, and HTTP streaming.

**Key Methods**:
- `make_request(method, endpoint, params, json_data, mode)` - Make authenticated API request
- `stream_data(endpoint, params, mode)` - HTTP streaming generator

#### `accounts.py` - AccountOperations
Account-related operations: account info, balances, multi-account support.

**Key Methods**:
- `get_account_info(mode)` - Get account details
- `get_account_balances(mode, account_id)` - Get balances

#### `market_data.py` - MarketDataOperations
Market data operations: historical bars, symbol search, futures symbols, streaming quotes.

**Key Methods**:
- `get_bars(symbol, interval, unit, bars_back, mode)` - Historical bars
- `search_symbols(pattern, category, asset_type, mode)` - Symbol search
- `get_futures_index_symbols(mode)` - Futures symbols
- `stream_quotes(symbols, mode)` - Stream quotes (async)

#### `orders.py` - OrderOperations
Order execution operations: place, cancel, modify, history, executions, streaming.

**Key Methods**:
- `place_order(...)` - Place order (Market, Limit, Stop, StopLimit, TrailingStop)
- `cancel_order(order_id, mode)` - Cancel order
- `modify_order(order_id, quantity, limit_price, stop_price, mode)` - Modify order
- `get_order_history(start_date, end_date, limit, mode)` - Order history
- `get_order_executions(order_id, mode)` - Order executions
- `stream_orders(account_id, mode)` - Stream orders (async)

#### `positions.py` - PositionOperations
Position operations: query positions, flatten positions.

**Key Methods**:
- `get_position(symbol, mode)` - Get position quantity
- `get_all_positions(mode)` - Get all positions
- `flatten_position(symbol, order_operations, mode)` - Close positions
- `stream_positions(account_id, mode)` - Stream positions (async)

#### `streaming.py` - StreamingManager
HTTP streaming manager with optional SDK Session support. Acts as both the session manager and session itself.

**Key Classes**:
- `StreamingManager`: Main streaming manager (aliased as `WebSocketManager` for backward compatibility)
  - Acts as both manager and session, forwarding SDK Session attributes via `__getattr__`
  - Provides HTTP Streaming methods and manages SDK Session lifecycle internally

**Key Methods**:
- `stream_quotes(symbols, mode)` - Stream quotes via HTTP
- `stream_orders(account_id, mode)` - Stream orders via HTTP
- `stream_positions(account_id, mode)` - Stream positions via HTTP
- `session` (property) - Returns self (StreamingManager instance) or None if SDK unavailable

### Data Flow

1. **Initialization**: `TradeStationAPI()` → Creates `TokenManager`, `BaseAPIClient`, operation modules
2. **Authentication**: `authenticate()` → OAuth flow → Tokens saved to JSON files
3. **API Request**: `make_request()` → `ensure_authenticated()` → HTTP request → Response
4. **Token Refresh**: Automatic on expiration → `refresh_access_token()` → Update tokens
5. **Streaming**: `stream_data()` → Long-lived HTTP connection → Parse NDJSON → Yield data

### Environment Variables

All environment variables are loaded via `config/secrets.py`:

- `TRADESTATION_CLIENT_ID` - OAuth client ID (required)
- `TRADESTATION_CLIENT_SECRET` - OAuth client secret (required)
- `TRADESTATION_REDIRECT_URI` - OAuth redirect URI (default: `http://localhost:8888/callback`)
- `TRADESTATION_ACCOUNT_ID` - Account ID (optional)
- `TRADING_MODE` - Trading mode: `PAPER` or `LIVE` (default: `PAPER`)
- `LOG_LEVEL` - Logging level (default: `INFO`)

## F. Usage Examples

### Basic Initialization

```python
from src.services.tradestation import TradeStationAPI

# Initialize API client
api = TradeStationAPI()

# Authenticate (opens browser for OAuth)
api.authenticate()  # Uses secrets.trading_mode (PAPER or LIVE)
```

### Account Operations

```python
# Get account information
account_info = api.get_account_info()
print(f"Account ID: {account_info['account_id']}")
print(f"Account Name: {account_info['name']}")

# Get account balances
balances = api.get_account_balances()
print(f"Equity: ${balances['equity']:.2f}")
print(f"Buying Power: ${balances['buying_power']:.2f}")
```

### Market Data

```python
# Get historical bars
bars = api.get_bars("MNQZ25", interval="1", unit="Minute", bars_back=100)
for bar in bars:
    print(f"Time: {bar['Time']}, Close: {bar['Close']}")

# Search symbols
symbols = api.search_symbols(pattern="MNQ", category="Future")
for symbol in symbols:
    print(f"Symbol: {symbol['Symbol']}, Name: {symbol['Name']}")
```

### Order Operations

```python
# Place market order
order_id, status = api.place_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=1,
    order_type="Market"
)
print(f"Order ID: {order_id}, Status: {status}")

# Place limit order
order_id, status = api.place_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=1,
    order_type="Limit",
    limit_price=15000.0
)

# Place trailing stop order
order_id, status = api.place_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=1,
    order_type="TrailingStop",
    trail_amount=1.5  # 1.5 points = $3.00 for MNQ
)

# Cancel order
success, message = api.cancel_order(order_id)
print(f"Canceled: {success}, Message: {message}")

# Get order history
orders = api.get_order_history(start_date="2025-01-01", limit=50)
for order in orders:
    print(f"Order: {order['OrderID']}, Symbol: {order['Symbol']}, Status: {order['Status']}")
```

### Position Operations

```python
# Get position for symbol
position = api.get_position("MNQZ25")
print(f"Position: {position}")  # Positive = long, negative = short, 0 = flat

# Get all positions
positions = api.get_all_positions()
for pos in positions:
    print(f"Symbol: {pos['symbol']}, Quantity: {pos['quantity']}")

# Flatten specific position
flattened = api.flatten_position(symbol="MNQZ25")
for order in flattened:
    print(f"Flattened: {order['symbol']}, Order ID: {order['order_id']}")

# Flatten all positions
flattened = api.flatten_position()  # No symbol = flatten all
```

### Real-Time Streaming

```python
import asyncio

async def stream_quotes_example():
    api = TradeStationAPI()
    api.authenticate()
    
    # Stream quotes via HTTP
    async for quote in api._websocket.stream_quotes(["MNQZ25"]):
        print(f"Quote: {quote.get('Symbol')} = ${quote.get('Last')}")

# Run async stream
asyncio.run(stream_quotes_example())
```

### Mode-Specific Operations

```python
# Explicitly use PAPER mode
api.authenticate(mode="PAPER")
bars = api.get_bars("MNQZ25", "1", "Minute", mode="PAPER")

# Explicitly use LIVE mode
api.authenticate(mode="LIVE")
order_id, status = api.place_order("MNQZ25", "BUY", 1, mode="LIVE")
```

### Direct Module Access

```python
from src.services.tradestation import BaseAPIClient, TokenManager, AccountOperations

# Use modules directly (advanced)
token_manager = TokenManager(client_id, client_secret, redirect_uri)
client = BaseAPIClient(token_manager)
accounts = AccountOperations(client, account_id)

account_info = accounts.get_account_info()
```

## G. Additional Information

- **Maintainer**: Trading Bot Development Team
- **License**: (See project root LICENSE file)

---

*This README documents the TradeStation API Service as a standalone module. For integration with the full trading bot system, see the main project README.*


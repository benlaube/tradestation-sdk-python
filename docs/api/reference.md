# TradeStation SDK API Reference

## About This Document

This is the **complete API reference** for all SDK classes, methods, models, and exceptions. It provides detailed parameter descriptions, return types, usage patterns, and code examples for every function in the SDK.

**Important:** This document focuses on the **SDK's API** (the methods and classes provided by this Python SDK). For information about which TradeStation API v3 endpoints the SDK calls, see **[API_ENDPOINT_MAPPING.md](API_ENDPOINT_MAPPING.md)**.

**Use this if:** You need to look up a specific SDK function, understand parameters, see return types, or find detailed method documentation.

**Related Documents:**
- 📋 **[CHEATSHEET.md](../CHEATSHEET.md)** - Quick code snippets (faster lookup)
- 💡 **[SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md)** - Real-world usage examples
- 📚 **[API_ENDPOINT_MAPPING.md](API_ENDPOINT_MAPPING.md)** - SDK functions mapped to TradeStation API v3 endpoints (shows which API endpoints are called)
- 🧭 **[SDK_ENDPOINT_MAPPING.md](sdk_endpoints.md)** - SDK methods to TradeStation API endpoints
- 📝 **[ORDER_FUNCTIONS_REFERENCE.md](ORDER_FUNCTIONS_REFERENCE.md)** - Detailed order function documentation
- 🏗️ **[MODELS.md](MODELS.md)** - Pydantic model documentation
- 📖 **[README.md](../README.md)** - SDK overview and getting started

## Metadata

- **Status:** Active
- **Created:** 12-05-2025
- **Last Updated:** 12-29-2025 12:52:55 EST
- **Version:** 1.0.1
- **Description:** Complete API reference documentation for all SDK classes, methods, models, and exceptions with detailed parameter descriptions and usage patterns
- **Type:** API Reference - Technical reference for developers using the SDK
- **Applicability:** When implementing SDK features, understanding method signatures, or looking up specific class/method documentation
- **Dependencies:**
  - [`API_ENDPOINT_MAPPING.md`](./API_ENDPOINT_MAPPING.md) - SDK function to API endpoint mapping
  - [`ORDER_FUNCTIONS_REFERENCE.md`](./ORDER_FUNCTIONS_REFERENCE.md) - Detailed order function documentation
  - [`SDK_USAGE_EXAMPLES.md`](./SDK_USAGE_EXAMPLES.md) - Usage examples
  - [`MODELS.md`](./MODELS.md) - Model documentation
- **How to Use:** Reference this document when implementing SDK features, understanding method parameters, or looking up class/method documentation

---

---

## Table of Contents

- [TradeStationSDK](#tradestationsdk)
- [TokenManager](#tokenmanager)
- [HTTPClient](#httpclient)
- [AccountOperations](#accountoperations)
- [MarketDataOperations](#marketdataoperations)
- [OrderOperations](#orderoperations)
- [PositionOperations](#positionoperations)
- [StreamingManager](#streamingmanager)
- [Models](#models)
- [Exceptions](#exceptions)

---

## TradeStationSDK

Main SDK class providing unified interface to all TradeStation API operations.

### Initialization

```python
# Standard initialization
sdk = TradeStationSDK()

# With full request/response logging enabled
sdk = TradeStationSDK(enable_full_logging=True)

# Or set via environment variable
# export TRADESTATION_FULL_LOGGING=true
sdk = TradeStationSDK()  # Reads from environment
```

**Parameters:**
- `enable_full_logging: bool = False` - If True, logs complete request/response bodies without truncation. Useful for debugging. Can also be set via `TRADESTATION_FULL_LOGGING` environment variable.

### Properties

- `active_mode: str` - Returns "PAPER" or "LIVE" (most recent mode used)
- `client: HTTPClient` - HTTP client instance (for advanced use)
- `token_manager: TokenManager` - Token manager instance (for advanced use)
- `accounts: AccountOperations` - Account operations instance
- `market_data: MarketDataOperations` - Market data operations instance
- `orders: OrderOperations` - Order operations instance
- `positions: PositionOperations` - Position operations instance
- `streaming: StreamingManager` - Streaming manager instance
- `session: StreamingManager | None` - Streaming session (backward compatibility)

### Authentication Methods

#### `authenticate(mode: str | None = None) -> None`

Perform OAuth2 authentication. Opens browser for first-time login.

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Raises:**
- `AuthenticationError` - If authentication fails

**Example:**
```python
sdk = TradeStationSDK()
sdk.authenticate(mode="PAPER")
```

---

#### `refresh_access_token(mode: str | None = None) -> None`

Refresh access token for specified mode.

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Raises:**
- `TokenExpiredError` - If refresh token is expired
- `AuthenticationError` - If refresh fails

**Example:**
```python
sdk.refresh_access_token(mode="PAPER")
```

---

#### `ensure_authenticated(mode: str | None = None) -> None`

Ensure authenticated. Automatically refreshes token if needed.

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Raises:**
- `AuthenticationError` - If authentication fails

**Example:**
```python
sdk.ensure_authenticated(mode="PAPER")
```

---

### Account Methods

#### `get_account_info(mode: str | None = None) -> dict`

Get account information including account ID.

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict` - Account information with keys:
  - `account_id: str` - TradeStation account ID
  - `accounts: list[dict]` - List of all accounts (for multi-account support)

**Example:**
```python
account = sdk.get_account_info(mode="PAPER")
print(f"Account ID: {account['account_id']}")
```

---

#### `get_account_balances(mode: str | None = None, account_id: str | None = None) -> dict[str, Any]`

Get account balances (basic).

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`
- `account_id: str | None` - Optional account ID. If None, uses default account

**Returns:**
- `dict[str, Any]` - Balance information with keys:
  - `equity: float` - Total account equity
  - `cash_balance: float` - Available cash
  - `buying_power: float` - Total buying power
  - `day_trading_buying_power: float` - Day trading buying power
  - `margin_available: float` - Available margin
  - `margin_used: float` - Margin in use
  - `maintenance_margin: float` - Maintenance margin requirement
  - `initial_margin_requirement: float` - Initial margin requirement
  - `net_liquidation_value: float` - Net liquidation value
  - `open_pnl: float` - Open P&L
  - `realized_pnl: float` - Realized P&L
  - `unrealized_pnl: float` - Unrealized P&L
  - `currency: str` - Account currency

**Example:**
```python
balances = sdk.get_account_balances(mode="PAPER")
print(f"Equity: ${balances['equity']:.2f}")
print(f"Buying Power: ${balances['buying_power']:.2f}")
```

---

#### `get_account_balances_detailed(account_ids: str | None = None, mode: str | None = None) -> dict[str, Any]`

Get detailed account balances with BalanceDetail and CurrencyDetails.

**Parameters:**
- `account_ids: str | None` - Comma-separated account IDs or None for default
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Response with keys:
  - `Balances: list[dict]` - List of balance dictionaries with detailed information
  - `Errors: list[dict]` - List of error dictionaries (if any)

**Example:**
```python
detailed = sdk.get_account_balances_detailed(account_ids="SIM123456", mode="PAPER")
for balance in detailed["Balances"]:
    print(f"Account: {balance['AccountID']}")
    print(f"Equity: {balance['Equity']}")
```

---

#### `get_account_balances_bod(account_ids: str | None = None, mode: str | None = None) -> dict[str, Any]`

Get Beginning of Day (BOD) balances.

**Parameters:**
- `account_ids: str | None` - Comma-separated account IDs or None for default
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Response with keys:
  - `BODBalances: list[dict]` - List of BOD balance dictionaries
  - `Errors: list[dict]` - List of error dictionaries (if any)

**Example:**
```python
bod = sdk.get_account_balances_bod(account_ids="SIM123456", mode="PAPER")
```

---

### Market Data Methods

#### `get_bars(symbol: str, interval: str, unit: str, bars_back: int = 200, mode: str | None = None) -> list[dict[str, Any]]`

Get historical bar data.

**Parameters:**
- `symbol: str` - Trading symbol (e.g., "MNQZ25")
- `interval: str` - Time interval (e.g., "1", "5")
- `unit: str` - "Minute", "Daily", "Weekly", "Monthly"
- `bars_back: int` - Number of bars to fetch (default: 200)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of bar dictionaries with keys:
  - `Open: float` - Opening price
  - `High: float` - High price
  - `Low: float` - Low price
  - `Close: float` - Closing price
  - `Volume: int` - Volume
  - `Timestamp: str` - Bar timestamp

**Example:**
```python
bars = sdk.get_bars("MNQZ25", "1", "Minute", bars_back=100, mode="PAPER")
for bar in bars:
    print(f"{bar['Timestamp']}: Close={bar['Close']}, Volume={bar['Volume']}")
```

---

#### `search_symbols(pattern: str = "", category: str = "Future", asset_type: str | None = None, mode: str | None = None) -> list[dict[str, Any]]`

Search for symbols.

**Parameters:**
- `pattern: str` - Symbol pattern (e.g., "MNQ", "ES")
- `category: str` - Symbol category: "Future", "Stock", "Option" (default: "Future")
- `asset_type: str | None` - Asset type filter: "Index", "Equity", etc.
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of symbol dictionaries

**Example:**
```python
symbols = sdk.search_symbols(pattern="MNQ", category="Future", mode="PAPER")
for symbol in symbols:
    print(f"{symbol['Symbol']}: {symbol['Description']}")
```

---

#### `get_quote_snapshots(symbols: str, mode: str | None = None) -> dict[str, Any]`

Get quote snapshots for one or more symbols.

**Parameters:**
- `symbols: str` - Comma-separated symbols (e.g., "MNQZ25,ESZ25")
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Response with keys:
  - `Quotes: list[dict]` - List of quote dictionaries
  - `Errors: list[dict]` - List of error dictionaries (if any)

**Example:**
```python
quotes = sdk.get_quote_snapshots("MNQZ25,ESZ25", mode="PAPER")
for quote in quotes["Quotes"]:
    print(f"{quote['Symbol']}: Last={quote['Last']}, Bid={quote['Bid']}, Ask={quote['Ask']}")
```

---

## OrderExecutionOperations

Order execution operations handle all order placement, modification, cancellation, and execution-related operations using the `/orderexecution/` API endpoints.

**Access:** `sdk.order_executions` or via main SDK delegation methods

### Core Order Execution Methods

#### `place_order(symbol: str, side: str, quantity: int, order_type: str = "Market", limit_price: float | None = None, stop_price: float | None = None, time_in_force: str = "DAY", wait_for_fill: bool = False, trail_amount: float | None = None, trail_percent: float | None = None, mode: str | None = None) -> tuple[str | None, str]`

Place an order.

**Parameters:**
- `symbol: str` - Trading symbol
- `side: str` - "BUY" or "SELL"
- `quantity: int` - Number of contracts
- `order_type: str` - "Market", "Limit", "Stop", "StopLimit", "TrailingStop" (default: "Market")
- `limit_price: float | None` - Limit price (for Limit/StopLimit orders)
- `stop_price: float | None` - Stop price (for Stop/StopLimit orders)
- `time_in_force: str` - "DAY", "GTC", "IOC", "FOK" (default: "DAY")
- `wait_for_fill: bool` - If True, waits for fill confirmation (default: False)
- `trail_amount: float | None` - Trail amount in points (for TrailingStop orders)
- `trail_percent: float | None` - Trail percentage (for TrailingStop orders)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `tuple[str | None, str]` - (order_id, status_message)

**Raises:**
- `InvalidRequestError` - If order parameters are invalid
- `TradeStationAPIError` - If order placement fails

**Example:**
```python
order_id, status = sdk.place_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    order_type="Limit",
    limit_price=25000.00,
    mode="PAPER"
)
print(f"Order placed: {order_id}, Status: {status}")
```

---

#### `cancel_order(order_id: str, mode: str | None = None) -> tuple[bool, str]`

Cancel an order.

**Parameters:**
- `order_id: str` - TradeStation order ID
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `tuple[bool, str]` - (success, message)

**Example:**
```python
success, message = sdk.cancel_order("924243071", mode="PAPER")
if success:
    print("Order cancelled successfully")
```

---

#### `modify_order(order_id: str, quantity: int | None = None, limit_price: float | None = None, stop_price: float | None = None, mode: str | None = None) -> tuple[bool, str]`

Modify an existing order.

**Parameters:**
- `order_id: str` - TradeStation order ID
- `quantity: int | None` - New quantity (optional)
- `limit_price: float | None` - New limit price (optional)
- `stop_price: float | None` - New stop price (optional)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `tuple[bool, str]` - (success, message)

**Example:**
```python
success, message = sdk.modify_order(
    order_id="924243071",
    quantity=3,
    limit_price=25010.00,
    mode="PAPER"
)
```

---

#### `get_order_history(start_date: str | None = None, end_date: str | None = None, limit: int = 100, mode: str | None = None) -> list[dict[str, Any]]`

Get historical orders.

**Parameters:**
- `start_date: str | None` - Start date in ISO format (YYYY-MM-DD) or None for all history
- `end_date: str | None` - End date in ISO format (YYYY-MM-DD) or None for today
- `limit: int` - Maximum number of orders (default: 100, max: 1000)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of order dictionaries

**Example:**
```python
history = sdk.get_order_history(
    start_date="2025-12-01",
    end_date="2025-12-05",
    limit=100,
    mode="PAPER"
)
for order in history:
    print(f"Order {order['OrderID']}: {order['Status']}")
```

---

#### `get_order_executions(order_id: str, mode: str | None = None) -> list[dict[str, Any]]`

Get order executions (fills).

**Parameters:**
- `order_id: str` - TradeStation order ID
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of execution dictionaries with keys:
  - `ExecutionID: str` - Execution ID
  - `Symbol: str` - Trading symbol
  - `TradeAction: str` - "Buy" or "Sell"
  - `Quantity: int` - Number of contracts filled
  - `Price: float` - Fill price
  - `Commission: float` - Commission paid
  - `ExecutionTime: str` - Execution timestamp

**Example:**
```python
executions = sdk.get_order_executions("924243071", mode="PAPER")
for exec in executions:
    print(f"Fill: {exec['Quantity']} @ ${exec['Price']:.2f}")
```

---

#### `confirm_order(symbol: str, side: str, quantity: int, order_type: str = "Market", limit_price: float | None = None, stop_price: float | None = None, time_in_force: str = "DAY", mode: str | None = None) -> dict[str, Any]`

Confirm an order (pre-flight check) to get estimated cost and commission.

**Parameters:**
- Same as `place_order()`

**Returns:**
- `dict[str, Any]` - Confirmation details (EstimatedCost, EstimatedCommission, etc.)

**Example:**
```python
confirmation = sdk.confirm_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    order_type="Limit",
    limit_price=25000.00,
    mode="PAPER"
)
print(f"Estimated cost: {confirmation.get('EstimatedCost')}")
```

---

#### `confirm_group_order(group_type: str, orders: list[dict[str, Any]], mode: str | None = None) -> dict[str, Any]`

Confirm a group order (OCO/Bracket) before placement.

**Parameters:**
- `group_type: str` - "OCO", "BRK", or "NORMAL"
- `orders: list[dict[str, Any]]` - List of order dictionaries
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Confirmation details including estimated costs

**Example:**
```python
confirmation = sdk.confirm_group_order("BRK", orders, mode="PAPER")
```

---

#### `place_group_order(group_type: str, orders: list[dict[str, Any]], mode: str | None = None) -> dict[str, Any]`

Place a group order (OCO/Bracket) - low-level method.

**Parameters:**
- `group_type: str` - "OCO", "BRK", or "NORMAL"
- `orders: list[dict[str, Any]]` - List of order dictionaries (see `TradeStationOrderRequest`)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Group order response with keys:
  - `GroupID: str` - Group order ID
  - `GroupName: str` - Group order name
  - `Type: str` - Group type
  - `Orders: list[dict]` - List of order responses with OrderIDs

**Example:**
```python
bracket_orders = [
    {
        "AccountID": "SIM123456",
        "Symbol": "MNQZ25",
        "TradeAction": "Buy",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": "25000.00",
        "TimeInForce": {"Duration": "DAY"}
    },
    # ... profit target and stop loss orders
]
result = sdk.place_group_order("BRK", bracket_orders, mode="PAPER")
```

---

#### `get_activation_triggers(mode: str | None = None) -> list[dict[str, Any]]`

Get available activation trigger keys for conditional orders.

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of trigger dictionaries with Key, Name, Description

**Example:**
```python
triggers = sdk.get_activation_triggers(mode="PAPER")
for trigger in triggers:
    print(f"{trigger['Key']}: {trigger['Name']}")
```

---

#### `get_routes(mode: str | None = None) -> list[dict[str, Any]]`

Get available routing options for order execution.

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of route dictionaries

**Example:**
```python
routes = sdk.get_routes(mode="PAPER")
```

---

### Convenience Functions

#### `place_limit_order(symbol: str, side: str, quantity: int, limit_price: float, time_in_force: str = "DAY", mode: str | None = None) -> tuple[str | None, str]`

Place a limit order (convenience wrapper around `place_order()`).

**Parameters:**
- `symbol: str` - Trading symbol
- `side: str` - "BUY" or "SELL"
- `quantity: int` - Number of contracts
- `limit_price: float` - Limit price
- `time_in_force: str` - "DAY", "GTC", "IOC", "FOK" (default: "DAY")
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `tuple[str | None, str]` - (order_id, status_message)

**Example:**
```python
order_id, status = sdk.place_limit_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    limit_price=25000.00,
    mode="PAPER"
)
```

---

#### `place_stop_order(symbol: str, side: str, quantity: int, stop_price: float, time_in_force: str = "DAY", mode: str | None = None) -> tuple[str | None, str]`

Place a stop order (convenience wrapper around `place_order()`).

**Parameters:**
- `symbol: str` - Trading symbol
- `side: str` - "BUY" or "SELL"
- `quantity: int` - Number of contracts
- `stop_price: float` - Stop price
- `time_in_force: str` - "DAY", "GTC", "IOC", "FOK" (default: "DAY")
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `tuple[str | None, str]` - (order_id, status_message)

**Example:**
```python
order_id, status = sdk.place_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    stop_price=24900.00,
    mode="PAPER"
)
```

---

#### `place_stop_limit_order(symbol: str, side: str, quantity: int, limit_price: float, stop_price: float, time_in_force: str = "DAY", mode: str | None = None) -> tuple[str | None, str]`

Place a stop-limit order (convenience wrapper around `place_order()`).

**Parameters:**
- `symbol: str` - Trading symbol
- `side: str` - "BUY" or "SELL"
- `quantity: int` - Number of contracts
- `limit_price: float` - Limit price
- `stop_price: float` - Stop price
- `time_in_force: str` - "DAY", "GTC", "IOC", "FOK" (default: "DAY")
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `tuple[str | None, str]` - (order_id, status_message)

**Example:**
```python
order_id, status = sdk.place_stop_limit_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    limit_price=24950.00,
    stop_price=24900.00,
    mode="PAPER"
)
```

---

#### `place_trailing_stop_order(symbol: str, side: str, quantity: int, trail_amount: float | None = None, trail_percent: float | None = None, time_in_force: str = "DAY", mode: str | None = None) -> tuple[str | None, str]`

Place a trailing stop order (convenience wrapper around `place_order()`).

**Parameters:**
- `symbol: str` - Trading symbol
- `side: str` - "BUY" or "SELL"
- `quantity: int` - Number of contracts
- `trail_amount: float | None` - Trail amount in price units (points) (optional)
  - Note: For futures, this is in price units, not dollar amounts.
  - For MNQ: 1 point = $2.00, so trail_amount=1.5 means $3.00 trail
- `trail_percent: float | None` - Trail percentage (optional, e.g., 1.0 for 1%)
- `time_in_force: str` - "DAY", "GTC", "IOC", "FOK" (default: "DAY")
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `tuple[str | None, str]` - (order_id, status_message)

**Example:**
```python
# Using trail amount (points)
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # $3.00 trail for MNQ
    mode="PAPER"
)

# Using trail percentage
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_percent=1.0,  # 1% trail
    mode="PAPER"
)
```

---

#### `place_bracket_order(symbol: str, entry_side: str, quantity: int, profit_target: float, stop_loss: float, entry_price: float | None = None, entry_order_type: str = "Market", time_in_force: str = "DAY", mode: str | None = None) -> dict[str, Any]`

Place a bracket order (entry + profit target + stop-loss).

Uses the proper group order API (BRK type) to ensure orders are linked.

**Parameters:**
- `symbol: str` - Trading symbol
- `entry_side: str` - "BUY" or "SELL" for entry
- `quantity: int` - Number of contracts
- `profit_target: float` - Profit target price (limit order)
- `stop_loss: float` - Stop-loss price (stop order)
- `entry_price: float | None` - Entry limit price (None for market entry)
- `entry_order_type: str` - "Market" or "Limit" (default: "Market")
- `time_in_force: str` - "DAY", "GTC", "IOC", "FOK" (default: "DAY")
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Group order response with:
  - `GroupID: str` - Group order ID
  - `GroupName: str` - Group order name
  - `Type: str` - "BRK"
  - `Orders: list[dict]` - List of 3 order responses (entry, profit target, stop-loss) with OrderIDs

**Example:**
```python
# Bracket order: Buy 2 MNQZ25 at market, profit target at 25100, stop-loss at 24900
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,
    entry_price=None,  # Market entry
    mode="PAPER"
)

# Extract order IDs
entry_order_id = result["Orders"][0]["OrderID"]
profit_order_id = result["Orders"][1]["OrderID"]
stop_order_id = result["Orders"][2]["OrderID"]

# Bracket order with limit entry
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,
    entry_price=25000.00,  # Limit entry
    entry_order_type="Limit",
    mode="PAPER"
)
```

---

#### `place_oco_order(orders: list[dict[str, Any]], mode: str | None = None) -> dict[str, Any]`

Place an OCO (One-Cancels-Other) order (convenience wrapper).

OCO orders are a group of orders where if one fills, the others are cancelled.

**Parameters:**
- `orders: list[dict[str, Any]]` - List of 2+ order dictionaries (same format as place_order)
  - Each order dict should have: AccountID, Symbol, TradeAction, OrderType, Quantity, etc.
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Group order response with:
  - `GroupID: str` - Group order ID
  - `GroupName: str` - Group order name
  - `Type: str` - "OCO"
  - `Orders: list[dict]` - List of order responses with OrderIDs

**Example:**
```python
# OCO order: Buy if price breaks above 25010, or sell short if price breaks below 24990
oco_orders = [
    {
        "AccountID": "SIM123456",
        "Symbol": "MNQZ25",
        "TradeAction": "Buy",
        "OrderType": "StopMarket",
        "Quantity": "2",
        "StopPrice": "25010.00",
        "TimeInForce": {"Duration": "DAY"}
    },
    {
        "AccountID": "SIM123456",
        "Symbol": "MNQZ25",
        "TradeAction": "SellShort",
        "OrderType": "StopMarket",
        "Quantity": "2",
        "StopPrice": "24990.00",
        "TimeInForce": {"Duration": "DAY"}
    }
]
result = sdk.place_oco_order(oco_orders, mode="PAPER")
```

---

## OrderOperations

Order query operations handle order queries and streaming using the `/brokerage/accounts/.../orders` API endpoints.

**Access:** `sdk.orders` or via main SDK delegation methods

### Order Query Methods

#### `get_order_history(start_date: str | None = None, end_date: str | None = None, limit: int = 100, mode: str | None = None) -> list[dict[str, Any]]`

Get historical orders.

**Parameters:**
- `start_date: str | None` - Start date in ISO format (YYYY-MM-DD) or None for all history
- `end_date: str | None` - End date in ISO format (YYYY-MM-DD) or None for today
- `limit: int` - Maximum number of orders (default: 100, max: 1000)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of order dictionaries

**Example:**
```python
history = sdk.get_order_history(
    start_date="2025-12-01",
    end_date="2025-12-05",
    limit=100,
    mode="PAPER"
)
for order in history:
    print(f"Order {order['OrderID']}: {order['Status']}")
```

---

#### `get_current_orders(account_ids: str | None = None, next_token: str | None = None, mode: str | None = None) -> dict[str, Any]`

Get current/open orders.

**Parameters:**
- `account_ids: str | None` - Comma-separated account IDs or None for default
- `next_token: str | None` - Pagination token for next page
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Dictionary with Orders list, Errors list, and optional NextToken

**Example:**
```python
current = sdk.get_current_orders(account_ids="SIM123456", mode="PAPER")
for order in current["Orders"]:
    print(f"Order {order['OrderID']}: {order['Status']}")
```

---

#### `get_orders_by_ids(order_ids: str, account_ids: str | None = None, mode: str | None = None) -> dict[str, Any]`

Get specific current orders by order ID(s).

**Parameters:**
- `order_ids: str` - Comma-separated order IDs
- `account_ids: str | None` - Comma-separated account IDs or None for default
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Dictionary with Orders list and Errors list

**Example:**
```python
orders = sdk.get_orders_by_ids("924243071,924243072", mode="PAPER")
```

---

#### `get_historical_orders_by_ids(order_ids: str, account_ids: str | None = None, start_date: str | None = None, end_date: str | None = None, mode: str | None = None) -> dict[str, Any]`

Get specific historical orders by order ID(s).

**Parameters:**
- `order_ids: str` - Comma-separated order IDs
- `account_ids: str | None` - Comma-separated account IDs or None for default
- `start_date: str | None` - Start date in ISO format (YYYY-MM-DD)
- `end_date: str | None` - End date in ISO format (YYYY-MM-DD)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `dict[str, Any]` - Dictionary with Orders list and Errors list

**Example:**
```python
historical = sdk.get_historical_orders_by_ids(
    "924243071",
    start_date="2025-12-01",
    mode="PAPER"
)
```

---

#### `stream_orders(account_id: str | None = None, mode: str | None = None) -> AsyncGenerator[dict[str, Any], None]`

Stream real-time order updates.

**Parameters:**
- `account_id: str | None` - TradeStation account ID (optional)
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Yields:**
- `OrderStream` - Order update dictionaries

**Example:**
```python
async for order in sdk.streaming.stream_orders("SIM123456", mode="PAPER"):
    if "StreamStatus" in order:
        continue  # Skip control messages
    print(f"Order {order['OrderID']}: {order['Status']}")
```

---

## PositionOperations

#### `get_position(symbol: str, mode: str | None = None) -> int`

Get position quantity for a symbol.

**Parameters:**
- `symbol: str` - Trading symbol
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `int` - Position quantity (positive=long, negative=short, 0=flat)

**Example:**
```python
position = sdk.get_position("MNQZ25", mode="PAPER")
print(f"Position: {position} contracts")
```

---

#### `get_all_positions(mode: str | None = None) -> list[dict[str, Any]]`

Get all positions.

**Parameters:**
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of position dictionaries with keys:
  - `Symbol: str` - Trading symbol
  - `Quantity: int` - Position quantity

**Example:**
```python
positions = sdk.get_all_positions(mode="PAPER")
for pos in positions:
    print(f"{pos['Symbol']}: {pos['Quantity']}")
```

---

#### `flatten_position(symbol: str | None = None, mode: str | None = None) -> list[dict[str, Any]]`

Flatten position(s) (close all or specific symbol).

**Parameters:**
- `symbol: str | None` - Optional symbol to flatten. If None, flattens all positions
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Returns:**
- `list[dict[str, Any]]` - List of order dictionaries for flattening orders

**Example:**
```python
# Flatten all positions
flattened = sdk.flatten_position(mode="PAPER")

# Flatten specific symbol
flattened = sdk.flatten_position(symbol="MNQZ25", mode="PAPER")
```

---

## StreamingManager

Manages HTTP Streaming sessions for real-time data.

### Methods

#### `stream_quotes(symbols: list[str], mode: str | None = None) -> AsyncGenerator[dict[str, Any], None]`

Stream real-time quotes.

**Parameters:**
- `symbols: list[str]` - List of symbols to stream
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Yields:**
- `dict[str, Any]` - Quote dictionaries (use `QuoteStream` model for validation)

**Example:**
```python
async for quote in sdk.streaming.stream_quotes(["MNQZ25"], mode="PAPER"):
    if "StreamStatus" in quote:
        continue  # Skip control messages
    print(f"{quote['Symbol']}: Last={quote['Last']}")
```

---

#### `stream_orders(account_id: str, mode: str | None = None) -> AsyncGenerator[dict[str, Any], None]`

Stream real-time order updates.

**Parameters:**
- `account_id: str` - TradeStation account ID
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Yields:**
- `dict[str, Any]` - Order update dictionaries (use `OrderStream` model for validation)

**Example:**
```python
async for order in sdk.streaming.stream_orders("SIM123456", mode="PAPER"):
    if "StreamStatus" in order:
        continue  # Skip control messages
    print(f"Order {order['OrderID']}: {order['Status']}")
```

---

#### `stream_positions(account_id: str, mode: str | None = None) -> AsyncGenerator[dict[str, Any], None]`

Stream real-time position updates.

**Parameters:**
- `account_id: str` - TradeStation account ID
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Yields:**
- `dict[str, Any]` - Position update dictionaries (use `PositionStream` model for validation)

**Example:**
```python
async for position in sdk.streaming.stream_positions("SIM123456", mode="PAPER"):
    if "StreamStatus" in position:
        continue  # Skip control messages
    print(f"{position['Symbol']}: {position['Quantity']} @ {position['AveragePrice']}")
```

---

#### `stream_balances(account_id: str, mode: str | None = None) -> AsyncGenerator[dict[str, Any], None]`

Stream real-time account balance updates.

**Parameters:**
- `account_id: str` - TradeStation account ID
- `mode: str | None` - "PAPER" or "LIVE". Defaults to `secrets.trading_mode`

**Yields:**
- `dict[str, Any]` - Balance update dictionaries with real-time balance information

**Example:**
```python
async for balance in sdk.streaming.stream_balances("SIM123456", mode="PAPER"):
    if "StreamStatus" in balance:
        continue  # Skip control messages
    print(f"Account: {balance.get('AccountID')}")
    print(f"Equity: {balance.get('Equity')}")
    print(f"Buying Power: {balance.get('BuyingPower')}")
```

---

## Models

### Request Models

#### `TradeStationOrderRequest`

Pydantic model for order placement requests.

**Fields:**
- `AccountID: str` - TradeStation account ID
- `Symbol: str` - Trading symbol
- `TradeAction: str` - "Buy" or "Sell"
- `OrderType: str` - "Market", "Limit", "Stop", "StopLimit", "TrailingStop"
- `Quantity: str` - Number of contracts (as string)
- `LimitPrice: str | None` - Limit price (optional)
- `StopPrice: str | None` - Stop price (optional)
- `TimeInForce: dict[str, str] | None` - Time in force: `{"Duration": "DAY"|"GTC"|"IOC"|"FOK"}`
- `TrailAmount: str | None` - Trail amount in points (optional)
- `TrailPercent: str | None` - Trail percentage (optional)

**Example:**
```python
from src.lib.tradestation import TradeStationOrderRequest

order_request = TradeStationOrderRequest(
    AccountID="SIM123456",
    Symbol="MNQZ25",
    TradeAction="Buy",
    OrderType="Limit",
    Quantity="2",
    LimitPrice="25000.00",
    TimeInForce={"Duration": "DAY"}
)
```

---

### Response Models (REST API)

#### `TradeStationOrderResponse`

Complete order response model with all 30+ fields.

**Key Fields:**
- `AccountID: str` - TradeStation account ID
- `OrderID: str` - TradeStation order ID
- `Status: str | None` - Order status (OPN, ACK, FLL, CNL, REJ)
- `Legs: list[TradeStationOrderLeg] | None` - Order legs (multi-leg orders)
- `ConditionalOrders: list[TradeStationConditionalOrder] | None` - Conditional order relationships
- `GroupID: str | None` - Order group ID (for OCO/Bracket)
- `CommissionFee: str | None` - Commission fee
- `TrailingStop: TradeStationTrailingStop | None` - Trailing stop parameters

---

### Streaming Models

#### `QuoteStream`

Streaming quote response with additional fields.

**Key Fields:**
- `Symbol: str` - Trading symbol (REQUIRED)
- `Last: str | None` - Last traded price
- `Bid: str | None` - Current bid price
- `Ask: str | None` - Current ask price
- `Volume: str | None` - Daily volume
- `VWAP: str | None` - Volume-weighted average price
- `High52Week: str | None` - 52-week high
- `Low52Week: str | None` - 52-week low
- `MarketFlags: MarketFlags | None` - Market-specific flags
- `Restrictions: list[str] | None` - Trading restrictions

**Example:**
```python
from src.lib.tradestation import QuoteStream

async for data in sdk.streaming.stream_quotes(["MNQZ25"]):
    if "StreamStatus" in data:
        continue
    quote = QuoteStream(**data)
    print(f"52-week high: {quote.High52Week}")
```

---

#### `OrderStream`

Streaming order update (same structure as REST order response).

**Example:**
```python
from src.lib.tradestation import OrderStream

async for data in sdk.streaming.stream_orders("SIM123456"):
    if "StreamStatus" in data:
        continue
    order = OrderStream(**data)
    print(f"Order {order.OrderID}: {order.Status}")
```

---

#### `PositionStream`

Streaming position update with detailed P&L information.

**Key Fields:**
- `AccountID: str` - TradeStation account ID
- `Symbol: str` - Trading symbol
- `Quantity: str` - Position quantity (negative for short)
- `AveragePrice: str | None` - Average entry price
- `Last: str | None` - Last traded price
- `Bid: str | None` - Current bid price
- `Ask: str | None` - Current ask price
- `TodaysProfitLoss: str | None` - Today's P&L
- `UnrealizedProfitLoss: str | None` - Unrealized P&L
- `UnrealizedProfitLossPercent: str | None` - Unrealized P&L percentage
- `Deleted: bool | None` - True if position was closed

**Example:**
```python
from src.lib.tradestation import PositionStream

async for data in sdk.streaming.stream_positions("SIM123456"):
    if "StreamStatus" in data:
        continue
    position = PositionStream(**data)
    if position.Deleted:
        print(f"Position {position.PositionID} closed")
    else:
        print(f"{position.Symbol}: P&L={position.UnrealizedProfitLoss}")
```

---

#### `BarStream`

Streaming bar payload for `marketdata/stream/barcharts/{symbol}` (used by `stream_bars()`).

**Key Fields (mirrors TradeStation Bar schema):**
- `TimeStamp: str` - ISO timestamp of bar close time
- `Open, High, Low, Close: str` - OHLC prices
- `TotalVolume: str` - Total volume
- `Epoch: int` - Unix epoch (milliseconds)
- `BarStatus: str | None` - Bar status (`Closed`, `Open`, etc.)
- `IsRealtime: bool | None` - True if bar is currently building
- `IsEndOfHistory: bool | None` - True when historical bars are finished
- Tick stats: `DownTicks`, `UpTicks`, `DownVolume`, `UpVolume`, `TotalTicks`, `UnchangedTicks`, `UnchangedVolume`

**Example (raw API payload):**
```json
{
  "TimeStamp": "2025-01-15T10:01:00Z",
  "Open": "21450.00",
  "High": "21452.00",
  "Low": "21448.50",
  "Close": "21450.25",
  "TotalVolume": "12345",
  "Epoch": 1705314060000,
  "BarStatus": "Closed",
  "IsRealtime": false,
  "IsEndOfHistory": false
}
```

**Example (SDK model):**
```python
async for data in sdk.market_data.stream_bars("MNQZ25", "1", "Minute"):
    bar = data  # BarStream
    print(f"{bar.TimeStamp} O={bar.Open} H={bar.High} L={bar.Low} C={bar.Close}")
```

---

## Exceptions

All exceptions inherit from `TradeStationAPIError` and include structured error details.

### `ErrorDetails`

Structured error information dataclass included in all exceptions.

**Attributes:**
- `code: str | None` - Error code (e.g., "INVALID_REQUEST", "AUTHENTICATION_ERROR")
- `message: str` - Human-readable error message
- `api_error_code: str | None` - TradeStation API error code
- `api_error_message: str | None` - TradeStation API error message
- `request_method: str | None` - HTTP method (GET, POST, etc.)
- `request_endpoint: str | None` - API endpoint
- `request_params: dict | None` - Request query parameters (sanitized)
- `request_body: dict | None` - Request body (sanitized)
- `response_status: int | None` - HTTP response status code
- `response_body: dict | None` - Response body
- `mode: str | None` - Trading mode (PAPER/LIVE)
- `operation: str | None` - SDK operation that failed (e.g., "place_order")

**Methods:**
- `to_human_readable() -> str` - Generate human-readable error message with context
- `to_dict() -> dict` - Return structured error representation

---

### `TradeStationAPIError`

Base exception for all TradeStation API errors.

**Attributes:**
- `details: ErrorDetails` - Structured error details

**Methods:**
- `__str__() -> str` - Returns human-readable error message
- `to_dict() -> dict` - Returns structured error representation

**Example:**
```python
try:
    sdk.place_order(...)
except TradeStationAPIError as e:
    # Human-readable message
    print(f"Error: {e}")
    
    # Structured details
    details = e.to_dict()
    print(f"API Error: {details['api_error_code']}")
    print(f"Request: {details['request_method']} {details['request_endpoint']}")
```

---

### `AuthenticationError`

Raised when authentication fails (401, 403).

**Example:**
```python
try:
    sdk.authenticate(mode="PAPER")
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
    print(f"Details: {e.details.to_dict()}")
```

---

### `RateLimitError`

Raised when rate limit is exceeded (429).

**Example:**
```python
try:
    sdk.place_order(...)
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # Implement backoff
    import time
    time.sleep(60)
```

---

### `InvalidRequestError`

Raised when request parameters are invalid (400).

**Example:**
```python
try:
    sdk.place_order(symbol="INVALID", side="BUY", quantity=0)
except InvalidRequestError as e:
    print(f"Invalid request: {e}")
    # Access request details
    print(f"Request body: {e.details.request_body}")
```

---

### `NetworkError`

Raised when network errors occur (500+ or connection failures).

**Example:**
```python
try:
    sdk.get_account_info()
except NetworkError as e:
    print(f"Network error: {e}")
    # Retry with backoff
```

---

### `TokenExpiredError`

Raised when access token is expired and refresh fails.

**Example:**
```python
try:
    sdk.refresh_access_token()
except TokenExpiredError as e:
    print(f"Token expired, re-authentication required: {e}")
    sdk.authenticate()
```

---

### `InvalidTokenError`

Raised when token is invalid or missing.

**Example:**
```python
try:
    sdk.ensure_authenticated()
except InvalidTokenError as e:
    print(f"Invalid token: {e}")
    sdk.authenticate()
```

---

## Mappers

### `normalize_order(order: Any) -> dict[str, Any] | None`

Normalize TradeStation order object to consistent dictionary format.

**Parameters:**
- `order: Any` - Order object (dict or object) from TradeStation API

**Returns:**
- `dict[str, Any] | None` - Normalized order dictionary or None if invalid

**Example:**
```python
from src.lib.tradestation import normalize_order

normalized = normalize_order(order_data)
if normalized:
    print(f"Order ID: {normalized['order_id']}")
    print(f"Symbol: {normalized['symbol']}")
    print(f"Status: {normalized['status']}")
```

---

### `normalize_position(position: Any) -> dict[str, Any] | None`

Normalize TradeStation position object to consistent dictionary format.

**Parameters:**
- `position: Any` - Position object (dict or object) from TradeStation API

**Returns:**
- `dict[str, Any] | None` - Normalized position dictionary or None if invalid

**Example:**
```python
from src.lib.tradestation import normalize_position

normalized = normalize_position(position_data)
if normalized:
    print(f"Symbol: {normalized['symbol']}")
    print(f"Quantity: {normalized['quantity']}")
    print(f"Unrealized P&L: {normalized['unrealized_pnl']}")
```

---

**Last Updated:** 2025-12-05


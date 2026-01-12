---
status: Active
created: 12-05-2025 17:19:33 EST
lastUpdated: 12-05-2025 14:21:15 EST
version: 1.0.0
description: Comprehensive examples demonstrating SDK usage patterns, error handling, best practices, and common implementation scenarios
type: Usage Guide - Practical reference for developers implementing SDK features
applicability: When implementing SDK features, learning SDK usage patterns, or understanding best practices
howtouse: Reference this document when implementing SDK features, learning usage patterns, or looking for code examples
---

# TradeStation SDK Examples

## About This Document

This document provides **comprehensive usage examples** demonstrating SDK usage patterns, error handling, best practices, and common implementation scenarios. Each example includes explanations and context.

**Use this if:** You want to see real-world code examples, learn best practices, or understand how to implement specific features.

**Related Documents:**

- 📚 **[API_REFERENCE.md](API_REFERENCE.md)** - Complete API reference (function signatures)
- 📋 **[CHEATSHEET.md](cheatsheet.md)** - Quick code snippets (faster lookup)
- 📖 **[README.md](../README.md)** - SDK overview and getting started
- 🚀 **[docs/getting-started/quickstart.md](../getting-started/quickstart.md)** - 2-minute getting started
- 📊 **[examples/README.md](../examples/README.md)** - Interactive Jupyter notebooks

---

## Table of Contents

- [Basic Usage](#basic-usage)
- [Authentication](#authentication)
- [Account Operations](#account-operations)
- [Market Data](#market-data)
- [Order Management](#order-management)
- [Convenience Functions](#convenience-functions)
- [Position Management](#position-management)
- [Streaming](#streaming)
- [Error Handling](#error-handling)
- [Advanced Patterns](#advanced-patterns)

---

## Basic Usage

### Initialize SDK

```python
from src.lib.tradestation import TradeStationSDK

# Initialize SDK (loads tokens if available)
sdk = TradeStationSDK()

# Initialize with full request/response logging enabled
# This logs complete request and response bodies (useful for debugging)
sdk = TradeStationSDK(enable_full_logging=True)

# Or set via environment variable
# export TRADESTATION_FULL_LOGGING=true
sdk = TradeStationSDK()  # Will read from environment

# Authenticate if needed (opens browser for first-time login)
sdk.ensure_authenticated(mode="PAPER")
```

---

## Authentication

### First-Time Authentication

```python
from src.lib.tradestation import TradeStationSDK, AuthenticationError

sdk = TradeStationSDK()

try:
    # Opens browser for login
    sdk.authenticate(mode="PAPER")
    print("✅ Authentication successful")
except AuthenticationError as e:
    print(f"❌ Authentication failed: {e}")
```

### Token Refresh

```python
from src.lib.tradestation import TradeStationSDK, TokenExpiredError

sdk = TradeStationSDK()

try:
    # Automatically refreshes if needed
    sdk.ensure_authenticated(mode="PAPER")
except TokenExpiredError:
    # Re-authenticate if refresh fails
    sdk.authenticate(mode="PAPER")
```

### Dual-Mode Authentication

```python
sdk = TradeStationSDK()

# Authenticate both modes
sdk.authenticate(mode="PAPER")
sdk.authenticate(mode="LIVE")

# Switch between modes
account_paper = sdk.get_account_info(mode="PAPER")
account_live = sdk.get_account_info(mode="LIVE")
```

---

## Account Operations

### Get Account Information

```python
sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Get account info
account = sdk.get_account_info(mode="PAPER")
print(f"Account ID: {account['account_id']}")

# List all accounts
for acc in account.get('accounts', []):
    print(f"  {acc['AccountID']}: {acc['Alias']} ({acc['AccountType']})")
```

### Get Account Balances

```python
# Basic balances
balances = sdk.get_account_balances(mode="PAPER")
print(f"Equity: ${balances['equity']:.2f}")
print(f"Buying Power: ${balances['buying_power']:.2f}")
print(f"Cash Balance: ${balances['cash_balance']:.2f}")
print(f"Margin Available: ${balances['margin_available']:.2f}")
print(f"Margin Used: ${balances['margin_used']:.2f}")
print(f"Open P&L: ${balances['open_pnl']:.2f}")

# Detailed balances (with BalanceDetail and CurrencyDetails)
detailed = sdk.get_account_balances_detailed(account_ids="SIM123456", mode="PAPER")
for balance in detailed["Balances"]:
    print(f"Account: {balance['AccountID']}")
    print(f"  Equity: {balance['Equity']}")
    print(f"  Buying Power: {balance['BuyingPower']}")

    # BalanceDetail (varies by account type)
    if "BalanceDetail" in balance:
        detail = balance["BalanceDetail"]
        print(f"  Day Trade Excess: {detail.get('DayTradeExcess', 'N/A')}")
        print(f"  Realized P&L: {detail.get('RealizedProfitLoss', 'N/A')}")

    # CurrencyDetails (for futures accounts)
    if "CurrencyDetails" in balance:
        for currency in balance["CurrencyDetails"]:
            print(f"  Currency: {currency['Currency']}")
            print(f"    Cash Balance: {currency['CashBalance']}")

# Beginning of Day balances
bod = sdk.get_account_balances_bod(account_ids="SIM123456", mode="PAPER")
for bod_balance in bod["BODBalances"]:
    print(f"BOD Equity: {bod_balance.get('Equity', 'N/A')}")
```

---

## Market Data

### Get Historical Bars

```python
# Get 1-minute bars
bars = sdk.get_bars(
    symbol="MNQZ25",
    interval="1",
    unit="Minute",
    bars_back=200,
    mode="PAPER"
)

print(f"Retrieved {len(bars)} bars")
for bar in bars[-5:]:  # Last 5 bars
    print(f"{bar['Timestamp']}: O={bar['Open']}, H={bar['High']}, L={bar['Low']}, C={bar['Close']}, V={bar['Volume']}")
```

### Search Symbols

```python
# Search for futures
symbols = sdk.search_symbols(
    pattern="MNQ",
    category="Future",
    asset_type="Index",
    mode="PAPER"
)

for symbol in symbols:
    print(f"{symbol['Symbol']}: {symbol.get('Description', 'N/A')}")
```

### Get Quote Snapshots

```python
# Get current quotes for multiple symbols
quotes = sdk.get_quote_snapshots("MNQZ25,ESZ25", mode="PAPER")

for quote in quotes["Quotes"]:
    print(f"{quote['Symbol']}: Last={quote['Last']}, Bid={quote['Bid']}, Ask={quote['Ask']}")

# Handle errors
if quotes.get("Errors"):
    for error in quotes["Errors"]:
        print(f"Error for {error['Symbol']}: {error['Error']}")
```

### Get Symbol Details

```python
details = sdk.get_symbol_details("MNQZ25", mode="PAPER")

for symbol in details["Symbols"]:
    print(f"Symbol: {symbol['Symbol']}")
    print(f"  Description: {symbol.get('Description', 'N/A')}")
    print(f"  Category: {symbol.get('Category', 'N/A')}")
    print(f"  Asset Type: {symbol.get('AssetType', 'N/A')}")
    print(f"  Exchange: {symbol.get('Exchange', 'N/A')}")
```

---

## Order Management

### Place Market Order

```python
order_id, status = sdk.place_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    order_type="Market",
    mode="PAPER"
)

if order_id:
    print(f"✅ Order placed: {order_id}")
else:
    print(f"❌ Order failed: {status}")
```

### Place Limit Order (Convenience Function - Recommended)

```python
# Convenience function - simpler interface
order_id, status = sdk.place_limit_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    limit_price=25000.00,
    time_in_force="DAY",
    mode="PAPER"
)

# Or use low-level function
order_id, status = sdk.place_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    order_type="Limit",
    limit_price=25000.00,
    time_in_force="DAY",
    mode="PAPER"
)
```

### Place Stop Order (Convenience Function - Recommended)

```python
# Convenience function - simpler interface
order_id, status = sdk.place_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    stop_price=24950.00,
    mode="PAPER"
)

# Or use low-level function
order_id, status = sdk.place_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    order_type="Stop",
    stop_price=24950.00,
    mode="PAPER"
)
```

### Place Stop-Limit Order (Convenience Function - Recommended)

```python
# Convenience function - simpler interface
order_id, status = sdk.place_stop_limit_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    limit_price=24950.00,
    stop_price=24900.00,
    mode="PAPER"
)
```

### Place Trailing Stop Order (Convenience Function - Recommended)

```python
# Convenience function - trail by amount (points)
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # 1.5 points = $3.00 for MNQ
    mode="PAPER"
)

# Or trail by percentage
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_percent=1.0,  # 1% trail
    mode="PAPER"
)

# Or use low-level function
order_id, status = sdk.place_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    order_type="TrailingStop",
    trail_amount=1.5,
    mode="PAPER"
)
```

### Cancel Order

```python
success, message = sdk.cancel_order("924243071", mode="PAPER")

if success:
    print("✅ Order cancelled")
else:
    print(f"❌ Cancellation failed: {message}")
```

### Modify Order

```python
success, message = sdk.modify_order(
    order_id="924243071",
    quantity=3,  # Change quantity
    limit_price=25010.00,  # Change limit price
    mode="PAPER"
)
```

### Get Order History

```python
# Get recent orders
history = sdk.get_order_history(
    start_date="2025-12-01",
    end_date="2025-12-05",
    limit=100,
    mode="PAPER"
)

for order in history:
    print(f"Order {order['OrderID']}: {order['Status']} - {order.get('Symbol', 'N/A')}")
    if order.get('FilledQuantity'):
        print(f"  Filled: {order['FilledQuantity']} @ ${order.get('AverageFillPrice', 0):.2f}")
```

### Get Order Executions

```python
executions = sdk.get_order_executions("924243071", mode="PAPER")

for exec in executions:
    print(f"Execution {exec['ExecutionID']}: {exec['Quantity']} @ ${exec['Price']:.2f}")
    print(f"  Commission: ${exec.get('Commission', 0):.2f}")
    print(f"  Time: {exec['ExecutionTime']}")
```

### Place Bracket Order

```python
account_id = sdk.get_account_info(mode="PAPER")["account_id"]
entry_price = 25000.00
profit_target = entry_price + 50.00  # $50 profit
stop_loss = entry_price - 25.00      # $25 stop

bracket_orders = [
    # Entry order
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Buy",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": str(entry_price),
        "TimeInForce": {"Duration": "DAY"}
    },
    # Profit target
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": str(profit_target),
        "TimeInForce": {"Duration": "GTC"}
    },
    # Stop loss
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "StopMarket",
        "Quantity": "2",
        "StopPrice": str(stop_loss),
        "TimeInForce": {"Duration": "GTC"}
    }
]

result = sdk.place_group_order(
    group_type="BRK",
    orders=bracket_orders,
    mode="PAPER"
)

print(f"Bracket order placed: GroupID={result.get('GroupID')}")
for order in result.get('Orders', []):
    print(f"  Order {order['OrderID']}: {order['Status']}")
```

### Place OCO Order

```python
account_id = sdk.get_account_info(mode="PAPER")["account_id"]
current_price = 25000.00

oco_orders = [
    # Take profit
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "Limit",
        "Quantity": "2",
        "LimitPrice": str(current_price + 50.00),
        "TimeInForce": {"Duration": "GTC"}
    },
    # Stop loss
    {
        "AccountID": account_id,
        "Symbol": "MNQZ25",
        "TradeAction": "Sell",
        "OrderType": "StopMarket",
        "Quantity": "2",
        "StopPrice": str(current_price - 25.00),
        "TimeInForce": {"Duration": "GTC"}
    }
]

result = sdk.place_group_order(
    group_type="OCO",
    orders=oco_orders,
    mode="PAPER"
)
```

---

## Convenience Functions

The SDK provides convenience functions that simplify common order types. These functions wrap the low-level `place_order()` and `place_group_order()` methods with simpler interfaces.

### When to Use Convenience Functions

**Use convenience functions when:**

- You want simpler, more readable code
- You're placing common order types (limit, stop, trailing stop, bracket, OCO)
- You want built-in validation and error handling
- You want type-safe parameters

**Use low-level functions when:**

- You need advanced order configurations
- You're building custom order types
- You need direct access to all API parameters
- You're implementing complex conditional orders

### Convenience Function Examples

All convenience functions are available via the main SDK class:

```python
# Limit order
order_id, status = sdk.place_limit_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    limit_price=25000.00,
    mode="PAPER"
)

# Stop order
order_id, status = sdk.place_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    stop_price=24900.00,
    mode="PAPER"
)

# Stop-limit order
order_id, status = sdk.place_stop_limit_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    limit_price=24950.00,
    stop_price=24900.00,
    mode="PAPER"
)

# Trailing stop order
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # $3.00 trail for MNQ
    mode="PAPER"
)

# Bracket order (entry + profit target + stop-loss)
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,
    entry_price=None,  # Market entry
    mode="PAPER"
)

# OCO order
oco_orders = [
    {"AccountID": "SIM123456", "Symbol": "MNQZ25", ...},
    {"AccountID": "SIM123456", "Symbol": "MNQZ25", ...}
]
result = sdk.place_oco_order(oco_orders, mode="PAPER")
```

### Direct Access to Operation Classes

You can also access convenience functions directly via the operation classes:

```python
# Via OrderExecutionOperations
order_id, status = sdk.order_executions.place_limit_order(
    symbol="MNQZ25",
    side="BUY",
    quantity=2,
    limit_price=25000.00,
    mode="PAPER"
)

# Via OrderOperations (for queries)
current_orders = sdk.orders.get_current_orders(mode="PAPER")
```

---

## Position Management

### Get Position

```python
# Get position for specific symbol
position = sdk.get_position("MNQZ25", mode="PAPER")
print(f"Position: {position} contracts")

if position > 0:
    print("Long position")
elif position < 0:
    print("Short position")
else:
    print("Flat")
```

### Get All Positions

```python
positions = sdk.get_all_positions(mode="PAPER")

for pos in positions:
    print(f"{pos['Symbol']}: {pos['Quantity']} contracts")
```

### Flatten Position

```python
# Flatten all positions
flattened = sdk.flatten_position(mode="PAPER")
print(f"Flattened {len(flattened)} position(s)")

# Flatten specific symbol
flattened = sdk.flatten_position(symbol="MNQZ25", mode="PAPER")
```

---

## Streaming

### Stream Quotes

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, QuoteStream, StreamStatus, Heartbeat

async def stream_quotes_example():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")

    async for quote in sdk.streaming.stream_quotes(["MNQZ25"], mode="PAPER"):
        # Streaming methods now return QuoteStream models directly
        # Control messages (StreamStatus, Heartbeat) are filtered automatically
        print(f"{quote.Symbol}: Last={quote.Last}, Bid={quote.Bid}, Ask={quote.Ask}")
        print(f"  52-week range: {quote.Low52Week} - {quote.High52Week}")
        print(f"  Volume: {quote.Volume}, VWAP: {quote.VWAP}")

asyncio.run(stream_quotes_example())
```

### Stream Orders

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, OrderStream

async def stream_orders_example():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")

    account_id = sdk.get_account_info(mode="PAPER")["account_id"]

    async for order in sdk.streaming.stream_orders(account_id, mode="PAPER"):
        # Streaming methods now return OrderStream models directly
        # Control messages (StreamStatus, Heartbeat) are filtered automatically
        print(f"Order {order.OrderID}: {order.Status} - {order.StatusDescription}")

        if order.Status == "FLL":
            print(f"  Filled: {order.FilledQuantity} @ ${order.FilledPrice}")
        print(f"  Type: {order.OrderType}, Quantity: {order.Quantity}")

asyncio.run(stream_orders_example())
```

### Stream Positions

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, PositionStream

async def stream_positions_example():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")

    account_id = sdk.get_account_info(mode="PAPER")["account_id"]

    async for position in sdk.streaming.stream_positions(account_id, mode="PAPER"):
        # Streaming methods now return PositionStream models directly
        # Control messages (StreamStatus, Heartbeat) are filtered automatically

        # Handle position deletion
        if position.Deleted:
            print(f"Position {position.PositionID} closed")
            continue

        print(f"{position.Symbol}: {position.Quantity} @ {position.AveragePrice}")
        print(f"  Unrealized P&L: ${position.UnrealizedProfitLoss}")
        print(f"  Market Value: {position.MarketValue}")
        print(f"  Today's P&L: {position.TodaysProfitLoss}")
            print(f"  Today's P&L: ${position.TodaysProfitLoss}")
            print(f"  Market Value: ${position.MarketValue}")
        except Exception as e:
            print(f"Error parsing position: {e}")

asyncio.run(stream_positions_example())
```

### Multi-Symbol Streaming

```python
async def stream_multiple_symbols():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")

    symbols = ["MNQZ25", "ESZ25", "MESZ25"]

    async for quote in sdk.streaming.stream_quotes(symbols, mode="PAPER"):
        if "StreamStatus" in quote or "Heartbeat" in quote:
            continue

        quote_obj = QuoteStream(**quote)
        print(f"{quote_obj.Symbol}: Last={quote_obj.Last}")
```

---

## Error Handling

### Comprehensive Error Handling

The SDK provides structured error handling with descriptive error messages. All exceptions include detailed context about the request and response.

```python
from src.lib.tradestation import (
    TradeStationSDK,
    TradeStationAPIError,
    AuthenticationError,
    RateLimitError,
    InvalidRequestError,
    NetworkError,
    TokenExpiredError,
    InvalidTokenError
)

sdk = TradeStationSDK()

try:
    sdk.ensure_authenticated(mode="PAPER")
    order_id, status = sdk.place_order(
        symbol="MNQZ25",
        side="BUY",
        quantity=2,
        mode="PAPER"
    )
except AuthenticationError as e:
    # Human-readable error message
    print(f"Authentication failed: {e}")

    # Structured error details
    error_dict = e.to_dict()
    print(f"Error code: {error_dict['code']}")
    print(f"API error: {error_dict['api_error_code']}")
    print(f"Request: {error_dict['request_method']} {error_dict['request_endpoint']}")

    # Re-authenticate
    sdk.authenticate(mode="PAPER")
except TokenExpiredError as e:
    print(f"Token expired: {e}")
    # Refresh token
    sdk.refresh_access_token(mode="PAPER")
except RateLimitError as e:
    print(f"Rate limit exceeded: {e}")
    # Implement backoff
    import time
    time.sleep(60)  # Wait 1 minute
except InvalidRequestError as e:
    # Error includes full request context
    print(f"Invalid request: {e}")
    print(f"Request details: {e.details.request_body}")
    # Fix request parameters
except NetworkError as e:
    print(f"Network error: {e}")
    # Retry with backoff
except TradeStationAPIError as e:
    # All errors provide structured details
    print(f"API error: {e}")
    print(f"Operation: {e.details.operation}")
    print(f"Mode: {e.details.mode}")
    # Handle generic error
except Exception as e:
    print(f"Unexpected error: {e}")
```

### Error Message Examples

**Human-Readable Format:**

```
Order placement failed: Invalid symbol 'INVALID_SYMBOL'
  - API Error Code: INVALID_SYMBOL
  - API Error Message: Symbol 'INVALID_SYMBOL' not found

  Request Details:
    - Method: POST
    - Endpoint: orderexecution/orders
    - Mode: PAPER
    - Parameters: None
    - Body: {'AccountID': 'SIM123456', 'Symbol': 'INVALID_SYMBOL', ...}

  Response Details:
    - Status: 400
    - Body: {'Error': 'Invalid symbol', 'Code': 'INVALID_SYMBOL'}
```

**Structured Format:**

```python
error_dict = exception.to_dict()
# Returns:
{
    "code": "INVALID_REQUEST",
    "message": "Order placement failed: Invalid symbol",
    "api_error_code": "INVALID_SYMBOL",
    "api_error_message": "Symbol 'INVALID_SYMBOL' not found",
    "request_method": "POST",
    "request_endpoint": "orderexecution/orders",
    "request_params": None,
    "request_body": {"AccountID": "SIM123456", "Symbol": "INVALID_SYMBOL", ...},
    "response_status": 400,
    "response_body": {"Error": "Invalid symbol", "Code": "INVALID_SYMBOL"},
    "mode": "PAPER",
    "operation": "place_order"
}
```

### Retry Logic

```python
import time
from src.lib.tradestation import TradeStationSDK, NetworkError, RateLimitError

def place_order_with_retry(sdk, symbol, side, quantity, max_retries=3):
    for attempt in range(max_retries):
        try:
            order_id, status = sdk.place_order(
                symbol=symbol,
                side=side,
                quantity=quantity,
                mode="PAPER"
            )
            return order_id, status
        except (NetworkError, RateLimitError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"Retry {attempt + 1}/{max_retries} after {wait_time}s...")
                time.sleep(wait_time)
                continue
            raise
    return None, "Max retries exceeded"

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")
order_id, status = place_order_with_retry(sdk, "MNQZ25", "BUY", 2)
```

---

## Advanced Patterns

### Order Status Monitoring

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, OrderStream

async def monitor_order_status(order_id_to_monitor):
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")

    account_id = sdk.get_account_info(mode="PAPER")["account_id"]

    async for data in sdk.streaming.stream_orders(account_id, mode="PAPER"):
        if "StreamStatus" in data or "Heartbeat" in data:
            continue

        try:
            order = OrderStream(**data)

            # Monitor specific order
            if order.OrderID == order_id_to_monitor:
                print(f"Order {order.OrderID}: {order.Status} - {order.StatusDescription}")

                if order.Status == "FLL":
                    print(f"✅ Order filled at ${order.FilledPrice}")
                    break
                elif order.Status == "CNL":
                    print("❌ Order cancelled")
                    break
                elif order.Status == "REJ":
                    print(f"❌ Order rejected: {order.RejectionReason}")
                    break
        except Exception as e:
            print(f"Error: {e}")

# Place order and monitor
sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")
order_id, _ = sdk.place_order("MNQZ25", "BUY", 2, mode="PAPER")

# Monitor order status
asyncio.run(monitor_order_status(order_id))
```

### Position P&L Tracking

```python
import asyncio
from src.lib.tradestation import TradeStationSDK, PositionStream

async def track_position_pnl(symbol_to_track):
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")

    account_id = sdk.get_account_info(mode="PAPER")["account_id"]

    async for data in sdk.streaming.stream_positions(account_id, mode="PAPER"):
        if "StreamStatus" in data or "Heartbeat" in data:
            continue

        try:
            position = PositionStream(**data)

            if position.Symbol == symbol_to_track:
                if position.Deleted:
                    print(f"Position {position.PositionID} closed")
                    break

                print(f"{position.Symbol}: {position.Quantity} @ ${position.AveragePrice}")
                print(f"  Current Price: ${position.Last}")
                print(f"  Unrealized P&L: ${position.UnrealizedProfitLoss} ({position.UnrealizedProfitLossPercent}%)")
                print(f"  Today's P&L: ${position.TodaysProfitLoss}")
                print(f"  Market Value: ${position.MarketValue}")
        except Exception as e:
            print(f"Error: {e}")

asyncio.run(track_position_pnl("MNQZ25"))
```

### Stream Account Balances

```python
import asyncio
from src.lib.tradestation import TradeStationSDK

async def stream_balances_example():
    sdk = TradeStationSDK()
    sdk.ensure_authenticated(mode="PAPER")

    account_id = sdk.get_account_info(mode="PAPER")["account_id"]

    async for data in sdk.streaming.stream_balances(account_id, mode="PAPER"):
        # Skip control messages
        if "StreamStatus" in data or "Heartbeat" in data:
            continue

        print(f"Account: {data.get('AccountID')}")
        print(f"  Equity: {data.get('Equity')}")
        print(f"  Buying Power: {data.get('BuyingPower')}")
        print(f"  Cash Balance: {data.get('CashBalance')}")
        print(f"  Today's P&L: {data.get('TodaysProfitLoss')}")

asyncio.run(stream_balances_example())
```

### Multi-Account Operations

```python
sdk = TradeStationSDK()

# Authenticate both modes
sdk.authenticate(mode="PAPER")
sdk.authenticate(mode="LIVE")

# Get accounts for both modes
paper_account = sdk.get_account_info(mode="PAPER")
live_account = sdk.get_account_info(mode="LIVE")

print(f"PAPER Account: {paper_account['account_id']}")
print(f"LIVE Account: {live_account['account_id']}")

# Get balances for both
paper_balances = sdk.get_account_balances(mode="PAPER")
live_balances = sdk.get_account_balances(mode="LIVE")

print(f"PAPER Equity: ${paper_balances['equity']:.2f}")
print(f"LIVE Equity: ${live_balances['equity']:.2f}")
```

### Using Models for Type Safety

```python
from src.lib.tradestation import (
    TradeStationSDK,
    TradeStationOrderRequest,
    QuoteStream,
    OrderStream,
    PositionStream
)

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Create order request using model
order_request = TradeStationOrderRequest(
    AccountID="SIM123456",
    Symbol="MNQZ25",
    TradeAction="Buy",
    OrderType="Limit",
    Quantity="2",
    LimitPrice="25000.00",
    TimeInForce={"Duration": "DAY"}
)

# Convert to dict for API call
order_dict = order_request.model_dump(exclude_none=True)

# Use streaming models
async for data in sdk.streaming.stream_quotes(["MNQZ25"], mode="PAPER"):
    if "StreamStatus" in data:
        continue

    quote = QuoteStream(**data)  # Type-safe parsing
    print(f"52-week high: {quote.High52Week}")
    print(f"Market flags: {quote.MarketFlags}")
```

---

**Last Updated:** 2025-12-05

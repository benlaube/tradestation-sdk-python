# TradeStation SDK - New Functions Summary

**Version:** 1.0.0  
**Last Updated:** 2025-12-05

Summary of new functions added to ensure all required trading operations are covered.

---

## New Functions Added

### 1. `is_order_filled()`

**Location:** `OrderExecutionOperations.is_order_filled()` / `TradeStationSDK.is_order_filled()`

**Purpose:** Convenience function to check if an order has been filled.

**Returns:** `bool` - True if order status is "FLL" (Filled) or "FLP" (Partial Fill)

**Example:**
```python
if sdk.is_order_filled("924243071", mode="PAPER"):
    print("Order is filled!")
```

---

### 2. `cancel_all_orders_for_symbol()`

**Location:** `OrderExecutionOperations.cancel_all_orders_for_symbol()` / `TradeStationSDK.cancel_all_orders_for_symbol()`

**Purpose:** Cancel all open orders for a specific symbol.

**Returns:** `list[dict[str, Any]]` - List of cancellation results with order_id, symbol, success, message

**Example:**
```python
results = sdk.cancel_all_orders_for_symbol("MNQZ25", mode="PAPER")
for result in results:
    print(f"Order {result['order_id']}: {result['success']}")
```

---

### 3. `cancel_all_orders()`

**Location:** `OrderExecutionOperations.cancel_all_orders()` / `TradeStationSDK.cancel_all_orders()`

**Purpose:** Cancel all open orders for account(s).

**Returns:** `list[dict[str, Any]]` - List of cancellation results with order_id, symbol, success, message

**Example:**
```python
results = sdk.cancel_all_orders(mode="PAPER")
print(f"Cancelled {len(results)} orders")
```

---

### 4. `replace_order()`

**Location:** `OrderExecutionOperations.replace_order()` / `TradeStationSDK.replace_order()`

**Purpose:** Replace an order by canceling the old one and placing a new one. Useful when you need to change symbol, side, or other parameters that cannot be modified with `modify_order()`.

**Returns:** `tuple[str | None, str]` - (new_order_id, status_message)

**Example:**
```python
new_order_id, status = sdk.replace_order(
    old_order_id="924243071",
    symbol="ESZ25",  # Different symbol
    side="SELL",     # Different side
    quantity=3,
    order_type="Limit",
    limit_price=25000.00,
    mode="PAPER"
)
```

---

## Enhanced Functions

### 5. `place_bracket_order()` - Enhanced with Trailing Stop Support

**Location:** `OrderExecutionOperations.place_bracket_order()` / `TradeStationSDK.place_bracket_order()`

**New Parameters:**
- `stop_loss` (float | None): Now optional when using trailing stop
- `trail_amount` (float | None): Trail amount in price units (points)
- `trail_percent` (float | None): Trail percentage
- `use_trailing_stop` (bool): If True, use trailing stop instead of fixed stop-loss

**Example:**
```python
# Bracket order with trailing stop (NEW)
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    use_trailing_stop=True,
    trail_amount=1.5,  # $3.00 trail for MNQ
    mode="PAPER"
)
```

---

## Coverage Status

All 9 required operations are now fully covered:

- ✅ Replace an open order with a new one - `replace_order()`
- ✅ Cancel an order - `cancel_order()`
- ✅ Place a bracket order with trailing stop - `place_bracket_order(..., use_trailing_stop=True)`
- ✅ Confirm an order has been filled - `is_order_filled()`, `get_order_executions()`
- ✅ Cancel all orders (symbol) - `cancel_all_orders_for_symbol()`
- ✅ Cancel all orders on account - `cancel_all_orders()`
- ✅ Flatten position (symbol) - `flatten_position(symbol)`
- ✅ Flatten all positions - `flatten_position()`
- ✅ Trailing stop order - `place_trailing_stop_order()`

---

**Last Updated:** 2025-12-05

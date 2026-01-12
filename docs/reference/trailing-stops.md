---
version: 1.0.0
lastUpdated: 12-05-2025 17:19:34 EST
---

# TradeStation SDK - Trailing Stop Variations

## About This Document

This document provides a **complete guide to all trailing stop variations** and configurations available in the SDK. It explains different trailing stop types, parameters, and use cases with detailed examples.

**Use this if:** You're working with trailing stop orders, need to understand trailing stop parameters, or want to see all available trailing stop configurations.

**Related Documents:**

- 📝 **[../guides/order-functions.md](../guides/order-functions.md)** - Detailed order function documentation
- 📚 **[../api/reference.md](../api/reference.md)** - Complete API reference
- ⚠️ **[docs/architecture/limitations.md](../architecture/limitations.md)** - Trailing stop limitations (points vs dollars)
- 💡 **[../guides/usage-examples.md](../guides/usage-examples.md)** - Trailing stop usage examples

---

Complete guide to all trailing stop variations and configurations available in the TradeStation SDK.

---

## Overview

Trailing stop orders automatically adjust the stop price as the market moves in your favor, helping to lock in profits while limiting losses. The TradeStation SDK supports multiple trailing stop variations through different functions and configurations.

---

## Trailing Stop Types

### 1. Standalone Trailing Stop Orders

**Function:** `place_trailing_stop_order()` or `place_order(order_type="TrailingStop")`

**Variations:**

#### A. Trail by Amount (Points)

Trails by a fixed price amount in points/price units.

**Key Points:**

- For futures, `trail_amount` is in **price units (points)**, not dollar amounts
- For MNQ: 1 point = $2.00, so `trail_amount=1.5` means $3.00 trail
- For ES: 1 point = $50.00, so `trail_amount=1.0` means $50.00 trail
- The stop price adjusts by this amount as price moves favorably

**Example:**

```python
# Trail by 1.5 points ($3.00 for MNQ)
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",  # Exit long position
    quantity=2,
    trail_amount=1.5,  # 1.5 points = $3.00 trail
    time_in_force="GTC",  # Good till cancelled
    mode="PAPER"
)
```

#### B. Trail by Percentage

Trails by a percentage of the current price.

**Key Points:**

- `trail_percent` is specified as a decimal (e.g., 1.0 = 1%, 0.5 = 0.5%)
- The stop price adjusts by this percentage as price moves favorably
- More dynamic than fixed amount - adjusts with price level

**Example:**

```python
# Trail by 1% of current price
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_percent=1.0,  # 1% trail
    time_in_force="GTC",
    mode="PAPER"
)
```

**Important:** You must use **either** `trail_amount` **or** `trail_percent`, not both. If both are provided, `trail_amount` takes precedence.

---

### 2. Trailing Stop in Bracket Orders

**Function:** `place_bracket_order(..., use_trailing_stop=True)`

**Variations:**

Bracket orders combine an entry order with both a profit target and a stop-loss. The stop-loss can be either a fixed stop or a trailing stop.

#### A. Bracket Order with Trailing Stop (Trail by Amount)

**Configuration:**

- Entry: Market or Limit order
- Profit Target: Limit order (fixed price)
- Stop-Loss: **Trailing Stop** with `trail_amount`

**Example:**

```python
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,  # Fixed profit target
    use_trailing_stop=True,
    trail_amount=1.5,  # $3.00 trail for MNQ
    entry_price=None,  # Market entry
    entry_order_type="Market",
    time_in_force="GTC",
    mode="PAPER"
)
```

#### B. Bracket Order with Trailing Stop (Trail by Percentage)

**Configuration:**

- Entry: Market or Limit order
- Profit Target: Limit order (fixed price)
- Stop-Loss: **Trailing Stop** with `trail_percent`

**Example:**

```python
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,  # Fixed profit target
    use_trailing_stop=True,
    trail_percent=1.0,  # 1% trail
    entry_price=25000.00,  # Limit entry
    entry_order_type="Limit",
    time_in_force="GTC",
    mode="PAPER"
)
```

#### C. Bracket Order with Fixed Stop-Loss (No Trailing)

**Configuration:**

- Entry: Market or Limit order
- Profit Target: Limit order (fixed price)
- Stop-Loss: **Fixed Stop** (not trailing)

**Example:**

```python
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    stop_loss=24900.00,  # Fixed stop-loss (not trailing)
    entry_price=None,
    entry_order_type="Market",
    time_in_force="GTC",
    mode="PAPER"
)
```

---

## Trailing Stop Parameters

### Trail Amount (`trail_amount`)

**Type:** `float | None`

**Description:** Trail by a fixed price amount in points/price units.

**Important Notes:**

- **For Futures:** Specified in price units (points), not dollar amounts
- **MNQ Example:** `trail_amount=1.5` = 1.5 points = $3.00 trail
- **ES Example:** `trail_amount=1.0` = 1.0 point = $50.00 trail
- The stop price adjusts by this amount as the market moves favorably
- Only moves in the favorable direction (locks in profits, doesn't widen losses)

**When to Use:**

- You want a fixed dollar/point trail regardless of price level
- Good for consistent risk management
- Easier to calculate exact dollar risk

**Example:**

```python
# Always trail by $3.00 (1.5 points for MNQ)
sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_amount=1.5,  # Fixed 1.5 points
    mode="PAPER"
)
```

---

### Trail Percentage (`trail_percent`)

**Type:** `float | None`

**Description:** Trail by a percentage of the current price.

**Important Notes:**

- Specified as a decimal (e.g., `1.0` = 1%, `0.5` = 0.5%, `2.5` = 2.5%)
- The stop price adjusts by this percentage as the market moves favorably
- More dynamic - trail amount increases as price increases
- Only moves in the favorable direction

**When to Use:**

- You want the trail to scale with price level
- Good for percentage-based risk management
- More appropriate for volatile instruments

**Example:**

```python
# Trail by 1% of current price
sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_percent=1.0,  # 1% trail
    mode="PAPER"
)
```

---

## Time in Force Options

All trailing stop orders support the following `time_in_force` options:

| Value | Description | Use Case |
|-------|-------------|----------|
| `"DAY"` | Valid until end of trading session | Intraday trading |
| `"GTC"` | Good till cancelled (max 90 days) | **Recommended for trailing stops** - Allows stop to trail over multiple days |
| `"IOC"` | Immediate or Cancel | Rarely used for trailing stops |
| `"FOK"` | Fill or Kill | Rarely used for trailing stops |

**Recommendation:** Use `"GTC"` for trailing stops to allow them to trail over multiple trading sessions.

---

## Trailing Stop Behavior

### How Trailing Stops Work

1. **Initial Placement:** Trailing stop is placed at a distance from current price
   - For `trail_amount=1.5`: Stop is 1.5 points below current price (for long positions)
   - For `trail_percent=1.0`: Stop is 1% below current price (for long positions)

2. **Favorable Movement:** As price moves in your favor, the stop price adjusts upward
   - The stop **only moves in the favorable direction**
   - It **never moves against you** (doesn't widen losses)

3. **Unfavorable Movement:** If price moves against you, the stop stays at its current level
   - The stop **does not move down** (doesn't widen losses)
   - Once price hits the stop, the order executes

### Example Scenario

**Long Position with Trailing Stop:**

```
Entry Price: $25,000
Trail Amount: 1.5 points ($3.00)

Price Movement:
- $25,000 → Stop at $24,998.50 (1.5 points below)
- $25,010 → Stop moves to $25,008.50 (trails up)
- $25,020 → Stop moves to $25,018.50 (trails up)
- $25,015 → Stop stays at $25,018.50 (doesn't move down)
- $25,018.50 → Stop triggers, position closed
```

---

## Function Comparison

| Function | Use Case | Trailing Stop Support |
|----------|----------|----------------------|
| `place_trailing_stop_order()` | Standalone trailing stop | ✅ Yes - `trail_amount` or `trail_percent` |
| `place_order(order_type="TrailingStop")` | Standalone trailing stop (direct) | ✅ Yes - `trail_amount` or `trail_percent` |
| `place_bracket_order(..., use_trailing_stop=True)` | Entry + profit target + trailing stop | ✅ Yes - `trail_amount` or `trail_percent` |
| `place_bracket_order(..., use_trailing_stop=False)` | Entry + profit target + fixed stop | ❌ No - Uses fixed `stop_loss` |

---

## Complete Examples

### Example 1: Standalone Trailing Stop (Amount)

```python
# Place a trailing stop to protect a long position
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",  # Exit long position
    quantity=2,
    trail_amount=1.5,  # $3.00 trail
    time_in_force="GTC",  # Good till cancelled
    mode="PAPER"
)
```

### Example 2: Standalone Trailing Stop (Percentage)

```python
# Place a trailing stop with percentage trail
order_id, status = sdk.place_trailing_stop_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    trail_percent=1.0,  # 1% trail
    time_in_force="GTC",
    mode="PAPER"
)
```

### Example 3: Bracket Order with Trailing Stop (Amount)

```python
# Enter position with profit target and trailing stop
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,  # Take profit at $25,100
    use_trailing_stop=True,
    trail_amount=1.5,  # $3.00 trail
    entry_price=None,  # Market entry
    entry_order_type="Market",
    time_in_force="GTC",
    mode="PAPER"
)

# Extract order IDs
entry_order_id = result["Orders"][0]["OrderID"]
profit_order_id = result["Orders"][1]["OrderID"]
trailing_stop_order_id = result["Orders"][2]["OrderID"]
```

### Example 4: Bracket Order with Trailing Stop (Percentage)

```python
# Enter position with limit entry, profit target, and trailing stop
result = sdk.place_bracket_order(
    symbol="MNQZ25",
    entry_side="BUY",
    quantity=2,
    profit_target=25100.00,
    use_trailing_stop=True,
    trail_percent=1.0,  # 1% trail
    entry_price=25000.00,  # Limit entry
    entry_order_type="Limit",
    time_in_force="GTC",
    mode="PAPER"
)
```

### Example 5: Direct Order Placement (Trailing Stop)

```python
# Place trailing stop directly via place_order
order_id, status = sdk.place_order(
    symbol="MNQZ25",
    side="SELL",
    quantity=2,
    order_type="TrailingStop",
    trail_amount=1.5,  # or trail_percent=1.0
    time_in_force="GTC",
    mode="PAPER"
)
```

---

## Limitations and Considerations

### 1. Trail Amount vs Trail Percent

- **Cannot use both:** You must choose either `trail_amount` or `trail_percent`, not both
- **Precedence:** If both are provided, `trail_amount` takes precedence
- **Validation:** SDK validates that at least one is provided

### 2. Price Units vs Dollar Amounts

- **Important:** For futures, `trail_amount` is in **price units (points)**, not dollar amounts
- **MNQ:** 1 point = $2.00
- **ES:** 1 point = $50.00
- **NQ:** 1 point = $20.00

### 3. Direction Considerations

- **Long Positions:** Use `side="SELL"` for trailing stop (exit long)
- **Short Positions:** Use `side="BUY"` for trailing stop (exit short)
- The trailing stop always trails in the favorable direction

### 4. Time in Force

- **GTC Recommended:** Use `"GTC"` for trailing stops to allow them to trail over multiple sessions
- **DAY Limitation:** `"DAY"` orders expire at end of session, may not trail overnight

### 5. Bracket Order Constraints

- **Trailing Stop in Brackets:** Only the stop-loss component can be trailing
- **Profit Target:** Always a fixed limit order (not trailing)
- **Entry:** Can be Market or Limit (not trailing)

---

## Summary

**Trailing Stop Variations Available:**

1. ✅ **Standalone Trailing Stop** - `place_trailing_stop_order()`
   - Trail by Amount (`trail_amount`)
   - Trail by Percentage (`trail_percent`)

2. ✅ **Bracket Order with Trailing Stop** - `place_bracket_order(..., use_trailing_stop=True)`
   - Trail by Amount (`trail_amount`)
   - Trail by Percentage (`trail_percent`)
   - Combined with entry order and profit target

3. ✅ **Direct Order Placement** - `place_order(order_type="TrailingStop")`
   - Trail by Amount (`trail_amount`)
   - Trail by Percentage (`trail_percent`)

**All variations support:**

- Multiple `time_in_force` options (DAY, GTC, IOC, FOK)
- Both PAPER and LIVE trading modes
- Full order lifecycle management (cancel, modify, query)

---

**Last Updated:** 2025-12-05

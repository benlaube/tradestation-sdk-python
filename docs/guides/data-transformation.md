---
version: 1.0.1
lastUpdated: 12-29-2025 13:54:55 EST
---

# Data Transformation Guide


## Overview

This guide explains how to work with TradeStation SDK data formats and when to use different transformation approaches. The SDK provides multiple ways to access and transform data, each suited for different use cases.

---

## Table of Contents

- [Primary API: Pydantic Models](#primary-api-pydantic-models)
- [Optional Utilities: Mappers](#optional-utilities-mappers)
- [When to Use Each Approach](#when-to-use-each-approach)
- [Transformation Examples](#transformation-examples)
- [Best Practices](#best-practices)
- [FAQ](#faq)

---

## Primary API: Pydantic Models

### Default Behavior

**The SDK's primary API returns Pydantic models with PascalCase field names**, matching the TradeStation API format exactly.

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Returns Pydantic model with PascalCase fields
orders = sdk.get_current_orders(mode="PAPER")
# orders.Orders[0].OrderID  # PascalCase
# orders.Orders[0].Symbol   # PascalCase
# orders.Orders[0].Status   # PascalCase
```

### Why PascalCase?

- **API Alignment:** TradeStation API uses PascalCase, so the SDK matches this format
- **Type Safety:** Pydantic models provide validation and type hints
- **Consistency:** All SDK methods return the same format
- **No Transformation Overhead:** Data is returned as-is from the API

### Accessing Model Data

```python
# Direct attribute access (recommended)
order = orders.Orders[0]
order_id = order.OrderID
symbol = order.Symbol
status = order.Status

# Convert to dictionary (PascalCase keys)
order_dict = order.model_dump()
# {"OrderID": "...", "Symbol": "...", "Status": "..."}

# Convert to JSON (PascalCase keys)
order_json = order.model_dump_json()
```

---

## Optional Utilities: Mappers

### What Are Mappers?

Mappers are **optional utility functions** that convert PascalCase data to snake_case dictionaries. They're provided for applications that need snake_case format (e.g., database storage with snake_case columns).

### Available Mappers

```python
from src.lib.tradestation import (
    normalize_order,
    normalize_position,
    normalize_quote,
    normalize_execution,
    normalize_account,
    normalize_balances,
    normalize_bod_balance,
    normalize_account_balances,
)
```

### Mapper Characteristics

- **Optional:** Not required for SDK functionality
- **Application-Specific:** Useful for specific use cases (database storage, etc.)
- **snake_case Output:** Converts PascalCase → snake_case
- **Flexible Input:** Handles dict, Pydantic models, or objects
- **Error Handling:** Returns `None` for invalid input

### Example Usage

```python
from src.lib.tradestation import TradeStationSDK, normalize_order

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Get orders (returns Pydantic models)
orders = sdk.get_current_orders(mode="PAPER")

# Transform to snake_case for database storage
for order_model in orders.Orders:
    normalized = normalize_order(order_model)
    if normalized:
        # normalized is now snake_case: {"order_id": "...", "symbol": "..."}
        db.insert_order(normalized)
```

### Mapper Coverage (what each normalizes)

- `normalize_order` - Orders (REST/stream)
- `normalize_position` - Positions (REST/stream)
- `normalize_quote` - Quote snapshots
- `normalize_execution` - Executions/fills
- `normalize_account` - Account summary
- `normalize_balances` - Balance detail
- `normalize_account_balances` - Account balances response wrapper
- `normalize_bod_balance` - Beginning-of-day balance entries

---

## When to Use Each Approach

### Use Pydantic Models (Default) When:

✅ **You want type safety and validation**
✅ **You're working with the data in Python**
✅ **You want to match the TradeStation API format exactly**
✅ **You're building a new application**
✅ **You don't need snake_case**

**Example Use Cases:**
- Building trading algorithms
- Real-time data processing
- API integrations
- Type-safe applications

### Use Mappers When:

✅ **You need snake_case for database storage**
✅ **You're migrating from an old system that used snake_case**
✅ **You have existing code expecting snake_case**
✅ **You're integrating with systems that require snake_case**

**Example Use Cases:**
- Database storage (PostgreSQL, MySQL with snake_case columns)
- Legacy system integration
- Data pipelines expecting snake_case
- ORM frameworks using snake_case

### Use Pydantic's Built-in Serialization When:

✅ **You need custom transformations**
✅ **You want to exclude/include specific fields**
✅ **You need different serialization formats**

**Example:**
```python
# Custom transformation with Pydantic
order_dict = order.model_dump(
    exclude_none=True,           # Exclude None values
    exclude={"CommissionFee"},    # Exclude specific fields
    by_alias=False,              # Use field names (PascalCase)
)

# Convert to camelCase (custom transformation)
import json
order_json = order.model_dump_json()
order_camel = json.loads(order_json)  # Then transform keys as needed
```

---

## Transformation Examples

### Example 1: Using Pydantic Models (Recommended)

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Get orders - returns Pydantic models
orders_response = sdk.get_current_orders(mode="PAPER")

# Access data directly (PascalCase)
for order in orders_response.Orders:
    print(f"Order {order.OrderID}: {order.Symbol} - {order.Status}")

    # Type-safe access with validation
    if order.FilledQuantity:
        print(f"Filled: {order.FilledQuantity}")
```

### Example 2: Using Mappers for Database Storage

```python
from src.lib.tradestation import TradeStationSDK, normalize_order
import psycopg2

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Get orders
orders_response = sdk.get_current_orders(mode="PAPER")

# Transform to snake_case for database
conn = psycopg2.connect("...")
cursor = conn.cursor()

for order_model in orders_response.Orders:
    normalized = normalize_order(order_model)
    if normalized:
        # Insert into database with snake_case columns
        cursor.execute(
            """
            INSERT INTO orders (order_id, symbol, status, filled_quantity)
            VALUES (%s, %s, %s, %s)
            """,
            (
                normalized["order_id"],
                normalized["symbol"],
                normalized["status"],
                normalized["filled_quantity"],
            )
        )
```

### Example 3: Custom Transformation with Pydantic

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

orders_response = sdk.get_current_orders(mode="PAPER")

# Custom transformation: PascalCase → camelCase
def to_camel_case(s: str) -> str:
    parts = s.split("_")
    return parts[0] + "".join(word.capitalize() for word in parts[1:])

for order in orders_response.Orders:
    # Get as dict
    order_dict = order.model_dump(exclude_none=True)

    # Transform keys to camelCase
    camel_dict = {to_camel_case(k): v for k, v in order_dict.items()}
    # {"orderId": "...", "symbol": "...", "status": "..."}
```

### Example 4: Streaming with Mappers

```python
from src.lib.tradestation import TradeStationSDK, normalize_order

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# Stream orders (returns Pydantic models)
async for order_stream in sdk.streaming.stream_orders(account_id="SIM123456"):
    # order_stream is a Pydantic OrderStream model (PascalCase)
    print(f"Order {order_stream.OrderID}: {order_stream.Status}")

    # Transform to snake_case if needed for database
    normalized = normalize_order(order_stream)
    if normalized:
        db.upsert_order(normalized)
```

---

## Best Practices

### 1. Prefer Pydantic Models for New Code

**Recommended:**
```python
# Use Pydantic models directly
orders = sdk.get_current_orders()
for order in orders.Orders:
    process_order(order)  # Type-safe, validated
```

**Avoid (unless necessary):**
```python
# Don't use mappers unless you need snake_case
orders = sdk.get_current_orders()
for order in orders.Orders:
    normalized = normalize_order(order)  # Unnecessary transformation
    process_order(normalized)
```

### 2. Use Mappers Only When Needed

Mappers add transformation overhead. Only use them when:
- You need snake_case format
- You're integrating with systems requiring snake_case
- You have existing code expecting snake_case

### 3. Leverage Pydantic's Built-in Features

Pydantic provides powerful serialization options:

```python
# Exclude None values
order_dict = order.model_dump(exclude_none=True)

# Exclude specific fields
order_dict = order.model_dump(exclude={"CommissionFee", "UnbundledRouteFee"})

# Include only specific fields
order_dict = order.model_dump(include={"OrderID", "Symbol", "Status"})

# Convert to JSON
order_json = order.model_dump_json(indent=2)
```

### 4. Handle Errors Gracefully

```python
from src.lib.tradestation import normalize_order

# Mappers return None for invalid input
normalized = normalize_order(order_data)
if normalized:
    # Use normalized data
    process_order(normalized)
else:
    # Handle invalid data
    logger.warning("Failed to normalize order data")
```

### 5. Consider Performance

- **Pydantic models:** Fast, no transformation overhead
- **Mappers:** Additional transformation step (minimal overhead)
- **Custom transformations:** Most flexible but requires custom code

For high-frequency operations (streaming, real-time processing), prefer Pydantic models directly.

---

## FAQ

### Q: Should I use mappers or Pydantic models?

**A:** Use Pydantic models (default) unless you specifically need snake_case format. Pydantic models provide type safety, validation, and match the TradeStation API format.

### Q: Are mappers required?

**A:** No. Mappers are optional utilities for specific use cases. The SDK works perfectly without them.

### Q: Can I use both?

**A:** Yes. Use Pydantic models for your application logic, and mappers only when you need snake_case (e.g., database storage).

### Q: Do mappers work with streaming data?

**A:** Yes. Mappers accept Pydantic models, dicts, or objects, so they work with streaming data:

```python
async for order_stream in sdk.streaming.stream_orders(account_id):
    normalized = normalize_order(order_stream)  # Works with Pydantic models
```

### Q: How do I convert Pydantic models to JSON?

**A:** Use Pydantic's built-in methods:

```python
# To JSON string
order_json = order.model_dump_json()

# To dict (then use json.dumps if needed)
order_dict = order.model_dump()
```

### Q: Can I customize the mapper output?

**A:** Mappers have a fixed snake_case format. For custom transformations, use Pydantic's `model_dump()` and transform the keys yourself.

### Q: Are mappers part of the core SDK?

**A:** Mappers are optional utilities exported from the SDK. They're not used internally by the SDK itself - the SDK returns Pydantic models directly.

### Q: What if I need a different format (camelCase, kebab-case)?

**A:** Use Pydantic's `model_dump()` and transform the keys:

```python
order_dict = order.model_dump()
# Transform keys as needed
camel_dict = {to_camel_case(k): v for k, v in order_dict.items()}
```

---

## Summary

| Approach | Format | Use When | Performance |
|----------|--------|----------|-------------|
| **Pydantic Models** (Default) | PascalCase | New code, type safety, API alignment | ⚡ Fastest |
| **Mappers** | snake_case | Database storage, legacy integration | ⚡ Fast |
| **Custom Transformation** | Any format | Custom requirements | ⚡ Depends on implementation |

**Recommendation:** Use Pydantic models as the default. Only use mappers when you specifically need snake_case format.

---

## Related Documentation

- **[Models Documentation](../models/README.md)** - Complete Pydantic model reference
- **[API Reference](../api/reference.md)** - Complete API documentation
- **[Usage Examples](./usage-examples.md)** - Code examples and patterns
- **[SDK Models Schema](../reference/sdk-models-schema.json)** - Complete JSON schema for all models

---

**Last Updated:** 2025-12-29 14:00:00 EST
**Version:** 1.0.0

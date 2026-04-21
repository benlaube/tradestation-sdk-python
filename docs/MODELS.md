# TradeStation SDK - Pydantic Models Documentation

## About This Document

This document provides **summary and status documentation** for all Pydantic models used in the SDK. It covers model coverage, field mapping, data collection status, and identifies missing fields.

**Use this if:** You want to understand model structure, see what fields are available, or identify missing data points.

**Related Documents:**
- 📚 **[docs/API_REFERENCE.md](API_REFERENCE.md)** - Complete API reference (includes model usage)
- 🏗️ **[models/](../models/)** - Source code for all Pydantic models
- 📖 **[README.md](../README.md)** - SDK documentation
- 💡 **[docs/SDK_USAGE_EXAMPLES.md](SDK_USAGE_EXAMPLES.md)** - Examples using models

## Metadata

- **Status:** Active
- **Created:** 12-05-2025
- **Last Updated:** 12-05-2025 14:21:15 EST
- **Version:** 1.0
- **Description:** Summary and status documentation for TradeStation API Pydantic models, including model coverage, field mapping, and data collection status
- **Type:** Model Reference - Technical reference for developers working with SDK models
- **Applicability:** When understanding model structure, reviewing field coverage, or identifying missing data points in model implementations
- **Dependencies:**
  - [`models/`](../models/) - SDK Pydantic model implementations
  - [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json) - Source OpenAPI specification
  - [`API_REFERENCE.md`](./API_REFERENCE.md) - Complete API reference including models
- **How to Use:** Reference this document to understand model status, identify missing fields, and review data collection completeness

---

## Current Contract Status (2026-04-14)

The SDK now treats Pydantic models as an enforced contract boundary, not just documentation.

### Current Behavior

- Exported request/response models inherit a shared strict base with `extra="forbid"`.
- Unknown broker fields raise `SDKValidationError` instead of being silently ignored.
- Audited SDK boundaries validate inbound/outbound payloads before returning public dict/list shapes.
- Validation and runtime failures now bubble up with structured `ErrorDetails` that include operation, endpoint, mode, and sanitized payload excerpts.
- Public SDK compatibility is preserved at the return-shape layer: successful calls still return dicts/lists, while malformed payloads now fail loud.

### Scope Hardened in This Pass

- Accounts
- Account discovery and balance convenience helpers
- Quote snapshots
- Market-data convenience helpers
- Positions
- Position convenience helpers that depend on order history / flattening
- Order history/current order lookups
- Order executions and placement request construction
- Session ID-token decoding
- Streaming quote/order/position/balance parsing

### Compatibility Notes

- `TRADESTATION_MODE` is the canonical environment variable for PAPER/LIVE mode selection.
- `TRADING_MODE` remains a deprecated fallback alias for compatibility.
- The historical analysis below remains useful as background, but where it conflicts with this section, this section is authoritative.

---

## Quick Answer to Your Questions

### Q: Are we collecting all data points from TradeStation API?

**A: NO - We're missing 20+ fields when syncing historical orders.**

**Current Status:**
- ✅ **WebSocket order updates** (`orders_handler.py`) - Captures ALL 30+ fields correctly
- ❌ **Historical order sync** (`sync_order_from_tradestation()`) - Only captures 11 fields
- ✅ **Database schema** - Has all fields (from migration `20251201000006`)
- ✅ **Order model** - Has all fields defined
- ✅ **normalize_order()** - Function exists and extracts all fields correctly

**Problem:** `sync_order_from_tradestation()` doesn't use `normalize_order()`, manually builds order_record with only 11 fields.

---

### Q: Should we have Request/Response models for TradeStation API?

**A: YES - Models created (v1.0, 2025-12-05)**

**Created:**
- ✅ `src/models/tradestation/requests.py` - Request models
- ✅ `src/models/tradestation/responses.py` - Response models
- ✅ Complete models for orders, order groups, executions

**Why:**
1. Ensure complete data capture (30+ fields)
2. Proper Bracket/OCO order handling
3. Type safety and validation
4. Future-proofing

---

### Q: Are we properly handling Bracket/OCO orders?

**A: PARTIALLY - Working when placing, broken when syncing**

**What Works:**
- ✅ Can place Bracket orders via `place_bracket_order()`
- ✅ Can place OCO orders via `place_group_order()`
- ✅ Database has `group_id`, `group_type`, `conditional_orders` fields
- ✅ Order model has all Bracket/OCO fields

**What's Broken:**
- ❌ When syncing FROM TradeStation, group relationships are NOT captured
- ❌ `sync_order_from_tradestation()` doesn't capture:
  - `group_id` / `GroupID`
  - `group_type` (can't determine from single order)
  - `conditional_orders` (OCO relationships)
  - `parent_order_id` (Bracket relationships)
- ❌ Can't reconstruct Bracket/OCO groups from database after sync

---

## What Was Created

### 1. TradeStation API Models

**Location:** `src/models/tradestation/`

**Files:**
- `__init__.py` - Exports
- `requests.py` - Request models
- `responses.py` - Response models

**Models:**
- `TradeStationOrderRequest` - Order placement request
- `TradeStationOrderGroupRequest` - Group order request (OCO/Bracket)
- `TradeStationOrderResponse` - Complete order response (30+ fields)
- `TradeStationOrderGroupResponse` - Group order response
- `TradeStationExecutionResponse` - Execution response
- Nested models: `TradeStationOrderLeg`, `TradeStationConditionalOrder`, etc.

### 2. Analysis Documents

**Created:**
- `docs/architecture/TRADESTATION_API_DATA_COVERAGE.md` - Complete analysis
- `docs/architecture/TRADESTATION_MODELS_SUMMARY.md` - This document

**Updated:**
- `docs/architecture/SYSTEM_ARCHITECTURE.md` - Added TradeStation models section
- `docs/architecture/MISSING_MODELS_ANALYSIS.md` - Updated TradeStation section

---

## What Needs to Be Fixed

### Critical: Update `sync_order_from_tradestation()`

**Current Code (BROKEN):**
```python
# src/services/supabase/trades.py::sync_order_from_tradestation()
order_record = {
    "order_id": order_id,
    "symbol": symbol,
    "action": action,
    # ... only 11 fields
    # ❌ Missing: group_id, conditional_orders, commission_fee, etc.
}
```

**Fix: Use `normalize_order()` (ALREADY EXISTS):**
```python
from src.services.data_ingestion.mappers import normalize_order

# Normalize order data (extracts ALL 30+ fields)
normalized = normalize_order(order_data)
if not normalized:
    return None

# Use normalized data (has ALL fields)
order_record = {
    "order_id": normalized["order_id"],
    "symbol": normalized["symbol"],
    # ... all 30+ fields including:
    "group_id": normalized.get("group_id"),
    "conditional_orders": normalized.get("conditional_orders"),
    "commission_fee": normalized.get("commission_fee"),
    # ... etc
}
```

**Why This Works:**
- ✅ `normalize_order()` already extracts all fields correctly
- ✅ Used successfully in `orders_handler.py`
- ✅ Handles dict and object inputs
- ✅ Database schema already supports all fields

### High Priority: Bracket/OCO Order Reconstruction

**Add after syncing order:**
```python
# Check for group relationships
if normalized.get("group_id") or normalized.get("conditional_orders"):
    group_id = normalized.get("group_id") or normalized.get("GroupName")
    if group_id:
        # Determine group type
        conditional_orders = normalized.get("conditional_orders") or []
        group_type = self._infer_group_type(conditional_orders)
        
        # Create/update order group
        self.upsert_order_group({
            "group_id": group_id,
            "group_type": group_type,
            "orders": [order_uuid],
            "account_id": account_uuid
        })
```

---

## Field Coverage Comparison

### TradeStation API Response (30+ fields)
```json
{
  "OrderID": "12345",
  "GroupID": "abc123",           // ❌ NOT captured
  "GroupName": "OCO 123",        // ❌ NOT captured
  "ConditionalOrders": [...],    // ❌ NOT captured
  "CommissionFee": "1.20",       // ❌ NOT captured
  "UnbundledRouteFee": "0.50",   // ❌ NOT captured
  "Routing": "Intelligent",      // ❌ NOT captured
  "TrailingStop": {...},         // ❌ NOT captured
  "Legs": [...],                 // ❌ NOT captured
  "MarketActivationRules": [...], // ❌ NOT captured
  "TimeActivationRules": [...],  // ❌ NOT captured
  // ... 20+ more fields
}
```

### What We Currently Capture (11 fields)
```python
{
  "order_id": "12345",           // ✅
  "symbol": "MNQZ25",            // ✅
  "action": "BUY",               // ✅
  "quantity": 2,                 // ✅
  "order_type": "MARKET",        // ✅
  "status": "FILLED",            // ✅
  "filled_quantity": 2,           // ✅
  "average_fill_price": 25016.50, // ✅
  "placed_at": "...",            // ✅
  "filled_at": "...",             // ✅
  "account_id": "SIM123456"      // ✅
  // ❌ Missing 20+ fields
}
```

### What We Should Capture (30+ fields)
```python
{
  # All 11 fields above, PLUS:
  "group_id": "abc123",                    // ✅ Should capture
  "group_type": "OCO",                     // ✅ Should capture
  "conditional_orders": [...],              // ✅ Should capture
  "market_activation_rules": [...],         // ✅ Should capture
  "time_activation_rules": [...],           // ✅ Should capture
  "trailing_stop": {...},                   // ✅ Should capture
  "commission_fee": 1.20,                  // ✅ Should capture
  "unbundled_route_fee": 0.50,             // ✅ Should capture
  "routing": "Intelligent",                 // ✅ Should capture
  "currency": "USD",                        // ✅ Should capture
  "duration": "DAY",                        // ✅ Should capture
  "good_till_date": "...",                  // ✅ Should capture
  "status_description": "Filled",           // ✅ Should capture
  "filled_price": 25016.50,                 // ✅ Should capture
  "advanced_options": "...",                // ✅ Should capture
  "opened_date_time": "...",                // ✅ Should capture
  "closed_date_time": "...",                // ✅ Should capture
  # ... etc
}
```

---

## Next Steps

1. ✅ **DONE** - Created TradeStation API models
2. ⚠️ **TODO** - Update `sync_order_from_tradestation()` to use `normalize_order()`
3. ⚠️ **TODO** - Add Bracket/OCO order group reconstruction
4. ⚠️ **TODO** - Test with real Bracket/OCO orders
5. ⚠️ **TODO** - Verify all fields are captured

---

## Files Created/Updated

### New Files
- `src/models/tradestation/__init__.py`
- `src/models/tradestation/requests.py`
- `src/models/tradestation/responses.py`
- `docs/architecture/TRADESTATION_API_DATA_COVERAGE.md`
- `docs/architecture/TRADESTATION_MODELS_SUMMARY.md`

### Updated Files
- `src/models/__init__.py` - Added TradeStation models import
- `docs/architecture/SYSTEM_ARCHITECTURE.md` - Updated TradeStation section
- `docs/architecture/MISSING_MODELS_ANALYSIS.md` - Updated TradeStation section

---

*See `docs/architecture/TRADESTATION_API_DATA_COVERAGE.md` for complete detailed analysis.*

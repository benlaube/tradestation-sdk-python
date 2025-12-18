# File References Audit Report

## Metadata

- **Status:** Active
- **Created:** 12-05-2025
- **Last Updated:** 12-05-2025 14:02:18 EST
- **Version:** 1.0
- **Description:** Audit report documenting file reference issues, single source of truth for API structures, and recommendations for fixing unlinked references in SDK documentation
- **Type:** Audit Report - Technical reference for documentation maintenance
- **Applicability:** When reviewing documentation consistency, fixing file references, or understanding API structure sources
- **Dependencies:**
  - [`tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json) - Primary source of truth for API contract
  - [`models/`](../models/) - SDK Pydantic model implementations
  - [`API_COVERAGE.md`](./API_COVERAGE.md) - API coverage documentation (referenced in audit)
  - [`GAP_ANALYSIS.md`](./GAP_ANALYSIS.md) - Gap analysis (referenced in audit)
  - [`README.md`](../README.md) - SDK README (referenced in audit)
- **How to Use:** Reference this audit report when fixing file references in documentation, understanding the relationship between OpenAPI spec and SDK models, or reviewing documentation consistency

---

## Single Source of Truth for API Request/Response Structures

### Primary Sources

1. **OpenAPI Specification (Authoritative API Definition)**
   - **Location:** [`../tradestation-api-v3-openapi.json`](../tradestation-api-v3-openapi.json)
   - **Purpose:** Official TradeStation API v3 specification
   - **Contains:** Complete API endpoint definitions, request/response schemas, authentication requirements
   - **Status:** ✅ Single source of truth for API contract

2. **Pydantic Models (SDK Implementation)**
   - **Location:** [`../models/`](../models/)
   - **Purpose:** Type-safe Python models for SDK implementation
   - **Contains:** Request models, REST response models, streaming models
   - **Status:** ✅ Single source of truth for SDK data structures
   - **Files:**
     - [`models/orders.py`](../models/orders.py) - Order request/response models
     - [`models/order_executions.py`](../models/order_executions.py) - Execution models
     - [`models/streaming.py`](../models/streaming.py) - Streaming API models
     - [`models/accounts.py`](../models/accounts.py) - Account models
     - [`models/accounts_list.py`](../models/accounts_list.py) - Account list REST models (GET /v3/brokerage/accounts)
     - [`models/streaming.py`](../models/streaming.py) - All streaming models (quotes, orders, positions, balances)
     - [`models/positions.py`](../models/positions.py) - Position models
     - [`models/quotes.py`](../models/quotes.py) - Quote models

### Relationship

- **OpenAPI Spec** → Defines the API contract (what TradeStation API expects/returns)
- **Pydantic Models** → Implements the contract in Python (what SDK uses internally)
- **SDK Code** → Uses Pydantic models for type safety and validation

---

## File Reference Audit Results

### Issues Found

1. **Unlinked File References** - File paths mentioned without markdown links
2. **Inconsistent Naming** - References to `APIv3Endpoints.json` vs `openapi (2) (2).json`
3. **Missing Cross-References** - Documentation files not linking to each other

### Files Requiring Updates

1. [`API_COVERAGE.md`](./API_COVERAGE.md) - Line 79: `openapi (2) (2).json` needs link
2. [`GAP_ANALYSIS.md`](./GAP_ANALYSIS.md) - Line 27: `APIv3Endpoints.json` needs correction and link
3. [`API_COVERAGE.md`](./API_COVERAGE.md) - Multiple `.py` file references need links
4. [`README.md`](../README.md) - Line 1088: `APIv3Endpoints.json` needs correction and link
5. All docs - Cross-references between docs should be linked

---

## Recommendations

1. ✅ Convert all file paths to markdown links
2. ✅ Standardize OpenAPI spec filename reference
3. ✅ Add cross-links between related documentation
4. ✅ Update references to use correct file names

---

**Next Steps:** Fix all file references in documentation files to use proper markdown links.

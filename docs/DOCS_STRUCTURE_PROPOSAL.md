# Proposed Documentation Structure

## Current State

Currently, all documentation is in a flat `docs/` directory with 20+ files. This makes it difficult to find specific documentation and understand the organization.

**Current Issues:**
- Flat structure makes navigation difficult
- No clear categorization of documentation types
- Hard to find related documentation
- No clear entry points for different user types (beginners vs advanced)
- Large files (MODELS.md) could be split for better maintainability

## Proposed Structure

```
docs/
├── README.md                          # Documentation index and navigation
│
├── getting-started/                   # Getting started guides
│   ├── README.md                      # Getting started index
│   ├── installation.md                # Installation guide
│   ├── quick-start.md                 # Quick start guide
│   └── authentication.md              # Authentication setup
│
├── api/                               # API documentation
│   ├── README.md                      # API documentation index
│   ├── reference.md                   # Complete API reference (from API_REFERENCE.md)
│   ├── endpoints.md                   # Endpoint mapping (from API_ENDPOINT_MAPPING.md)
│   ├── coverage.md                    # API coverage analysis (from API_COVERAGE.md)
│   ├── operations.md                 # Operation coverage (from OPERATION_COVERAGE.md)
│   └── structure.md                  # API structure (from API_STRUCTURE.md, API_STRUCTURE_DETAILED.md)
│
├── models/                            # Model documentation
│   ├── README.md                      # Models overview (from MODELS.md)
│   ├── orders.md                      # Order models documentation
│   ├── streaming.md                   # Streaming models documentation
│   ├── accounts.md                    # Account models documentation
│   ├── positions.md                   # Position models documentation
│   └── quotes.md                      # Quote models documentation
│
├── guides/                            # How-to guides and examples
│   ├── README.md                      # Guides index
│   ├── usage-examples.md              # SDK usage examples (from SDK_USAGE_EXAMPLES.md)
│   ├── code-examples.md               # OpenAPI code examples (from OPENAPI_CODE_EXAMPLES.md)
│   ├── order-functions.md             # Order functions reference (from ORDER_FUNCTIONS_REFERENCE.md)
│   └── submodule-integration.md       # Submodule integration (from SUBMODULE_INTEGRATION.md)
│
├── architecture/                     # Architecture and design docs
│   ├── README.md                      # Architecture index
│   ├── overview.md                    # SDK architecture (from TRADESTATIONSDK_ARCHITECTURE.md)
│   ├── feature-comparison.md         # Feature comparison (from FEATURE_COMPARISON.md)
│   └── gap-analysis.md                # Gap analysis (from GAP_ANALYSIS.md)
│
├── reference/                         # Reference materials
│   ├── README.md                      # Reference index
│   ├── functions-list.md              # SDK functions list (from SDK_FUNCTIONS_LIST.md)
│   ├── new-functions.md               # New functions summary (from NEW_FUNCTIONS_SUMMARY.md)
│   ├── trailing-stops.md              # Trailing stop variations (from TRAILING_STOP_VARIATIONS.md)
│   └── audit-references.md            # Audit file references (from AUDIT_FILE_REFERENCES.md)
│
└── analysis/                          # Analysis and research docs
    ├── README.md                      # Analysis index
    ├── openapi-analysis.md            # OpenAPI analysis (from OPENAPI_ANALYSIS_SUMMARY.md)
    └── roadmap.md                     # Development roadmap (from ROADMAP.md)
```

## Migration Plan

### Phase 1: Create Structure
1. Create new directory structure
2. Create README.md files for each section
3. Move files to appropriate locations

### Phase 2: Update Content
1. Split large files (MODELS.md → models/*.md)
2. Update cross-references
3. Add navigation links

### Phase 3: Update Indexes
1. Update main README.md with new structure
2. Update INDEX.md to point to new locations
3. Update all internal links

## Benefits

1. **Better Organization** - Related docs grouped together by purpose
2. **Easier Navigation** - Clear hierarchy with README files as entry points
3. **Scalability** - Easy to add new docs in appropriate sections without cluttering
4. **Discoverability** - Users can find docs by category (getting started, API, models, etc.)
5. **Maintainability** - Easier to keep docs organized and up-to-date
6. **User Experience** - Clear paths for different user types (beginners → getting-started/, developers → api/, model users → models/)
7. **Reduced File Size** - Split large files (MODELS.md) into domain-specific files
8. **Better Cross-Referencing** - Related docs are closer together, easier to link

## Implementation Priority

**Phase 1 (High Priority):**
- Create directory structure
- Move files to appropriate locations
- Create README.md files for each section
- Update main docs/README.md

**Phase 2 (Medium Priority):**
- Split MODELS.md into domain-specific files
- Update cross-references throughout documentation
- Add navigation links between related docs

**Phase 3 (Low Priority):**
- Add diagrams and visual aids
- Enhance examples with more use cases
- Add search functionality (if needed)

## File Mapping

| Current File | Proposed Location |
|-------------|-------------------|
| GETTING_STARTED.md | getting-started/README.md |
| API_REFERENCE.md | api/reference.md |
| API_ENDPOINT_MAPPING.md | api/endpoints.md |
| API_COVERAGE.md | api/coverage.md |
| OPERATION_COVERAGE.md | api/operations.md |
| API_STRUCTURE.md | api/structure.md |
| API_STRUCTURE_DETAILED.md | api/structure.md (merge) |
| MODELS.md | models/README.md |
| SDK_USAGE_EXAMPLES.md | guides/usage-examples.md |
| OPENAPI_CODE_EXAMPLES.md | guides/code-examples.md |
| ORDER_FUNCTIONS_REFERENCE.md | guides/order-functions.md |
| SUBMODULE_INTEGRATION.md | guides/submodule-integration.md |
| TRADESTATIONSDK_ARCHITECTURE.md | architecture/overview.md |
| FEATURE_COMPARISON.md | architecture/feature-comparison.md |
| GAP_ANALYSIS.md | architecture/gap-analysis.md |
| SDK_FUNCTIONS_LIST.md | reference/functions-list.md |
| NEW_FUNCTIONS_SUMMARY.md | reference/new-functions.md |
| TRAILING_STOP_VARIATIONS.md | reference/trailing-stops.md |
| AUDIT_FILE_REFERENCES.md | reference/audit-references.md |
| OPENAPI_ANALYSIS_SUMMARY.md | analysis/openapi-analysis.md |
| ROADMAP.md | analysis/roadmap.md |
| INDEX.md | README.md (update) |
| README.md | README.md (keep, update) |

## Model Documentation Status

**Current State:** All models are documented in `docs/MODELS.md` (single file)

**Proposed State:** Split into domain-specific files:
- `models/README.md` - Overview and quick reference
- `models/orders.md` - Order models (from MODELS.md section)
- `models/streaming.md` - Streaming models
- `models/accounts.md` - Account models
- `models/positions.md` - Position models
- `models/quotes.md` - Quote models

**Status Check:**
- ✅ All models are documented in MODELS.md
- ❌ Models are NOT split into individual files (proposed)
- ✅ Model source code has docstrings
- ✅ Models have README.md in models/ directory (just created)

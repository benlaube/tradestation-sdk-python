# TradeStation SDK Documentation

## Metadata

- **Version:** 1.1
- **Last Updated:** 12-28-2025 EST
- **Type:** Documentation Index
- **Status:** Active
- **Description:** Main documentation index and navigation hub for TradeStation SDK documentation
- **Related Documents:**
  - [Main README](../README.md) - SDK overview and quick start
  - [Quick Start Guide](../QUICKSTART.md) - 2-minute quick start

---

## Documentation Index

Welcome to the TradeStation SDK documentation. This directory contains comprehensive documentation organized by category.

### Quick Navigation

| Category | Description | Entry Point |
|----------|-------------|-------------|
| 🚀 **Getting Started** | Installation, quick start, authentication | [Getting Started](getting-started/README.md) |
| 📚 **API Reference** | Complete API documentation | [API Documentation](api/README.md) |
| 🏗️ **Models** | Pydantic model documentation | [Models Documentation](models/README.md) |
| 💡 **Guides** | How-to guides and examples | [Guides & Examples](guides/README.md) |
| 🏛️ **Architecture** | System architecture and design | [Architecture](architecture/README.md) |
| 📖 **Reference** | Quick reference materials | [Reference Materials](reference/README.md) |
| 🔬 **Analysis** | Analysis and research docs | [Analysis & Research](analysis/README.md) |

---

## Documentation Sections

### 🚀 Getting Started

**For new users:** Start here to learn how to use the SDK.

- **[Getting Started Tutorial](getting-started/README.md)** - 15-minute comprehensive tutorial
- **[Installation Guide](../INSTALLATION.md)** - Detailed installation instructions
- **[Quick Start Guide](../QUICKSTART.md)** - 2-minute quick start

### 📚 API Documentation

**Complete API reference and endpoint documentation.**

- **[API Reference](api/reference.md)** - Complete API reference with all methods
- **[Endpoint Mapping](api/endpoints.md)** - SDK methods → API endpoints mapping
- **[API Coverage](api/coverage.md)** - Endpoint coverage analysis
- **[Operation Coverage](api/operations.md)** - Operation coverage analysis
- **[API Structure](api/structure.md)** - Visual diagrams of API structure

### 🏗️ Models Documentation

**Pydantic model documentation and field coverage.**

- **[Models Overview](models/README.md)** - Complete model documentation and field coverage
- **[Models Source Code](../models/)** - Model implementations with docstrings
- **[Models README](../models/README.md)** - Models directory overview

### 💡 Guides & Examples

**How-to guides, code examples, and integration instructions.**

- **[Usage Examples](guides/usage-examples.md)** - SDK usage examples with code
- **[Code Examples](guides/code-examples.md)** - OpenAPI code examples
- **[Order Functions](guides/order-functions.md)** - Order function reference
- **[Submodule Integration](guides/submodule-integration.md)** - Git submodule workflow

### 🏛️ Architecture

**System architecture, design decisions, and comparisons.**

- **[SDK Architecture Overview](architecture/overview.md)** - Complete SDK architecture
- **[Feature Comparison](architecture/feature-comparison.md)** - Comparison with other SDKs
- **[Gap Analysis](architecture/gap-analysis.md)** - Missing features analysis

### 📖 Reference Materials

**Quick reference materials and technical references.**

- **[SDK Functions List](reference/functions-list.md)** - Complete function list (includes [New Functions section](reference/functions-list.md#new-functions))
- **[Trailing Stop Variations](reference/trailing-stops.md)** - Trailing stop options
- **[Audit File References](reference/audit-references.md)** - Audit documentation links

### 🔬 Analysis & Research

**Analysis documents, research, and development planning.**

- **[OpenAPI Analysis](analysis/openapi-analysis.md)** - OpenAPI specification analysis
- **[Development Roadmap](analysis/roadmap.md)** - Future development plans

---

## Documentation Structure

```
docs/
├── README.md                    # This file (documentation index)
├── getting-started/             # Getting started guides
│   └── README.md               # Getting started index
├── api/                        # API documentation
│   ├── README.md               # API documentation index
│   ├── reference.md            # Complete API reference
│   ├── endpoints.md            # Endpoint mapping
│   ├── coverage.md            # API coverage analysis
│   ├── operations.md          # Operation coverage
│   └── structure.md           # API structure diagrams
├── models/                     # Model documentation
│   └── README.md              # Models overview
├── guides/                     # How-to guides
│   ├── README.md              # Guides index
│   ├── usage-examples.md      # Usage examples
│   ├── code-examples.md       # Code examples
│   ├── order-functions.md     # Order functions
│   └── submodule-integration.md # Submodule integration
├── architecture/              # Architecture docs
│   ├── README.md              # Architecture index
│   ├── overview.md            # SDK architecture
│   ├── feature-comparison.md  # Feature comparison
│   └── gap-analysis.md        # Gap analysis
├── reference/                 # Reference materials
│   ├── README.md              # Reference index
│   ├── functions-list.md      # Functions list (includes new functions)
│   ├── trailing-stops.md     # Trailing stops
│   └── audit-references.md   # Audit references
└── analysis/                  # Analysis & research
    ├── README.md              # Analysis index
    ├── openapi-analysis.md    # OpenAPI analysis
    └── roadmap.md             # Development roadmap
```

---

## Related Documentation

### Main SDK Documentation

- **[Main README](../README.md)** - Complete SDK overview and quick start
- **[Quick Start Guide](../QUICKSTART.md)** - 2-minute quick start
- **[Installation Guide](../INSTALLATION.md)** - Installation instructions
- **[Cheat Sheet](../CHEATSHEET.md)** - Quick reference
- **[Limitations](../LIMITATIONS.md)** - Known constraints
- **[Security Guide](../SECURITY.md)** - Security best practices

### Source Code Documentation

- **[Models Source Code](../models/)** - Pydantic model implementations
- **[Models README](../models/README.md)** - Models directory overview
- **[Examples](../examples/)** - Jupyter notebooks and code examples
- **[CLI Tools](../cli/)** - Command-line tools

---

## Finding Documentation

**New to the SDK?**
1. Start with [Getting Started](getting-started/README.md)
2. Read [Quick Start Guide](../QUICKSTART.md)
3. Review [Usage Examples](guides/usage-examples.md)

**Looking for API methods?**
- Use [API Reference](api/reference.md) - Complete method reference
- Check [SDK Functions List](reference/functions-list.md) - Alphabetical list

**Understanding models?**
- See [Models Overview](models/README.md) - Complete model documentation
- Review [Models Source Code](../models/) - Implementation details

**Architecture questions?**
- Read [SDK Architecture Overview](architecture/overview.md)
- Check [API Structure](api/structure.md) - Visual diagrams

---

## Documentation Standards

All documentation follows these standards:
- **Metadata:** All files include version, last updated, type, and description
- **Diagrams:** All diagrams use Mermaid format
- **Cross-References:** Related documents are linked
- **Examples:** Code examples are provided where applicable

See [Documentation Structure Proposal](DOCS_STRUCTURE_PROPOSAL.md) for complete organization details.

---

**Last Updated:** 12-28-2025 EST
**Documentation Version:** 1.1

# TradeStation SDK Changelog

## About This Document

This changelog tracks **all notable changes** to the TradeStation SDK, including new features, bug fixes, breaking changes, and improvements. Entries are organized by date with detailed descriptions of what changed and why.

**Use this if:** You want to see what's new, track version history, or understand breaking changes between versions.

**Related Documents:**
- 📖 **[README.md](README.md)** - Complete SDK documentation
- 🗺️ **[docs/ROADMAP.md](docs/ROADMAP.md)** - Future plans and upcoming features
- ⚠️ **[LIMITATIONS.md](LIMITATIONS.md)** - Known issues and planned fixes
- 🔄 **[MIGRATION.md](MIGRATION.md)** - Migration guide for version upgrades

**Note:** This changelog tracks SDK-specific changes. For project-wide changes, see the root `CHANGELOG.md`.

---

All notable changes to the internal TradeStation SDK (`src/lib/tradestation/`) will be documented in this file.

This changelog tracks SDK-specific changes including:
- API endpoint implementations and updates
- Model changes and additions
- Mapper updates
- Documentation updates
- Error handling improvements
- Authentication and session management changes
- Streaming functionality updates

---

## 2025-12-29 - Code Structure Reorganization & Comprehensive Normalization Functions

**Highlights**
- ✅ Major code reorganization: Operations and utilities moved to dedicated subpackages
- ✅ Added 6 new normalization functions for all major data models
- ✅ Complete MarketDataOperations documentation added to API reference
- ✅ All file moves preserved git history through proper renames

**Added**
- `normalize_quote()` - Normalize quote snapshot data to consistent snake_case dictionary format
- `normalize_execution()` - Normalize execution/fill data to consistent snake_case dictionary format
- `normalize_account()` - Normalize account summary to consistent snake_case dictionary format
- `normalize_balances()` - Normalize balance detail to consistent snake_case dictionary format
- `normalize_account_balances()` - Normalize account balances response wrapper to consistent format
- `normalize_bod_balance()` - Normalize beginning-of-day balance entries to consistent format
- Helper utility functions: `_get_value()`, `_to_float()`, `_to_int()` for robust data extraction
- `operations/` subpackage with dedicated `__init__.py` for domain-specific operations
- `utils/` subpackage with dedicated `__init__.py` for shared utilities

**Changed**
- **Code Structure Reorganization:**
  - Moved all operation modules to `operations/` directory:
    - `accounts.py` → `operations/accounts.py`
    - `market_data.py` → `operations/market_data.py`
    - `order_executions.py` → `operations/order_executions.py`
    - `orders.py` → `operations/orders.py`
    - `positions.py` → `operations/positions.py`
    - `streaming.py` → `operations/streaming.py`
  - Moved all utility modules to `utils/` directory:
    - `client.py` → `utils/client.py`
    - `logger.py` → `utils/logger.py`
    - `mappers.py` → `utils/mappers.py`
- **Import Path Updates:**
  - Updated `__init__.py` to import from `operations/` and `utils/` subpackages
  - Updated all operation modules to use relative imports (`..utils.client`, `..utils.logger`)
  - Updated `session.py` to import from `utils.logger`
  - All imports maintain backward compatibility through proper package structure
- **Documentation:**
  - Added complete `MarketDataOperations` method documentation to `docs/api/reference.md`:
    - Options methods: `get_option_expirations()`, `get_option_strikes()`, `get_option_spread_types()`, `get_option_risk_reward()`
    - Streaming methods: `stream_quotes()`, `stream_bars()`, `stream_option_chains()`, `stream_option_quotes()`, `stream_market_depth_quotes()`, `stream_market_depth_aggregates()`
    - Additional methods: `get_futures_index_symbols()`, `get_symbol_details()`, `get_crypto_symbol_names()`
  - Updated `docs/guides/data-transformation.md` with comprehensive normalizer coverage section
  - Updated `docs/reference/functions-list.md` with all new normalizers (utilities count: 4 → 10)
  - Updated all architecture documentation (`overview.md`, `gap-analysis.md`) with new file paths
  - Updated `README.md`, `CONTRIBUTING.md`, `FINAL_STATUS.md` directory structure sections

**Fixed**
- `.DS_Store` files now properly ignored via `.gitignore` update

**Documentation**
- `docs/api/reference.md` - Version updated to 1.1.0, added complete MarketDataOperations documentation
- `docs/guides/data-transformation.md` - Version updated to 1.0.1, added mapper coverage section
- `docs/reference/functions-list.md` - Updated with all new normalizers and utility count
- `docs/architecture/overview.md` - Updated all file path references to new structure
- `docs/architecture/gap-analysis.md` - Updated SDK implementation paths
- `docs/guides/order-functions.md` - Updated file path references
- `README.md` - Updated directory structure section
- `CONTRIBUTING.md` - Updated directory structure section
- `FINAL_STATUS.md` - Updated source code directory listing

**Files Modified**
- ✅ `operations/__init__.py` (new) - Package initialization for operations subpackage
- ✅ `operations/accounts.py` (moved from root) - Updated imports
- ✅ `operations/market_data.py` (moved from root) - Updated imports
- ✅ `operations/order_executions.py` (moved from root) - Updated imports
- ✅ `operations/orders.py` (moved from root) - Updated imports
- ✅ `operations/positions.py` (moved from root) - Updated imports
- ✅ `operations/streaming.py` (moved from root) - Updated imports
- ✅ `utils/__init__.py` (new) - Package initialization for utils subpackage
- ✅ `utils/client.py` (moved from root) - Updated relative imports
- ✅ `utils/logger.py` (moved from root) - No changes needed
- ✅ `utils/mappers.py` (moved from root) - Added 6 new normalization functions + helpers
- ✅ `__init__.py` - Updated imports to use operations/ and utils/ subpackages
- ✅ `session.py` - Updated import to use `utils.logger`
- ✅ `.gitignore` - Added `.DS_Store` and `*.DS_Store` patterns
- ✅ `docs/api/reference.md` - Complete MarketDataOperations documentation, version 1.1.0
- ✅ `docs/guides/data-transformation.md` - Normalizer coverage section, version 1.0.1
- ✅ `docs/reference/functions-list.md` - Updated utilities count and normalizer entries
- ✅ `docs/architecture/overview.md` - Updated file path references
- ✅ `docs/architecture/gap-analysis.md` - Updated SDK implementation paths
- ✅ `docs/guides/order-functions.md` - Updated file path references
- ✅ `README.md` - Updated directory structure
- ✅ `CONTRIBUTING.md` - Updated directory structure
- ✅ `FINAL_STATUS.md` - Updated source code listing
- ✅ `CHANGELOG.md` - Added this entry

---

## [1.0.1] - 2025-12-28

**Highlights**
- ✅ Token storage: Optional keychain/secret-service integration with secure file fallback
- ✅ OAuth port: Automatic port selection (8888-8898 range) to prevent conflicts
- ✅ HTTP client: Async support with httpx (optional, backward compatible)
- ✅ Security: Improved token file permissions and directory security

**Added**
- Token storage keychain integration (macOS Keychain, Linux Secret Service, Windows Credential Manager)
- Configurable token storage via `TRADESTATION_TOKEN_STORAGE` environment variable
- Custom token directory support via `TRADESTATION_TOKEN_DIR` environment variable
- Automatic OAuth port selection with fallback range 8888-8898
- OAuth port override via `TRADESTATION_OAUTH_PORT` environment variable
- Async HTTP client support using httpx (opt-in via `use_async=True` or `TRADESTATION_USE_ASYNC=true`)
- `make_request_async()` method for async API operations
- `aclose()` method for async client cleanup

**Changed**
- Token storage directory permissions automatically set to `chmod 700` (owner access only)
- Token file permissions automatically set to `chmod 600` (owner read/write only)
- Improved OAuth port conflict handling with automatic fallback
- Enhanced error messages for port conflicts and token storage issues

**Fixed**
- OAuth authentication no longer fails when default port (8888) is in use
- **Critical:** OAuth redirect_uri now automatically updates to match auto-selected port (prevents redirect_uri_mismatch errors)
- Token storage security improved with automatic permission restrictions
- Better error handling for token storage operations

**Documentation**
- Updated `LIMITATIONS.md` to reflect v1.0.1 improvements (items 1-3 resolved)
- Updated `API_REFERENCE.md` to clarify SDK API vs TradeStation API endpoints
- Added async usage examples and configuration documentation
- Updated `SECURITY.md` with keychain storage instructions

**Files Modified**
- ✅ `session.py` - Token storage keychain support, OAuth port auto-selection
- ✅ `client.py` - Async HTTP client support with httpx
- ✅ `config.py` - Added async client configuration
- ✅ `__init__.py` - SDK initialization with async support
- ✅ `LIMITATIONS.md` - Updated to reflect fixes
- ✅ `CHANGELOG.md` - Added v1.0.1 entry
- ✅ `docs/API_REFERENCE.md` - Clarified scope
- ✅ `pyproject.toml` - Version bump to 1.0.1

---

## 2025-12-18 - Submodule Workflow, Docstrings, Security Hardening

**Highlights**
- Added a dedicated git submodule integration guide (`docs/SUBMODULE_INTEGRATION.md`) and linked it from `README.md`, `INSTALLATION.md`, and the docs index for discoverability.
- Ensured 100% docstring coverage by documenting nested streaming helpers (`run_stream`) and test fixtures to comply with coding standards.
- Expanded high-level SDK façade (`TradeStationSDK`) docstrings to fully describe arguments/returns for all public methods.
- Strengthened streaming/session documentation (retry/health/OAuth side effects) and preserved raw account balance fields when Pydantic strips extras (fixes balance parsing tests).
- Added a vendored-installation option to `INSTALLATION.md` for teams pinning the SDK inside other repositories.

**Files Modified**
- ✅ `docs/SUBMODULE_INTEGRATION.md` (new)
- ✅ `docs/INDEX.md`
- ✅ `INSTALLATION.md`
- ✅ `README.md`
- ✅ `market_data.py`, `orders.py`, `positions.py`, `streaming.py`, `session.py`, `accounts.py`, `tests/conftest.py`

---

## 2025-12-09 - REST API Retry Logic Implementation

**Major Enhancement:** Added built-in retry logic with exponential backoff for all REST API methods.

### Retry Logic Features

**Automatic Retry for Recoverable Errors:**
- ✅ Network errors (connection timeouts, DNS failures)
- ✅ Rate limit errors (429) with server Retry-After header support
- ✅ Server errors (500+) - temporary failures
- ❌ Non-recoverable errors (401, 403, 400, 404) are not retried

**Configuration:**
- Default max retries: 3 attempts
- Default initial retry delay: 1.0 seconds
- Default max retry delay: 60.0 seconds
- Retry enabled by default (can be disabled)

**Smart Error Handling:**
- Categorizes errors as `RecoverableError` or `NonRecoverableError`
- Exponential backoff: 1s → 2s → 4s → 8s → ... (up to max delay)
- Rate limit errors respect server `Retry-After` header when available
- Automatic token refresh before retry attempts

**Comprehensive Logging:**
- Logs all retry attempts with context (attempt number, error type, backoff delay)
- Logs final failure after max retries exceeded
- Structured logging with source, action, and component tags

**Implementation Details:**
- Added `_make_request_internal()` method for core request logic
- Modified `make_request()` to wrap requests with retry logic
- Added retry configuration parameters to `HTTPClient.__init__()`
- Backward compatible: all parameters optional with sensible defaults

**Files Modified:**
- ✅ `client.py` - Added retry logic to HTTPClient class
- ✅ `LIMITATIONS.md` - Updated to reflect retry logic implementation
- ✅ `CHANGELOG.md` - This entry

**Usage:**
```python
from tradestation_sdk import TradeStationSDK

# Default retry behavior (3 retries, 1s initial delay)
sdk = TradeStationSDK()
account = sdk.get_account_info(mode="PAPER")  # Automatically retries on recoverable errors

# Custom retry configuration
sdk._client.max_retries = 5
sdk._client.retry_delay = 2.0
sdk._client.max_retry_delay = 120.0
sdk._client.enable_retry = True  # or False to disable
```

**Note:** Streaming methods already had retry logic via `_with_retry()`. This implementation adds the same robust retry logic to REST API methods for consistency.

---

## 2025-12-09 - Package Rename & Final Organization

**Enhancement:** Renamed package to `tradestation-python-sdk` and consolidated documentation for better organization.

### Package Rename

**Package Name Change:**
- From: `tradestation-sdk`
- To: `tradestation-python-sdk`

**Reason:** More natural language ("TradeStation Python SDK"), better grouping with other TradeStation packages on PyPI, more professional.

**Files Updated (17):**
- ✅ pyproject.toml - Package name and all GitHub URLs
- ✅ setup.py - Package name and all GitHub URLs
- ✅ README.md - Badge, install commands, GitHub URLs
- ✅ QUICKSTART.md - Install commands, GitHub URLs
- ✅ INSTALLATION.md - All pip/git commands and URLs
- ✅ MIGRATION.md - Install commands and GitHub URLs
- ✅ CONTRIBUTING.md - Git clone and GitHub URLs
- ✅ DEPLOYMENT.md - Install commands and GitHub URLs
- ✅ LIMITATIONS.md - GitHub URLs
- ✅ CHEATSHEET.md - GitHub URLs
- ✅ RELEASE_CHECKLIST.md - Install commands and GitHub URLs
- ✅ docs/GETTING_STARTED.md - Install commands and URLs
- ✅ docs/ROADMAP.md - GitHub URLs
- ✅ docs/INDEX.md - GitHub URLs, updated file references
- ✅ examples/README.md - GitHub URLs
- ✅ examples/01_authentication.ipynb - Install command
- ✅ __init__.py - Fixed info() method bug

**Import Name Preserved:**
- Package: `tradestation-python-sdk` (new)
- Import: `tradestation_sdk` (unchanged)
- All Python code continues to work without modification

### File Consolidation

**Moved to .cursor/ (internal documentation):**
- IMPROVEMENTS_SUMMARY.md → .cursor/IMPROVEMENTS_SUMMARY.md
- SDK_TRANSFORMATION_COMPLETE.md → .cursor/SDK_TRANSFORMATION_COMPLETE.md

**Moved to docs/ (better organization):**
- ROADMAP.md → docs/ROADMAP.md
- GETTING_STARTED.md → docs/GETTING_STARTED.md

**Result:**
- Root directory: 23 → 12 .md files (48% reduction)
- Better organized and less overwhelming
- Internal docs separated from user-facing docs

### Bug Fixes

**Fixed info() Method:**
- Issue: Called non-existent `has_valid_tokens()` method on TokenManager
- Fix: Changed to use existing `get_tokens()` method with None check
- Verified: Import and info() method working correctly

### Documentation Updates

**Updated all references to moved files:**
- docs/INDEX.md - Added ROADMAP and GETTING_STARTED to learning path
- README.md - Updated quick links table
- All cross-references updated

**New Documentation:**
- .cursor/PACKAGE_NAME_UPDATE_COMPLETE.md - Consolidation and rename summary
- FINAL_STATUS.md - Comprehensive final status report

---

## 2025-12-07 - Plug-and-Play SDK Enhancement

**Major Enhancement:** Comprehensive improvements to make SDK plug-and-play for external users, including package distribution, documentation enhancements, examples, CLI tools, and more.

### Distribution & Installation

**Package Distribution:**
- ✅ Added `pyproject.toml` for modern Python packaging
- ✅ Added `setup.py` for backward compatibility
- ✅ Added `LICENSE` file (MIT License)
- ✅ Added installation instructions for pip, source, and development
- ✅ Defined dependencies, optional dependencies (dev, examples)
- ✅ Configured pytest, black, ruff, and coverage tools

### Documentation Enhancements

**README.md Updates:**
- ✅ Added comprehensive "Quick Start (5 Minutes)" guide with step-by-step instructions
- ✅ Added "FAQ & Troubleshooting" section with 8+ common issues and solutions
- ✅ Added "API Rate Limits" section with best practices and retry examples
- ✅ Added "Known Limitations" section with 8+ limitations and workarounds
- ✅ Enhanced Installation section with multiple installation methods
- ✅ Improved navigation with updated table of contents

**New Documentation Files:**
- ✅ Created `LIMITATIONS.md` - Comprehensive known limitations document (13+ limitations with solutions)
- ✅ Enhanced existing documentation structure

### Examples & Learning Resources

**Jupyter Notebooks:**
- ✅ Created `examples/` directory with README
- ✅ Added `01_authentication.ipynb` - Interactive authentication tutorial
- ✅ Added `quick_start.py` - Standalone quick start script
- ✅ Documented example usage patterns

**CLI Testing Tools:**
- ✅ Created `cli/` directory with README
- ✅ Added `test_auth.py` - Authentication testing tool
- ✅ Added `test_connection.py` - Comprehensive connection test (6 test categories)
- ✅ All CLI tools support PAPER and LIVE modes
- ✅ Exit codes for automation support (0 = success, 1 = failure)

### SDK Features

**New Methods:**
- ✅ Added `info()` method to TradeStationSDK - Get SDK information and diagnostics
  - Returns version, API version, authenticated modes, active mode, features, etc.
  - Useful for debugging and verifying SDK setup

**Feature Improvements:**
- ✅ Enhanced error messages in all exception types
- ✅ Improved docstrings for all public-facing methods
- ✅ Better type hints and return value documentation

### Developer Experience

**Setup & Configuration:**
- ✅ Documented environment variable setup
- ✅ Added `.env.example` patterns
- ✅ Improved credential verification instructions

**Troubleshooting:**
- ✅ Port conflict solutions (OAuth callback)
- ✅ Authentication failure diagnostics
- ✅ Token expiration handling
- ✅ Symbol search tips (expired contracts)
- ✅ Rate limit management strategies
- ✅ Module import error solutions
- ✅ Streaming connection recovery

**Known Limitations Documented:**
1. Token storage security (plain JSON)
2. OAuth port conflicts
3. Synchronous HTTP client (blocking I/O)
4. No built-in request retry logic
5. Bar data interval constraints (minute-only)
6. Trailing stop units (points, not dollars)
7. Account ID resolution (multi-account)
8. HTTP Streaming vs WebSocket
9. Concurrent stream limits (~10)
10. API rate limits
11. Python 3.10+ requirement
12. OS compatibility notes
13. Error message inconsistency (edge cases)

**Roadmap Published:**
- v1.1 (Q1 2026): Token encryption, auto-port selection, improved error messages
- v1.2 (Q2 2026): Built-in retry logic, rate limit tracking, circuit breaker pattern
- v2.0 (Q3 2026): Native async support, connection pooling, WebSocket support

### Testing & Validation

**CLI Test Suite:**
- ✅ `test_auth.py` - Authentication and token management
- ✅ `test_connection.py` - Comprehensive 6-test validation:
  1. Authentication
  2. Account information
  3. Account balances
  4. Market data (symbol search, quotes, bars)
  5. Order queries (history, current orders)
  6. Position queries

**Test Features:**
- Exit codes for automation
- Color-coded output (✅❌⚠️)
- Detailed error reporting
- Mode selection (PAPER/LIVE)
- Safety warnings for LIVE mode

### Files Added

**Distribution:**
- `pyproject.toml` - Modern Python packaging configuration
- `setup.py` - Backward compatibility setup script
- `LICENSE` - MIT License file

**Documentation:**
- `LIMITATIONS.md` - Comprehensive known limitations (13+ items)
- `examples/README.md` - Examples directory overview
- `cli/README.md` - CLI tools documentation

**Examples:**
- `examples/01_authentication.ipynb` - Interactive auth tutorial
- `examples/quick_start.py` - Standalone quick start script

**CLI Tools:**
- `cli/test_auth.py` - Authentication testing
- `cli/test_connection.py` - Comprehensive connection test

### Migration Notes

**For Existing Users:**
- No breaking changes - all existing code continues to work
- New `info()` method provides SDK diagnostics
- Enhanced documentation for better troubleshooting
- CLI tools available for testing and validation

**For New Users:**
- Follow "Quick Start (5 Minutes)" guide in README
- Use CLI tools to verify setup
- Check LIMITATIONS.md for known constraints
- Explore Jupyter notebooks for learning

### Dependencies Updated

**Core Dependencies** (unchanged):
- httpx>=0.27.2
- PyJWT>=2.8.0
- pydantic>=2.12.5

**New Dependencies:**
- python-dotenv>=1.0.0 (for .env file support)

**Optional Dependencies:**
- dev: pytest, black, ruff, coverage tools
- examples: jupyter, notebook, matplotlib, pandas

### Metadata

- **SDK Version:** 1.0.0 (unchanged, enhancements are additive)
- **Release Date:** 2025-12-07
- **Python Requirement:** >=3.10
- **License:** MIT
- **Status:** Production Ready (Beta - external distribution)

---

## 2025-12-05 - Stream Reliability & Automatic Reconnection

**Major Enhancement:** Added comprehensive stream reliability features to all streaming methods, including automatic reconnection, retry logic, session recovery, REST polling fallback, and stream health tracking.

### Code Changes

**StreamingManager Enhancements (`streaming.py`):**
- ✅ **Generic Retry Wrapper:** Added `_with_retry()` method that wraps any async generator with automatic reconnection, retry logic, health tracking, and session recovery
- ✅ **Automatic Reconnection:** All streaming methods (`stream_quotes`, `stream_orders`, `stream_positions`, `stream_balances`, `stream_orders_by_ids`) now include automatic reconnection with exponential backoff
- ✅ **Session Auto-Recovery:** Added `_ensure_session()` method that automatically refreshes tokens and recreates sessions before streaming
- ✅ **REST Polling Fallback:** Added `_poll_quotes_rest()`, `_poll_orders_rest()`, `_poll_positions_rest()` methods for automatic fallback when HTTP streaming fails
- ✅ **Stream Health Tracking:** Added `StreamHealth` dataclass and `get_stream_health()` method to monitor stream reliability metrics
- ✅ **Error Categorization:** Integrated with `RecoverableError` and `NonRecoverableError` for smart retry logic

**New Parameters for All Streaming Methods:**
- `max_retries: int = 10` - Maximum number of retry attempts
- `retry_delay: float = 1.0` - Initial retry delay in seconds
- `max_retry_delay: float = 60.0` - Maximum retry delay in seconds
- `auto_reconnect: bool = True` - Enable automatic reconnection on errors
- `fallback_to_polling: bool = True` - Enable REST polling fallback (quotes, orders, positions)
- `polling_interval: float = 1.0` - Interval for REST polling in seconds

**Exception Enhancements (`exceptions.py`):**
- ✅ Added `RecoverableError` exception for errors that can be retried (network, temporary failures)
- ✅ Added `NonRecoverableError` exception for errors that should not be retried (authentication, invalid request)

**HTTPClient Updates (`client.py`):**
- ✅ Updated error categorization to raise `RecoverableError` or `NonRecoverableError` based on error type
- ✅ Network errors (connection timeouts, DNS failures) → `RecoverableError`
- ✅ Server errors (500+ status codes) → `RecoverableError`
- ✅ Rate limit errors (429) → `RecoverableError` (can retry after backoff)
- ✅ Authentication errors (401, 403) → `NonRecoverableError`
- ✅ Invalid request errors (400) → `NonRecoverableError`
- ✅ Not found errors (404) → `NonRecoverableError`

### Benefits

- **Automatic Reliability:** SDK handles all stream reliability concerns automatically - no manual retry logic needed
- **Better Error Handling:** Smart retry logic only retries recoverable errors, fails fast on non-recoverable errors
- **Session Management:** Automatic token refresh and session recreation - no manual session recovery needed
- **REST Fallback:** Seamless fallback to REST polling when HTTP streaming fails - ensures continuous data flow
- **Observability:** Stream health tracking provides visibility into stream reliability and performance
- **Simplified Consumers:** Data ingestion handlers can focus on business logic instead of stream reliability

### Usage Example

```python
from src.lib.tradestation import TradeStationSDK

sdk = TradeStationSDK()
sdk.ensure_authenticated(mode="PAPER")

# SDK handles reconnection, retry, and fallback automatically
async for quote in sdk.streaming.stream_quotes(
    ["MNQZ25"],
    mode="PAPER",
    auto_reconnect=True,      # Automatic reconnection on errors
    fallback_to_polling=True  # REST polling fallback if streaming fails
):
    print(f"{quote.Symbol}: {quote.Last}")

# Monitor stream health
health = sdk.streaming.get_stream_health("quotes")
if health:
    print(f"Messages: {health.message_count}, Errors: {health.error_count}")
    print(f"Is Healthy: {health.is_healthy}")
```

### Breaking Changes

None - All changes are backward compatible. Existing code continues to work, and new reliability features are enabled by default with sensible defaults.

---

## 2025-12-05 14:58 - Default Mode & Account ID Inheritance from SDK Instance

**Enhancement:** SDK now stores default `mode` and `account_id` at the instance level, allowing cleaner API calls without passing these parameters every time.

### Code Changes

**SDK Instance Defaults:**
- Added `self.default_mode = secrets.trading_mode` to `TradeStationSDK.__init__()`
- `active_mode` property now updates `default_mode` to match the last authenticated mode
- Users authenticate one mode at a time, so the last authenticated mode becomes the default

**Operation Classes Updated:**
- `AccountOperations`: Added `default_mode` parameter to `__init__()`, uses instance default when `mode=None`
- `OrderOperations`: Added `default_mode` parameter to `__init__()`, uses instance default when `mode=None`
- `PositionOperations`: Added `default_mode` parameter to `__init__()`, uses instance default when `mode=None`
- `OrderExecutionOperations`: Added `default_mode` parameter to `__init__()`, uses instance default when `mode=None`

**Function Updates:**
- All functions in `AccountOperations`, `OrderOperations`, `PositionOperations`, and `OrderExecutionOperations` now use `self.default_mode` when `mode=None` is passed
- Updated docstrings to reflect: "If None, uses instance default_mode (from SDK initialization or last authenticated mode)"
- Removed redundant `if mode is None: mode = secrets.trading_mode` patterns in favor of instance defaults

**SDK Initialization:**
- All operation classes now receive `self.default_mode` during SDK initialization
- Default mode is initialized from `secrets.trading_mode` but can be updated via `active_mode` property

### Benefits

- **Cleaner API:** Functions can be called without passing `mode` every time: `sdk.get_position("MNQZ25")` instead of `sdk.get_position("MNQZ25", mode="PAPER")`
- **Automatic Mode Tracking:** Last authenticated mode automatically becomes the default for subsequent calls
- **Backward Compatible:** All existing code continues to work - `mode` parameter can still be explicitly provided to override defaults
- **Consistent Behavior:** All operation classes use the same default mode inheritance pattern
- **Better UX:** Users don't need to remember which mode they authenticated with - SDK tracks it automatically

### Usage Example

```python
# Initialize SDK
sdk = TradeStationSDK()

# Authenticate in PAPER mode
sdk.authenticate("PAPER")  # default_mode is now "PAPER"

# All subsequent calls use PAPER mode by default
position = sdk.get_position("MNQZ25")  # Uses PAPER mode automatically
orders = sdk.get_current_orders()  # Uses PAPER mode automatically
pnl = sdk.get_todays_profit_loss()  # Uses PAPER mode automatically

# Can still override mode per call if needed
live_position = sdk.get_position("MNQZ25", mode="LIVE")  # Explicit override
```

### Breaking Changes

None - All changes are backward compatible. Existing code that passes `mode` explicitly continues to work. Code that doesn't pass `mode` now benefits from automatic default mode inheritance.

---

## 2025-12-05 14:53 - Comprehensive Input Validation for Order Execution Functions

**Major Enhancement:** Added comprehensive input validation to all order execution functions with detailed error messages to prevent invalid API calls.

### Code Changes

**Validation Added to `place_order()`:**
- ✅ Symbol validation: Non-empty string, max 50 characters, whitespace check
- ✅ Side validation: Must be "BUY" or "SELL" (case-insensitive)
- ✅ Quantity validation: Must be positive integer, max 10,000 contracts
- ✅ Order type validation: Must be valid enum (Market, Limit, Stop, StopLimit, TrailingStop)
- ✅ Time in force validation: Must be valid enum (DAY, GTC, IOC, FOK, DYP, GCP, GTD, GDP, OPG, CLO, 1, 3, 5)
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided
- ✅ Price validation: limit_price and stop_price must be positive, finite numbers, reasonable range ($0.01 - $1,000,000)
- ✅ Price relationship warnings: Warns about potentially illogical StopLimit configurations
- ✅ Trailing stop validation: Enhanced with type, positive, and max value checks (already existed, now comprehensive)

**Validation Added to `cancel_order()`:**
- ✅ Order ID validation: Non-empty string, max 50 characters, whitespace check
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided

**Validation Added to `modify_order()`:**
- ✅ Order ID validation: Non-empty string, max 50 characters, whitespace check
- ✅ At least one update required: quantity, limit_price, or stop_price must be provided
- ✅ Quantity validation: Must be positive integer, max 10,000 contracts
- ✅ Price validation: limit_price and stop_price must be positive, finite numbers, reasonable range
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided

**Validation Added to `replace_order()`:**
- ✅ Old order ID validation: Non-empty string, max 50 characters, whitespace check
- ✅ New order validation: Handled by `place_order()` (reuses all validation)

**Validation Added to `cancel_all_orders_for_symbol()`:**
- ✅ Symbol validation: Non-empty string, max 50 characters, whitespace check
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided

**Validation Added to `cancel_all_orders()`:**
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided

**Validation Added to `is_order_filled()`:**
- ✅ Order ID validation: Non-empty string, max 50 characters, whitespace check
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided

**Validation Added to `get_order_executions()`:**
- ✅ Order ID validation: Non-empty string, max 50 characters, whitespace check
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided

**Validation Added to `confirm_order()`:**
- ✅ Symbol, side, quantity validation: Same as `place_order()`
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided

**Validation Added to `place_bracket_order()`:**
- ✅ Symbol validation: Non-empty string, max 50 characters, whitespace check
- ✅ Entry side validation: Must be "BUY" or "SELL" (case-insensitive)
- ✅ Quantity validation: Must be positive integer, max 10,000 contracts
- ✅ Profit target validation: Must be positive, reasonable range
- ✅ Stop loss validation: Must be positive when not using trailing stop
- ✅ Entry price validation: Must be positive when provided
- ✅ Entry order type validation: Must be "Market" or "Limit"
- ✅ Time in force validation: Must be valid enum
- ✅ Mode validation: Must be "PAPER" or "LIVE" if provided
- ✅ Logical validation warnings: Warns about potentially illogical price relationships (profit target/stop loss relative to entry)

**Validation Added to `place_trailing_stop_order()`:**
- ✅ Trail parameter validation: Already existed, now comprehensive with detailed error messages

### Error Message Improvements

All validation errors now include:
- ❌ Clear error indicator
- Detailed error message with actual value received
- Type information when type mismatch occurs
- Recommended ranges/limits when values are out of range
- Specific guidance (e.g., "Maximum recommended: 10,000 contracts")

### Benefits

- **Prevents Invalid API Calls:** Catches errors before making API requests, saving time and API quota
- **Better Error Messages:** Detailed, actionable error messages help developers fix issues quickly
- **Type Safety:** Validates types before API calls, preventing runtime errors
- **Range Validation:** Prevents unreasonably large or small values that would fail at API level
- **Consistent Validation:** All order execution functions use the same validation patterns

### Breaking Changes

None - All validation is additive. Invalid inputs that previously would have failed at the API level now fail earlier with clearer error messages.

---

## 2025-12-05 14:45 - Order Status Filtering & Position P&L Convenience Functions

**New Features:** Added convenience functions for filtering orders by status and retrieving position P&L metrics.

### Code Changes

**Order Status Filtering Functions (OrderOperations)**
- `get_orders_by_status()` - Filter orders by single status or list of statuses
- `get_open_orders()` - Get open/working orders (OPN, ACK, PLA, FPR, RPD, RSN, UCN)
- `get_filled_orders()` - Get filled orders (FLL, FLP)
- `get_canceled_orders()` - Get canceled orders (CAN, EXP, OUT, TSC, UCH)
- `get_rejected_orders()` - Get rejected orders (REJ)

**Position P&L Convenience Functions (PositionOperations)**
- `get_todays_profit_loss()` - Get today's profit and loss across all positions (sums TodaysProfitLoss)
- `get_todays_trades()` - Get today's filled trades (orders filled today with FLL/FLP status)
- `get_unrealized_profit_loss()` - Get unrealized profit and loss across all positions (sums UnrealizedProfitLoss)

**SDK Main Class Updates**
- Added delegation methods for all new order status filtering functions
- Added delegation methods for all new position P&L functions
- All functions accessible via `sdk.get_*()` pattern

### Documentation Changes

**Updated Documentation**
- `docs/SDK_FUNCTIONS_LIST.md` - Added Order Status Convenience Functions section, updated Position Functions section, updated function counts
- Added API endpoint/dependency column to all function tables
- Linked all order functions to `ORDER_FUNCTIONS_REFERENCE.md`

### Benefits

- **Better Order Filtering:** Replaces vague `get_current_orders()` with specific status-based filters
- **Simplified P&L Access:** Easy access to today's P&L and unrealized P&L without manual position iteration
- **Trade Tracking:** Quick access to today's filled trades for performance analysis
- **Status Clarity:** Clear functions for common order status categories (open, filled, canceled, rejected)

### Breaking Changes

None - All new functions are additions. `get_current_orders()` remains available for backward compatibility.

---

## 2025-12-05 15:30 - Order Operations Refactoring & Convenience Functions

**Major Refactoring:** Separated order execution operations from order query operations and added convenience functions for common order types.

### Code Changes

**New Class: OrderExecutionOperations**
- Created `src/lib/tradestation/order_executions.py` with new `OrderExecutionOperations` class
- Handles all `/orderexecution/` API endpoint operations:
  - `place_order()`, `cancel_order()`, `modify_order()`
  - `get_order_executions()`, `confirm_order()`, `confirm_group_order()`
  - `place_group_order()`, `get_activation_triggers()`, `get_routes()`

**Refactored: OrderOperations**
- Updated `src/lib/tradestation/orders.py` to focus on order queries only
- Keeps only `/brokerage/accounts/.../orders` endpoint methods:
  - `get_order_history()`, `get_current_orders()`, `get_orders_by_ids()`
  - `get_historical_orders_by_ids()`, `stream_orders()`
- Updated class docstring to reflect query-only operations

**Convenience Functions Added**
- `place_limit_order()` - Simplified limit order placement
- `place_stop_order()` - Simplified stop order placement
- `place_stop_limit_order()` - Simplified stop-limit order placement
- `place_trailing_stop_order()` - Simplified trailing stop order placement
- `place_bracket_order()` - Bracket order builder (entry + profit target + stop-loss)
- `place_oco_order()` - OCO (One-Cancels-Other) order wrapper

**SDK Main Class Updates**
- Updated `TradeStationSDK.__init__()` to initialize both `OrderExecutionOperations` and `OrderOperations`
- Added properties: `sdk.order_executions` and `sdk.orders`
- Updated all delegation methods to route execution methods to `_order_executions` and query methods to `_orders`
- Added convenience function delegations for backward compatibility

### Documentation Changes

**New Documentation**
- Created `docs/API_ENDPOINT_MAPPING.md` - Comprehensive SDK function to API endpoint mapping organized by class

**Updated Documentation**
- `README.md` - Added OrderExecutionOperations section, convenience functions section, and updated examples
- `docs/API_REFERENCE.md` - Added OrderExecutionOperations class documentation and all convenience functions
- `docs/SDK_USAGE_EXAMPLES.md` - Added convenience function examples and usage patterns
- `docs/API_COVERAGE.md` - Updated to reflect new class structure (OrderExecutionOperations vs OrderOperations)

### Benefits

- **Clear Separation of Concerns:** Execution operations (placement, modification, cancellation) separated from query operations (history, current orders, streaming)
- **Simplified API:** Convenience functions reduce boilerplate for common order types
- **Better Organization:** Methods grouped by their underlying API endpoints
- **Backward Compatibility:** All existing SDK methods continue to work via delegation
- **Type Safety:** All convenience functions maintain type safety with Pydantic models

### Breaking Changes

None - All existing code continues to work via delegation methods in the main SDK class.

---

## 2025-12-05 13:05 - Mermaid Diagram Format Fix

**Fixed:** Converted Mermaid diagrams from `.mmd` to `.md` format for better viewing.

### Documentation Changes
- Converted [`docs/API_STRUCTURE.mmd`](./docs/API_STRUCTURE.mmd) → [`docs/API_STRUCTURE.md`](./docs/API_STRUCTURE.md)
- Converted [`docs/API_STRUCTURE_DETAILED.mmd`](./docs/API_STRUCTURE_DETAILED.mmd) → [`docs/API_STRUCTURE_DETAILED.md`](./docs/API_STRUCTURE_DETAILED.md)
- Updated all references in documentation to point to `.md` files
- Added viewing instructions to diagram files

**Why `.md` instead of `.mmd`:**
- ✅ Renders automatically in Cursor/VS Code markdown preview
- ✅ Renders automatically on GitHub
- ✅ Standard format used throughout the codebase (see `docs/architecture/CODEBASE_STRUCTURE_DIAGRAMS.md`)
- ✅ Better accessibility and viewing options
- ✅ Can include documentation alongside diagrams

**How to View:**
- **Cursor/VS Code:** Open `.md` file and use preview (Cmd+Shift+V / Ctrl+Shift+V)
- **GitHub:** Navigate to file - diagrams render automatically
- **Online:** Copy Mermaid code block to [Mermaid Live Editor](https://mermaid.live)

---

## 2025-12-05 13:01 - OpenAPI Specification Analysis & Documentation Updates

**Added:** Comprehensive OpenAPI specification analysis, Mermaid diagrams, code examples extraction, and file reference fixes.

### File Changes
- Renamed `openapi (2) (2).json` → [`tradestation-api-v3-openapi.json`](./docs/reference/tradestation-api-v3-openapi.json) for clarity
- Verified `docs/reference/tradestation-api-v3-openapi.json` and root `APIv3Endpoints.json` are **identical** (same file)

### Documentation Created
- [`docs/OPENAPI_CODE_EXAMPLES.md`](./docs/OPENAPI_CODE_EXAMPLES.md) - Extracted **190 code examples** from OpenAPI spec (Shell, Node.js, Python, C#, JSON)
- [`docs/API_STRUCTURE.md`](./docs/API_STRUCTURE.md) - Mermaid diagram of API v3 structure (embedded in markdown)
- [`docs/API_STRUCTURE_DETAILED.md`](./docs/API_STRUCTURE_DETAILED.md) - Detailed Mermaid diagram with endpoint relationships (embedded in markdown)
- [`docs/AUDIT_FILE_REFERENCES.md`](./docs/AUDIT_FILE_REFERENCES.md) - File reference audit report

### Documentation Updates
- Updated [`docs/GAP_ANALYSIS.md`](./docs/GAP_ANALYSIS.md) with complete OpenAPI specification analysis:
  - Complete endpoint inventory (33 v3 endpoints across 3 tags)
  - Endpoint-by-endpoint comparison with SDK implementation
  - Coverage summary (100% of OpenAPI v3 endpoints + 2 additional endpoints)
  - References to code examples and Mermaid diagrams
- Updated all file references to use proper markdown links:
  - [`docs/API_COVERAGE.md`](./docs/API_COVERAGE.md) - Fixed OpenAPI spec reference
  - [`docs/GAP_ANALYSIS.md`](./docs/GAP_ANALYSIS.md) - Fixed OpenAPI spec reference and added analysis
  - [`README.md`](./README.md) - Fixed OpenAPI spec reference and location
  - [`docs/AUDIT_FILE_REFERENCES.md`](./docs/AUDIT_FILE_REFERENCES.md) - Updated with new filename

### OpenAPI Analysis Results
- **Total v3 Endpoints:** 33
  - **Brokerage:** 11 endpoints (all implemented ✅)
  - **MarketData:** 14 endpoints (all implemented ✅)
  - **Order Execution:** 8 endpoints (all implemented ✅)
- **Code Examples:** 190 examples across 5 languages
- **SDK Coverage:** 100% of OpenAPI v3 endpoints + 2 additional endpoints (balance streaming, order executions)

---

## 2025-12-05 12:48 - SDK Documentation Rule & Dedicated Changelog

**Added:** Auto-applied documentation hygiene rule and dedicated SDK changelog.

### Documentation Changes
- Introduced `.cursor/rules/tradestation-sdk-documentation.mdc` to enforce metadata, dependency tracking, and changelog updates for SDK docs.
- Created this dedicated SDK changelog (`CHANGELOG.md`) to track SDK-specific changes separately from project-wide changes.
- Rule applies automatically when editing `docs/**` or `**/README.md` files within the SDK.
- Updated rule (v1.1.0) to require updates to SDK-specific `CHANGELOG.md` instead of root changelog for SDK documentation changes.

---

## 2025-12-05 14:44 - Internal SDK Migration

**Major Refactoring:** Migrated from external `tastyware/tradestation` SDK to internal self-contained SDK.

### Code Changes

**New Internal SDK Structure:**
- Created comprehensive internal TradeStation SDK with all API operations
- Reimplemented OAuth authentication and token management (`session.py`)
- All operation modules: `accounts.py`, `orders.py`, `positions.py`, `market_data.py`, `streaming.py`
- Models moved to `src/lib/tradestation/models/`
- Custom exceptions (`exceptions.py`) for SDK error handling
- Main SDK class: `TradeStationSDK` (replaces external SDK dependency)

**Documentation:**
- Moved TradeStation docs to `src/lib/tradestation/docs/`
- Created comprehensive API documentation: `API_REFERENCE.md`, `API_COVERAGE.md`, `GAP_ANALYSIS.md`, `MODELS.md`, `SDK_USAGE_EXAMPLES.md`

**Benefits:**
- No external SDK dependencies
- Complete control over API integration
- Full data capture (all 30+ TradeStation API fields)
- Better error handling with custom exceptions
- Improved maintainability and extensibility

---

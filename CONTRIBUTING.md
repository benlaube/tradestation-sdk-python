---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:34 EST
type: Documentation
description: Documentation file
---

# Contributing to TradeStation SDK

## About This Document

This document provides **guidelines and best practices** for contributing to the TradeStation SDK. It covers development setup, code style, testing requirements, documentation standards, and the contribution process.

**Use this if:** You want to contribute code, documentation, or examples to the SDK.

**Related Documents:**

- 📖 **[README.md](README.md)** - Complete SDK documentation
- 📦 **[INSTALLATION.md](docs/getting-started/installation.md)** - Development installation setup
- 📚 **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - API documentation standards
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - How to document changes
- 🗺️ **[docs/ROADMAP.md](docs/ROADMAP.md)** - Planned features and priorities

---

Thank you for considering contributing to the TradeStation SDK! This document provides guidelines and best practices for contributing.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Making Changes](#making-changes)
- [Testing](#testing)
- [Code Style](#code-style)
- [Documentation](#documentation)
- [Submitting Changes](#submitting-changes)

---

## Code of Conduct

Be respectful, constructive, and professional. We're all here to build better trading tools.

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- TradeStation Developer account
- Git
- Familiarity with REST APIs and OAuth2

### Fork & Clone

```bash
# Fork the repository on GitHub, then:
git clone https://github.com/YOUR_USERNAME/tradestation-python-sdk.git
cd tradestation-python-sdk
```

---

## Development Setup

### 1. Create Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate  # Windows
```

### 2. Install Development Dependencies

```bash
pip install -e ".[dev]"
```

This installs:

- SDK dependencies (httpx, pydantic, PyJWT)
- Development tools (pytest, black, ruff)
- Testing tools (pytest-asyncio, pytest-cov, pytest-mock)

### 3. Set Up Environment Variables

Copy `.env.example` to `.env` and add your credentials:

```bash
cp .env.example .env
```

Edit `.env` with your TradeStation credentials.

### 4. Verify Setup

```bash
# Run authentication test
python cli/test_auth.py PAPER

# Run comprehensive connection test
python cli/test_connection.py
```

---

## Making Changes

### Branching Strategy

Create a feature branch:

```bash
# Create a new branch
git checkout -b feature/my-new-feature
```

Branch naming convention:

- `feat/` - New features
- `fix/` - Bug fixes
- `docs/` - Documentation updates
- `test/` - Test improvements
- `chore/` - Maintenance tasks

### Code Organization

The SDK is organized by domain:

```
tradestation_sdk/
├── __init__.py           # Main SDK class
├── session.py            # OAuth authentication
├── exceptions.py         # Custom exceptions
├── config.py             # SDK configuration
├── operations/           # Domain operations
│   ├── accounts.py
│   ├── market_data.py
│   ├── order_executions.py
│   ├── orders.py
│   ├── positions.py
│   └── streaming.py
├── utils/                # Shared utilities
│   ├── client.py         # HTTP client
│   ├── logger.py         # Logging helpers
│   └── mappers.py        # Data normalization
└── models/               # Pydantic models
    ├── orders.py
    ├── order_executions.py
    ├── accounts.py
    ├── positions.py
    ├── quotes.py
    └── streaming.py
```

### Adding New Features

#### 1. Add New API Endpoint

```python
# In accounts.py
def get_new_feature(self, mode: str | None = None) -> dict[str, Any]:
    """
    Get new feature data.

    Args:
        mode: "PAPER" or "LIVE"

    Returns:
        Dictionary with feature data

    Example:
        >>> result = sdk.get_new_feature(mode="PAPER")
        >>> print(result)

    Dependencies: HTTPClient.make_request
    """
    if mode is None:
        mode = self.default_mode

    response = self.client.make_request("GET", "new/endpoint", mode=mode)
    return response
```

```python
# In __init__.py
def get_new_feature(self, mode: str | None = None) -> dict[str, Any]:
    """Get new feature. Delegates to AccountOperations."""
    return self._accounts.get_new_feature(mode)
```

```python
# In tests/test_accounts.py
def test_get_new_feature(self, mock_http_client, mocker):
    """Test get_new_feature returns data."""
    mocker.patch.object(
        mock_http_client,
        "make_request",
        return_value={"data": "test"}
    )

    account_ops = AccountOperations(mock_http_client)
    result = account_ops.get_new_feature("PAPER")

    assert result == {"data": "test"}
```

**Step 4:** Update documentation

- Add to `docs/API_REFERENCE.md`
- Add to `docs/SDK_USAGE_EXAMPLES.md`
- Add to `CHANGELOG.md`

#### 2. Add New Model

```python
# In models/new_feature.py
from pydantic import BaseModel, Field

class NewFeatureResponse(BaseModel):
    """Response model for new feature API."""

    field1: str = Field(..., description="Description of field1")
    field2: int | None = Field(None, description="Optional field2")

    class Config:
        populate_by_name = True  # Allow both snake_case and PascalCase
```

---

## Testing

### Running Tests

```bash
# Run tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_accounts.py -v

# Run specific test
pytest tests/test_accounts.py::test_get_account_info -v
```

### Writing Tests

Every new function must have tests covering:

- ✅ Success case
- ✅ Error handling
- ✅ Edge cases
- ✅ Mode switching (PAPER/LIVE)

**Test Template:**

```python
import pytest
from tradestation_sdk import TradeStationSDK

@pytest.mark.unit
class TestNewFeature:
    """Tests for new feature."""

    def test_success_case(self, mock_http_client, mocker):
        """Test new feature returns expected data."""
        # Arrange
        mocker.patch.object(
            mock_http_client,
            "make_request",
            return_value={"expected": "data"}
        )

        # Act
        result = sdk.new_feature(mode="PAPER")

        # Assert
        assert result == {"expected": "data"}

    def test_error_handling(self, mock_http_client, mocker):
        """Test new feature handles errors."""
        mocker.patch.object(
            mock_http_client,
            "make_request",
            side_effect=TradeStationAPIError("Test error")
        )

        with pytest.raises(TradeStationAPIError):
            sdk.new_feature(mode="PAPER")
```

### Test Coverage Requirements

- **Minimum:** 80% code coverage
- **Goal:** 90%+ code coverage
- **Critical paths:** 100% coverage (authentication, order placement)

---

## Code Style

### Python Style Guide

We follow [PEP 8](https://pep8.org/) with some modifications:

- **Line Length:** 120 characters (not 79)
- **Quotes:** Double quotes for strings (except dict keys)
- **Type Hints:** Required for all function parameters and return values
- **Docstrings:** Required for all public functions

### Formatting Tools

**Black** (auto-formatter):

```bash
black .
```

**Ruff** (linter):

```bash
ruff check . --fix
```

**Type Checking** (mypy):

```bash
mypy .
```

### Docstring Format

Use Google-style docstrings:

```python
def function_name(param1: str, param2: int = 0) -> dict[str, Any]:
    """
    Brief description of function (one line).

    Longer description if needed. Explain what the function does,
    any important behavior, and caveats.

    Args:
        param1: Description of param1
        param2: Description of param2 (default: 0)

    Returns:
        Dictionary with result data including:
        - key1: Description
        - key2: Description

    Raises:
        ValueError: If param1 is empty
        TradeStationAPIError: If API request fails

    Example:
        >>> result = function_name("test", 42)
        >>> print(result['key1'])
        'value'

    See Also:
        - related_function(): Related functionality

    Dependencies: module1, module2
    """
```

### Type Hints

Always use type hints:

```python
# ✅ Good
def get_data(symbol: str, mode: str | None = None) -> dict[str, Any]:
    pass

# ❌ Bad
def get_data(symbol, mode=None):
    pass
```

```bash
# Build documentation
mkdocs build
```

### Documentation Files

- `README.md` - Main SDK documentation
- `LIMITATIONS.md` - Known limitations and constraints
- `CHANGELOG.md` - Version history and changes
- `docs/API_REFERENCE.md` - Complete API reference
- `docs/SDK_USAGE_EXAMPLES.md` - Usage examples
- `examples/` - Interactive examples and scripts

### Documentation Standards

- Use code blocks with syntax highlighting
- Include working examples
- Link to related documentation
- Keep examples simple and focused
- Test all code examples (they should work)

---

## Submitting Changes

### Before Submitting

1. **Run all tests:**

   ```bash
   pytest
   ```

2. **Check code quality:**

   ```bash
   black .
   ruff check . --fix
   ```

3. **Update CHANGELOG.md:**

   ```markdown
   ## [Unreleased]

   ### Added
   - New feature description

   ### Changed
   - What changed

   ### Fixed
   - Bug fix description
   ```

4. **Update documentation** (if applicable)

### Commit Messages

Use Conventional Commits format:

```
<type>(<scope>): <subject>

[optional body]

[optional footer]
```

**Types:**

- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation changes
- `test` - Test additions/changes
- `refactor` - Code refactoring
- `chore` - Maintenance tasks

**Examples:**

```
feat(orders): add support for conditional orders

Add support for TradeStation conditional orders with market
and time activation rules.

fix(streaming): handle connection timeout in stream_quotes

docs(readme): add quick start guide and troubleshooting section
```

### Pull Request Process

1. **Create Pull Request** on GitHub
2. **Fill in PR template:**
   - What changed?
   - Why was this needed?
   - How was it tested?
   - Screenshots/logs (if applicable)

3. **Wait for review** - Maintainers will review within 1-2 weeks
4. **Address feedback** - Make requested changes
5. **Merge** - Once approved, maintainers will merge

---

## Development Tips

### Testing with PAPER Mode

Always test with PAPER mode first:

```python
# ✅ Safe for testing
sdk.authenticate(mode="PAPER")
order_id, status = sdk.place_order("AAPL", "BUY", 10, mode="PAPER")

# ⚠️ Use LIVE mode with caution
sdk.authenticate(mode="LIVE")  # Real money!
```

### Debugging

Enable full logging for debugging:

```python
# Enable full request/response logging
sdk = TradeStationSDK(enable_full_logging=True)

# Or via environment variable
import os
os.environ['TRADESTATION_FULL_LOGGING'] = 'true'
```

### Working with Mock Data

Use the test fixtures for development:

```python
from tests.fixtures.api_responses import MOCK_ACCOUNTS_LIST

# Test with mock data
print(MOCK_ACCOUNTS_LIST)
```

---

## Questions?

- 📖 Read the [README](README.md) and [docs/](docs/)
- 💬 [GitHub Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)
- 🐛 [Open an Issue](https://github.com/benlaube/tradestation-python-sdk/issues)

---

**Thank you for contributing!** 🎉

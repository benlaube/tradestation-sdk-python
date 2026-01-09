---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:32 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - Release Checklist

## About This Document

This is a **comprehensive checklist** for preparing SDK releases. It covers code quality, documentation, package configuration, testing, and publication steps. Use this when preparing for PyPI releases.

**Use this if:** You're preparing a new SDK version for release or want to ensure release quality.

**Related Documents:**
- 📝 **[CHANGELOG.md](CHANGELOG.md)** - Document changes here before release
- 📖 **[README.md](README.md)** - Update version numbers and features
- 📦 **[INSTALLATION.md](INSTALLATION.md)** - Verify installation instructions
- 🧪 **[tests/README.md](tests/README.md)** - Run all tests before release
- 📚 **[docs/API_REFERENCE.md](docs/API_REFERENCE.md)** - Update API docs if needed

---

Use this checklist when preparing for a public release.

---

## Pre-Release Validation

### Code Quality

- [ ] **All tests pass** - `pytest` returns 0 failures
- [ ] **90%+ code coverage** - `pytest --cov` shows ≥90%
- [ ] **No linting errors** - `ruff check .` passes
- [ ] **Code formatted** - `black .` applied
- [ ] **Type checking passes** - `mypy .` (if configured)
- [ ] **No TODO/FIXME** in production code
- [ ] **No debug code** - No `print()`, `breakpoint()`, etc.
- [ ] **No hardcoded credentials** - All from environment

### Documentation

- [ ] **README.md complete** - All sections filled
- [ ] **CHANGELOG.md updated** - Version entry added
- [ ] **All docs reviewed** - No broken links
- [ ] **All code examples tested** - Examples actually work
- [ ] **API reference complete** - All functions documented
- [ ] **Version numbers consistent** - Same version everywhere

### Package Configuration

- [ ] **pyproject.toml complete** - All metadata filled
- [ ] **setup.py works** - `python setup.py --version` returns correct version
- [ ] **MANIFEST.in correct** - All files included
- [ ] **requirements.txt accurate** - All dependencies listed
- [ ] **LICENSE file present** - License clearly stated
- [ ] **.gitignore complete** - Sensitive files excluded

### Examples & Tools

- [ ] **Jupyter notebooks work** - All notebooks run without errors
- [ ] **CLI tools work** - `test_auth.py` and `test_connection.py` pass
- [ ] **examples/quick_start.py works** - Script runs successfully
- [ ] **.env.example provided** - Template for users

---

## GitHub Repository Setup

### Repository Configuration

- [ ] **Repository created** - `github.com/benlaube/tradestation-python-sdk`
- [ ] **Description set** - Short, descriptive tagline
- [ ] **Topics added** - trading, api, sdk, futures, tradestation, python
- [ ] **README.md at root** - GitHub shows README on landing page
- [ ] **LICENSE at root** - GitHub detects license
- [ ] **.gitignore at root** - Proper ignore patterns

### Repository Settings

- [ ] **Issues enabled** - For bug reports and features
- [ ] **Discussions enabled** - For Q&A and community
- [ ] **Wiki disabled** - Use docs/ instead
- [ ] **Projects disabled** - Use issues instead
- [ ] **Branch protection** - Protect `main` branch
- [ ] **PR required** - No direct commits to main

### GitHub Actions (Optional but Recommended)

- [ ] **CI/CD setup** - Run tests on every commit
- [ ] **Lint check** - Automated code quality checks
- [ ] **Coverage report** - Automated coverage reporting
- [ ] **Release automation** - Auto-publish to PyPI

**Example workflow:** `.github/workflows/test.yml`

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: ['3.10', '3.11', '3.12']

    steps:
    - uses: actions/checkout@v3
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        pip install -e ".[dev]"
    - name: Run tests
      run: pytest --cov
```

### Issue Templates

- [ ] **Bug report template** - `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] **Feature request template** - `.github/ISSUE_TEMPLATE/feature_request.md`
- [ ] **Question template** - `.github/ISSUE_TEMPLATE/question.md`

---

## PyPI Publishing

### Prepare Package

- [ ] **Build package** - `python -m build`
- [ ] **Check package** - `twine check dist/*`
- [ ] **Test install locally** - `pip install dist/*.whl`
- [ ] **Verify imports** - `python -c "import tradestation_sdk"`
- [ ] **Test CLI tools** - Run after local install

### PyPI Account Setup

- [ ] **PyPI account created** - https://pypi.org/account/register/
- [ ] **2FA enabled** - Security requirement
- [ ] **API token created** - For automated publishing
- [ ] **Token saved** - In `~/.pypirc` or CI/CD secrets

### Test PyPI First (Recommended)

```bash
# Upload to Test PyPI
twine upload --repository testpypi dist/*

# Install from Test PyPI
pip install --index-url https://test.pypi.org/simple/ tradestation-sdk

# Verify it works
python -c "import tradestation_sdk; print(tradestation_sdk.__version__)"
```

### Publish to PyPI

```bash
# Build package
python -m build

# Upload to PyPI (production)
twine upload dist/*
```

- [ ] **Uploaded to PyPI** - https://pypi.org/project/tradestation-sdk/
- [ ] **Verified on PyPI** - Package page looks correct
- [ ] **Installed from PyPI** - `pip install tradestation-python-sdk` works
- [ ] **Tested after install** - All features work

---

## Release Announcement

### GitHub Release

- [ ] **Create release** - On GitHub releases page
- [ ] **Tag version** - `v1.0.0`
- [ ] **Release title** - "TradeStation SDK v1.0.0 - Initial Release"
- [ ] **Release notes** - Copy from CHANGELOG.md
- [ ] **Attach files** - Source code archives
- [ ] **Mark as latest** - Set as latest release

**Release Notes Template:**

```markdown
## TradeStation SDK v1.0.0

First public release of comprehensive TradeStation API v3 SDK for Python.

### ✨ Features

- OAuth2 authentication with automatic token refresh
- Full TradeStation API v3 support (92% coverage)
- PAPER and LIVE mode support
- HTTP Streaming with auto-reconnection
- Type-safe Pydantic models
- Comprehensive error handling
- 90%+ test coverage

### 📚 Documentation

- 23 documentation files (30,000+ words)
- 3 Jupyter notebooks
- 2 CLI testing tools
- Quick start guides (2min, 5min, 15min)
- Complete API reference

### 📦 Installation

```bash
pip install tradestation-python-sdk
```

See [QUICKSTART.md](QUICKSTART.md) for 2-minute setup.

### 📖 Resources

- [Complete Documentation](README.md)
- [API Reference](docs/API_REFERENCE.md)
- [Examples](examples/)
- [Security Guide](SECURITY.md)

### 🙏 Thank You

Thank you to everyone who contributed and provided feedback!

**Full Changelog:** [CHANGELOG.md](CHANGELOG.md)
```

### Community Announcement

**Where to announce:**

- [ ] **Reddit**
  - r/algotrading
  - r/python
  - r/AutomatedTrading
  - r/Daytrading

- [ ] **Social Media**
  - Twitter/X with hashtags: #algotrading #python #trading #opensource
  - LinkedIn
  - Dev.to blog post

- [ ] **Forums**
  - QuantConnect forums
  - Elite Trader forums
  - TradeStation forums

- [ ] **Email**
  - Newsletter (if you have one)
  - Beta testers
  - Early adopters

**Announcement Template:**

```markdown
🎉 TradeStation SDK v1.0.0 Released!

Comprehensive Python SDK for TradeStation API v3:
✅ OAuth2 authentication
✅ PAPER & LIVE mode support
✅ Real-time streaming
✅ Type-safe models
✅ 92% API coverage
✅ 90%+ tests

Get started in 2 minutes: https://github.com/benlaube/tradestation-python-sdk

pip install tradestation-python-sdk

#algotrading #python #trading #opensource
```

---

## Post-Release

### Monitor

- [ ] **Watch GitHub issues** - Respond within 24-48 hours
- [ ] **Monitor PyPI downloads** - Track adoption
- [ ] **Check discussions** - Answer questions
- [ ] **Review feedback** - Incorporate suggestions

### Maintain

- [ ] **Fix critical bugs** - Within 24-48 hours
- [ ] **Release patches** - For bug fixes
- [ ] **Update docs** - Based on user feedback
- [ ] **Plan next release** - v1.1 roadmap

---

## Version Checklist (Per Release)

For each new version:

- [ ] **Update version** - In `__init__.py`, `pyproject.toml`, `setup.py`
- [ ] **Update CHANGELOG.md** - Add release notes
- [ ] **Update ROADMAP.md** - Mark completed features
- [ ] **Test thoroughly** - All tests pass
- [ ] **Build package** - `python -m build`
- [ ] **Test install** - Local install works
- [ ] **Upload to Test PyPI** - Verify works
- [ ] **Upload to PyPI** - Production release
- [ ] **Create GitHub release** - Tag and notes
- [ ] **Announce** - Community announcement
- [ ] **Update docs** - Version references

---

## Release Automation (Future)

**GitHub Actions workflow for automated releases:**

```yaml
name: Publish to PyPI

on:
  release:
    types: [published]

jobs:
  publish:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - uses: actions/setup-python@v4
      with:
        python-version: '3.10'
    - name: Install dependencies
      run: |
        pip install build twine
    - name: Build package
      run: python -m build
    - name: Publish to PyPI
      env:
        TWINE_USERNAME: __token__
        TWINE_PASSWORD: ${{ secrets.PYPI_API_TOKEN }}
      run: twine upload dist/*
```

---

**Use this checklist for every release to ensure quality and consistency!** ✅

---

**Last Updated:** 2025-12-29
**Current Version:** 1.0.1

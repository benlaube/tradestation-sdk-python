---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:34 EST
type: Documentation
description: Documentation file
---

# TradeStation SDK - Installation Guide

## About This Document

This is a **comprehensive installation guide** covering all installation methods, platforms, and scenarios. Use this if you need detailed installation instructions beyond the basic `pip install`.

**Use this if:** You need to install from source, set up development environment, or install on specific platforms.

**Related Documents:**
- 🚀 **[QUICKSTART.md](QUICKSTART.md)** - Fast 2-minute setup (most users)
- 📖 **[README.md](README.md)** - Complete SDK documentation
- 🔄 **[MIGRATION.md](MIGRATION.md)** - Migrating from other SDKs
- 🔒 **[SECURITY.md](SECURITY.md)** - Security considerations for credentials
- 🤝 **[CONTRIBUTING.md](CONTRIBUTING.md)** - Development setup for contributors

---

Comprehensive installation guide for all scenarios and platforms.

---

## Quick Install (Most Users)

```bash
pip install tradestation-python-sdk
```

**Done!** Skip to [Configuration](#configuration) section.

---

## Detailed Installation Options

### Option 1: Install from PyPI (Recommended)

**For stable releases:**

```bash
pip install tradestation-python-sdk
```

**For specific version:**

```bash
pip install tradestation-python-sdk==1.0.0
```

**For latest features (pre-release):**

```bash
pip install --pre tradestation-sdk
```

---

### Option 2: Install from Source

**For development or latest unreleased features:**

```bash
# Clone repository
git clone https://github.com/benlaube/tradestation-python-sdk.git
cd tradestation-sdk

# Install in editable mode
pip install -e .
```

**With development dependencies:**

```bash
pip install -e ".[dev]"
```

This includes:
- pytest, pytest-asyncio, pytest-cov
- black, ruff, mypy
- All core dependencies

---

### Option 3: Use as Git Submodule (Vendored SDK)

**For teams embedding the SDK inside another repo with a pinned commit:**

```bash
# From the root of your app repo
git submodule add -b main git@github.com:<your-org>/tradestation-python-sdk.git libs/tradestation-sdk
git submodule update --init --recursive

# Install from the submodule path
pip install -e ./libs/tradestation-sdk
# (optional) track it in requirements.txt
echo "-e ./libs/tradestation-sdk" >> requirements.txt
```

- Update to latest: `git submodule update --remote --merge libs/tradestation-sdk`
- Pin to a release: `(cd libs/tradestation-sdk && git checkout v1.0.0)`
- See [docs/SUBMODULE_INTEGRATION.md](docs/SUBMODULE_INTEGRATION.md) for detailed workflow, CI tips, and rollback steps.

---

### Option 4: Install in Virtual Environment (Recommended for Isolation)

**Using venv (Python standard):**

```bash
# Create virtual environment
python -m venv .venv

# Activate (macOS/Linux)
source .venv/bin/activate

# Activate (Windows)
.venv\Scripts\activate

# Install SDK
pip install tradestation-python-sdk
```

**Using conda:**

```bash
# Create conda environment
conda create -n trading python=3.10
conda activate trading

# Install SDK
pip install tradestation-python-sdk
```

---

### Option 5: Install with Docker

**Dockerfile:**

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install SDK
RUN pip install tradestation-python-sdk

# Copy your trading scripts
COPY . /app

CMD ["python", "your_script.py"]
```

**Build and run:**

```bash
docker build -t my-trading-bot .
docker run --env-file .env my-trading-bot
```

---

## Platform-Specific Instructions

### Windows

**Using Python from Microsoft Store:**

```powershell
# Install Python 3.10+ from Microsoft Store
# Then install SDK
pip install tradestation-python-sdk
```

**Using Python.org installer:**

```powershell
# Download Python 3.10+ from python.org
# Install with "Add to PATH" checked
# Then:
pip install tradestation-python-sdk
```

**Common Windows Issues:**

1. **"pip not found"** - Python not in PATH
   ```powershell
   python -m pip install tradestation-python-sdk
   ```

2. **"Access denied"** - Run as administrator or use `--user` flag
   ```powershell
   pip install --user tradestation-sdk
   ```

---

### macOS

**Using Homebrew Python:**

```bash
# Install Python 3.10+
brew install python@3.10

# Install SDK
pip3 install tradestation-sdk
```

**Using system Python:**

```bash
# Check Python version
python3 --version  # Should be 3.10+

# Install SDK
pip3 install tradestation-sdk
```

**Common macOS Issues:**

1. **"SSL certificate verify failed"** - Trust certificates
   ```bash
   /Applications/Python\ 3.10/Install\ Certificates.command
   ```

2. **Permission errors** - Use `--user` flag
   ```bash
   pip3 install --user tradestation-sdk
   ```

---

### Linux (Ubuntu/Debian)

```bash
# Install Python 3.10+ if not already installed
sudo apt update
sudo apt install python3.10 python3.10-venv python3-pip

# Install SDK
pip3 install tradestation-sdk
```

**Using system Python:**

```bash
python3 -m pip install tradestation-python-sdk
```

---

### Linux (RHEL/CentOS/Fedora)

```bash
# Install Python 3.10+
sudo dnf install python3.10 python3-pip

# Install SDK
pip3 install tradestation-sdk
```

---

## Verifying Installation

### Check SDK Installation

```bash
# Check if SDK is installed
python -c "import tradestation_sdk; print(tradestation_sdk.__version__)"
```

Expected output: `1.0.0`

### Check Dependencies

```bash
# List installed packages
pip list | grep -E "tradestation|httpx|pydantic|PyJWT"
```

Expected:
```
httpx               0.27.2
pydantic            2.12.5
PyJWT               2.8.0
tradestation-sdk    1.0.0
```

### Run Test Script

```bash
# Download and run test script
python cli/test_connection.py
```

---

## Configuration

After installation, set up your credentials:

### Step 1: Create .env File

```bash
# Copy example file
cp .env.example .env

# Edit with your credentials
nano .env  # or vim, code, notepad, etc.
```

### Step 2: Add Credentials

```env
TRADESTATION_CLIENT_ID=your_client_id_here
TRADESTATION_CLIENT_SECRET=your_client_secret_here
TRADESTATION_REDIRECT_URI=http://localhost:8888/callback
TRADING_MODE=PAPER
```

### Step 3: Get Credentials

1. Go to https://developer.tradestation.com
2. Sign in with your TradeStation account
3. Create a new application
4. Copy Client ID and Client Secret
5. Set Redirect URI to `http://localhost:8888/callback`

### Step 4: Test Configuration

```bash
python cli/test_auth.py PAPER
```

Expected output: `✅ Authentication successful`

---

## Upgrading

### Upgrade to Latest Version

```bash
pip install --upgrade tradestation-sdk
```

### Check Current Version

```python
import tradestation_sdk
print(tradestation_sdk.__version__)
```

### Upgrade Notes

See [CHANGELOG.md](CHANGELOG.md) for version-specific upgrade notes.

**From v0.x to v1.0:**
- No breaking changes (v1.0 is first public release)
- New features: auto-reconnection, convenience functions, enhanced errors

---

## Uninstalling

```bash
pip uninstall tradestation-sdk
```

---

## Troubleshooting Installation

### "No module named 'tradestation_sdk'"

**Cause:** SDK not installed or wrong environment.

**Solution:**
```bash
# Verify pip is from correct environment
which pip  # macOS/Linux
where pip  # Windows

# Install SDK
pip install tradestation-python-sdk

# Verify installation
pip list | grep tradestation
```

---

### "Package not found" or "Could not find a version"

**Cause:** PyPI index issues or SDK not yet published.

**Solution:**
```bash
# Install from source
git clone https://github.com/benlaube/tradestation-python-sdk.git
cd tradestation-sdk
pip install -e .
```

---

### "Requires Python >=3.10"

**Cause:** Python version is too old (3.9 or earlier).

**Solution:**

**Option 1:** Upgrade Python
```bash
# macOS (Homebrew)
brew install python@3.10

# Ubuntu/Debian
sudo apt install python3.10

# Windows - Download from python.org
```

**Option 2:** Use Docker
```dockerfile
FROM python:3.10-slim
RUN pip install tradestation-python-sdk
```

---

### Dependency Conflicts

**Cause:** Conflicting package versions.

**Solution:**

**Option 1:** Use fresh virtual environment
```bash
python -m venv fresh_env
source fresh_env/bin/activate
pip install tradestation-python-sdk
```

**Option 2:** Check conflicting packages
```bash
pip check
```

**Option 3:** Install with force-reinstall
```bash
pip install --force-reinstall tradestation-sdk
```

---

## Platform-Specific Issues

### macOS: "SSL: CERTIFICATE_VERIFY_FAILED"

**Solution:**
```bash
/Applications/Python\ 3.10/Install\ Certificates.command
```

### Windows: "Error: Microsoft Visual C++ 14.0 required"

**Solution:**
1. Install [Microsoft C++ Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
2. Or use pre-built wheels: `pip install --only-binary :all: tradestation-sdk`

### Linux: "externally-managed-environment"

**Cause:** PEP 668 - system Python protection.

**Solution:**

**Option 1:** Use virtual environment (recommended)
```bash
python -m venv .venv
source .venv/bin/activate
pip install tradestation-python-sdk
```

**Option 2:** Use pipx (for CLI tools)
```bash
pipx install tradestation-sdk
```

**Option 3:** Override (not recommended)
```bash
pip install --break-system-packages tradestation-sdk
```

---

## Next Steps After Installation

1. ✅ **Verify installation:** `python -c "import tradestation_sdk; print(tradestation_sdk.__version__)"`
2. ✅ **Configure credentials:** Create `.env` file
3. ✅ **Test connection:** Run `python cli/test_connection.py`
4. ✅ **Follow Quick Start:** See [QUICKSTART.md](QUICKSTART.md)

---

## Need Help?

- 📖 [FAQ & Troubleshooting](README.md#faq--troubleshooting)
- 🐛 [Report Installation Issues](https://github.com/benlaube/tradestation-python-sdk/issues)
- 💬 [Get Help on Discussions](https://github.com/benlaube/tradestation-python-sdk/discussions)

---

**Last Updated:** 2025-12-29
**SDK Version:** 1.0.1

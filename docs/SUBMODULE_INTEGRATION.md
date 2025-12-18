# Using the TradeStation SDK as a Git Submodule

## About This Document

- **Status:** Active  
- **Last Updated:** 2025-12-18  
- **Purpose:** How to embed this SDK into another repository via `git submodule`, keep it updated, and install it in downstream environments.  
- **Use this if:** You want to vendor the SDK without publishing to PyPI or you need deterministic version pinning across projects.  
- **Related docs:** [INSTALLATION.md](../INSTALLATION.md), [DEPLOYMENT.md](../DEPLOYMENT.md), [SECURITY.md](../SECURITY.md)

---

## TL;DR (Happy Path)

```bash
# From the root of the consuming repo
git submodule add -b main git@github.com:<your-org>/tradestation-python-sdk.git libs/tradestation-sdk
git submodule update --init --recursive

# Install in editable mode so imports work from the submodule path
pip install -e ./libs/tradestation-sdk

# (Optional) Add to requirements.txt
echo \"-e ./libs/tradestation-sdk\" >> requirements.txt
```

To update later:

```bash
git submodule update --remote --merge libs/tradestation-sdk   # track main
# or pin to a tag/commit:
(cd libs/tradestation-sdk && git checkout v1.0.0)
git add libs/tradestation-sdk
git commit -m \"chore: bump tradestation-sdk submodule\"
```

---

## Prerequisites

- Python **3.10+**
- `git` access to the SDK repository (SSH or HTTPS)
- Ability to run `pip install -e`
- Environment variables for TradeStation credentials (see [INSTALLATION.md](../INSTALLATION.md#configuration) and [SECURITY.md](../SECURITY.md))

---

## Recommended Layout

```
your-app/
├── .gitmodules
├── libs/
│   └── tradestation-sdk/        # submodule checkout
├── requirements.txt             # include \"-e ./libs/tradestation-sdk\"
└── src/ or app/                 # your application code
```

Imports stay the same because the SDK is packaged:  
```python
from tradestation import TradeStationSDK
```

---

## Installation Steps (Detailed)

1) **Add the submodule**
```bash
git submodule add -b main git@github.com:<your-org>/tradestation-python-sdk.git libs/tradestation-sdk
git submodule update --init --recursive
```

2) **Install the SDK from the submodule path**
```bash
pip install -e ./libs/tradestation-sdk           # for development
# or
pip install ./libs/tradestation-sdk              # for a locked install
```

3) **Track it in your dependency file**
```bash
echo \"-e ./libs/tradestation-sdk\" >> requirements.txt
```

4) **Configure environment**
- Set `TRADESTATION_CLIENT_ID`, `TRADESTATION_CLIENT_SECRET`, `TRADESTATION_REDIRECT_URI`, `TRADING_MODE`, `TRADESTATION_ACCOUNT_ID` as needed.
- Keep tokens out of source control; they are stored under `logs/` by default.

5) **Verify**
```bash
cd libs/tradestation-sdk
pytest src/lib/tradestation/tests   # optional sanity check
```

---

## Updating, Pinning, and Rolling Back

- **Track latest `main`:**
  ```bash
  git submodule update --remote --merge libs/tradestation-sdk
  ```
- **Pin to a release tag/commit:**
  ```bash
  (cd libs/tradestation-sdk && git checkout v1.0.0)
  git add libs/tradestation-sdk
  git commit -m \"chore: pin tradestation-sdk to v1.0.0\"
  ```
- **Rollback:** checkout the previous known-good commit inside the submodule, then commit the pointer change in the parent repo.

**CI tip:** ensure your pipeline runs `git submodule update --init --recursive` before installing requirements.

---

## Notes & Caveats

- The SDK writes logs to `logs/` relative to the current working directory; ensure that path exists or set `LOG_DIR` in your app before initializing the SDK logger.
- OAuth flow opens a local callback server on port **8888** by default; override via `TRADESTATION_REDIRECT_URI` if the consuming app uses a different port.
- Keep secrets out of the submodule. Use your host project's secrets manager; do not commit `.env` files from the SDK directory.
- If you later publish to PyPI, consuming projects can switch from `-e ./libs/tradestation-sdk` to the pinned PyPI version without code changes.

---

## What to Do Next

- Read [INSTALLATION.md](../INSTALLATION.md) for platform-specific steps.
- Review [SECURITY.md](../SECURITY.md) before enabling **LIVE** mode.
- Run the CLI smoke tests from `cli/` to confirm connectivity after submodule install.

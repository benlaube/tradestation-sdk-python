---
version: 1.0.0
lastUpdated: 12-29-2025 17:19:34 EST
type: Documentation
description: Documentation file
---

# AI Agent Context & Memory (TradeStation SDK)
>
> **Audience:** AI Developer Agents working in `src/lib/tradestation/` (this SDK).
>
> **DO NOT** store runtime secrets, tokens, or real user data in this file.

---

## 1. Mission (What this repo is)

Build and maintain a **self-contained Python SDK** for the **TradeStation API v3** that supports:

- OAuth2 Authorization Code flow with **automatic token refresh**
- PAPER vs LIVE mode switching (sim API vs live API)
- REST operations (accounts, market data, orders, positions, executions)
- HTTP Streaming (NDJSON) with resiliency (reconnect + fallback)
- Type-safe models (Pydantic) and structured error handling

**Primary user-facing docs start at** [README.md](README.md) and [docs/INDEX.md](docs/INDEX.md).

---

## 2. Sources of truth (authoritative references)

When something conflicts, treat these as the canonical sources (top = most authoritative for that topic):

- **Public SDK surface area (what we export / what users call)**:
  - [**init**.py](__init__.py) (exports + façade)
  - [docs/reference/functions-list.md](docs/reference/functions-list.md) (human-readable list)
  - [docs/API_REFERENCE.md](docs/API_REFERENCE.md) (API guide + examples)
- **OAuth, token storage, port behavior**:
  - [session.py](session.py) (implementation)
  - [LIMITATIONS.md](LIMITATIONS.md) (constraints + operational guidance)
  - [SECURITY.md](SECURITY.md) (best practices)
- **HTTP behavior (base URLs, retries, logging, error parsing)**:
  - [client.py](client.py) (implementation)
  - [exceptions.py](exceptions.py) (error taxonomy + structured details)
  - [LIMITATIONS.md](LIMITATIONS.md) (rate limits + constraints)
- **Streaming behavior**:
  - [streaming.py](streaming.py) (implementation)
  - [README.md](README.md) (streaming usage + troubleshooting)
- **Configuration (env vars + defaults)**:
  - [config.py](config.py) (env var loading + defaults)
  - [README.md](README.md) + [INSTALLATION.md](docs/getting-started/installation.md) (setup guidance)
- **Dev workflow (lint/format/tests/hooks/secrets scanning)**:
  - [pyproject.toml](pyproject.toml) (ruff/pytest/coverage config)
  - [.pre-commit-config.yaml](.pre-commit-config.yaml) + [.secrets.baseline](.secrets.baseline)
  - [CONTRIBUTING.md](CONTRIBUTING.md)

---

## 3. High-level architecture (Where things live)

This SDK is intentionally split by concern:

- **SDK façade / exports**: [**init**.py](__init__.py) (`TradeStationSDK`, public API surface)
- **OAuth + token storage**: [session.py](session.py) (`TokenManager`, callback server)
- **HTTP concerns (retry/logging/errors)**: [utils/client.py](utils/client.py) (`HTTPClient`)
- **Domain operations**:
  - [operations/accounts.py](operations/accounts.py)
  - [operations/market_data.py](operations/market_data.py)
  - [operations/orders.py](operations/orders.py) (order queries)
  - [operations/order_executions.py](operations/order_executions.py) (order placement/modify/cancel/confirm)
  - [operations/positions.py](operations/positions.py)
- **Streaming**: [operations/streaming.py](operations/streaming.py) (HTTP streaming manager + resiliency)
- **Models**: [models/](models/) (Pydantic request/response models)
- **Normalization**: [utils/mappers.py](utils/mappers.py) (normalize API shapes)
- **Errors**: [exceptions.py](exceptions.py) (typed errors + structured details)
- **Docs**: [docs/](docs/) (+ root docs like [LIMITATIONS.md](LIMITATIONS.md), [SECURITY.md](SECURITY.md))

If you need “what endpoints exist / what’s implemented”, use:

- [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
- [docs/API_ENDPOINT_MAPPING.md](docs/API_ENDPOINT_MAPPING.md)
- [docs/api/sdk_endpoints.md](docs/api/sdk_endpoints.md) / [docs/api/operations.md](docs/api/operations.md)

---

## 4. Critical behaviors & decisions (Don’t regress these)

### 4.1 PAPER vs LIVE base URLs

- **PAPER**: `https://sim-api.tradestation.com/v3`
- **LIVE**: `https://api.tradestation.com/v3`

Reference: [utils/client.py](utils/client.py) (`get_base_url`) and [**init**.py](__init__.py) defaults.

### 4.2 Token storage location (security-sensitive)

Tokens are persisted **outside this SDK folder** by default:

- Default directory: `<repo-root>/config/` (git-ignored)
- Files:
  - `config/tokens_paper.json`
  - `config/tokens_live.json`
- Permissions:
  - token dir: `chmod 700`
  - token files: `chmod 600`

Overrides:

- `TRADESTATION_TOKEN_DIR` to change directory
- `TRADESTATION_TOKEN_STORAGE=keychain|file|auto` for storage backend

Reference: [session.py](session.py) (`TOKEN_DIR`, `TOKEN_FILE_*`).

### 4.3 OAuth callback port handling

OAuth callback server:

- uses **a local HTTP server** during auth
- supports **auto-selecting a free port** in range **8888–8898**
- can be forced via `TRADESTATION_OAUTH_PORT`

Important constraint:

- The **exact redirect URI** must be registered in the [TradeStation Developer Portal](https://developer.tradestation.com/).
- If the SDK auto-selects a port, it also **updates `redirect_uri`** to match.

Reference: [session.py](session.py) (`_find_available_port`, `TokenManager.authenticate`).

### 4.4 Streaming is HTTP Streaming (NDJSON), not WebSockets

TradeStation v3 streaming is **long-lived HTTP** with newline-delimited JSON control/data messages.

The SDK’s streaming layer should:

- filter/handle control messages (`StreamStatus`, `Heartbeat`)
- auto-reconnect with backoff
- optionally fall back to REST polling where implemented

Reference: [streaming.py](streaming.py) and docs under “Streaming” in [README.md](README.md).

### 4.5 Bar interval constraint (TradeStation API limitation)

Second-based bar intervals are **not supported** (minute-based intervals only).

See: [LIMITATIONS.md](LIMITATIONS.md) (“Bar Data Interval Constraints”).

---

## 5. Configuration (Environment variables)

Core credentials:

- `TRADESTATION_CLIENT_ID`
- `TRADESTATION_CLIENT_SECRET`
- `TRADESTATION_REDIRECT_URI` (default: `http://localhost:8888/callback`)
- `TRADESTATION_ACCOUNT_ID` (recommended for production / multi-account)

Mode & logging:

- `TRADING_MODE` (`PAPER` or `LIVE`)
- `LOG_LEVEL` (default `INFO`)
- `TRADESTATION_FULL_LOGGING` (avoid in production; request/response bodies)

Async:

- `TRADESTATION_USE_ASYNC=true|false` (opt-in async HTTP via httpx)

OAuth / token storage:

- `TRADESTATION_OAUTH_PORT`
- `TRADESTATION_TOKEN_DIR`
- `TRADESTATION_TOKEN_STORAGE=auto|file|keychain`

Reference: [config.py](config.py) + [session.py](session.py) + [utils/client.py](utils/client.py).

---

## 6. Developer workflow (tests, lint, formatting, hooks)

### 6.1 Install (dev)

Use the SDK’s packaging config:

- Install dev dependencies:
  - `pip install -e ".[dev]"`

See: [INSTALLATION.md](docs/getting-started/installation.md) and [CONTRIBUTING.md](CONTRIBUTING.md).

### 6.2 Run tests

- `pytest`
- Optional: `pytest --cov=. --cov-report=html`

See: [pyproject.toml](pyproject.toml) (`[tool.pytest.ini_options]`) and [tests/](tests/).

### 6.3 Format + lint

- `ruff check . --fix`
- `ruff format .`

Formatting/lint config lives in [pyproject.toml](pyproject.toml) (`[tool.ruff]`, `[tool.black]`).

### 6.4 Pre-commit + secret scanning (required before commits)

This SDK ships with:

- [.pre-commit-config.yaml](.pre-commit-config.yaml)
- [.secrets.baseline](.secrets.baseline)

Run:

- `pre-commit run --all-files`

If detect-secrets flags something real: rotate the credential and purge it from history (don’t “allowlist” real secrets).

---

## 7. Documentation rules (keep single sources of truth)

Avoid duplicating long docs in multiple places; prefer links.

When behavior changes:

- Update [CHANGELOG.md](CHANGELOG.md) (this SDK’s changelog)
- Update [LIMITATIONS.md](LIMITATIONS.md) if a limitation changes
- Update API docs if public functions/endpoints change:
  - [docs/API_REFERENCE.md](docs/API_REFERENCE.md)
  - [docs/reference/functions-list.md](docs/reference/functions-list.md)

---

## 8. When adding new SDK surface area (pattern to follow)

1. Add the low-level operation method to the relevant domain module (e.g., [market_data.py](market_data.py)).
2. Add delegation (and docstring) in `TradeStationSDK` ([**init**.py](__init__.py)) if it’s part of the public façade.
3. Add/extend Pydantic models in [models/](models/) if the response/request is structured.
4. Add tests under [tests/](tests/) (mock HTTP responses; avoid real network calls in unit tests).
5. Update docs (API reference + changelog).

See: [CONTRIBUTING.md](CONTRIBUTING.md) for examples and docstring conventions.

---

## 9. Quick debugging checklist (SDK)

- **Auth failing**: check redirect URI registration and whether the SDK auto-selected a port (see logs).
- **Token issues**: confirm token files under `config/` and permissions; check `TRADESTATION_TOKEN_*` env vars.
- **429 rate limits**: confirm retry behavior and backoff ([utils/client.py](utils/client.py)), reduce call rate, batch requests.
- **Streaming drops**: confirm reconnect settings and fallback behavior in [streaming.py](streaming.py).

Primary references:

- [README.md](README.md) (FAQ section)
- [LIMITATIONS.md](LIMITATIONS.md)
- [SECURITY.md](SECURITY.md)

---

## 10. Reference index (internal vs external)

### 10.1 Internal docs (SDK repo)

- **Getting started / overview**: [README.md](README.md), [docs/INDEX.md](docs/INDEX.md), [docs/GETTING_STARTED.md](docs/GETTING_STARTED.md)
- **API surface**: [docs/API_REFERENCE.md](docs/API_REFERENCE.md), [docs/reference/functions-list.md](docs/reference/functions-list.md)
- **Endpoints & coverage**: [docs/API_ENDPOINT_MAPPING.md](docs/API_ENDPOINT_MAPPING.md), [docs/API_COVERAGE.md](docs/API_COVERAGE.md), [docs/api/sdk_endpoints.md](docs/api/sdk_endpoints.md)
- **Security & ops**: [SECURITY.md](SECURITY.md), [DEPLOYMENT.md](DEPLOYMENT.md), [LIMITATIONS.md](LIMITATIONS.md)
- **Dev process**: [CONTRIBUTING.md](CONTRIBUTING.md), [RELEASE_CHECKLIST.md](RELEASE_CHECKLIST.md), [CHANGELOG.md](CHANGELOG.md)
- **OpenAPI spec (vendored)**: [tradestation-api-v3-openapi.json](docs/reference/tradestation-api-v3-openapi.json)

### 10.2 External references (TradeStation + related)

- **TradeStation Developer Portal**: `https://developer.tradestation.com/`
- **TradeStation WebAPI docs**: `https://developer.tradestation.com/webapi`
- **OAuth host used by SDK**: `https://signin.tradestation.com/`

---

*Last Updated: 12-29-2025 16:19:02 EST*

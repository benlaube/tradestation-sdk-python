---
version: 1.1.0
lastUpdated: 01-12-2026 18:05:00 EST
---

# CI/CD Workflows

This directory contains GitHub Actions workflows for Continuous Integration (CI) and Continuous Deployment (CD).

## Workflows

### 1. `ci.yml` (Continuous Integration)

**Triggers:**

- Pushes to the `main` branch.
- Pull Requests targeting the `main` branch.

**What it does:**

- Check out the code.
- Set up Python (matrix: 3.10, 3.11, 3.12).
- Install dependencies (including dev tools).
- **Linting:** Runs `ruff check` and `ruff format` to ensure code quality.
- **Testing:** Runs `pytest` to execute the full test suite.

**Why:** Ensures that no broken code or style violations are merged into the main codebase.

### 2. `cd.yml` (Continuous Deployment)

**Triggers:**

- When a new **Release** is published in GitHub.

**What it does:**

- Check out the code.
- Set up Python.
- Install build tools (`build`).
- **Build:** Creates the source distribution (`.tar.gz`) and wheel (`.whl`).
- **Publish:** Uploads the package to PyPI using Trusted Publishing (OIDC).

**How to use:**

1. Bump the version in `pyproject.toml`.
2. Commit and push to `main`.
3. Go to the GitHub repository -> "Releases" -> "Draft a new release".
4. Create a tag (e.g., `v1.1.0`) and publish.
5. This workflow will automatically run and publish to PyPI.

**Prerequisites:**

- You must configure [Trusted Publishing](https://docs.pypi.org/trusted-publishing/) on PyPI for this repository.

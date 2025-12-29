# Scripts Directory

## Metadata
- **Version:** 1.0.0
- **Last Updated:** 2025-12-29 16:26:28 EST
- **Type:** Reference Material
- **Status:** Active
- **Description:** Utility scripts for SDK development and maintenance

---

## Overview

This directory contains utility scripts for SDK development, maintenance, and validation.

## Scripts

### `generate_model_schemas.py`

Generates JSON schema file for all TradeStation SDK Pydantic models.

**Usage:**
```bash
python scripts/generate_model_schemas.py
```

**Output:**
- `docs/reference/sdk-models-schema.json` - Complete JSON schema for all models

**Purpose:**
- Export all Pydantic model schemas to a single JSON file
- Used for documentation, validation, and integration purposes
- Auto-generated file (do not edit manually)

**When to Run:**
- After adding new Pydantic models
- After modifying existing model structures
- Before releases to ensure schema is up-to-date

### `validate-markdown-metadata.py`

Pre-commit hook script to validate markdown metadata structure.

**Usage:**
```bash
# Validate specific files
python scripts/validate-markdown-metadata.py file1.md file2.md

# As pre-commit hook (automatic)
pre-commit run validate-markdown-metadata --all-files
```

**Purpose:**
- Validates that all .md files have proper metadata structure
- Checks required fields: Version, Last Updated
- Validates format matches `.cursor/rules/markdown-metadata.mdc` requirements
- Prevents commits with invalid metadata

**Validation Rules:**
- Requires `## Metadata` section
- Requires `**Version:**` field (format: X.Y or X.Y.Z)
- Requires `**Last Updated:**` field (format: YYYY-MM-DD HH:MM:SS EST)
- Validates version format is numeric
- Validates date format matches expected pattern

**Integration:**
- Configured in `.pre-commit-config.yaml`
- Runs automatically on `git commit` for staged .md files
- Can be run manually for validation

---

## Related Documentation

- [Markdown Metadata Rule](../.cursor/rules/markdown-metadata.mdc) - Metadata requirements
- [Pre-commit Configuration](../.pre-commit-config.yaml) - Pre-commit hook setup
- [Models Documentation](../docs/models/README.md) - Model documentation

---

## Maintenance

- Keep scripts up-to-date with SDK structure changes
- Update import paths if directory structure changes
- Test scripts after major refactoring
- Document new scripts in this README

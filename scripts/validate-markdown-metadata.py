#!/usr/bin/env python3
"""
Pre-commit hook to validate markdown metadata.

Validates that all .md files have proper YAML frontmatter metadata structure according to
.cursor/rules/markdown-metadata.mdc requirements.

Usage:
    python scripts/validate-markdown-metadata.py [file1.md] [file2.md] ...

Or as pre-commit hook:
    pre-commit run validate-markdown-metadata --all-files
"""

import re
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("Error: PyYAML is required. Install with: pip install pyyaml")
    sys.exit(1)

# Required metadata fields
REQUIRED_FIELDS = ["version", "lastUpdated"]

# Date format pattern: MM-DD-YYYY HH:MM:SS EST
DATE_PATTERN = r"^\d{2}-\d{2}-\d{4}\s+\d{2}:\d{2}:\d{2}\s+EST$"


def extract_yaml_frontmatter(content: str) -> tuple[dict | None, str]:
    """Extract YAML frontmatter from markdown content."""
    lines = content.split("\n")

    # Check if file starts with YAML frontmatter
    if not lines or lines[0].strip() != "---":
        return None, content

    # Find closing ---
    frontmatter_end = None
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            frontmatter_end = i
            break

    if frontmatter_end is None:
        return None, content

    # Extract YAML content
    yaml_content = "\n".join(lines[1:frontmatter_end])
    remaining_content = "\n".join(lines[frontmatter_end + 1 :])

    try:
        metadata = yaml.safe_load(yaml_content)
        return metadata if metadata else {}, remaining_content
    except yaml.YAMLError:
        return None, content


def validate_metadata(metadata: dict, file_path: Path) -> tuple[bool, list[str]]:
    """Validate metadata dictionary against requirements."""
    errors = []

    # Check required fields
    for field in REQUIRED_FIELDS:
        if field not in metadata or not metadata[field]:
            errors.append(f"Missing required field: {field}")

    # Check version format
    if "version" in metadata:
        version = str(metadata["version"])
        parts = version.split(".")
        if len(parts) not in [2, 3]:
            errors.append(f"Invalid version format: {version} (expected X.Y or X.Y.Z)")
        elif not all(part.isdigit() for part in parts):
            errors.append(f"Invalid version format: {version} (must be numeric)")

    # Check lastUpdated format (MM-DD-YYYY HH:MM:SS EST)
    if "lastUpdated" in metadata:
        last_updated = str(metadata["lastUpdated"])
        if not re.match(DATE_PATTERN, last_updated):
            errors.append(f"Invalid 'lastUpdated' format: {last_updated} (expected: MM-DD-YYYY HH:MM:SS EST)")

    return len(errors) == 0, errors


def validate_file(file_path: Path) -> tuple[bool, list[str]]:
    """Validate a single markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"Error reading file: {e}"]

    # Extract YAML frontmatter
    metadata, _ = extract_yaml_frontmatter(content)

    if metadata is None:
        return False, ["Missing YAML frontmatter (must start with '---')"]

    # Validate metadata
    is_valid, errors = validate_metadata(metadata, file_path)

    return is_valid, errors


def main():
    """Main validation function."""
    # Get files from command line or git staged files
    if len(sys.argv) > 1:
        files = [Path(f) for f in sys.argv[1:]]
    else:
        # Get staged .md files from git
        import subprocess

        try:
            result = subprocess.run(
                ["git", "diff", "--cached", "--name-only", "--diff-filter=ACM"],
                capture_output=True,
                text=True,
                check=True,
            )
            files = [Path(f) for f in result.stdout.strip().split("\n") if f.endswith(".md") and Path(f).exists()]
        except subprocess.CalledProcessError:
            print("Warning: Could not get staged files from git. Pass files as arguments.")
            return 0

    if not files:
        print("No markdown files to validate.")
        return 0

    # Validate each file
    all_valid = True
    for file_path in files:
        if not file_path.exists():
            continue

        is_valid, errors = validate_file(file_path)

        if not is_valid:
            all_valid = False
            print(f"❌ {file_path}:")
            for error in errors:
                print(f"   - {error}")
        else:
            print(f"✅ {file_path}: Metadata valid")

    if not all_valid:
        print("\n❌ Metadata validation failed. Please fix the errors above.")
        print("\nRequired YAML frontmatter format:")
        print("---")
        print("version: X.Y or X.Y.Z")
        print("lastUpdated: MM-DD-YYYY HH:MM:SS EST")
        print("---")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

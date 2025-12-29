#!/usr/bin/env python3
"""
Pre-commit hook to validate markdown metadata.

Validates that all .md files have proper metadata structure according to
.cursor/rules/markdown-metadata.mdc requirements.

Usage:
    python scripts/validate-markdown-metadata.py [file1.md] [file2.md] ...

Or as pre-commit hook:
    pre-commit run validate-markdown-metadata --all-files
"""

import re
import sys
from pathlib import Path
from typing import Optional

# Required metadata fields (from markdown-metadata.mdc)
REQUIRED_FIELDS = {
    "Version": r"\*\*Version:\*\*\s*[\d.]+",
    "Last Updated": r"\*\*Last Updated:\*\*\s*[\d-]+\s+[\d:]+\s+EST",
}

# Optional but recommended fields
OPTIONAL_FIELDS = {
    "Type": r"\*\*Type:\*\*\s*.+",
    "Description": r"\*\*Description:\*\*\s*.+",
}

# Patterns to identify metadata section
METADATA_SECTION_PATTERN = r"^##\s+Metadata\s*$"
METADATA_FIELD_PATTERN = r"^-\s+\*\*([^*]+):\*\*\s*(.+)$"


def extract_metadata_section(content: str) -> Optional[str]:
    """Extract the metadata section from markdown content."""
    lines = content.split("\n")
    metadata_start = None
    metadata_end = None
    
    for i, line in enumerate(lines):
        if re.match(METADATA_SECTION_PATTERN, line):
            metadata_start = i
        elif metadata_start is not None and line.startswith("## ") and i > metadata_start:
            metadata_end = i
            break
    
    if metadata_start is None:
        return None
    
    if metadata_end is None:
        metadata_end = len(lines)
    
    return "\n".join(lines[metadata_start:metadata_end])


def validate_metadata(metadata_section: str, file_path: Path) -> tuple[bool, list[str]]:
    """Validate metadata section against requirements."""
    errors = []
    
    # Check required fields
    for field_name, pattern in REQUIRED_FIELDS.items():
        if not re.search(pattern, metadata_section, re.MULTILINE | re.IGNORECASE):
            errors.append(f"Missing required field: {field_name}")
    
    # Check version format
    version_match = re.search(r"\*\*Version:\*\*\s*([\d.]+)", metadata_section, re.IGNORECASE)
    if version_match:
        version = version_match.group(1)
        parts = version.split(".")
        if len(parts) not in [2, 3]:
            errors.append(f"Invalid version format: {version} (expected X.Y or X.Y.Z)")
        elif not all(part.isdigit() for part in parts):
            errors.append(f"Invalid version format: {version} (must be numeric)")
    
    # Check last updated format
    last_updated_match = re.search(
        r"\*\*Last Updated:\*\*\s*(\d{4}-\d{2}-\d{2})\s+(\d{2}:\d{2}:\d{2})\s+(EST|PST|UTC)",
        metadata_section,
        re.IGNORECASE
    )
    if not last_updated_match:
        errors.append("Invalid 'Last Updated' format (expected: YYYY-MM-DD HH:MM:SS EST)")
    
    return len(errors) == 0, errors


def validate_file(file_path: Path) -> tuple[bool, list[str]]:
    """Validate a single markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        return False, [f"Error reading file: {e}"]
    
    # Extract metadata section
    metadata_section = extract_metadata_section(content)
    
    if metadata_section is None:
        return False, ["Missing '## Metadata' section"]
    
    # Validate metadata
    is_valid, errors = validate_metadata(metadata_section, file_path)
    
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
                check=True
            )
            files = [
                Path(f) for f in result.stdout.strip().split("\n")
                if f.endswith(".md") and Path(f).exists()
            ]
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
        print("\nRequired metadata format:")
        print("## Metadata")
        print("- **Version:** X.Y or X.Y.Z")
        print("- **Last Updated:** YYYY-MM-DD HH:MM:SS EST")
        print("- **Type:** [Documentation Type]")
        print("- **Description:** [Brief description]")
        return 1
    
    return 0


if __name__ == "__main__":
    sys.exit(main())

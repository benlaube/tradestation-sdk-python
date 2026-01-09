#!/usr/bin/env python3
"""
Convert markdown metadata sections to YAML frontmatter format.

Converts existing markdown metadata (## Metadata section) to YAML frontmatter
at the top of files.

Usage:
    python scripts/convert-markdown-metadata.py [file1.md] [file2.md] ...
"""

import re
import sys
from datetime import datetime
from pathlib import Path


# Date format conversion: YYYY-MM-DD or MM-DD-YYYY to MM-DD-YYYY HH:MM:SS EST
def convert_date(date_str: str) -> str:
    """Convert date string to MM-DD-YYYY HH:MM:SS EST format."""
    # Try to parse various date formats
    date_str = date_str.strip()

    # If already in MM-DD-YYYY format, add time
    if re.match(r"^\d{2}-\d{2}-\d{4}", date_str):
        if "EST" in date_str or ":" in date_str:
            # Already has time, just ensure format
            return date_str
        else:
            # Add current time
            now = datetime.now()
            return f"{date_str} {now.strftime('%H:%M:%S')} EST"

    # Try YYYY-MM-DD format
    if re.match(r"^\d{4}-\d{2}-\d{2}", date_str):
        parts = date_str.split("-")
        if len(parts) == 3:
            # Convert YYYY-MM-DD to MM-DD-YYYY
            if "EST" in date_str or ":" in date_str:
                # Has time, extract and convert
                time_part = ""
                if " " in date_str:
                    date_part, rest = date_str.split(" ", 1)
                    time_part = " " + rest
                else:
                    date_part = date_str.replace(" EST", "").strip()
                    time_part = " EST"

                parts = date_part.split("-")
                if len(parts) == 3:
                    return f"{parts[1]}-{parts[2]}-{parts[0]}{time_part}"
            else:
                now = datetime.now()
                return f"{parts[1]}-{parts[2]}-{parts[0]} {now.strftime('%H:%M:%S')} EST"

    # If can't parse, use current date
    now = datetime.now()
    return now.strftime("%m-%d-%Y %H:%M:%S EST")


def extract_markdown_metadata(content: str) -> tuple[dict | None, int, int]:
    """Extract markdown metadata section."""
    lines = content.split("\n")
    metadata_start = None
    metadata_end = None

    for i, line in enumerate(lines):
        if re.match(r"^##\s+Metadata\s*$", line):
            metadata_start = i
        elif metadata_start is not None:
            # End on next ## heading or --- separator
            if line.startswith("## ") or (line.strip() == "---" and i > metadata_start + 1):
                metadata_end = i
                break

    if metadata_start is None:
        return None, 0, 0

    if metadata_end is None:
        metadata_end = len(lines)

    metadata_section = "\n".join(lines[metadata_start:metadata_end])
    metadata = {}

    # Parse markdown list format: - **Field:** value
    for line in metadata_section.split("\n"):
        match = re.match(r"^-\s+\*\*([^*]+):\*\*\s*(.+)$", line)
        if match:
            field = match.group(1).strip().lower().replace(" ", "")
            value = match.group(2).strip()

            # Convert field names
            if field == "version":
                metadata["version"] = value
            elif field == "lastupdated":
                metadata["lastUpdated"] = convert_date(value)
            elif field == "type":
                metadata["type"] = value
            elif field == "status":
                metadata["status"] = value
            elif field == "description":
                metadata["description"] = value
            elif field == "created":
                metadata["created"] = convert_date(value)
            else:
                # Keep other fields as-is (camelCase)
                camel_field = "".join(
                    word.capitalize() if i > 0 else word.lower() for i, word in enumerate(field.split())
                )
                metadata[camel_field] = value

    return metadata, metadata_start, metadata_end


def convert_file(file_path: Path) -> bool:
    """Convert a single markdown file."""
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return False

    # Check if already has YAML frontmatter
    if content.strip().startswith("---"):
        print(f"⏭️  {file_path}: Already has YAML frontmatter")
        return True

    # Extract markdown metadata
    metadata, start, end = extract_markdown_metadata(content)

    if metadata is None:
        # Try to extract from other formats (like README.md with **Version:** at top)
        lines = content.split("\n")
        for i, line in enumerate(lines[:20]):  # Check first 20 lines
            if "**Version:**" in line or "**Last Updated:**" in line:
                # Found metadata in different format, extract it
                metadata = {}
                for j in range(i, min(i + 10, len(lines))):
                    if "**Version:**" in lines[j]:
                        match = re.search(r"\*\*Version:\*\*\s*(.+)", lines[j])
                        if match:
                            metadata["version"] = match.group(1).strip()
                    elif "**Last Updated:**" in lines[j] or "**Last Updated:**" in lines[j]:
                        match = re.search(r"\*\*Last Updated:\*\*\s*(.+)", lines[j])
                        if match:
                            metadata["lastUpdated"] = convert_date(match.group(1).strip())
                    elif "**SDK Version:**" in lines[j]:
                        match = re.search(r"\*\*SDK Version:\*\*\s*(.+)", lines[j])
                        if match:
                            if "version" not in metadata:
                                metadata["version"] = match.group(1).strip()

                if metadata:
                    # Remove old metadata lines
                    new_lines = lines[:i] + lines[i + 3 :] if i + 3 < len(lines) else lines[:i]
                    content = "\n".join(new_lines)
                    break

        if not metadata:
            print(f"⚠️  {file_path}: No metadata found, adding minimal frontmatter")
            # Add minimal required metadata
            now = datetime.now()
            metadata = {
                "version": "1.0.0",
                "lastUpdated": now.strftime("%m-%d-%Y %H:%M:%S EST"),
                "type": "Documentation",
                "description": "Documentation file",
            }
            # Insert at beginning
            yaml_frontmatter = "---\n"
            for key, value in metadata.items():
                yaml_frontmatter += f"{key}: {value}\n"
            yaml_frontmatter += "---\n\n"
            new_content = yaml_frontmatter + content
            file_path.write_text(new_content, encoding="utf-8")
            print(f"✅ {file_path}: Added minimal YAML frontmatter")
            return True

    if metadata:
        # Ensure required fields
        if "version" not in metadata:
            metadata["version"] = "1.0.0"
        if "lastUpdated" not in metadata:
            now = datetime.now()
            metadata["lastUpdated"] = now.strftime("%m-%d-%Y %H:%M:%S EST")

        # Create YAML frontmatter
        yaml_frontmatter = "---\n"
        for key, value in metadata.items():
            yaml_frontmatter += f"{key}: {value}\n"
        yaml_frontmatter += "---\n\n"

        # Remove old metadata section
        lines = content.split("\n")
        if start > 0 and end > 0:
            new_lines = lines[:start] + lines[end + 1 :]
        else:
            new_lines = lines

        # Remove leading empty lines from content
        while new_lines and not new_lines[0].strip():
            new_lines.pop(0)

        new_content = yaml_frontmatter + "\n".join(new_lines)
        file_path.write_text(new_content, encoding="utf-8")
        print(f"✅ {file_path}: Converted to YAML frontmatter")
        return True

    return False


def main():
    """Main conversion function."""
    if len(sys.argv) > 1:
        files = [Path(f) for f in sys.argv[1:]]
    else:
        print("Usage: python scripts/convert-markdown-metadata.py [file1.md] [file2.md] ...")
        return 1

    converted = 0
    for file_path in files:
        if file_path.exists() and file_path.suffix == ".md":
            if convert_file(file_path):
                converted += 1
        else:
            print(f"⚠️  {file_path}: Not a markdown file or doesn't exist")

    print(f"\n✅ Converted {converted} file(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())

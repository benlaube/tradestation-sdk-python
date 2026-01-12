#!/usr/bin/env python3
"""
Validate links in Markdown files.

Checks for:
1. Broken local file links
2. Broken anchor links (within same file or other files)
3. Validates relative paths

Usage:
    python scripts/validate_links.py
"""

import re
import sys
import urllib.parse
from pathlib import Path

# Regex to find markdown links: [text](link)
LINK_PATTERN = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
# Regex to find headings for anchors: # Heading or <a id="anchor">
HEADING_PATTERN = re.compile(r"^(#+)\s+(.+)$")
HTML_ANCHOR_PATTERN = re.compile(r'<a\s+[^>]*id="([^"]+)"')


def get_anchors_from_file(file_path: Path) -> set[str]:
    """Extract all valid anchors (headings and IDs) from a markdown file."""
    anchors = set()
    try:
        content = file_path.read_text(encoding="utf-8")
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return anchors

    # GitHub-style header anchors: lowercase, spaces to hyphens, remove punctuation
    for line in content.splitlines():
        # Markdown headings
        match = HEADING_PATTERN.match(line)
        if match:
            heading_text = match.group(2).strip()
            # Basic GitHub slugification (approximate)
            slug = heading_text.lower().replace(" ", "-")
            slug = re.sub(r"[^\w\-]", "", slug)
            anchors.add(slug)

        # HTML anchors
        for match in HTML_ANCHOR_PATTERN.finditer(line):
            anchors.add(match.group(1))

    return anchors


def validate_link(
    source_file: Path, link: str, project_root: Path, anchor_cache: dict[Path, set[str]]
) -> tuple[bool, str]:
    """
    Validate a single link.
    Returns (is_valid, error_message).
    """
    # Ignore web links
    if link.startswith(("http://", "https://", "mailto:")):
        return True, ""

    # Split link and anchor
    parsed = urllib.parse.urlparse(link)
    path = parsed.path
    anchor = parsed.fragment

    # 1. Internal Anchor (#anchor)
    if not path and anchor:
        if source_file not in anchor_cache:
            anchor_cache[source_file] = get_anchors_from_file(source_file)

        if anchor not in anchor_cache[source_file]:
            # Try loosely (GitHub sometimes allows different slugification)
            return False, f"Anchor #{anchor} not found in {source_file.name}"
        return True, ""

    # 2. Local File Link
    if path:
        # Resolve absolute path relative to source file
        try:
            # Handle absolute paths from root (starting with /) vs relative
            if path.startswith("/"):
                # metrics/foo.md -> relative to project root usually, but in standard markdown / usually means root
                target_file = (project_root / path.lstrip("/")).resolve()
            else:
                target_file = (source_file.parent / path).resolve()
        except OSError:
            return False, f"Invalid path syntax: {path}"

        # Check if file exists
        if not target_file.exists():
            return False, f"File not found: {path} (resolved to {target_file})"

        # Check if target is a file or directory
        if target_file.is_dir():
            # Warning only, or check for index/README?
            # Usually linking to a dir is fine if it renders the dir listing or README
            if not (target_file / "README.md").exists() and not (target_file / "index.md").exists():
                return True, ""  # Accepting directory links for now

        # 3. Anchor in Target File
        if anchor:
            if target_file not in anchor_cache:
                anchor_cache[target_file] = get_anchors_from_file(target_file)

            if anchor not in anchor_cache[target_file]:
                return False, f"Anchor #{anchor} not found in {target_file.name}"

    return True, ""


def main():
    root_dir = Path.cwd()
    print(f"Validating markdown links in: {root_dir}")

    error_count = 0
    anchor_cache = {}

    # Find all .md files
    md_files = list(root_dir.rglob("*.md"))

    for file_path in md_files:
        # Skip node_modules or hidden dirs
        if ".git" in file_path.parts or "node_modules" in file_path.parts:
            continue

        try:
            content = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            print(f"Skipping binary/unreadable file: {file_path}")
            continue

        # Find all links
        for match in LINK_PATTERN.finditer(content):
            text = match.group(1)
            link = match.group(2)

            is_valid, error = validate_link(file_path, link, root_dir, anchor_cache)
            if not is_valid:
                error_count += 1
                rel_path = file_path.relative_to(root_dir)
                print(f"❌ {rel_path}: Broken link '[{text}]({link})' -> {error}")

    if error_count == 0:
        print("✅ All links valid!")
        sys.exit(0)
    else:
        print(f"\nExample link validation complete. Found {error_count} broken links.")
        sys.exit(1)


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Strip remaining Wayback Machine references from downloaded static files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

WAYBACK_PATTERNS = [
    # Wayback toolbar / banner scripts
    re.compile(r'<script[^>]*src=["\'][^"\']*web-static\.archive\.org[^"\']*["\'][^>]*></script>', re.I),
    re.compile(r'<link[^>]*href=["\'][^"\']*web-static\.archive\.org[^"\']*["\'][^>]*/?>', re.I),
    re.compile(r'<!-- BEGIN WAYBACK TOOLBAR INSERT -->.*?<!-- END WAYBACK TOOLBAR INSERT -->', re.S | re.I),
    # Wayback replay URLs → original paths
    re.compile(
        r'https?://web\.archive\.org/web/\d+[a-z]*_/(https?://[^"\'\s\)]+)',
        re.I,
    ),
    re.compile(
        r'/web/\d+[a-z]*_/(https?://[^"\'\s\)]+)',
        re.I,
    ),
    # Wayback __wm init scripts
    re.compile(r'<script[^>]*>.*?__wm\.init.*?</script>', re.S | re.I),
]

TEXT_EXTENSIONS = {".html", ".htm", ".css", ".js", ".json", ".xml", ".svg"}


def _rewrite_wayback_urls(content: str) -> str:
    for pattern in WAYBACK_PATTERNS[:3]:
        content = pattern.sub("", content)
    for pattern in WAYBACK_PATTERNS[3:5]:
        content = pattern.sub(lambda m: m.group(1), content)
    content = WAYBACK_PATTERNS[5].sub("", content)
    return content


def cleanup_directory(site_dir: Path) -> tuple[int, int]:
    files_changed = 0
    refs_removed = 0

    for path in site_dir.rglob("*"):
        if not path.is_file() or path.suffix.lower() not in TEXT_EXTENSIONS:
            continue
        try:
            original = path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue

        before_count = original.lower().count("web.archive.org") + original.lower().count("archive.org")
        cleaned = _rewrite_wayback_urls(original)
        after_count = cleaned.lower().count("web.archive.org") + cleaned.lower().count("archive.org")

        if cleaned != original:
            path.write_text(cleaned, encoding="utf-8")
            files_changed += 1
            refs_removed += before_count - after_count

    return files_changed, refs_removed


def main() -> int:
    site_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    if not site_dir.is_dir():
        print(f"Error: {site_dir} is not a directory", file=sys.stderr)
        return 1

    files_changed, refs_removed = cleanup_directory(site_dir)
    print(f"Cleaned {files_changed} files, removed ~{refs_removed} archive references")
    return 0


if __name__ == "__main__":
    sys.exit(main())

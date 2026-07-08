#!/usr/bin/env python3
"""Download centerindustrial.com from the Wayback Machine archive.

Skips live-site fallback because centerindustrial.com is down — we are
rebuilding specifically from the archive.

Usage:
    export WAYBACK_URL="https://web.archive.org/web/20250404141503/https://centerindustrial.com/"
    export OUTPUT_DIR="./site"
    python3 scripts/download-wayback.py
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

import requests
from wayback_archive.config import Config
from wayback_archive.downloader import WaybackDownloader

LIVE_DOMAINS = {"centerindustrial.com", "www.centerindustrial.com"}
SKIP_LIVE_FALLBACK = os.getenv("SKIP_LIVE_FALLBACK", "true").lower() in ("true", "1", "yes")


def _is_live_site_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.netloc in LIVE_DOMAINS


def _patch_skip_live_fallback() -> None:
    """Prevent wayback-archive from hitting the dead live site."""
    if not SKIP_LIVE_FALLBACK:
        return

    original_get = requests.Session.get

    def patched_get(self, url, *args, **kwargs):
        if _is_live_site_url(url):
            raise requests.exceptions.ConnectionError(
                f"Skipping live site (known down): {url[:80]}"
            )
        return original_get(self, url, *args, **kwargs)

    requests.Session.get = patched_get


def _fix_trailing_slash_paths(output_dir: Path) -> int:
    """Fix wayback-archive bug: trailing-slash URLs overwrite index.html."""
    fixed = 0
    for html_file in output_dir.rglob("index.html"):
        parent = html_file.parent
        if parent == output_dir:
            continue
        # If parent dir name looks like a path segment, ensure it's a directory
        rel = parent.relative_to(output_dir)
        if not rel.parts:
            continue
        # Check if a sibling file stole this path (flat file named after dir)
        segment = rel.parts[-1]
        flat_file = parent.parent / f"{segment}.html"
        if flat_file.exists() and flat_file != html_file:
            # Move flat file into proper directory
            target = parent / "index.html"
            if not target.exists() or target.stat().st_size < flat_file.stat().st_size:
                target.parent.mkdir(parents=True, exist_ok=True)
                flat_file.rename(target)
                fixed += 1
    return fixed


def main() -> int:
    sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, "reconfigure") else None

    config = Config()
    is_valid, error = config.validate()
    if not is_valid:
        print(f"Error: {error}", file=sys.stderr, flush=True)
        return 1

    _patch_skip_live_fallback()
    if SKIP_LIVE_FALLBACK:
        print("Live-site fallback: DISABLED (centerindustrial.com is down)", flush=True)

    downloader = WaybackDownloader(config)
    try:
        downloader.download()
    except KeyboardInterrupt:
        print("\nDownload interrupted by user", flush=True)
        return 1
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr, flush=True)
        return 1

    output_dir = Path(config.output_dir)
    fixed = _fix_trailing_slash_paths(output_dir)
    if fixed:
        print(f"Fixed {fixed} trailing-slash path(s)", flush=True)

    return 0


if __name__ == "__main__":
    sys.exit(main())

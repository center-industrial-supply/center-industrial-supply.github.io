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
import sys
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
    """Prevent wayback-archive from hitting or logging attempts against the dead live site."""
    if not SKIP_LIVE_FALLBACK:
        return

    import builtins

    real_print = builtins.print
    original_get = requests.Session.get

    def filtered_print(*args, **kwargs):
        msg = str(args[0]) if args else ""
        if "trying original URL" in msg or "Downloaded from original URL" in msg:
            return
        return real_print(*args, **kwargs)

    def patched_get(self, url, *args, **kwargs):
        if _is_live_site_url(url):
            raise requests.exceptions.ConnectionError(
                f"Skipping live site (known down): {url[:80]}"
            )
        return original_get(self, url, *args, **kwargs)

    builtins.print = filtered_print
    requests.Session.get = patched_get


def _patch_trailing_slash_path_bug() -> None:
    """Fix wayback-archive bug: /about-us/ overwrites root index.html."""
    original_get_local_path = WaybackDownloader._get_local_path

    def patched_get_local_path(self, url: str):
        from urllib.parse import urlparse, unquote
        import os
        from pathlib import Path

        parsed = urlparse(url)

        if "fonts.googleapis.com" in parsed.netloc or "fonts.gstatic.com" in parsed.netloc:
            return original_get_local_path(self, url)
        if self._is_squarespace_cdn(url):
            return original_get_local_path(self, url)

        path = unquote(parsed.path)
        while path.startswith("/"):
            path = path[1:]
        while "//" in path:
            path = path.replace("//", "/")

        # Fixed: preserve directory structure for trailing-slash URLs
        if not path:
            path = "index.html"
        elif path.endswith("/"):
            path = path.rstrip("/") + "/index.html"

        known_asset_extensions = {
            ".css", ".js", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp",
            ".ico", ".woff", ".woff2", ".ttf", ".eot", ".otf", ".pdf", ".zip",
            ".mp4", ".mp3", ".avi", ".mov", ".wmv", ".flv", ".doc", ".docx",
        }
        has_extension = "." in os.path.basename(path)
        is_asset = has_extension and os.path.splitext(path)[1].lower() in known_asset_extensions

        if not has_extension and not is_asset:
            dir_part = os.path.dirname(path) if os.path.dirname(path) else ""
            base_part = os.path.basename(path) if os.path.basename(path) else "index"
            if dir_part:
                path = os.path.join(dir_part, base_part + ".html")
            else:
                path = base_part + ".html"

        return Path(self.config.output_dir) / path

    WaybackDownloader._get_local_path = patched_get_local_path


def main() -> int:
    sys.stdout.reconfigure(line_buffering=True) if hasattr(sys.stdout, "reconfigure") else None

    config = Config()
    is_valid, error = config.validate()
    if not is_valid:
        print(f"Error: {error}", file=sys.stderr, flush=True)
        return 1

    _patch_skip_live_fallback()
    _patch_trailing_slash_path_bug()
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

    return 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Verify every brand in src/data/brands.ts has a resolvable logo asset."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS_TS = ROOT / "src" / "data" / "brands.ts"


def main() -> int:
    text = BRANDS_TS.read_text(encoding="utf-8")
    entries = re.findall(
        r'name:\s*"([^"]+)"\s*,\s*slug:\s*"([^"]+)"\s*,\s*logo:\s*"([^"]*)"',
        text,
    )

    if not entries:
        print("No brands found in brands.ts", file=sys.stderr)
        return 1

    errors: list[str] = []
    for name, slug, logo in entries:
        if not logo:
            errors.append(f"{name} ({slug}): logo path is empty")
            continue

        asset = ROOT / "public" / logo.lstrip("/")
        if not asset.is_file():
            errors.append(f"{name} ({slug}): missing file {logo}")
            continue

        if asset.read_bytes()[:40].startswith(b"version https://git-lfs.github.com"):
            errors.append(f"{name} ({slug}): LFS pointer at {logo}")

    if errors:
        print("Brand logo validation failed:")
        for err in errors:
            print(f"  - {err}")
        return 1

    print(f"All {len(entries)} brand logos validated.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

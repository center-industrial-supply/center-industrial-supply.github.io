#!/usr/bin/env python3
"""Confirm every brand logo path in brands.ts resolves to a real image file."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BRANDS_TS = ROOT / "src" / "data" / "brands.ts"
PUBLIC = ROOT / "public"


def main() -> int:
    text = BRANDS_TS.read_text(encoding="utf-8")
    names = re.findall(r'name:\s*"([^"]+)"', text)
    logos = re.findall(r'logo:\s*"([^"]*)"', text)
    if len(names) != len(logos):
        print(f"Parse mismatch: {len(names)} names vs {len(logos)} logos")
        return 1

    failed = 0
    for name, logo in zip(names, logos, strict=True):
        if name == "Weldflame" and logo == "":
            print(f"OK  {name:16} (wordmark fallback)")
            continue
        if not logo:
            print(f"FAIL {name}: empty logo")
            failed += 1
            continue
        path = PUBLIC / logo.lstrip("/")
        if not path.is_file():
            print(f"FAIL {name}: missing {path}")
            failed += 1
            continue
        head = path.read_bytes()[:80]
        if head.startswith(b"version https://git-lfs.github.com/spec"):
            print(f"FAIL {name}: LFS pointer {path}")
            failed += 1
            continue
        print(f"OK  {name:16} {logo}")

    if "Hgstar" in names:
        print("FAIL Hgstar is still in brands.ts")
        failed += 1

    required = {
        "JFY",
        "Weldmax",
        "DWT",
        "Norton",
        "HR Laser",
        "Taiwan Plasma",
        "Axxair",
        "Max Photonics",
    }
    missing = required - set(names)
    if missing:
        print(f"FAIL missing brands: {sorted(missing)}")
        failed += 1

    print(f"{len(names)} brands checked")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Last-resort fixes for remaining 14 product images."""

from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS = ROOT / "src/content/products"
DL = ROOT / ".cursor/skills/retrieve-product-image/scripts/download-product-image.py"

FIXES = {
    # Axxair (axxair.com product pages)
    "open-head-orbital-welding": "https://www.axxair.com/wp-content/uploads/sites/23/2026/04/SATO-115.jpg",
    "closed-head-orbital-welding": "https://www.axxair.com/wp-content/uploads/sites/23/2026/04/SATFX-115.jpg",
    # AMG — use wayback full-size paths that matched earlier successful batch pattern
    "amg-cnc-h-beam-drilling-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/AMG-CNC-H-Beam-Drilling-Machine-1.jpg",
    "table-type-cnc-cutting-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2021/01/FSC510-1.png",
    # Wilson — kayo.com.tw is Wilson OEM; fallback to wayback centerindustrial archive
    "kh-101-gas-pressure-regulator-medium-duty-ul-listed-en-iso-2503-as-426": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/KH-101E-Gas-Regulator-Oxygen-_-Acetylene.jpg",
    "kh-101-lm-flowgauge-regulator-ul-listed-en-iso-2503": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/KH-101-30LM-CD-32-MD-Flowgauge-Regulator.jpg",
    "kfr-101-electrically-co2-pre-heated-flowmeter-regulator": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-15-at-2.35.00-PM.png",
    "wilson-f621-series-flashback-arrestors-for-regulator-ul-listed-en-iso-5175-1": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/F621-9-Flashback-Arrestor-for-regulators.png",
    # OTC legacy models — wayback archive of original site product photos
    "aii-1pc-series-1pb-series-2pf-series": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/all-in-one.jpg",
    "dm-350": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/DM-350.jpg",
    "xds-350sii-500sii": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/XD-350SII_500SII.png",
    "otc-wt3510-co2-mig-mag-blue-torch-ii": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2023/06/Untitled-design-18-1.png",
    # Weldflame gloves — wayback archive
    "weldflame-welding-gloves-orange": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2023/05/Weldflame-MMA-MIG-welding-gloves-01-orange.jpg",
    "weldflame-welding-gloves-yellow": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2023/05/Weldflame-MMA-MIG-welding-gloves-02-yellow.jpg",
}


def make_filename(brand: str, title: str, ext: str) -> str:
    bp = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-")
    tp = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")
    return f"{bp}-{tp}{ext}"


def update_fm(path: Path, image_path: str) -> None:
    lines = path.read_text().splitlines(keepends=True)
    end = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    fm, body = lines[1:end], lines[end:]
    new_fm, skip = [], False
    for line in fm:
        if line.startswith("images:"):
            skip = True
            continue
        if skip and line.startswith("- "):
            continue
        skip = False
        new_fm.append(line)
    ins = len(new_fm)
    for i, l in enumerate(new_fm):
        if l.startswith("category:"):
            ins = i + 1
            break
    new_fm.insert(ins, "images:\n")
    new_fm.insert(ins + 1, f'  - "{image_path}"\n')
    path.write_text("".join(["---\n", *new_fm, *body]))


def download(url: str, slug: str, brand: str, title: str) -> str | None:
    ext = Path(url.split("?")[0]).suffix.lower() or ".jpg"
    if ext == ".jpeg":
        ext = ".jpg"
    fn = make_filename(brand, title, ext)
    out = f"public/images/products/{slug}/{fn}"
    full = ROOT / out
    if full.exists() and full.stat().st_size > 4000:
        return f"/images/products/{slug}/{fn}"
    r = subprocess.run(
        [sys.executable, str(DL), "--url", url, "--output", out,
         "--min-width", "200", "--min-height", "200", "--min-bytes", "3000"],
        capture_output=True, text=True,
    )
    if r.returncode != 0:
        if full.exists():
            full.unlink()
        print(f"  ERR {slug}: {r.stderr.strip()}", file=sys.stderr)
        return None
    return f"/images/products/{slug}/{fn}"


def main() -> None:
    ok = fail = 0
    failed = []
    for slug, url in sorted(FIXES.items()):
        path = PRODUCTS / f"{slug}.md"
        text = path.read_text()
        if re.search(r'^images:\s*\n\s+-\s+"', text, re.M):
            print(f"SKIP {slug}")
            continue
        brand = re.search(r'^brand:\s*"([^"]+)"', text, re.M).group(1)
        title = re.search(r'^title:\s*"([^"]+)"', text, re.M).group(1)
        site = download(url, slug, brand, title)
        if site:
            update_fm(path, site)
            ok += 1
            print(f"OK   {slug}: {site}")
        else:
            fail += 1
            failed.append(slug)
            print(f"FAIL {slug}")
        time.sleep(0.2)
    print(f"\nOK={ok} FAIL={fail}")
    if failed:
        print("Failed:", ", ".join(failed))


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Final pass: assign remaining product images with verified source URLs."""

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
    # OTC robots (otc-daihen.com — largest productImages per page)
    "fd-b6": "https://otc-daihen.com/assets/image-cache//storage/productImages/NogE14RUmiNXqKvP6EHdoBp9trKu6TO2yGcFxuvi.21f5ac33.webp",
    "fd-b6l": "https://otc-daihen.com/assets/image-cache//storage/productImages/1iHkZmnawCTGJvXfstdqS4safbKHXaYy5BXj9KVh.21f5ac33.webp",
    "fd-v8": "https://otc-daihen.com/assets/image-cache//storage/productImages/6IhVMRg6lpLhMxT4vwYzmXS3MblHeP3tj2YLJC7P.21f5ac33.webp",
    "fd-v8l-2": "https://otc-daihen.com/assets/image-cache//storage/productImages/27qfEoUpjTwfGpWcsyoJ6FF6mpxLav3qV92brmhu.21f5ac33.webp",
    "fd-v25-fd-v50-fd-v80-fd-v100-fd-v130-fd-v166": "https://otc-daihen.com/assets/image-cache//storage/productImages/pJQ5v9h8QIna1cYeGxQIs5n65e9xT1APYUOXDdRI.21f5ac33.webp",
    "fd-v6s-7-axis": "https://otc-daihen.com/assets/image-cache//storage/productImages/hps6OWDgLz01Wmvsj9A5KVk8yKWwUUgybt2BF57b.21f5ac33.webp",
    "synchro-feed": "https://otc-daihen.com/assets/image-cache/template/Medien/Bilder/Home/yt-thumbnail-synchrofeed.2b589d97.webp",
    "dm-350": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/DM-350.jpg",
    "xds-350sii-500sii": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/XD-350SII_500SII.png",
    "aii-1pc-series-1pb-series-2pf-series": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/all-in-one.jpg",
    "otc-wt3510-co2-mig-mag-blue-torch-ii": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2023/06/Untitled-design-18-1.png",
    # DWT (dwt-gmbh.de)
    "pipe-beveler-mf3-25": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveler/pipe-beveler-mf3-25-xl/1-pipe-beveler-mf3-25xl.jpg",
    "pipe-beveler-mf4-r": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveler/pipe-beveler-mf4r/1-pipe-beveler-mf4-r.jpg",
    "pipe-cold-cutting-range-2-48": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-cutting-beveling/pipe-cold-cutting/pipe-cold-cutting-machine-dlw/1-pipe-cold-cutting-machine-dlw.jpg",
    "clamshell-pipe-cold-cutter-type-dlw-hd-48-57": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-cutting-beveling/pipe-cold-cutting/pipe-cold-cutting-machine-dlw/1-pipe-cold-cutting-machine-dlw.jpg",
    # Axxair wayback for welding heads
    "closed-head-orbital-welding": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/SATF-40NDHX.jpg",
    "open-head-orbital-welding": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/SATO-115.jpg",
    # AMG wayback
    "amg-cnc-h-beam-drilling-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/AMG-CNC-H-Beam-Drilling-Machine-1.jpg",
    "table-type-cnc-cutting-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2021/01/FSC510-1.png",
    # Wilson wayback
    "kh-101-gas-pressure-regulator-medium-duty-ul-listed-en-iso-2503-as-426": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/KH-101E-Gas-Regulator-Oxygen-_-Acetylene.jpg",
    "kh-101-lm-flowgauge-regulator-ul-listed-en-iso-2503": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/KH-101-30LM-CD-32-MD-Flowgauge-Regulator.jpg",
    "kfr-101-electrically-co2-pre-heated-flowmeter-regulator": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-15-at-2.35.00-PM.png",
    "wilson-f621-series-flashback-arrestors-for-regulator-ul-listed-en-iso-5175-1": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/F621-9-Flashback-Arrestor-for-regulators.png",
    # Weldflame — weldflame.com unreachable (SSL); qgweld.com hosts OEM product photography for same models
    "cg2-11-magnetic-pipe-gas-cutting-machine": "https://www.qgweld.com/wp-content/uploads/2023/11/Automatic-Pipe-Gas-Plasma-Cutter.jpg",
    "hk12-portable-gas-cutting-machine-single-torch": "https://www.qgweld.com/wp-content/uploads/2023/08/HK-12-beetle-portable-flame-cutting-machine1.jpg",
    "hk12-ii-automatic-gas-cutting-machine-double-torch": "https://www.qgweld.com/wp-content/uploads/2023/08/HK-12-beetle-portable-flame-cutting-machine1.jpg",
    "cg2-11g-hand-pipe-cutting-machine": "https://www.qgweld.com/wp-content/uploads/2023/08/CG2-11G-chain-type-beveling-machine1.jpg",
    "cg2-150-profiling-gas-cutting-machine": "https://www.qgweld.com/wp-content/uploads/2023/08/Profiling-Gas-Cutter-CG2-150A-2.jpg",
}


def make_filename(brand: str, title: str, ext: str) -> str:
    bp = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-")
    tp = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")
    return f"{bp}-{tp}{ext}"


def has_images(text: str) -> bool:
    return bool(re.search(r'^images:\s*\n\s+-\s+"', text, re.M))


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
    if full.exists() and full.stat().st_size > 5000:
        return f"/images/products/{slug}/{fn}"
    r = subprocess.run(
        [sys.executable, str(DL), "--url", url, "--output", out,
         "--min-width", "200", "--min-height", "200", "--min-bytes", "4000"],
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
        if not path.exists():
            failed.append((slug, "no-md"))
            fail += 1
            continue
        text = path.read_text()
        if has_images(text):
            print(f"SKIP {slug}")
            continue
        m = re.search(r'^brand:\s*"([^"]+)"', text, re.M)
        t = re.search(r'^title:\s*"([^"]+)"', text, re.M)
        brand = m.group(1) if m else "Brand"
        title = t.group(1) if t else slug
        site = download(url, slug, brand, title)
        if not site:
            fail += 1
            failed.append((slug, url[:70]))
            print(f"FAIL {slug}")
            continue
        update_fm(path, site)
        ok += 1
        print(f"OK   {slug}: {site}")
        time.sleep(0.15)
    print(f"\nOK={ok} FAIL={fail}")
    for s, u in failed:
        print(f"  {s}: {u}")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Fix remaining product image assignments with corrected source resolution."""

from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PRODUCTS_DIR = ROOT / "src" / "content" / "products"
DOWNLOAD_SCRIPT = (
    ROOT / ".cursor/skills/retrieve-product-image/scripts/download-product-image.py"
)
UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

# slug -> image URL (brand official or wayback archive of original site assets)
FIXES: dict[str, str] = {
    # OTC robots/power (otc-daihen.com)
    "fd-a20": "https://otc-daihen.com/assets/image-cache//storage/productImages/eRkEHsimE9I4XtC3detYsot539Q35GgWgpJpXPzS.21f5ac33.webp",
    "fd-b6": "https://otc-daihen.com/assets/image-cache//storage/productImages/7FQYgWsAbLtUymWegbtYlI5AUNEaH2UfbgQSgxE0.6fa0d29a.webp",
    "fd-b6l": "https://otc-daihen.com/assets/image-cache//storage/productImages/ad1hnaiG3zH06RE2INlSNUZqmb2pWVCmIQM9rb0s.6fa0d29a.webp",
    "fd-v8": "https://otc-daihen.com/assets/image-cache//storage/productImages/hA4bF4TzAkYyo041JGDuXwaLeiUqueRX78hoQTBU.6fa0d29a.webp",
    "fd-v8l-2": "https://otc-daihen.com/assets/image-cache//storage/productImages/f7ozQjNx9x1vbYtfvOot8SEoyFMAPbrhqXOCh2X0.6fa0d29a.webp",
    "fd-v6s-7-axis": "https://otc-daihen.com/assets/image-cache//storage/productImages/XdO5VmfkmeNIJl5wT9cyXax4Y00nbfrGrYWzUlKh.6fa0d29a.webp",
    "fd-v25-fd-v50-fd-v80-fd-v100-fd-v130-fd-v166": "https://otc-daihen.com/assets/image-cache//storage/productImages/LeXWkrXO6u5tJp8tCjBGhKZSVBiYPRyKDe9tRlJv.6fa0d29a.webp",
    "cptx-210": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/CPTX-210.jpg",
    "cpve-400ii": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/CPVE-400II.jpg",
    "wb-m350l": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/WB-M350L.jpg",
    "synchro-feed": "https://otc-daihen.com/assets/image-cache/template/Medien/Bilder/Welding/Welding-process/MIG-MAG/Synchrofeed/synchrofeed-pro.db81cd75.webp",
    "dm-350": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/DM-350.jpg",
    "xds-350sii-500sii": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/XD-350SII_500SII.png",
    "aii-1pc-series-1pb-series-2pf-series": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/all-in-one.jpg",
    "otc-wt3510-co2-mig-mag-blue-torch-ii": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2023/06/Untitled-design-18-1.png",
    # DWT (dwt-gmbh.de)
    "pipe-beveler-mf2-25": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveler/pipe-beveler-mf2-25/1-pipe-beveler-mf2-25.jpg",
    "pipe-beveler-mf3-25": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveler/pipe-beveler-mf3-25/1-pipe-beveler-mf3-25.jpg",
    "pipe-beveler-mf3-25xl": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveler/pipe-beveler-mf3-25-xl/1-pipe-beveler-mf3-25xl.jpg",
    "pipe-beveler-mf4-r": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveler/pipe-beveler-mf4-r/1-pipe-beveler-mf4-r.jpg",
    "pipe-beveler-mf4": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveler/pipe-beveler-mf4/1-pipe-beveler-mf4.jpg",
    "pipe-beveling-machine-type-mf2iw": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveling-machine/pipe-beveling-machine-mf2iw/1-pipe-beveling-machine-mf2iw.jpg",
    "pipe-beveling-machine-type-mf3i": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveling-machine/pipe-beveling-machine-mf3i/1-pipe-beveling-machine-mf3i.jpg",
    "pipe-beveling-machine-type-mf3iw": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveling-machine/pipe-beveling-machine-mf3iw/1-pipe-beveling-machine-mf3iw.jpg",
    "pipe-beveling-machine-type-mf4i": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveling-machine/pipe-beveling-machine-mf4i/1-pipe-beveling-machine-mf4i.jpg",
    "pipe-beveling-machine-type-mf5i": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveling-machine/pipe-beveling-machine-mf5i/1-pipe-beveling-machine-mf5i.jpg",
    "pipe-beveling-machine-type-mf6i-50": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-beveling-equipment/pipe-beveling-machine/pipe-beveling-machine-mf6i-50/1-pipe-beveling-machine-mf6i-50.jpg",
    "pipe-cold-cutting-range-2-48": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-cutting-equipment/pipe-cold-cutting-machine/pipe-cold-cutting-machine-2-48/1-pipe-cold-cutting-machine-2-48.jpg",
    "clamshell-pipe-cold-cutter-type-dlw-hd-48-57": "https://www.dwt-gmbh.de/userfiles/image/convert/en/products/pipe-cutting-equipment/pipe-cold-cutting-machine/clamshell-pipe-cold-cutter-dlw-hd-48-57/1-clamshell-pipe-cold-cutter-dlw-hd-48-57.jpg",
    # Axxair (axxair.com)
    "axxair-orbital-welding-machines": "https://www.axxair.com/wp-content/uploads/sites/23/2026/05/DSC_0037.jpg",
    "prefabrication-orbital-welding": "https://www.axxair.com/wp-content/uploads/sites/23/2026/05/DSC_0037.jpg",
    "sx122-172-222-322-simple-wire": "https://www.axxair.com/wp-content/uploads/sites/23/2026/05/DSC_0037.jpg",
    "sx122-172-222-322-avc-osc": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/AVC_OSC.jpg",
    "open-head-orbital-welding": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/SATO-115.jpg",
    "closed-head-orbital-welding": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/SATF-40NDHX.jpg",
    # AMG (wayback archive)
    "amg-cnc-h-beam-drilling-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/AMG-CNC-H-Beam-Drilling-Machine-1.jpg",
    "table-type-cnc-cutting-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2021/01/FSC510-1.png",
    # Wilson (wayback archive)
    "kh-101-gas-pressure-regulator-medium-duty-ul-listed-en-iso-2503-as-426": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/KH-101E-Gas-Regulator-Oxygen-_-Acetylene.jpg",
    "kh-101-lm-flowgauge-regulator-ul-listed-en-iso-2503": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/KH-101-30LM-CD-32-MD-Flowgauge-Regulator.jpg",
    "kfr-101-electrically-co2-pre-heated-flowmeter-regulator": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/Screen-Shot-2020-10-15-at-2.35.00-PM.png",
    "wilson-f621-series-flashback-arrestors-for-regulator-ul-listed-en-iso-5175-1": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/F621-9-Flashback-Arrestor-for-regulators.png",
    # Weldflame (wayback archive)
    "hk12-portable-gas-cutting-machine-single-torch": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/HK12-Portable-Gas-Cutting-Machine-single-torch.jpg",
    "hk12-ii-automatic-gas-cutting-machine-double-torch": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/HK12-II-Portable-Gas-Cutting-Machine-Double-Torch.jpg",
    "cg2-11-magnetic-pipe-gas-cutting-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/CG2-11-Magnetic-Pipe-Gas-Cutting-Machine.bmp",
    "cg2-11g-hand-pipe-cutting-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/CG2-11G-Hand-type-Pipe-Gas-Cutting-Machine.bmp",
    "cg2-150-profiling-gas-cutting-machine": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2020/10/CG2-150-Profile-Gas-Cutting-Machine.bmp",
    "weldflame-welding-gloves-orange": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2023/05/Weldflame-MMA-MIG-welding-gloves-01-orange.jpg",
    "weldflame-welding-gloves-yellow": "https://web.archive.org/web/https://centerindustrial.com/wp-content/uploads/2023/05/Weldflame-MMA-MIG-welding-gloves-02-yellow.jpg",
}


def make_filename(brand: str, title: str, ext: str) -> str:
    brand_part = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-")
    title_part = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")
    return f"{brand_part}-{title_part}{ext}"


def parse_product(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key in ("title", "slug", "brand"):
        match = re.search(rf'^{key}:\s*"([^"]+)"', text, re.M)
        if match:
            fields[key] = match.group(1)
    fields["has_images"] = bool(re.search(r'^images:\s*\n\s+-\s+"', text, re.M))
    return fields


def update_frontmatter(path: Path, image_path: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    end_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    frontmatter = lines[1:end_idx]
    body = lines[end_idx:]
    new_fm: list[str] = []
    skip = False
    for line in frontmatter:
        if line.startswith("images:"):
            skip = True
            continue
        if skip and line.startswith("- "):
            continue
        skip = False
        new_fm.append(line)
    insert_idx = len(new_fm)
    for idx, line in enumerate(new_fm):
        if line.startswith("category:"):
            insert_idx = idx + 1
            break
    for idx, line in enumerate(new_fm):
        if line.startswith("brand:") and insert_idx == len(new_fm):
            insert_idx = idx + 1
    new_fm.insert(insert_idx, "images:\n")
    new_fm.insert(insert_idx + 1, f'  - "{image_path}"\n')
    path.write_text("".join(["---\n", *new_fm, *body]), encoding="utf-8")


def download(url: str, slug: str, brand: str, title: str) -> str | None:
    ext = Path(url.split("?")[0]).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
        ext = ".jpg"
    if ext == ".jpeg":
        ext = ".jpg"
    filename = make_filename(brand, title, ext)
    rel_output = f"public/images/products/{slug}/{filename}"
    output = ROOT / rel_output
    if output.exists() and output.stat().st_size > 5000:
        return f"/images/products/{slug}/{filename}"

    result = subprocess.run(
        [
            sys.executable,
            str(DOWNLOAD_SCRIPT),
            "--url",
            url,
            "--output",
            rel_output,
            "--min-width",
            "250",
            "--min-height",
            "250",
            "--min-bytes",
            "5000",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if output.exists():
            output.unlink()
        print(f"  ERR: {result.stderr.strip()}", file=sys.stderr)
        return None
    return f"/images/products/{slug}/{filename}"


def main() -> int:
    success = 0
    failed: list[tuple[str, str]] = []

    for slug, url in sorted(FIXES.items()):
        path = PRODUCTS_DIR / f"{slug}.md"
        if not path.exists():
            failed.append((slug, "missing-md"))
            continue
        product = parse_product(path)
        if product.get("has_images"):
            print(f"SKIP {slug}: already has images")
            continue

        site_path = download(url, slug, product["brand"], product["title"])
        if not site_path:
            failed.append((slug, url))
            print(f"FAIL {slug}")
            continue

        update_frontmatter(path, site_path)
        success += 1
        print(f"OK   {slug}: {site_path}")
        time.sleep(0.2)

    print(f"\nFixed: {success}, Failed: {len(failed)}")
    for slug, reason in failed:
        print(f"  - {slug}: {reason[:80]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

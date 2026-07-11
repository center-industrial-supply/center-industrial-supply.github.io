#!/usr/bin/env python3
"""Bulk-assign product images from official brand sources for target brands."""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PRODUCTS_DIR = ROOT / "src" / "content" / "products"
CATEGORIES_DIR = ROOT / "src" / "content" / "product-categories"
DOWNLOAD_SCRIPT = (
    ROOT / ".cursor/skills/retrieve-product-image/scripts/download-product-image.py"
)

UA = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
TARGET_BRANDS = {"OTC", "DWT", "AMG", "Axxair", "Wilson", "Weldflame"}
WAYBACK_TS = ""  # empty = latest snapshot via https://web.archive.org/web/{url}


# Axxair product-specific images from official site
AXXAIR_IMAGES: dict[str, str] = {
    "axxair-orbital-cutting-machines": "https://www.axxair.com/wp-content/uploads/sites/23/2026/05/Machine-de-coupe-CC-122.1.jpg",
    "the-eco-cutting-range": "https://www.axxair.com/wp-content/uploads/sites/23/2026/04/121ECO_Tube_475x425.jpg",
    "the-ccx22-cutting-range": "https://www.axxair.com/wp-content/uploads/sites/23/2026/04/CC421-Orbital-Cutting.jpg",
    "the-421-521-721-1100-range": "https://www.axxair.com/wp-content/uploads/sites/23/2026/04/CC721-Orbital-Cutting.jpg",
    "axxair-orbital-bevelling-machines": "https://www.axxair.com/wp-content/uploads/sites/23/2026/04/GA172_Tube_475x425.jpg",
    "ga-122-172-222-322": "https://www.axxair.com/wp-content/uploads/sites/23/2026/04/GA172_Tube_475x425.jpg",
}

# slug -> (source_url, source_type)
# source_type: direct | otc-page | dwt-page | axxair-page | wayback
BRAND_SOURCES: dict[str, tuple[str, str]] = {
    # OTC robots (otc-daihen.com product pages)
    "fd-a20": ("https://otc-daihen.com/product-page/13/", "otc-page"),
    "fd-b6": ("https://otc-daihen.com/product-page/31/", "otc-page"),
    "fd-b6l": ("https://otc-daihen.com/product-page/26/", "otc-page"),
    "fd-v8": ("https://otc-daihen.com/product-page/27/", "otc-page"),
    "fd-v8l-2": ("https://otc-daihen.com/product-page/25/", "otc-page"),
    "fd-v6s-7-axis": ("https://otc-daihen.com/product-page/5/", "otc-page"),
    "fd-v25-fd-v50-fd-v80-fd-v100-fd-v130-fd-v166": (
        "https://otc-daihen.com/product-page/1/",
        "otc-page",
    ),
    "welbee-a350p": ("https://otc-daihen.com/product-page/1911/", "otc-page"),
    "wb-m350l": ("https://otc-daihen.com/product-page/1944/", "otc-page"),
    "cptx-210": ("https://otc-daihen.com/product-page/1944/", "otc-page"),
    "synchro-feed": (
        "https://otc-daihen.com/welding/welding-process/migmag/processes/synchrofeed.html",
        "otc-synchro",
    ),
    # DWT pipe bevelers / cutters (dwt-gmbh.de)
    "pipe-beveler-mf2-25": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/aussenspannende-rohrfraesmaschinen/rohrfraesmaschine-mf2-25/",
        "dwt-page",
    ),
    "pipe-beveler-mf3-25": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/aussenspannende-rohrfraesmaschinen/rohrfraesmaschine-mf3-25/",
        "dwt-page",
    ),
    "pipe-beveler-mf3-25xl": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/aussenspannende-rohrfraesmaschinen/rohrfraesmaschine-mf3-25xl/",
        "dwt-page",
    ),
    "pipe-beveler-mf3-r": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/aussenspannende-rohrfraesmaschinen/rohrfraesmaschine-mf3-r/",
        "dwt-page",
    ),
    "pipe-beveler-mf4-r": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/aussenspannende-rohrfraesmaschinen/rohrfraesmaschine-mf4-r/",
        "dwt-page",
    ),
    "pipe-beveler-mf4": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/aussenspannende-rohrfraesmaschinen/rohrfraesmaschine-mf4/",
        "dwt-page",
    ),
    "pipe-beveling-machine-type-mf2iw": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/innerspannende-rohranfasmaschinen/rohranfasmaschine-mf2iw/",
        "dwt-page",
    ),
    "pipe-beveling-machine-type-mf3i": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/innerspannende-rohranfasmaschinen/rohranfasmaschine-mf3i/",
        "dwt-page",
    ),
    "pipe-beveling-machine-type-mf3iw": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/innerspannende-rohranfasmaschinen/rohranfasmaschine-mf3iw/",
        "dwt-page",
    ),
    "pipe-beveling-machine-type-mf4i": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/innerspannende-rohranfasmaschinen/rohranfasmaschine-mf4i/",
        "dwt-page",
    ),
    "pipe-beveling-machine-type-mf5i": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/innerspannende-rohranfasmaschinen/rohranfasmaschine-mf5i/",
        "dwt-page",
    ),
    "pipe-beveling-machine-type-mf6i-50": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-anfasen/innerspannende-rohranfasmaschinen/rohranfasmaschine-mf6i-50/",
        "dwt-page",
    ),
    "pipe-cold-cutting-range-2-48": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-schneiden/rohr-kalt-schneidmaschinen/rohr-kalt-schneidmaschine-2-48/",
        "dwt-page",
    ),
    "clamshell-pipe-cold-cutter-type-dlw-hd-48-57": (
        "https://www.dwt-gmbh.de/rohrbearbeitung/rohre-schneiden/rohr-kalt-schneidmaschinen/klappenschneidgeraet-dlw-hd-48-57/",
        "dwt-page",
    ),
    # Axxair
    "axxair-orbital-cutting-machines": (
        "https://www.axxair.com/en/orbital-cutting-machines/",
        "axxair-page",
    ),
    "axxair-orbital-welding-machines": (
        "https://www.axxair.com/en/orbital-welding-machines/",
        "axxair-page",
    ),
    "axxair-orbital-bevelling-machines": (
        "https://www.axxair.com/en/orbital-beveling-machines/",
        "axxair-page",
    ),
    "the-eco-cutting-range": (
        "https://www.axxair.com/en/orbital-cutting-machines/eco-range/",
        "axxair-page",
    ),
    "the-ccx22-cutting-range": (
        "https://www.axxair.com/en/orbital-cutting-machines/ccx22-range/",
        "axxair-page",
    ),
    "the-421-521-721-1100-range": (
        "https://www.axxair.com/en/orbital-cutting-machines/cc721-range/",
        "axxair-page",
    ),
    "ga-122-172-222-322": (
        "https://www.axxair.com/en/orbital-beveling-machines/ga-range/",
        "axxair-page",
    ),
    "sx122-172-222-322-simple-wire": (
        "https://www.axxair.com/en/orbital-welding-machines/sx-range/",
        "axxair-page",
    ),
    "sx122-172-222-322-avc-osc": (
        "https://www.axxair.com/en/orbital-welding-machines/sx-range/",
        "axxair-page",
    ),
    "prefabrication-orbital-welding": (
        "https://www.axxair.com/en/orbital-welding-machines/sx-range/",
        "axxair-page",
    ),
    "open-head-orbital-welding": (
        "https://www.axxair.com/en/orbital-welding-machines/open-head/",
        "axxair-page",
    ),
    "closed-head-orbital-welding": (
        "https://www.axxair.com/en/orbital-welding-machines/closed-head/",
        "axxair-page",
    ),
}


def curl_get(url: str) -> str:
    result = subprocess.run(
        ["curl", "-fsSL", "-A", UA, "-L", "--max-time", "25", url],
        capture_output=True,
        text=True,
    )
    return result.stdout if result.returncode == 0 else ""


def make_filename(brand: str, title: str, ext: str) -> str:
    brand_part = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-")
    title_part = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")
    return f"{brand_part}-{title_part}{ext}"


def parse_product(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str | Path | bool] = {"path": path}
    for key in ("title", "slug", "brand", "category"):
        match = re.search(rf'^{key}:\s*"([^"]+)"', text, re.M)
        if match:
            fields[key] = match.group(1)
    fields["has_images"] = bool(re.search(r'^images:\s*\n\s+-\s+"', text, re.M))
    return fields


def load_category_images() -> dict[str, str]:
    images: dict[str, str] = {}
    for path in CATEGORIES_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for match in re.finditer(
            r'-\s*slug:\s*"([^"]+)"\s*\n(?:[^\n]*\n)*?\s*image:\s*"([^"]+)"',
            text,
        ):
            images[match.group(1)] = match.group(2)
    return images


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


def copy_local_image(src_url: str, slug: str, brand: str, title: str) -> str | None:
    src_path = PUBLIC / src_url.lstrip("/")
    if not src_path.is_file():
        return None
    ext = src_path.suffix.lower()
    filename = make_filename(brand, title, ext)
    dest_dir = PUBLIC / "images" / "products" / slug
    dest_path = dest_dir / filename
    dest_dir.mkdir(parents=True, exist_ok=True)
    if not dest_path.exists():
        shutil.copy2(src_path, dest_path)
    return f"/images/products/{slug}/{filename}"


def download_image(url: str, slug: str, brand: str, title: str) -> str | None:
    ext = Path(url.split("?")[0]).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp", ".bmp"}:
        ext = ".jpg"
    filename = make_filename(brand, title, ext if ext != ".jpeg" else ".jpg")
    rel_output = f"public/images/products/{slug}/{filename}"
    output = ROOT / rel_output
    if output.exists() and output.stat().st_size > 10_000:
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
            "300",
            "--min-height",
            "300",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        if output.exists():
            output.unlink()
        return None
    return f"/images/products/{slug}/{filename}"


def extract_otc_image(html: str, base: str = "https://otc-daihen.com") -> str | None:
    matches = re.findall(
        r'(?:src|content)="(/assets/image-cache//storage/productImages/[^"]+\.(?:webp|jpg|png))"',
        html,
    )
    if matches:
        return urljoin(base, matches[0])
    matches = re.findall(
        r'(?:src|content)="(/assets/image-cache/template/Medien/Bilder/Welding/[^"]+\.(?:webp|jpg|png))"',
        html,
    )
    if matches:
        return urljoin(base, matches[0])
    return None


def extract_dwt_image(html: str) -> str | None:
    imgs = re.findall(
        r"(https://www\.dwt-gmbh\.de/userfiles/image/convert/en/products/[^\"'?]+\.(?:jpg|webp|png))",
        html,
    )
    if not imgs:
        rel = re.findall(
            r"(/userfiles/image/convert/en/products/[^\"'?]+\.(?:jpg|webp|png))",
            html,
        )
        imgs = [f"https://www.dwt-gmbh.de{i.split('?')[0]}" for i in rel]
    else:
        imgs = [i.split("?")[0] for i in imgs]
    for img in imgs:
        name = img.split("/")[-1]
        if name.startswith("1-") or "pipe-beveler" in img or "pipe-beveling" in img:
            return img
    return imgs[0] if imgs else None


def extract_axxair_image(html: str) -> str | None:
    imgs = re.findall(
        r"(https://www\.axxair\.com/wp-content/uploads/[^\"'?]+\.(?:jpg|webp|png))",
        html,
    )
    product_imgs = [
        i.split("?")[0]
        for i in imgs
        if not any(x in i.lower() for x in ("favicon", "logo", "home-page", "header"))
    ]
    return product_imgs[0] if product_imgs else None


def wayback_url(original: str) -> str:
    if WAYBACK_TS:
        return f"https://web.archive.org/web/{WAYBACK_TS}/{original}"
    return f"https://web.archive.org/web/{original}"


def resolve_image_url(slug: str, brand: str, category_image: str) -> tuple[str | None, str]:
    if slug in AXXAIR_IMAGES:
        return AXXAIR_IMAGES[slug], "axxair-brand"
    if slug in BRAND_SOURCES:
        source, kind = BRAND_SOURCES[slug]
        if kind == "direct":
            return source, "brand-direct"
        html = curl_get(source)
        if not html:
            return None, f"fetch-failed:{source}"
        if kind == "otc-page":
            img = extract_otc_image(html)
            return (urljoin("https://otc-daihen.com", img) if img and img.startswith("/") else img), "otc-brand"
        if kind == "otc-synchro":
            img = extract_otc_image(html)
            return (urljoin("https://otc-daihen.com", img) if img and img.startswith("/") else img), "otc-brand"
        if kind == "dwt-page":
            return extract_dwt_image(html), "dwt-brand"
        if kind == "axxair-page":
            return extract_axxair_image(html), "axxair-brand"

    if category_image:
        local = PUBLIC / category_image.lstrip("/")
        if local.is_file():
            return category_image, "local-wp"

        original = f"https://centerindustrial.com{category_image}"
        full_original = original.replace("-300x300", "")
        for candidate in (original, full_original):
            wb = wayback_url(candidate)
            check = subprocess.run(
                ["curl", "-fsSL", "-A", UA, "-o", "/dev/null", "-w", "%{http_code}", wb],
                capture_output=True,
                text=True,
            )
            if check.stdout.strip() == "200":
                return wb, "wayback-archive"

    return None, "no-source"


def process_product(product: dict, category_images: dict[str, str]) -> tuple[str, str | None, str]:
    slug = str(product["slug"])
    title = str(product.get("title", slug))
    brand = str(product.get("brand", ""))

    if product.get("has_images"):
        return slug, None, "already-has-images"

    cat_img = category_images.get(slug, "")
    local_path = copy_local_image(cat_img, slug, brand, title) if cat_img else None
    if local_path:
        update_frontmatter(product["path"], local_path)  # type: ignore[arg-type]
        return slug, local_path, "local-wp-copy"

    image_url, source = resolve_image_url(slug, brand, cat_img)
    if not image_url:
        return slug, None, source

    if image_url.startswith("/"):
        local_path = copy_local_image(image_url, slug, brand, title)
        if local_path:
            update_frontmatter(product["path"], local_path)  # type: ignore[arg-type]
            return slug, local_path, source

    site_path = download_image(image_url, slug, brand, title)
    if not site_path:
        return slug, None, f"download-failed:{image_url}"

    update_frontmatter(product["path"], site_path)  # type: ignore[arg-type]
    return slug, site_path, source


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--brand", help="Filter by brand")
    parser.add_argument("--slug", help="Process single slug")
    parser.add_argument("--delay", type=float, default=0.3)
    args = parser.parse_args()

    category_images = load_category_images()
    products = [parse_product(path) for path in sorted(PRODUCTS_DIR.glob("*.md"))]
    products = [
        p
        for p in products
        if p.get("brand") in TARGET_BRANDS and not p.get("has_images")
    ]
    if args.brand:
        products = [p for p in products if p.get("brand") == args.brand]
    if args.slug:
        products = [p for p in products if p.get("slug") == args.slug]

    success = 0
    failed: list[tuple[str, str]] = []

    for product in products:
        slug, path, status = process_product(product, category_images)
        if path:
            success += 1
            print(f"OK   {slug}: {path} ({status})")
        else:
            failed.append((slug, status))
            print(f"FAIL {slug}: {status}")
        time.sleep(args.delay)

    print(f"\n=== SUMMARY ===")
    print(f"Success: {success}")
    print(f"Failed:  {len(failed)}")
    print(f"Total:   {len(products)}")
    if failed:
        print("\nFailed slugs:")
        for slug, reason in failed:
            print(f"  - {slug}: {reason}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

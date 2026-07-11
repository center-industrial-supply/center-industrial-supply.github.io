#!/usr/bin/env python3
"""Bulk-assign product images from brand sites and local assets.

Sources images for products missing the `images:` frontmatter field:
1. Reachable local assets (category refs, wp-content)
2. Brand-specific scrapers (GYS, Hypertherm, etc.)
3. Generic og:image extraction from brand product pages
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import quote, urljoin

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "src" / "content" / "products"
CATEGORIES_DIR = ROOT / "src" / "content" / "product-categories"
PUBLIC_DIR = ROOT / "public"
DOWNLOAD_SCRIPT = (
    ROOT / ".cursor/skills/retrieve-product-image/scripts/download-product-image.py"
)

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

BRAND_DOMAINS: dict[str, list[str]] = {
    "ESAB": ["esab.com", "esabna.com"],
    "GYS": ["gys.fr", "gys.com"],
    "OTC": ["otc-daihen.com"],
    "Hypertherm": ["hypertherm.com"],
    "AMG": ["amg-machinery.com", "amg.be"],
    "Aotai": ["aotaiwelding.com"],
    "Kjellberg": ["kjellberg.com", "kjellberg-finsterwalde.de"],
    "MOSA": ["mosa.com"],
    "Weldflame": ["weldflame.com"],
    "Wilson": ["wilsonweld.com"],
    "Hgstar": ["hgstarlaser.com"],
    "IKING": ["iking.cn"],
    "Exact": ["exact-tools.com"],
    "Axxair": ["axxair.com"],
    "DWT": ["dwt-gmbh.com"],
    "TBI": ["tbi-industries.com"],
    "Hyundai": ["hdwelding.co.kr"],
    "ironcat": ["ironcatwelding.com"],
    "Dayok": ["dayok.com"],
    "Shindaiwa": ["shindaiwa.co.jp"],
    "newfire": ["newfire.com.cn"],
    "Taiwan Plasma": ["tplasma.com.tw"],
}

# Known direct image URLs for products that don't scrape easily.
KNOWN_IMAGES: dict[str, str] = {
    "powermax85-sync-plasma-cutter": (
        "https://www.hypertherm.com/globalassets/products/powermax/"
        "85-sync/bs_pmx85sync_600x420_2.jpg"
    ),
    "hypertherm-powermax65-sync-plasma-cutter": (
        "https://www.hypertherm.com/globalassets/products/powermax/"
        "65-sync/bs_pmx65sync_600x420_2.jpg"
    ),
    "powermax45-xp-plasma-cutter": (
        "https://www.hypertherm.com/globalassets/products/powermax/"
        "powermax45-xp/pmx45xp_notorch_375x188_bw.jpg"
    ),
}

# GYS product reference numbers (from datasheets / old site URLs).
GYS_REFS: dict[str, str] = {
    "easmig-160": "032255",
    "easymig-180-4-xl": "066571",
}


def curl_get(url: str, *, referer: str = "") -> str:
    cmd = ["curl", "-fsSL", "-A", USER_AGENT]
    if referer:
        cmd.extend(["-H", f"Referer: {referer}"])
    cmd.append(url)
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        return ""
    return result.stdout


def curl_download(url: str, dest: Path, *, referer: str = "") -> bool:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-fsSL", "-A", USER_AGENT]
    if referer:
        cmd.extend(["-H", f"Referer: {referer}"])
    cmd.extend(["-o", str(dest), url])
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def validate_image(path: Path, *, min_width: int = 400, min_height: int = 400) -> bool:
    try:
        from PIL import Image
    except ImportError:
        return path.stat().st_size > 10_000

    try:
        with Image.open(path) as img:
            w, h = img.size
        return w >= min_width and h >= min_height and path.stat().st_size > 10_000
    except OSError:
        return False


def make_filename(brand: str, title: str, ext: str) -> str:
    brand_part = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-")
    title_part = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")
    parts = [p for p in [brand_part, title_part] if p]
    name = "-".join(parts) if parts else "Product"
    return f"{name}{ext}"


def parse_product(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key in ("title", "slug", "brand", "category"):
        m = re.search(rf"^{key}:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
        if m:
            fields[key] = m.group(1)
    fields["path"] = path
    fields["has_images"] = bool(re.search(r"^images:", text, re.M))
    return fields


def load_category_images() -> dict[str, str]:
    images: dict[str, str] = {}
    for path in CATEGORIES_DIR.rglob("*.md"):
        text = path.read_text(encoding="utf-8")
        for m in re.finditer(
            r"-\s*slug:\s*[\"']?([^\"'\n]+)[\"']?\s*\n\s*title:.*?\n\s*image:\s*[\"']?([^\"'\n]+)[\"']?",
            text,
            re.S,
        ):
            images[m.group(1)] = m.group(2)
    return images


def reachable(url: str) -> bool:
    rel = url.lstrip("/")
    return (PUBLIC_DIR / rel).is_file()


def copy_local_image(src_url: str, slug: str, brand: str, title: str) -> str | None:
    src_path = PUBLIC_DIR / src_url.lstrip("/")
    if not src_path.is_file():
        return None

    ext = src_path.suffix.lower()
    filename = make_filename(brand, title, ext)
    dest_dir = PUBLIC_DIR / "images" / "products" / slug
    dest_path = dest_dir / filename

    if dest_path.exists():
        return f"/images/products/{slug}/{filename}"

    dest_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src_path, dest_path)
    return f"/images/products/{slug}/{filename}"


def download_image(url: str, slug: str, brand: str, title: str, *, referer: str = "") -> str | None:
    ext = Path(url.split("?")[0]).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".jpg"

    filename = make_filename(brand, title, ext)
    rel_output = f"public/images/products/{slug}/{filename}"
    output = ROOT / rel_output

    if output.exists() and validate_image(output):
        return f"/images/products/{slug}/{filename}"

    if referer:
        if not curl_download(url, output, referer=referer):
            return None
    else:
        result = subprocess.run(
            [
                sys.executable,
                str(DOWNLOAD_SCRIPT),
                "--url",
                url,
                "--output",
                rel_output,
                "--min-width",
                "350",
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

    if not output.exists() or not validate_image(output, min_width=350, min_height=300):
        if output.exists():
            output.unlink()
        return None

    return f"/images/products/{slug}/{filename}"


def update_frontmatter(path: Path, image_path: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return

    frontmatter = lines[1:end_idx]
    body = lines[end_idx:]

    # Remove existing images block.
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

    # Insert images after category or brand.
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


def extract_og_image(html: str) -> str | None:
    for pattern in (
        r'property="og:image"\s+content="([^"]+)"',
        r'content="([^"]+)"\s+property="og:image"',
    ):
        m = re.search(pattern, html)
        if m:
            return m.group(1)
    return None


def fetch_gys_image(slug: str, title: str) -> str | None:
    ref = GYS_REFS.get(slug)
    if not ref:
        # Search GYS site by product name.
        search_url = f"https://www.gys.fr/en/search?q={quote(title)}"
        html = curl_get(search_url)
        refs = re.findall(r"/prod-(\d{6})-", html)
        if refs:
            ref = refs[0]

    if not ref:
        # Try searching with simplified name.
        simple = re.sub(r"[^a-zA-Z0-9 ]", " ", title).strip()
        search_url = f"https://www.gys.fr/en/search?q={quote(simple)}"
        html = curl_get(search_url)
        refs = re.findall(r"/prod-(\d{6})-", html)
        if refs:
            ref = refs[0]

    if not ref:
        return None

    page_url = f"https://www.gys.fr/prod-{ref}-/-/-/en?lang=en"
    html = curl_get(page_url)
    tifs = re.findall(r"tif/2048x2048/([^\"']+)", html)
    if not tifs:
        tifs_370 = re.findall(r"tif/370x370/([^\"']+)", html)
        if tifs_370:
            tifs = tifs_370
        else:
            return None

    image_id = tifs[0]
    size = "2048x2048" if "2048x2048" in html else "370x370"
    if "2048x2048" in html and tifs:
        size = "2048x2048"
    image_url = f"https://www.gys.fr/img/common/tif/{size}/{image_id}"
    return image_url


def fetch_hypertherm_image(slug: str, title: str) -> str | None:
    if slug in KNOWN_IMAGES:
        return KNOWN_IMAGES[slug]

    slug_map = {
        "powermax85-sync-plasma-cutter": "powermax85-sync",
        "hypertherm-powermax65-sync-plasma-cutter": "powermax65-sync",
        "powermax45-xp-plasma-cutter": "powermax45-xp",
    }
    page_slug = slug_map.get(slug)
    if not page_slug:
        return None

    page_url = f"https://www.hypertherm.com/hypertherm/powermax/{page_slug}/"
    html = curl_get(page_url)
    og = extract_og_image(html)
    if og:
        # Try higher-res variant.
        hi = re.sub(r"_\d+x\d+", "_600x420", og)
        if curl_get(hi):
            test = subprocess.run(
                ["curl", "-fsSL", "-o", "/dev/null", "-w", "%{http_code}", "-A", USER_AGENT, hi],
                capture_output=True,
                text=True,
            )
            if test.stdout.strip() == "200":
                return hi
        return og
    return None


def fetch_brand_image(brand: str, title: str, slug: str) -> str | None:
    if brand == "GYS":
        return fetch_gys_image(slug, title)
    if brand == "Hypertherm":
        return fetch_hypertherm_image(slug, title)
    if slug in KNOWN_IMAGES:
        return KNOWN_IMAGES[slug]

    domains = BRAND_DOMAINS.get(brand, [])
    for domain in domains:
        search_url = f"https://www.google.com/search?q={quote(f'{brand} {title} site:{domain}')}"
        # Use brand site search where available.
        if brand == "ESAB":
            for region in ["eu/eur_en", "us/nam_en"]:
                url = (
                    f"https://esab.com/{region}/products-solutions/search/"
                    f"?q={quote(title)}"
                )
                html = curl_get(url)
                product_links = re.findall(
                    r'href="(/[^"]*products-solutions/product/[^"]+)"', html
                )
                for link in product_links[:3]:
                    page_html = curl_get(f"https://esab.com{link}")
                    og = extract_og_image(page_html)
                    if og and "cloudfront" in og:
                        return og
                    cdn_imgs = re.findall(
                        r"(https://d363suj4pdptk4\.cloudfront\.net[^\"'<> ]+\.(?:jpg|png|webp))",
                        page_html,
                    )
                    if cdn_imgs:
                        return cdn_imgs[0]

        if brand == "DWT":
            url = f"https://www.dwt-gmbh.com/en/products/"
            html = curl_get(url)
            links = re.findall(r'href="([^"]+)"', html)
            for link in links:
                if slug.replace("-", "") in link.replace("-", "").lower():
                    page_html = curl_get(urljoin("https://www.dwt-gmbh.com", link))
                    og = extract_og_image(page_html)
                    if og:
                        return og

    return None


def process_product(
    product: dict,
    category_images: dict[str, str],
    *,
    dry_run: bool = False,
) -> tuple[str, str | None, str]:
    slug = product["slug"]
    title = product.get("title", slug)
    brand = product.get("brand", "")

    if product.get("has_images"):
        return slug, None, "already has images"

    # 1. Local reachable category image.
    cat_img = category_images.get(slug, "")
    if cat_img and reachable(cat_img):
        if dry_run:
            return slug, cat_img, "local category ref (dry-run)"
        site_path = copy_local_image(cat_img, slug, brand, title)
        if site_path:
            update_frontmatter(product["path"], site_path)
            return slug, site_path, "local category ref"

    # 2. Known direct URL.
    image_url = KNOWN_IMAGES.get(slug)

    # 3. Brand-specific fetch.
    if not image_url:
        image_url = fetch_brand_image(brand, title, slug)

    if not image_url:
        return slug, None, f"no source found ({brand})"

    if dry_run:
        return slug, image_url, "would download (dry-run)"

    referer = ""
    if "gys.fr" in image_url:
        referer = "https://www.gys.fr/"

    site_path = download_image(image_url, slug, brand, title, referer=referer)
    if not site_path:
        return slug, None, f"download failed: {image_url}"

    update_frontmatter(product["path"], site_path)
    return slug, site_path, "downloaded"


def main() -> int:
    parser = argparse.ArgumentParser(description="Bulk-assign product images.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--brand", help="Only process products for this brand")
    parser.add_argument("--slug", help="Only process this product slug")
    parser.add_argument("--limit", type=int, default=0, help="Max products to process")
    parser.add_argument("--delay", type=float, default=0.5, help="Delay between requests")
    args = parser.parse_args()

    category_images = load_category_images()
    products = [parse_product(p) for p in sorted(PRODUCTS_DIR.glob("*.md"))]
    products = [p for p in products if not p.get("has_images")]

    if args.brand:
        products = [p for p in products if p.get("brand", "").lower() == args.brand.lower()]
    if args.slug:
        products = [p for p in products if p["slug"] == args.slug]
    if args.limit:
        products = products[: args.limit]

    success = 0
    failed = 0

    for product in products:
        slug, path, status = process_product(
            product, category_images, dry_run=args.dry_run
        )
        if path:
            success += 1
            print(f"OK  {slug}: {path} ({status})")
        else:
            failed += 1
            print(f"SKIP {slug}: {status}")
        time.sleep(args.delay)

    print(f"\nDone: {success} assigned, {failed} skipped, {len(products)} total")
    return 0


if __name__ == "__main__":
    sys.exit(main())

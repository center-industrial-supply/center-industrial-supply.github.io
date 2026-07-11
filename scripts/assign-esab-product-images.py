#!/usr/bin/env python3
"""Assign official ESAB product images using curl_cffi (Cloudflare bypass)."""

from __future__ import annotations

import io
import re
import subprocess
import sys
import time
from pathlib import Path
from urllib.parse import urljoin

from curl_cffi import requests

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "src" / "content" / "products"
DOWNLOAD_SCRIPT = (
    ROOT / ".cursor/skills/retrieve-product-image/scripts/download-product-image.py"
)
EUROCARDIS_PDF = Path("/tmp/esab-catalogs/eurocardis.pdf")
PPE_PDF = Path("/tmp/esab-catalogs/9vo362evff5njtpc8hbv23p7503b3us8.pdf")
FILTAIR_PDF = Path("/tmp/esab-catalogs/2o7ly6slye68y01r9g3ukrhb39kr6ayt.pdf")

CF_BASE = (
    "https://d363suj4pdptk4.cloudfront.net/externalApps/"
    "c7efbbab-3f6a-497d-9dae-cbb24f5f4774/conversion/PIM/assets"
)

# Curated product page URLs (GB paths verified on esab.com).
PAGE_URLS: dict[str, list[str]] = {
    "a-series": [
        "https://esab.com/gb/eur_en/products-solutions/product/cutting-automation/plasma-systems/a-series-power-supply/",
    ],
    "a2-multitrac": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/welding-tractors/a2-multitrac-saw/",
    ],
    "a6-mastertrac-a6tf": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/welding-tractors/a6-mastertrac-a6tf-single-twin-saw/",
    ],
    "a6-mastertrac-a6tf-tandem": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/welding-tractors/a6-mastertrac-a6tf-tandem/",
    ],
    "versotrac-etw-1000-welding-tractor": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/welding-tractors/versotrac-ewt-1000/",
    ],
    "mechtrac": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/gantries/mechtrac-1730-2100-2500-3000/",
    ],
    "gantrac": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/gantries/gantrac/",
    ],
    "pipeweld-orbiter": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/mechanized-welding/pipeweld-orbiter/",
    ],
    "cab-system-300s-300m": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/column-and-boom-systems/esab-cab-300s/",
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/column-and-boom-systems/esab-cab-300m/",
    ],
    "cab-system-460s-460m": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/column-and-boom-systems/esab-cab-460m/",
    ],
    "cab-44-55-66-and-77": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-automation/submerged-arc-welding/column-and-boom-systems/cab-system-600m/",
    ],
    "rogue-150i-180i-200i": [
        "https://esab.com/gb/eur_en/products-solutions/product/welding-equipment/stick-welders-smaw/rogue-es-201ip-pro/",
    ],
    "esab-7018l-3-2x350mm-20kg": [
        "https://esab.com/gb/eur_en/products-solutions/product/filler-metals/mild-steel/stick-electrodes-smaw/ferex-7018-lt/",
        "https://esab.com/gb/eur_en/products-solutions/product/filler-metals/mild-steel/stick-electrodes-smaw/fortrex-7018/",
        "https://esab.com/gb/eur_en/products-solutions/product/filler-metals/mild-steel/stick-electrodes-smaw/ok-48-00/",
    ],
    "esab-leather-welding-gloves": [
        "https://esab.com/gb/eur_en/products-solutions/product/ppe-safety/hands-and-body/heavy-duty-gloves-m2000/",
    ],
    "warrior-spectacles": [
        "https://esab.com/gb/eur_en/products-solutions/product/ppe-safety/head-and-face/warrior-spectacles/",
    ],
    "warrior-clear-spectacles": [
        "https://esab.com/gb/eur_en/products-solutions/product/ppe-safety/head-and-face/warrior-spectacles/",
    ],
    "warrior-amber-spectacles": [
        "https://esab.com/gb/eur_en/products-solutions/product/ppe-safety/head-and-face/warrior-spectacles/",
    ],
    "warrior-shade-5-spectacles": [
        "https://esab.com/gb/eur_en/products-solutions/product/ppe-safety/head-and-face/warrior-spectacles/",
    ],
}

# Direct CloudFront image URLs when product pages lack extractable hero images.
DIRECT_IMAGES: dict[str, str] = {
    "a-series": f"{CF_BASE}/149300",
    "a2-multitrac": f"{CF_BASE}/157634",
    "a6-mastertrac-a6tf-tandem": f"{CF_BASE}/9009",
    "versotrac-etw-1000-welding-tractor": f"{CF_BASE}/24805",
    "cab-system-300s-300m": f"{CF_BASE}/126575",
    "cab-system-460s-460m": f"{CF_BASE}/126584",
    "rogue-150i-180i-200i": f"{CF_BASE}/146701",
    "esab-leather-welding-gloves": f"{CF_BASE}/136910",
}

# PDF catalog extractions: slug -> (pdf_path, page_1based, image_index, min_w, min_h)
PDF_IMAGES: dict[str, tuple[Path, int, int, int, int]] = {
    "buddy-arc-145": (EUROCARDIS_PDF, 12, 0, 300, 150),
    "caddy-mig-c200i": (EUROCARDIS_PDF, 22, 0, 300, 300),
    "aristo-mig-4004i-pulse": (EUROCARDIS_PDF, 52, 4, 300, 300),
    "aristo-mig-4004i-pulse-2": (EUROCARDIS_PDF, 52, 4, 300, 300),
    "miggytrac-b501": (EUROCARDIS_PDF, 89, 1, 180, 180),
    "railtrac-b42v": (EUROCARDIS_PDF, 89, 0, 200, 200),
    # ESAB 2017 PPE accessories catalog (assets.esab.com linked distributor PDF).
    "esab-eye-wear-eco-clear-spectacles": (PPE_PDF, 16, 2, 300, 150),
    "eco-amber-spectacles": (PPE_PDF, 16, 3, 300, 150),
    "esab-leather-welding-gloves-fallback": (PPE_PDF, 24, 1, 300, 300),
    "warrior-spectacles": (PPE_PDF, 15, 15, 300, 300),
    "warrior-clear-spectacles": (PPE_PDF, 15, 15, 300, 300),
    "warrior-amber-spectacles": (PPE_PDF, 15, 15, 300, 300),
    "warrior-shade-5-spectacles": (PPE_PDF, 15, 15, 300, 300),
}


def make_filename(brand: str, title: str, ext: str) -> str:
    brand_part = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-")
    title_part = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")
    if brand_part and title_part.lower().startswith(brand_part.lower() + "-"):
        title_part = title_part[len(brand_part) + 1 :]
    parts = [p for p in [brand_part, title_part] if p]
    return "-".join(parts) + ext if parts else f"Product{ext}"


def parse_product(path: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key in ("title", "slug", "brand", "category"):
        m = re.search(rf'^{key}:\s*["\']?(.+?)["\']?\s*$', text, re.M)
        if m:
            fields[key] = m.group(1)
    fields["path"] = path
    fields["has_images"] = bool(re.search(r"^images:", text, re.M))
    return fields


def extract_image_url(html: str, page_url: str) -> str | None:
    cloudfront = re.findall(
        r"(https://d363suj4pdptk4\.cloudfront\.net/externalApps/[^\"']+/conversion/PIM/assets/\d+)",
        html,
    )
    if cloudfront:
        return cloudfront[0]

    alt_cf = re.findall(
        r"(https://d24otazn342w10\.cloudfront\.net/externalApps/[^\"']+/conversion/PIM/assets/\d+)",
        html,
    )
    if alt_cf:
        return alt_cf[0]

    og = re.search(r'property="og:image"\s+content="([^"]+)"', html)
    if og and "logo" not in og.group(1).lower():
        return og.group(1)

    assets = re.findall(
        r"(https://assets\.esab\.com/assetbank-esab/servlet/file\?[^\"']+)",
        html,
    )
    if assets:
        return assets[0]

    s3 = re.findall(
        r"(https://s3\.amazonaws\.com/assetbank[^\"']+\.(?:jpg|jpeg|png|webp))",
        html,
        flags=re.I,
    )
    if s3:
        return s3[0]

    site_assets = re.findall(
        r"(https://esab\.com/sites/[^\"'\\]+/assets/[^\"'\\]+\.(?:jpg|jpeg|png|webp))",
        html,
        flags=re.I,
    )
    if site_assets:
        return site_assets[0]

    data_myfile = re.findall(
        r'data-myfile="(/sites/[^"]+\.(?:jpg|jpeg|png|webp))"', html, re.I
    )
    if data_myfile:
        return urljoin(page_url, data_myfile[0])

    cache_files = re.findall(
        r"(/sites/[a-z_]+/cache/file/[A-F0-9]+\.(?:jpg|jpeg|png|webp))",
        html,
        flags=re.I,
    )
    if cache_files:
        region_match = re.search(r"esab\.com/([a-z]{2}/[a-z_]+)/", page_url)
        if region_match:
            region = region_match.group(1).split("/")[0]
            for cf in cache_files:
                if f"/sites/{region}_" in cf or f"/sites/{region}/" in cf:
                    return urljoin(page_url, cf)
        return urljoin(page_url, cache_files[0])

    return None


def fetch_page(url: str) -> str | None:
    for impersonate in ("chrome110", "safari15_5", "chrome120"):
        try:
            resp = requests.get(url, impersonate=impersonate, timeout=30)
        except Exception:
            continue
        if resp.status_code != 200 or len(resp.text) < 20_000:
            time.sleep(0.5)
            continue
        if "Choose your location" in resp.text[:8000]:
            return None
        return resp.text
    return None


def ensure_eurocardis_pdf() -> None:
    if EUROCARDIS_PDF.exists() and EUROCARDIS_PDF.stat().st_size > 1_000_000:
        return
    EUROCARDIS_PDF.parent.mkdir(parents=True, exist_ok=True)
    url = (
        "https://eurocardis.com/wp-content/uploads/2014/06/"
        "Cata%CC%81logo-Soldadura-y-Corte-Esab.pdf"
    )
    resp = requests.get(url, impersonate="chrome110", timeout=120)
    resp.raise_for_status()
    EUROCARDIS_PDF.write_bytes(resp.content)


def ensure_ppe_pdf() -> None:
    if PPE_PDF.exists() and PPE_PDF.stat().st_size > 100_000:
        return
    PPE_PDF.parent.mkdir(parents=True, exist_ok=True)
    url = (
        "https://www.ventsvar.ru/upload/iblock/5ab/"
        "9vo362evff5njtpc8hbv23p7503b3us8.pdf"
    )
    resp = requests.get(url, impersonate="chrome110", timeout=120)
    resp.raise_for_status()
    PPE_PDF.write_bytes(resp.content)


def ensure_filtair_pdf() -> None:
    if FILTAIR_PDF.exists() and FILTAIR_PDF.stat().st_size > 100_000:
        return
    FILTAIR_PDF.parent.mkdir(parents=True, exist_ok=True)
    url = (
        "https://www.ventsvar.ru/upload/iblock/afd/"
        "2o7ly6slye68y01r9g3ukrhb39kr6ayt.pdf"
    )
    resp = requests.get(url, impersonate="chrome110", timeout=120)
    resp.raise_for_status()
    FILTAIR_PDF.write_bytes(resp.content)


def extract_filtair_crop(model: str) -> bytes | None:
    """Crop individual Filtair Pro masks from the ESAB product datasheet PDF."""
    import fitz
    from PIL import Image

    ensure_filtair_pdf()
    doc = fitz.open(str(FILTAIR_PDF))
    page = doc[0]
    pix = page.get_pixmap(dpi=200)
    img = Image.open(io.BytesIO(pix.tobytes("png")))
    w, h = img.size
    boxes = {
        "8010": (int(w * 0.05), int(h * 0.18), int(w * 0.42), int(h * 0.36)),
        "8020cv": (int(w * 0.52), int(h * 0.18), int(w * 0.92), int(h * 0.36)),
        "8030v": (int(w * 0.52), int(h * 0.42), int(w * 0.92), int(h * 0.58)),
    }
    box = boxes.get(model)
    if not box:
        return None
    cropped = img.crop(box)
    if cropped.width < 300 or cropped.height < 300:
        return None
    buf = io.BytesIO()
    cropped.convert("RGB").save(buf, format="JPEG", quality=92)
    return buf.getvalue()


def extract_pdf_image(
    pdf_path: Path, page_num: int, img_index: int, min_w: int, min_h: int
) -> bytes | None:
    import fitz
    from PIL import Image

    doc = fitz.open(str(pdf_path))
    page = doc[page_num - 1]
    imgs = page.get_images(full=True)
    if img_index >= len(imgs):
        return None

    base = doc.extract_image(imgs[img_index][0])
    data = base["image"]
    ext = base["ext"].lower()

    if ext in {"jpx", "jp2", "j2k"}:
        img = Image.open(io.BytesIO(data))
        buf = io.BytesIO()
        img.convert("RGB").save(buf, format="JPEG", quality=92)
        data = buf.getvalue()
    elif ext == "jpeg":
        ext = "jpg"

    with Image.open(io.BytesIO(data)) as img:
        w, h = img.size
    if w < min_w or h < min_h:
        return None
    return data


def download_image(
    url: str | None,
    slug: str,
    brand: str,
    title: str,
    *,
    pdf_bytes: bytes | None = None,
    min_width: int = 300,
    min_height: int = 300,
) -> str | None:
    from PIL import Image

    if pdf_bytes:
        ext = ".jpg"
        filename = make_filename(brand, title, ext)
        rel_output = f"public/images/products/{slug}/{filename}"
        output = ROOT / rel_output
        output.parent.mkdir(parents=True, exist_ok=True)
        if output.exists():
            output.unlink()
        output.write_bytes(pdf_bytes)
        with Image.open(output) as img:
            w, h = img.size
        if w < min_width or h < min_height:
            output.unlink(missing_ok=True)
            return None
        return f"/images/products/{slug}/{filename}"

    if not url:
        return None

    ext = Path(url.split("?")[0]).suffix.lower()
    if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
        ext = ".jpg"

    filename = make_filename(brand, title, ext)
    rel_output = f"public/images/products/{slug}/{filename}"
    output = ROOT / rel_output

    if output.exists():
        output.unlink()

    result = subprocess.run(
        [
            sys.executable,
            str(DOWNLOAD_SCRIPT),
            "--url",
            url,
            "--output",
            rel_output,
            "--min-width",
            str(min_width),
            "--min-height",
            str(min_height),
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        try:
            resp = requests.get(url, impersonate="chrome110", timeout=60)
            resp.raise_for_status()
            output.parent.mkdir(parents=True, exist_ok=True)
            output.write_bytes(resp.content)
            with Image.open(output) as img:
                w, h = img.size
            if w < min_width or h < min_height:
                output.unlink(missing_ok=True)
                return None
        except Exception:
            output.unlink(missing_ok=True)
            return None

    return f"/images/products/{slug}/{filename}"


def update_frontmatter(path: Path, image_path: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return

    end_idx = next((i for i in range(1, len(lines)) if lines[i].strip() == "---"), None)
    if end_idx is None:
        return

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


def resolve_image(slug: str) -> tuple[str | None, str, bytes | None, int, int]:
    if slug in DIRECT_IMAGES:
        return DIRECT_IMAGES[slug], "direct CloudFront URL", None, 300, 300

    filtair_models = {
        "esab-filtair-pro-8010-ffp1-white": "8010",
        "esab-filtair-pro-8020cv-ffp2-grey": "8020cv",
        "esab-filtair-pro-8030v-ffp3-orange": "8030v",
    }
    if slug in filtair_models:
        data = extract_filtair_crop(filtair_models[slug])
        if data:
            return (
                None,
                f"ESAB Filtair Pro datasheet PDF ({filtair_models[slug]})",
                data,
                300,
                300,
            )

    if slug in PDF_IMAGES:
        pdf_path, page, img_idx, min_w, min_h = PDF_IMAGES[slug]
        if not pdf_path.exists():
            if pdf_path == EUROCARDIS_PDF:
                ensure_eurocardis_pdf()
            elif pdf_path == PPE_PDF:
                ensure_ppe_pdf()
            elif pdf_path == FILTAIR_PDF:
                ensure_filtair_pdf()
        if pdf_path.exists():
            data = extract_pdf_image(pdf_path, page, img_idx, min_w, min_h)
            if data:
                return None, f"PDF catalog {pdf_path.name} p{page} img{img_idx}", data, min_w, min_h

    for page_url in PAGE_URLS.get(slug, []):
        html = fetch_page(page_url)
        if not html:
            continue
        image_url = extract_image_url(html, page_url)
        if image_url:
            return image_url, page_url, None, 300, 300
        time.sleep(0.2)

    return None, "no image found on ESAB pages", None, 300, 300


def main() -> int:
    ensure_eurocardis_pdf()

    products = [parse_product(p) for p in sorted(PRODUCTS_DIR.glob("*.md"))]
    products = [p for p in products if p.get("brand") == "ESAB" and not p.get("has_images")]

    success: list[str] = []
    failed: list[tuple[str, str]] = []

    for product in products:
        slug = product["slug"]
        title = product.get("title", slug)
        brand = product.get("brand", "ESAB")

        image_url, source, pdf_bytes, min_w, min_h = resolve_image(slug)
        if not image_url and not pdf_bytes:
            failed.append((slug, source))
            print(f"FAIL {slug}: {source}")
            continue

        site_path = download_image(
            image_url,
            slug,
            brand,
            title,
            pdf_bytes=pdf_bytes,
            min_width=min_w,
            min_height=min_h,
        )
        if not site_path:
            failed.append((slug, f"download failed: {(image_url or source)[:120]}"))
            print(f"FAIL {slug}: download failed")
            continue

        update_frontmatter(product["path"], site_path)
        success.append(slug)
        print(f"OK   {slug}: {site_path} ({source[:80]})")
        time.sleep(0.5)

    print(f"\nDone: {len(success)} succeeded, {len(failed)} failed")
    if failed:
        print("Failures:")
        for slug, reason in failed:
            print(f"  - {slug}: {reason}")

    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())

#!/usr/bin/env python3
"""Migrate archived HTML in public/product and public/product-category to Astro content."""

from __future__ import annotations

import html
import re
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PUBLIC = ROOT / "public"
PRODUCT_SRC = PUBLIC / "product"
CATEGORY_SRC = PUBLIC / "product-category"
PRODUCT_OUT = ROOT / "src" / "content" / "products"
CATEGORY_OUT = ROOT / "src" / "content" / "product-categories"


def clean_text(value: str) -> str:
    return html.unescape(re.sub(r"\s+", " ", value)).strip()


def yaml_quote(value: str) -> str:
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def yaml_list(items: list[str], indent: int = 0) -> str:
    if not items:
        return "[]"
    pad = " " * indent
    lines = [f"{pad}- {yaml_quote(item)}" for item in items]
    return "\n".join(lines)


def extract_title(page_html: str, fallback: str) -> str:
    for pattern in (
        r"<h1[^>]*class=[\"']?[^\"'>]*product-title[^>]*>([^<]+)",
        r"<h1[^>]*class=[\"']?[^\"'>]*page-title[^>]*>([^<]+)",
        r"<title>([^<]+)</title>",
    ):
        match = re.search(pattern, page_html, re.IGNORECASE)
        if match:
            title = clean_text(match.group(1))
            title = re.sub(r"\s*-\s*Center Industrial Supply.*$", "", title, flags=re.IGNORECASE)
            if title:
                return title
    return fallback.replace("-", " ")


def extract_meta_description(page_html: str) -> str:
    match = re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\']([^"\']+)', page_html, re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    match = re.search(r'property=["\']og:description["\'][^>]+content=["\']([^"\']+)', page_html, re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    return ""


def extract_short_description(page_html: str) -> str:
    match = re.search(
        r'class=woocommerce-product-details__short-description[^>]*>(.*?)</div>',
        page_html,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return clean_text(text)


def extract_description_html(page_html: str) -> str:
    match = re.search(
        r'id=tab-description[^>]*>(.*?)</div></div></div>',
        page_html,
        re.IGNORECASE | re.DOTALL,
    )
    if not match:
        return ""
    body = match.group(1)
    body = re.sub(r"<h2[^>]*>Product description</h2>", "", body, flags=re.IGNORECASE)
    body = re.sub(r"\.\./\.\./", "/", body)
    body = re.sub(r"\.\./", "/", body)
    body = re.sub(r'href=["\']([^"\']*?)index\.html([^"\']*)', r'href="\1\2', body)
    body = re.sub(r"\s+", " ", body).strip()
    return body


def normalize_asset_path(url: str) -> str:
    url = url.replace("../", "")
    if "wp-content/uploads/" in url:
        path = url[url.index("wp-content/uploads/") :]
    else:
        return ""
    path = re.sub(r"\?.*$", "", path)
    return "/" + path


def extract_images(page_html: str) -> list[str]:
    images: list[str] = []
    gallery_match = re.search(
        r"class=woocommerce-product-gallery[^>]*>.*?</div></div></div>",
        page_html,
        re.IGNORECASE | re.DOTALL,
    )
    search_html = gallery_match.group(0) if gallery_match else page_html
    skip = ("brand-logo", "small-brand", "cisc-logo", "woocommerce-placeholder")
    for match in re.finditer(r"wp-content/uploads/[^\"' >?]+", search_html):
        path = "/" + match.group(0)
        if any(token in path.lower() for token in skip):
            continue
        if path not in images:
            images.append(path)
    return images[:6]


def extract_brand(page_html: str) -> str:
    match = re.search(r'class=tagged_as[^>]*>Brand:\s*<a[^>]*>([^<]+)', page_html, re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    match = re.search(r"product-brand-container[^>]*>\s*<span>([^<]+)", page_html, re.IGNORECASE)
    if match:
        return clean_text(match.group(1))
    return ""


def extract_category_path(page_html: str) -> str:
    match = re.search(r'class=posted_in[^>]*>Category:\s*<a href=([^ >]+)', page_html, re.IGNORECASE)
    if not match:
        return ""
    href = match.group(1)
    href = href.replace("../", "").replace("index.html", "").strip("/")
    if href.startswith("product-category/"):
        return href.removeprefix("product-category/")
    return href


def extract_breadcrumb(page_html: str) -> list[dict[str, str]]:
    match = re.search(r'<div class=breadcrumb>.*?<ol>(.*?)</ol>', page_html, re.IGNORECASE | re.DOTALL)
    if not match:
        return []
    crumbs: list[dict[str, str]] = []
    for item in re.finditer(r"<li>(.*?)</li>", match.group(1), re.IGNORECASE | re.DOTALL):
        chunk = item.group(1)
        link = re.search(r'<a href=["\']([^"\']+)["\'][^>]*>([^<]+)', chunk, re.IGNORECASE)
        if link:
            href = link.group(1).replace("../", "/").replace("index.html", "/")
            if not href.startswith("/"):
                href = "/" + href
            crumbs.append({"label": clean_text(link.group(2)), "href": href})
        else:
            text = clean_text(re.sub(r"<[^>]+>", "", chunk))
            if text:
                crumbs.append({"label": text, "href": ""})
    return crumbs


def extract_category_description(page_html: str) -> str:
    match = re.search(r'<div class=term-description>(.*?)</div>', page_html, re.IGNORECASE | re.DOTALL)
    if not match:
        return ""
    text = re.sub(r"<[^>]+>", " ", match.group(1))
    return clean_text(text)


def extract_category_children(page_html: str, base_slug: str) -> tuple[list[dict], list[dict]]:
    subcategories: list[dict] = []
    products: list[dict] = []

    list_match = re.search(r'<ul class="products[^"]*">(.*?)</ul>', page_html, re.IGNORECASE | re.DOTALL)
    if not list_match:
        return subcategories, products

    chunks = re.split(r"<li class=", list_match.group(1), flags=re.IGNORECASE)
    for chunk in chunks[1:]:
        if "product" not in chunk:
            continue
        is_category = "product-category" in chunk
        link = re.search(r"<a[^>]+href=([^ >]+)[^>]*>(.*?)</a>", chunk, re.IGNORECASE | re.DOTALL)
        if not link:
            continue
        href = link.group(1).replace("index.html", "").strip("/")
        slug = href.split("/")[-1] if href else ""
        title_match = re.search(r"<h2[^>]*>(.*?)</h2>", chunk, re.IGNORECASE | re.DOTALL)
        title = clean_text(re.sub(r"<[^>]+>", "", title_match.group(1))) if title_match else slug.replace("-", " ")
        title = re.sub(r"\s*\(\d+\)\s*$", "", title)
        img_match = re.search(r"<img[^>]+src=([^ >]+)", chunk, re.IGNORECASE)
        image = normalize_asset_path(img_match.group(1)) if img_match else ""

        entry = {"slug": slug, "title": title, "image": image}
        if is_category:
            subcategories.append(entry)
        else:
            products.append(entry)

    return subcategories, products


def write_markdown(path: Path, frontmatter: str, body: str = "") -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = f"---\n{frontmatter}\n---\n"
    if body:
        content += f"\n{body.strip()}\n"
    path.write_text(content, encoding="utf-8")


def migrate_products() -> int:
    count = 0
    for product_dir in sorted(PRODUCT_SRC.iterdir()):
        if not product_dir.is_dir():
            continue
        index = product_dir / "index.html"
        if not index.exists():
            continue

        slug = product_dir.name
        page_html = index.read_text(encoding="utf-8", errors="ignore")
        title = extract_title(page_html, slug)
        description = extract_short_description(page_html) or extract_meta_description(page_html)
        brand = extract_brand(page_html)
        category = extract_category_path(page_html)
        images = extract_images(page_html)
        body = extract_description_html(page_html)
        breadcrumbs = extract_breadcrumb(page_html)

        fm_lines = [
            f"title: {yaml_quote(title)}",
            f"slug: {yaml_quote(slug)}",
            f"layout: product",
        ]
        if description:
            fm_lines.append(f"description: {yaml_quote(description[:500])}")
        if brand:
            fm_lines.append(f"brand: {yaml_quote(brand)}")
        if category:
            fm_lines.append(f"category: {yaml_quote(category)}")
        if images:
            fm_lines.append("images:")
            fm_lines.append(yaml_list(images, indent=0))
        if breadcrumbs:
            fm_lines.append("breadcrumb:")
            for crumb in breadcrumbs:
                fm_lines.append(f"  - label: {yaml_quote(crumb['label'])}")
                if crumb["href"]:
                    fm_lines.append(f"    href: {yaml_quote(crumb['href'])}")

        out_path = PRODUCT_OUT / f"{slug}.md"
        write_markdown(out_path, "\n".join(fm_lines), body)
        count += 1
    return count


def migrate_categories() -> int:
    count = 0
    for index in sorted(CATEGORY_SRC.rglob("index.html")):
        rel = index.parent.relative_to(CATEGORY_SRC)
        slug_path = rel.as_posix()
        if slug_path == ".":
            continue

        page_html = index.read_text(encoding="utf-8", errors="ignore")
        title = extract_title(page_html, slug_path.split("/")[-1])
        description = extract_category_description(page_html) or extract_meta_description(page_html)
        subcategories, products = extract_category_children(page_html, slug_path)
        breadcrumbs = extract_breadcrumb(page_html)
        parent = "/".join(slug_path.split("/")[:-1]) if "/" in slug_path else ""

        fm_lines = [
            f"title: {yaml_quote(title)}",
            f"slug: {yaml_quote(slug_path)}",
            f"layout: category",
        ]
        if description:
            fm_lines.append(f"description: {yaml_quote(description[:500])}")
        if parent:
            fm_lines.append(f"parent: {yaml_quote(parent)}")
        if subcategories:
            fm_lines.append("subcategories:")
            for item in subcategories:
                fm_lines.append(f"  - slug: {yaml_quote(item['slug'])}")
                fm_lines.append(f"    title: {yaml_quote(item['title'])}")
                if item["image"]:
                    fm_lines.append(f"    image: {yaml_quote(item['image'])}")
        if products:
            fm_lines.append("products:")
            for item in products:
                fm_lines.append(f"  - slug: {yaml_quote(item['slug'])}")
                fm_lines.append(f"    title: {yaml_quote(item['title'])}")
                if item["image"]:
                    fm_lines.append(f"    image: {yaml_quote(item['image'])}")
        if breadcrumbs:
            fm_lines.append("breadcrumb:")
            for crumb in breadcrumbs:
                fm_lines.append(f"  - label: {yaml_quote(crumb['label'])}")
                if crumb["href"]:
                    fm_lines.append(f"    href: {yaml_quote(crumb['href'])}")

        out_path = CATEGORY_OUT / f"{slug_path}.md"
        write_markdown(out_path, "\n".join(fm_lines))
        count += 1
    return count


def main() -> None:
    PRODUCT_OUT.mkdir(parents=True, exist_ok=True)
    CATEGORY_OUT.mkdir(parents=True, exist_ok=True)

    products = migrate_products()
    categories = migrate_categories()
    print(f"Migrated {products} products and {categories} categories")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""Sync embedded product titles in category markdown from canonical product frontmatter."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "src" / "content" / "products"
CATEGORIES_DIR = ROOT / "src" / "content" / "product-categories"

TITLE_RE = re.compile(r'^title:\s*"(.*)"\s*$', re.MULTILINE)
SLUG_RE = re.compile(r'^\s+slug:\s*"(.*)"\s*$', re.MULTILINE)
PRODUCT_TITLE_RE = re.compile(r'^(\s+title:\s*")(.*)(")\s*$', re.MULTILINE)


def load_product_titles() -> dict[str, str]:
    titles: dict[str, str] = {}
    for path in PRODUCTS_DIR.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        slug_match = re.search(r'^slug:\s*"(.*)"\s*$', text, re.MULTILINE)
        title_match = TITLE_RE.search(text)
        if slug_match and title_match:
            titles[slug_match.group(1)] = title_match.group(1)
    return titles


def sync_category_file(path: Path, product_titles: dict[str, str]) -> int:
    text = path.read_text(encoding="utf-8")
    if "products:" not in text:
        return 0

    lines = text.splitlines(keepends=True)
    updated = 0
    current_slug: str | None = None
    in_products = False

    for index, line in enumerate(lines):
        if line.startswith("products:"):
            in_products = True
            continue
        if in_products and re.match(r"^\S", line) and not line.startswith(" "):
            in_products = False
            current_slug = None
            continue
        if not in_products:
            continue

        slug_match = re.match(r'^\s+-\s+slug:\s*"(.*)"\s*$', line)
        if slug_match:
            current_slug = slug_match.group(1)
            continue

        title_match = re.match(r'^(\s+title:\s*")(.*)(")\s*$', line)
        if title_match and current_slug:
            canonical = product_titles.get(current_slug)
            if canonical and canonical != title_match.group(2):
                lines[index] = f'{title_match.group(1)}{canonical}{title_match.group(3)}\n'
                updated += 1
            current_slug = None

    if updated:
        path.write_text("".join(lines), encoding="utf-8")
    return updated


def main() -> None:
    product_titles = load_product_titles()
    total = 0
    for path in sorted(CATEGORIES_DIR.rglob("*.md")):
        total += sync_category_file(path, product_titles)
    print(f"Updated {total} embedded product titles across category files.")


if __name__ == "__main__":
    main()

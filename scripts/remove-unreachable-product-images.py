#!/usr/bin/env python3
"""Remove product image URLs that are not present in public/."""

from __future__ import annotations

import re
import sys
from pathlib import Path


def reachable(image_url: str, public_dir: Path) -> bool:
    rel = image_url.lstrip("/")
    return (public_dir / rel).is_file()


def update_product_file(path: Path, public_dir: Path) -> tuple[bool, int, int]:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return False, 0, 0

    end_idx = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_idx = idx
            break
    if end_idx is None:
        return False, 0, 0

    frontmatter = lines[1:end_idx]
    body = lines[end_idx + 1 :]

    images_idx = None
    for idx, line in enumerate(frontmatter):
        if line.startswith("images:"):
            images_idx = idx
            break
    if images_idx is None:
        return False, 0, 0

    image_lines: list[tuple[int, str]] = []
    idx = images_idx + 1
    while idx < len(frontmatter) and frontmatter[idx].startswith("- "):
        image_lines.append((idx, frontmatter[idx][2:].strip().strip('"')))
        idx += 1

    if not image_lines:
        return False, 0, 0

    kept = [(i, url) for i, url in image_lines if reachable(url, public_dir)]
    removed_count = len(image_lines) - len(kept)
    if removed_count == 0:
        return False, 0, 0

    if kept:
        for line_idx, url in kept:
            frontmatter[line_idx] = f'- "{url}"\n'
        for line_idx, _ in reversed(image_lines):
            if line_idx not in {i for i, _ in kept}:
                del frontmatter[line_idx]
    else:
        del frontmatter[images_idx : images_idx + 1 + len(image_lines)]

    path.write_text("".join(["---\n", *frontmatter, "---\n", *body]), encoding="utf-8")
    return True, removed_count, len(kept)


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    products_dir = root / "src" / "content" / "products"
    public_dir = root / "public"

    changed_files = 0
    total_removed = 0

    for path in sorted(products_dir.glob("*.md")):
        changed, removed, kept = update_product_file(path, public_dir)
        if changed:
            changed_files += 1
            total_removed += removed
            print(f"{path.name}: removed {removed}, kept {kept}")

    print(f"\nUpdated {changed_files} product files, removed {total_removed} unreachable image URLs")
    return 0


if __name__ == "__main__":
    sys.exit(main())

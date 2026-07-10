---
name: find-category-stock-photo
description: "Find and install a royalty-free stock photo for a Center Industrial product category from sources such as Unsplash. Use when an agent needs to: (1) Replace category emoji icons with stock photography, (2) Add or update a category hero/thumbnail image in product category markdown, (3) Source royalty-free category imagery, or (4) Verify that a stock photo fits a product category before committing it."
paths:
  - "src/content/product-categories/*.md"
  - "public/images/categories/**/*"
  - "src/data/categories.ts"
---

# Find Category Stock Photo

## Keywords

category image, category photo, stock photo, royalty-free, unsplash, pexels, category icon, emoji replacement, category thumbnail, category hero, product category image, industrial stock photo

## Overview

Find and install a **royalty-free stock photograph** for a Center Industrial **top-level product category**. Unlike product images (see `retrieve-product-image`), category photos are thematic/industrial stock shots that represent the category at a glance — not specific branded equipment catalog shots.

Prefer **Unsplash** and other sources with clear commercial-use licenses. Download and host images locally under `public/images/categories/`.

---

## When to Use

- A category card still uses an emoji icon instead of a photo
- The user asks to add stock photography to product category markdown
- A category `image:` path is missing, broken, or needs replacement
- Bulk refresh of category imagery across the catalog

---

## Workflow

Follow these steps in order. Do not skip category-fit verification.

### Step 1: Identify the Category

Read the top-level category markdown in `src/content/product-categories/{slug}.md` and `src/data/categories.ts`. Extract:

| Field | Use |
|-------|-----|
| `title` | Display name |
| `slug` | Filename stem and frontmatter key |
| `description` | Thematic context for image search |

Only top-level categories (files directly under `product-categories/`, not nested subcategory files) get stock photos for the homepage/products grid.

---

### Step 2: Search Royalty-Free Stock Sources

**Preferred sources (in order):**

1. **Unsplash** — `site:unsplash.com/photos {search terms}`
2. **Pexels** — `site:pexels.com {search terms}`
3. **Wikimedia Commons** — only when Unsplash/Pexels lack a suitable image

**Search term examples by category theme:**

| Category theme | Example search terms |
|--------------|---------------------|
| Welding equipment | welding machine, welding equipment workshop, industrial welder |
| Consumables | welding wire spool, steel coil, filler metal |
| Engine-driven welders | diesel generator, portable generator, construction equipment |
| Welding automation | automated welding, production line robotic welding, factory automation |
| Robot systems | welding robot, robotic arm manufacturing |
| CNC cutting/drilling | CNC laser cutting, plasma cutting machine, metal fabrication |
| Tube & pipe | metal pipes factory, steel tubes industrial |
| Induction heating | metal furnace, industrial heat treatment, molten steel |
| PPE & accessories | welding helmet, welding safety gear |
| Laser welding | laser metal processing, laser cutting machine |
| Torches | welding torch sparks, oxy-fuel cutting |
| Stud welding | metal fabrication welding, industrial fastening |

**Reject as sources:**

- Google Images random results without a clear license
- Getty/iStock preview images embedded in Unsplash search (Unsplash+ / paid)
- Brand product catalog shots (use `retrieve-product-image` instead)
- Images that return HTTP 403 on Unsplash download (usually Unsplash+ / premium)

Test download with:

```bash
curl -fsSL -o /tmp/probe.jpg "https://unsplash.com/photos/{PHOTO_ID}/download?force=true&w=1200"
```

---

### Step 3: Verify Category Fit (Required)

Every candidate image must pass **all** checks below before download.

#### Accept

- Subject matter clearly relates to the category title/description
- Industrial/manufacturing context matches Center Industrial's audience
- Image reads well as a small card thumbnail (not overly cluttered)
- License allows commercial use (Unsplash License, Pexels License, etc.)
- Minimum **800px** on the shorter side at download width 1200
- Free download succeeds (HTTP 200, valid JPEG/PNG/WebP)

#### Reject

- Unrelated subject (office, food, nature, unrelated machinery)
- Image is mostly text, logo, or infographic
- Watermarked or rights-managed stock
- Unsplash+ / premium-only (lock icon, 403 on download)
- Too dark, blurry, or abstract to convey the category
- Duplicate theme already used by another category in the repo

#### Category-fit checklist (score before committing)

| Check | Question |
|-------|----------|
| Subject match | Does the main subject relate to this category's products? |
| Audience fit | Would a welding/industrial buyer recognize the category? |
| Thumbnail test | Is the subject identifiable at ~260px card width? |
| Distinctness | Is it visually distinct from other category images already in use? |
| License | Is the source explicitly royalty-free for commercial use? |

If any check fails, continue searching. Do not settle on a weak match.

**Visual verification:** After download, inspect the image with the Read tool (supports images) and confirm it passes the checklist.

---

### Step 4: Download and Store

Save under:

```
public/images/categories/{slug}.jpg
```

- **Filename:** `{slug}.jpg` matching the category slug exactly
- Use `.jpg` unless the source is PNG/WebP and JPEG conversion would lose quality
- Prefer width **1200px** from Unsplash (`?force=true&w=1200`)

**Download** using the helper script (preferred):

```bash
python3 .cursor/skills/find-category-stock-photo/scripts/download-category-image.py \
  --url "https://unsplash.com/photos/ekuWP0hcdKk/download?force=true&w=1200" \
  --output "public/images/categories/standard-equipment.jpg"
```

**After download, verify:**

- File exists and size is > 30 KB
- Image dimensions are at least 600×400
- File is a valid image (not a Git LFS pointer — see below)

Record attribution in `references/category-image-sources.md` (photographer, source URL, category slug).

#### Git LFS (required)

This repo tracks all `*.jpg` and `*.png` via Git LFS (see `.gitattributes`). After download:

1. `git add` stores the binary in LFS automatically — do not paste or commit pointer text manually
2. Confirm tracking: `git lfs ls-files public/images/categories/{slug}.jpg`
3. Confirm real file on disk: `file public/images/categories/{slug}.jpg` must report `JPEG image data`, not `ASCII text`
4. Fresh clones need `git lfs install && git lfs pull` before local dev/build
5. CI deploy workflow must checkout with `lfs: true` (see `.github/workflows/deploy.yml`)

---

### Step 5: Update Category Markdown

Add or replace the `image` field in the top-level category markdown frontmatter:

```yaml
---
title: "Standard Equipment"
slug: "standard-equipment"
layout: category
description: "..."
image: "/images/categories/standard-equipment.jpg"
---
```

Rules:

- Paths are **site-root absolute** (start with `/`, no `public/` prefix)
- Place `image:` after `description:` when present, otherwise after `layout:`
- Only add to top-level `src/content/product-categories/{slug}.md` files

Also update `src/data/categories.ts` — replace `icon` with `image` using the same path so `CategoryCards` stays in sync.

---

### Step 6: Validate

1. Confirm the file exists at `public/images/categories/{slug}.jpg`
2. Confirm it is not an LFS pointer: `bash scripts/verify-not-lfs-pointers.sh`
3. Visually inspect the image — confirm category-fit checklist passes
4. Run `npm run build` to ensure the content schema accepts the frontmatter
5. Spot-check the homepage and `/products/` category cards in the browser
6. Report: source URL, photographer (if known), saved path, and dimensions

---

## Helper Script

`scripts/download-category-image.py` downloads a stock image URL and validates it.

```bash
python3 .cursor/skills/find-category-stock-photo/scripts/download-category-image.py --help
```

| Flag | Description |
|------|-------------|
| `--url` | Image URL to download (required) |
| `--output` | Destination path under repo root (required) |
| `--min-width` | Minimum width in pixels (default: 600) |
| `--min-height` | Minimum height in pixels (default: 400) |
| `--dry-run` | Validate URL without writing |

---

## Related Project Files

| File | Purpose |
|------|---------|
| `src/content/product-categories/*.md` | Top-level category content with `image:` frontmatter |
| `src/data/categories.ts` | Category card data for homepage/products page |
| `src/components/CategoryCards.astro` | Renders category card images |
| `public/images/categories/` | Hosted category stock photos |
| `.cursor/skills/retrieve-product-image/` | Brand product photography (not stock) |
| `agents.md` | Repo-wide image path conventions |

---

## Quick Reference

1. Read category → identify `title`, `slug`, `description`
2. Search Unsplash/Pexels → reject premium/unlicensed results
3. **Verify category fit** → subject, audience, thumbnail, distinctness, license
4. Download → `public/images/categories/{slug}.jpg`
5. Update `image:` in category markdown and `src/data/categories.ts`
6. Build and visually verify category cards

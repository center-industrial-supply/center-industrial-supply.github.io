---
name: retrieve-product-image
description: "Retrieve a high-quality product photography image for a Center Industrial product from official brand sources on the web. Use when an agent needs to: (1) Find or add a product image for a product page, (2) Replace a missing or placeholder product image, (3) Source official brand product photography (not customer action or in-use photos), or (4) Download and wire up product images for the Center Industrial website."
paths:
  - "src/content/products/**/*.md"
  - "public/images/products/**/*"
---

# Retrieve Product Image

## Keywords

product image, product photo, product photography, missing image, placeholder image, brand image, official product image, download product image, add product image, retrieve image, source image, hero image, product thumbnail, welding equipment photo, catalog image

## Overview

Find and install a **product photography** image for a Center Industrial product. The image must show the product itself — typically a studio or catalog shot on a neutral background — and must **not** be a customer action photo (people welding, sparks flying, factory floor, lifestyle/in-use shots).

Prefer images from the **official brand website** at the **highest practical resolution**.

---

## When to Use

- A product page is missing an `images:` entry or shows the placeholder (`/images/placeholder.png`)
- The user asks to find, add, or replace a product image
- Bulk image recovery for products listed in `BROKEN-ASSETS.md`
- A product image URL is unreachable (see `scripts/remove-unreachable-product-images.py`)

---

## Workflow

Follow these steps in order. Do not skip validation.

### Step 1: Identify the Product

Read the product markdown file in `src/content/products/{slug}.md` and extract:

| Field | Use |
|-------|-----|
| `title` | Primary search term |
| `brand` | Restrict search to official brand sources |
| `slug` | Filename stem for saved image |
| `category` | Context for disambiguation |

If the user names a product without a file, locate the matching markdown file first.

Check whether `images:` already exists and whether files in `public/` are reachable.

---

### Step 2: Search Official Brand Sources First

Use `references/brand-sites.md` for known brand domains and search patterns.

**Search order (highest priority first):**

1. **Brand product page** — search `{brand} {product title} site:{brand-domain}`
2. **Brand product catalog / downloads** — PDF catalogs often link to high-res assets
3. **Brand media or asset CDN** — look for `og:image`, `srcset`, or JSON-LD `image` on the product page
4. **Authorized distributor pages** — only if the brand site has no usable image

**Do not use as primary sources:**

- Stock photo sites
- Random marketplace listings (Amazon, eBay) unless no brand source exists
- User-generated or social media images
- Images clearly showing people operating the equipment

Fetch the product page with `WebFetch` and inspect image candidates.

---

### Step 3: Select the Right Image (Product Photography Only)

Evaluate every candidate against these criteria.

#### Accept (product photography)

- Isolated product on white, gray, or neutral background
- Studio/catalog pack shot — product centered, no operator
- Official product render or cutout from brand site
- Straight-on or three-quarter product angle typical of spec sheets
- Image appears in the product hero, gallery, or `og:image` on the brand product page

#### Reject (action / lifestyle photos)

- Person welding, cutting, or holding the product
- Sparks, smoke, or active arc visible
- Factory, workshop, or job-site background with workers
- Marketing banners with overlaid text/logos only (no clear product)
- Thumbnails embedded in unrelated blog posts
- Images where the product is tiny or incidental

#### Prefer highest quality

1. Full-size original URL (no `-300x300`, `-150x150`, `thumbnail`, or `small` in path)
2. Largest `srcset` entry or `data-zoom-image` / lightbox URL
3. Direct `.jpg` / `.png` / `.webp` from brand CDN
4. Minimum acceptable width: **800px** (prefer 1200px+ when available)

If only a thumbnail is available on the page, inspect the page HTML/JSON for a linked full-size asset before accepting the thumbnail.

---

### Step 4: Download and Store the Image

Save the image under `public/images/products/` (not `public/wp-content/` — this site is moving away from WordPress).

**Path convention:**

```
public/images/products/{YYYY}/{MM}/{filename}
```

- Use the current year and month (e.g. `2026/07/`)
- **Filename:** `{Brand}-{Product-Name}.{ext}` — Pascal-case words, hyphens between words, e.g. `ESAB-Buddy-Arc-145.jpg`, `GYS-PROTIG-200-DC-HF.jpg`
- Normalize from `title` and `brand`; avoid spaces in filenames
- Preserve the original extension (`.jpg`, `.png`, `.webp`)

**Download** using the helper script (preferred):

```bash
python3 .cursor/skills/retrieve-product-image/scripts/download-product-image.py \
  --url "https://brand.example/path/to/image.jpg" \
  --output "public/images/products/2026/07/ESAB-Buddy-Arc-145.jpg"
```

Or with curl when the script is not needed:

```bash
curl -fsSL -o "public/images/products/2026/07/ESAB-Buddy-Arc-145.jpg" "https://..."
```

**After download, verify:**

- File exists and size is > 10 KB
- Image dimensions are at least 400×400 (prefer 800×800+)
- File is a valid image (script checks this automatically)

---

### Step 5: Update Product Frontmatter

Add or replace the `images` field in the product markdown file.

```yaml
images:
  - "/images/products/2026/07/ESAB-Buddy-Arc-145.jpg"
```

Rules:

- Paths are **site-root absolute** (start with `/`, no `public/` prefix)
- Use a YAML list with quoted strings
- Place `images:` after `category:` and before the closing `---`
- If `images:` already exists with broken URLs, replace unreachable entries; keep reachable ones unless the user asked to replace

**Example** — `src/content/products/buddy-arc-145.md`:

```yaml
---
title: "Buddy Arc 145"
slug: "buddy-arc-145"
layout: product
description: "..."
brand: "ESAB"
category: "standard-equipment/mma-welding-equipment/esab"
images:
  - "/images/products/2026/07/ESAB-Buddy-Arc-145.jpg"
---
```

---

### Step 6: Validate

1. Confirm the file exists at `public/images/products/...`
2. Visually inspect the image (Read tool supports images) — confirm it is product photography, not an action shot
3. Run `npm run build` if available to ensure the content schema accepts the frontmatter
4. Report to the user: source URL, saved path, dimensions, and brand attribution

---

## Helper Script

`scripts/download-product-image.py` downloads an image URL to the repo and validates it.

```bash
python3 .cursor/skills/retrieve-product-image/scripts/download-product-image.py --help
```

| Flag | Description |
|------|-------------|
| `--url` | Image URL to download (required) |
| `--output` | Destination path under repo root (required) |
| `--min-width` | Minimum width in pixels (default: 400) |
| `--min-height` | Minimum height in pixels (default: 400) |
| `--dry-run` | Validate URL headers without writing |

---

## Handling Common Scenarios

### No brand product page found

1. Try alternate product name spellings (with/without hyphens, model numbers)
2. Search the brand's regional site (e.g. `esab.com` vs `esabna.com`)
3. Check a product catalog PDF on the brand site
4. As a last resort, use a reputable distributor image that is clearly product photography — cite the source

### Only action photos available

Do **not** settle for an action photo. Tell the user:

- Which brand sources were checked
- That only in-use/lifestyle images were found
- Ask whether they have a catalog asset or approve a placeholder until a studio image is available

### Multiple valid images

Pick the one that is:

1. Highest resolution
2. Most clearly product-only (neutral background)
3. Best match to the exact model (check model number in filename or alt text)

### Product already has a low-res thumbnail

Replace if you find the same image at higher resolution (e.g. swap `*-300x300.jpg` for full-size). Keep the old file unless asked to clean up.

---

## Quality Checklist

Before marking complete, confirm:

- [ ] Image is **product photography**, not an action/lifestyle shot
- [ ] Image is from an **official or authorized** source
- [ ] Saved under `public/images/products/{YYYY}/{MM}/`
- [ ] Filename follows `{Brand}-{Product-Name}.{ext}` convention
- [ ] Product markdown updated with `images:` site-root path
- [ ] Image verified readable and meets minimum dimensions

---

## Related Project Files

| File | Purpose |
|------|---------|
| `src/content/products/*.md` | Product content with `images:` frontmatter |
| `src/layouts/ProductLayout.astro` | Renders `images[0]` as primary product image |
| `public/images/products/` | Product photography assets served by Astro |
| `agents.md` | Repo-wide agent conventions including image path rules |
| `BROKEN-ASSETS.md` | List of URLs that failed Wayback recovery |
| `scripts/remove-unreachable-product-images.py` | Strips broken `images:` entries |

---

## Quick Reference

1. Read product → identify `title`, `brand`, `slug`
2. Search brand site → product page → hero/gallery image
3. Reject action photos → accept studio/catalog shots
4. Download highest resolution → `public/images/products/{YYYY}/{MM}/{Brand}-{Product}.{ext}`
5. Update `images:` in product markdown
6. Verify image visually and build

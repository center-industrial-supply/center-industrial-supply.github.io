# center-industrial-supply.github.io

Static rebuild of [centerindustrial.com](https://centerindustrial.com) from the Wayback Machine archive (snapshot `20250404141503`, April 4, 2025).

Live site: https://center-industrial-supply.github.io

## Framework: Astro

This site uses [Astro](https://astro.build) as the static site generator. Content is organized as markdown files with YAML frontmatter (Jekyll-style), built into pages via Astro content collections and layouts.

### Development

```bash
npm install
npm run dev      # local dev server at http://localhost:4321
npm run build    # output to dist/
npm run preview  # preview production build
```

### Project structure

```
src/
  content/
    products/              # 174 product pages (markdown + frontmatter)
    product-categories/    # 87 category pages (nested directories)
  components/              # Header, Footer, CategoryCards, etc.
  data/                    # Top-level category nav data
  layouts/
    BaseLayout.astro       # Site shell (header/footer)
    PageLayout.astro       # Standard interior pages
    ProductLayout.astro    # Single product pages
    CategoryLayout.astro   # Category listing pages
  lib/                     # Build-time utilities
  pages/                   # Route entry points (home, about, dynamic routes)
public/
  assets/                  # CSS, JS
  images/                  # Product, category, and brand images (preferred for new assets)
    products/              # Product photography
  wp-content/              # Legacy WordPress assets from archive (do not add new files here)
scripts/
  migrate-to-content.py    # One-time HTML → markdown migration
  download-wayback.py      # Wayback recovery utilities
```

### Content model (Jekyll-style frontmatter)

**Product** (`src/content/products/buddy-arc-145.md`):

```yaml
---
title: "Buddy Arc 145"
slug: "buddy-arc-145"
layout: product
description: "..."
brand: "ESAB"
category: "standard-equipment/mma-welding-equipment/esab"
images:
  - "/images/products/buddy-arc-145/ESAB-Buddy-Arc-145.jpg"
---
```

**Category** (`src/content/product-categories/standard-equipment.md`):

```yaml
---
title: "Standard Equipment"
slug: "standard-equipment"
layout: category
description: "Manual Gas Apparatus, MMA, MIG/MAG..."
subcategories:
  - slug: "gas-welding-and-cutting-apparatus"
    title: "Gas Welding and Cutting Apparatus"
    image: "/images/categories/gas-welding-and-cutting-apparatus.png"
---
```

New images belong under `public/images/` (see [agents.md](agents.md)). Legacy `/wp-content/uploads/` paths from the WordPress archive may still appear in migrated content.

### Editing pages

- **Products & categories**: Edit markdown files in `src/content/`. URLs are preserved (`/product/{slug}/`, `/product-category/{nested-path}/`).
- **Site pages** (home, about, contact, support): Edit Astro files in `src/pages/` with frontmatter blocks.
- **Navigation data**: `src/data/categories.ts`, `src/data/brands.ts`

To re-migrate from archived HTML (if re-downloaded from Wayback):

```bash
python3 scripts/migrate-to-content.py
```

## Recovery scripts

To re-download pages from the Wayback Machine:

```bash
pip install wayback-archive
export WAYBACK_URL="https://web.archive.org/web/20250404141503/https://centerindustrial.com/"
export OUTPUT_DIR="./public"
export SKIP_LIVE_FALLBACK=true
python3 scripts/download-wayback.py
python3 scripts/cleanup-wayback-refs.py ./public
python3 scripts/migrate-to-content.py
```

See [BROKEN-ASSETS.md](BROKEN-ASSETS.md) for missing URLs from the archive.

Agent conventions (image paths, content model, skills): [agents.md](agents.md).

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) builds with `npm run build` and deploys the `dist/` folder to GitHub Pages on every push to `main`.

# Agent Guide — Center Industrial Website

Instructions for AI agents working in this repository.

## Stack

- **Framework:** [Astro](https://astro.build) static site generator
- **Content:** Markdown with YAML frontmatter in `src/content/`
- **Deploy:** GitHub Pages via GitHub Actions (`npm run build` → `dist/`)

## Image assets (no WordPress paths)

This site is moving away from WordPress. **Do not add new assets under `public/wp-content/`.**

### Product images

Store new product photography at:

```
public/images/products/{YYYY}/{MM}/{Brand}-{Product-Name}.{ext}
```

Reference in frontmatter as site-root absolute paths:

```yaml
images:
  - "/images/products/2026/07/ESAB-Buddy-Arc-145.jpg"
```

| Rule | Detail |
|------|--------|
| Directory | `public/images/products/` |
| Filename | `{Brand}-{Product-Name}.{ext}` — Pascal-case words, hyphens between words |
| Frontmatter path | Starts with `/`, no `public/` prefix |
| Quality | Official brand product photography only (studio/catalog shots, not action photos) |

Use the **`retrieve-product-image`** skill (`.cursor/skills/retrieve-product-image/`) when sourcing product images from brand websites.

### Other images

| Type | Path |
|------|------|
| Site CSS/JS | `public/assets/` |
| Category images | `public/images/categories/` (preferred for new assets) |
| Brand logos | `public/images/brands/` (preferred for new assets) |
| Placeholder | `public/images/placeholder.png` |

### Legacy WordPress assets

Migrated content may still reference `/wp-content/uploads/...`. When updating those products, move images to `public/images/products/` and update frontmatter. Do not create new files under `wp-content/`.

## Content locations

| Content | Path | URL pattern |
|---------|------|-------------|
| Products | `src/content/products/*.md` | `/product/{slug}/` |
| Categories | `src/content/product-categories/**/*.md` | `/product-category/{nested-path}/` |
| Site pages | `src/pages/` | varies |
| Navigation data | `src/data/categories.ts`, `src/data/brands.ts` |

## Product frontmatter

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

## Commands

```bash
npm install
npm run dev      # http://localhost:4321
npm run build
npm run preview
```

## Skills

| Skill | When to use |
|-------|-------------|
| `retrieve-product-image` | Find and install official brand product photography for a product page |

Skills live in `.cursor/skills/`.

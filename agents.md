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
public/images/products/{slug}/{Brand}-{Product-Name}.{ext}
```

Reference in frontmatter as site-root absolute paths:

```yaml
images:
  - "/images/products/buddy-arc-145/ESAB-Buddy-Arc-145.jpg"
```

| Rule | Detail |
|------|--------|
| Directory | `public/images/products/{slug}/` — one folder per product, named after the product slug |
| Filename | `{Brand}-{Product-Name}.{ext}` — Pascal-case words, hyphens between words |
| Frontmatter path | Starts with `/`, no `public/` prefix |
| Quality | Official brand product photography only (studio/catalog shots, not action photos) |

Use the **`retrieve-product-image`** skill (`.cursor/skills/retrieve-product-image/`) when sourcing product images from brand websites.

Use the **`find-category-stock-photo`** skill (`.cursor/skills/find-category-stock-photo/`) when sourcing royalty-free stock photos for product category cards.

### Git LFS

All `.jpg` and `.png` files are tracked by Git LFS (see `.gitattributes`).

| Rule | Detail |
|------|--------|
| Dev setup | Run `git lfs install && git lfs pull` after cloning |
| Committing images | Download real binaries; `git add` stores them in LFS automatically |
| Never commit pointers | Pointer files start with `version https://git-lfs.github.com/spec/v1` — reject these |
| Verify locally | `file public/images/...` must say `JPEG image data` or `PNG image data`, not `ASCII text` |
| CI deploy | `.github/workflows/deploy.yml` checks out with `lfs: true` |

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
  - "/images/products/buddy-arc-145/ESAB-Buddy-Arc-145.jpg"
# clearance: true   # optional; include the product on /clearance/
---
```

## Pull request previews

Every PR gets a Cloudflare Pages preview for the `cisc` project. The Cloudflare bot comments both URLs on the PR:

| URL | Pattern | Use |
|-----|---------|-----|
| **Branch Preview URL** (preferred) | `https://<sanitized-branch>.cisc-6o4.pages.dev` | Stable PR env while the branch updates |
| Preview URL | `https://<commit-hash>.cisc-6o4.pages.dev` | Exact commit |

**Always include the Branch Preview URL** (the PR env) whenever you share a PR in Slack, the PR description, or a wrap-up. Do not share only the GitHub PR link.

How to get it:

1. Open or update the PR, then wait for the `Cloudflare Pages` check and the `cloudflare-workers-and-pages` comment.
2. Read it with `gh pr view <n> --json comments` and use the **Branch Preview URL**.
3. If the comment is not up yet, wait and retry. Do not invent or guess the hostname.

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

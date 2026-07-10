# Brands Hierarchy Plan

> **Jira:** [LABS-52](https://r1sen.atlassian.net/browse/LABS-52) — Create brand → brand-product-category → products hierarchy  
> **Status:** Phase 1 complete — brand markdown + logos seeded  
> **Slack:** #center-rebuild

## Goal

Introduce a **brand-first** browse path alongside the existing product-type category tree:

```
Brand
 └── Brand Product Category
      └── Product
```

Example:

```
ESAB
 └── TIG Welding Equipment
      └── Caddy Tig 2200i AC/DC
```

## Current state (before this plan)

| Layer | Location | Notes |
| --- | --- | --- |
| Brands | `src/data/brands.ts` | 14 featured names, homepage text only |
| Categories | `src/content/product-categories/` | 87 pages, nested by equipment type |
| Products | `src/content/products/` | 174 products with optional `brand` + `category` |

## Phase 1 deliverables (this PR)

### 1. Brand content collection

Created **`src/content/brands/`** — one markdown file per brand (25 total):

| Tier | Count | Brands |
| --- | --- | --- |
| Featured (homepage) | 14 | ESAB, GYS, OTC, Hypertherm, AMG, Aotai, Kjellberg, MOSA, Shindaiwa, Weldflame, Wilson, Hgstar, IKING, Exact |
| Catalog (additional) | 11 | Axxair, DWT, Dayok, Hyundai, Ironcat, Newfire, Taiwan Plasma, TBI, Generico, Permanent, Weldmax |

Each brand markdown includes:

```yaml
---
title: "ESAB"
slug: "esab"
layout: brand
description: "..."
featured: true
officialUrl: https://www.esab.com
logo: /images/brands/esab.svg
productCount: 37
brandProductCategories:
  - slug: tig-welding-equipment
    title: Tig Welding Equipment
    categoryPath: standard-equipment/tig-welding-equipment/esab-tig-welding-equipment
---
```

Schema registered in `src/content.config.ts` under the `brands` collection.

### 2. Brand logos

Logos stored at **`public/images/brands/`** (per `agents.md` convention).

| Brand | Logo | Source quality |
| --- | --- | --- |
| ESAB | `/images/brands/esab.svg` | Official (Wikimedia Commons) |
| GYS | `/images/brands/gys.png` | Favicon — replace with full logo |
| OTC | `/images/brands/otc.png` | Favicon |
| Hypertherm | `/images/brands/hypertherm.png` | Favicon |
| AMG | `/images/brands/amg.svg` | **Wordmark placeholder** — site unreachable from CI |
| Aotai | `/images/brands/aotai.png` | Favicon |
| Kjellberg | `/images/brands/kjellberg.svg` | Official (Wikimedia Commons) |
| MOSA | `/images/brands/mosa.svg` | Official site SVG |
| Shindaiwa | `/images/brands/shindaiwa.png` | Wikimedia photo — verify/replace |
| Weldflame | `/images/brands/weldflame.svg` | **Wordmark placeholder** — SSL blocked |
| Wilson | `/images/brands/wilson.svg` | **Wordmark placeholder** — DNS blocked |
| Hgstar | `/images/brands/hgstar.png` | Favicon |
| IKING | `/images/brands/iking.png` | Favicon |
| Exact | `/images/brands/exact.png` | **Official** (exacttools.com) |
| Axxair | `/images/brands/axxair.png` | Favicon |
| DWT | `/images/brands/dwt.png` | Favicon |
| Dayok | `/images/brands/dayok.png` | Favicon |
| Hyundai | `/images/brands/hyundai.png` | Favicon |
| Ironcat | `/images/brands/ironcat.svg` | **Wordmark placeholder** |
| Newfire | `/images/brands/newfire.png` | Favicon |
| Taiwan Plasma | `/images/brands/taiwan-plasma.svg` | **Wordmark placeholder** |
| TBI | `/images/brands/tbi.png` | Favicon/ICO |
| Generico | `/images/brands/generico.svg` | **Wordmark placeholder** (private label) |
| Permanent | `/images/brands/permanent.svg` | **Wordmark placeholder** (private label) |
| Weldmax | `/images/brands/weldmax.svg` | **Wordmark placeholder** (private label) |

**Follow-up:** Replace favicon-grade and wordmark-placeholder logos with official brand assets (request from manufacturers or manual download from brand sites).

### 3. Brand registry summary

| Slug | Display name | Products | Featured | Brand product categories |
| --- | --- | --- | --- | --- |
| esab | ESAB | 37 | ✓ | 11 |
| gys | GYS | 22 | ✓ | 4 |
| otc | OTC | 17 | ✓ | 6 |
| axxair | Axxair | 12 | | 3 |
| dwt | DWT | 14 | | 4 |
| wilson | Wilson | 11 | ✓ | 1 |
| amg | AMG | 9 | ✓ | 4 |
| aotai | Aotai | 7 | ✓ | 3 |
| weldflame | Weldflame | 7 | ✓ | 1 |
| taiwan-plasma | Taiwan Plasma | 4 | | 1 |
| hypertherm | Hypertherm | 3 | ✓ | 1 |
| iking | IKING | 3 | ✓ | 1 |
| ironcat | Ironcat | 2 | | 0 |
| mosa | MOSA | 2 | ✓ | 1 |
| shindaiwa | Shindaiwa | 2 | ✓ | 1 |
| dayok | Dayok | 1 | | 1 |
| exact | Exact | 1 | ✓ | 1 |
| generico | Generico | 1 | | 1 |
| hgstar | Hgstar | 1 | ✓ | 1 |
| hyundai | Hyundai | 1 | | 1 |
| kjellberg | Kjellberg | 1 | ✓ | 1 |
| newfire | Newfire | 1 | | 0 |
| permanent | Permanent | 1 | | 1 |
| tbi | TBI | 1 | | 1 |
| weldmax | Weldmax | 1 | | 1 |

## Naming normalization (for Phase 2)

| Frontmatter value | Canonical name | Slug |
| --- | --- | --- |
| `KJELLBERG` | Kjellberg | `kjellberg` |
| `ironcat` | Ironcat | `ironcat` |
| `newfire` | Newfire | `newfire` |
| `weldmax` | Weldmax | `weldmax` |

12 products still lack a `brand:` field (mostly Exact pipe tools). Backfill in Phase 2.

## Proposed URL structure (Phase 2)

| Page | URL |
| --- | --- |
| All brands index | `/brands/` |
| Brand landing | `/brand/{brand-slug}/` |
| Brand product category | `/brand/{brand-slug}/{category-slug}/` |
| Product (unchanged) | `/product/{slug}/` |

Legacy WordPress brand archives at `/product-tag/{brand}/` should redirect to `/brand/{brand-slug}/`.

## Implementation phases

### Phase 2 — Pages & routing

1. Add `BrandLayout.astro` and routes under `src/pages/brand/[...slug].astro`
2. Build `/brands/` index page with logo cards
3. Brand landing page: logo, description, child category cards
4. Brand-product-category page: product grid filtered by `brand` + `categoryPath`
5. Wire homepage brand names (`src/data/brands.ts`) → brand landing pages

### Phase 3 — Navigation & SEO

1. Add "Brands" to header/footer nav
2. Product breadcrumbs: `Home → Brands → ESAB → TIG Welding Equipment → Product`
3. Cross-link from product-type category pages to brand pages
4. Redirects from `/product-tag/{brand}/` (27 legacy tags)

### Phase 4 — Data quality

1. Script to derive/validate brand → category → product mapping from frontmatter
2. Normalize brand casing across 174 product files
3. Backfill missing `brand:` on Exact/Hgstar/generic products
4. Replace placeholder/favicon logos with official assets
5. Extend `src/data/brands.ts` from string[] to structured objects (or remove in favor of content collection)

## Data derivation logic

Brand-product-category membership is derived from existing product frontmatter:

```
product.brand == brand.title
AND product.category starts with brandProductCategory.categoryPath
```

Alternative: add explicit `brandCategory` field to products for cleaner mapping.

## Acceptance criteria (full LABS-52)

- [x] Brand content model defined (`src/content.config.ts` + `src/content/brands/`)
- [x] Brand markdown populated for all 25 catalog brands
- [x] Logo attached for every brand (mix of official, favicon, and interim wordmarks)
- [ ] Brand landing pages at `/brand/{slug}/`
- [ ] Brand-product-category pages list correct products
- [ ] Product pages show brand-first breadcrumb
- [ ] `/brands/` index page
- [ ] Homepage brand names link to brand pages
- [ ] No broken links from existing category navigation
- [ ] Legacy `/product-tag/` redirects

## Out of scope

- E-commerce (cart/checkout)
- Replacing the product-type category tree
- New product content beyond taxonomy wiring

## References

- Parent rebuild: [LABS-50](https://r1sen.atlassian.net/browse/LABS-50)
- Brand site domains: `.cursor/skills/retrieve-product-image/references/brand-sites.md`
- Agent conventions: `agents.md`
- Live site: https://center-industrial-supply.github.io

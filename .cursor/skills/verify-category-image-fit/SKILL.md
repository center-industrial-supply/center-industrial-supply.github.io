---
name: verify-category-image-fit
description: "Audit Center Industrial product category and subcategory card images against their title, name, and description. Use when an agent needs to: (1) Review whether category stock photos match category metadata, (2) Produce a pass/fail report for category imagery, (3) Identify mismatched or swapped category images before or after replacement, or (4) Re-verify images after sourcing replacements with find-category-stock-photo."
paths:
  - "src/content/product-categories/*.md"
  - "src/data/categories.ts"
  - "public/images/categories/**/*"
  - ".cursor/skills/find-category-stock-photo/**/*"
---

# Verify Category Image Fit

## Keywords

category image verification, image fit audit, category mismatch, stock photo review, category card audit, subcategory image check, visual verification, category imagery QA

## Overview

Systematically compare every **top-level product category** and **subcategory card image** against its `title`, `name`, and `description`. Produce a structured pass/fail report and flag images that should be replaced using `find-category-stock-photo`.

This skill is **read-only verification**. To install replacement images, follow `find-category-stock-photo` after the audit.

---

## When to Use

- Bulk audit of category card imagery across the catalog
- Before committing new stock photos from `find-category-stock-photo`
- After replacing images to confirm the fix (single re-check pass — do not loop)
- User asks to review category images against names/descriptions

---

## Category Definitions

Each category has a **definition** used for verification. Read from frontmatter in this order:

| Field | Location | Notes |
|-------|----------|-------|
| `title` | Category markdown | Primary display name |
| `description` | Category markdown or `src/data/categories.ts` | Thematic scope |
| `name` | `src/data/categories.ts` only | Top-level cards; should align with `title` |

**If `description` is missing** from markdown, derive one from:
1. `src/data/categories.ts` `description` (top-level only)
2. Subcategory `title` + parent category context
3. Product slugs/titles listed under the category (skim first 3–5)
4. Write a concise one-line definition and **add it to the category markdown frontmatter** as `description:`

Example derived definition for `Engine Driven Welders`:
> Portable diesel or petrol engine-driven welding power sources for field and construction work.

---

## Scope

| Tier | Markdown source | Image path |
|------|-----------------|------------|
| Top-level (12) | `src/content/product-categories/{slug}.md` | `/images/categories/{slug}.jpg` |
| Subcategory (31) | Parent file `subcategories:` array | `/images/categories/subcategories/{slug}.jpg` |

Also cross-check `src/data/categories.ts` for top-level `image` paths.

---

## Verification Workflow

### Step 1: Collect Metadata

For each category, record:

```
slug, title, description, image path, parent (if subcategory)
```

Run `git lfs pull --include="public/images/categories/**"` if images show as LFS pointers.

### Step 2: Visual Inspection (Required)

Open each image with the Read tool (supports JPEG/PNG). For every image, answer the checklist below.

**Do not rely on filename, attribution notes, or Unsplash titles alone** — confirm the actual pixels match the category.

### Step 3: Score Each Image

| Verdict | Criteria |
|---------|----------|
| **PASS** | Subject clearly represents the category title/description; identifiable at card thumbnail size (~260px) |
| **BORDERLINE** | Industrial/welding related but wrong process, wrong product type, or too generic |
| **FAIL** | Unrelated subject, wrong equipment type, swapped with another category, or duplicates another category's theme |

### Step 4: Category-Fit Checklist

Every image must pass **all** checks for PASS:

| # | Check | Question |
|---|-------|----------|
| 1 | Subject match | Does the main subject relate to this category's products/process? |
| 2 | Title match | Would a buyer searching for this category name recognize the image? |
| 3 | Description match | Does the image reflect the description scope (not a adjacent category)? |
| 4 | Thumbnail test | Is the subject identifiable at ~260px card width? |
| 5 | Distinctness | Is it visually distinct from sibling/other category images? |
| 6 | Not swapped | Does it show what a *different* category in the repo is supposed to show? |

If check 6 is yes → verdict is **FAIL (swapped)**.

### Step 5: Common Mismatch Patterns

Watch for these recurring errors in this catalog:

| Pattern | Example |
|---------|---------|
| Process confusion | Laser **cutting** photo on Laser **Welding** |
| Foundry vs induction | Molten metal pour on Induction Heating |
| Generator vs compressor | Air compressor on Engine Driven Welders |
| Generic flea market | Used-tool pile on Standard Equipment |
| MMA ↔ MIG swap | Stick welder image on MIG/MAG subcategory |
| CNC laser reused | Flat-plate laser cutter on orbital **pipe** subcategories |
| Angle grinder reuse | Hand grinder on specialized pipe cold cutter categories |
| PPE product mismatch | Welding scene where gloves/helmet/spectacles aren't the subject |
| Automotive assembly | Car factory robots on Welding Automation |

### Step 6: Produce Report

Output a table for **FAIL** and **BORDERLINE** entries:

```markdown
| Slug | Title | Verdict | Issue |
|------|-------|---------|-------|
| laser-welding | Laser Welding | FAIL | Shows CNC laser cutting, not welding |
```

Summarize counts: `PASS: N / TOTAL`.

### Step 7: Fix Mismatches (One Pass)

For each FAIL/BORDERLINE item:

1. Follow `find-category-stock-photo` to source a replacement
2. Re-run **this skill** on changed images only (single verification pass)
3. Update `references/category-image-sources.md` with new attribution
4. Do **not** loop again after the re-check

---

## Subcategory Disambiguation

When verifying subcategories under the same parent, also confirm the image differs from **sibling** subcategories:

| Parent | Siblings to distinguish |
|--------|------------------------|
| `standard-equipment` | MIG vs MMA vs TIG vs plasma vs gas apparatus |
| `cutting-drilling-automation` | Laser vs plasma vs plate drilling vs beam |
| `tube-and-pipe-*` | Orbital cutting vs bevelling vs welding vs cold cutter |
| `ppe-and-accessories` | Helmet vs gloves vs spectacles vs respirator vs fire blanket |
| `robot-systems` | Welding robots vs spot/material handling vs positioners |

---

## Helper Script

Batch re-download from attribution file (use only when attribution is trusted):

```bash
python3 .cursor/skills/verify-category-image-fit/scripts/download-verified-images.py
```

Use after manual verification to batch-install approved image URLs.

---

## Related Files

| File | Purpose |
|------|---------|
| `src/content/product-categories/*.md` | Category title, description, image paths |
| `src/data/categories.ts` | Homepage card names/descriptions/images |
| `public/images/categories/` | Top-level stock photos |
| `public/images/categories/subcategories/` | Subcategory card photos |
| `.cursor/skills/find-category-stock-photo/` | Source and install replacements |
| `.cursor/skills/find-category-stock-photo/references/category-image-sources.md` | Attribution log |

---

## Quick Reference

1. Pull LFS images → read all category markdown + `categories.ts`
2. Add missing `description:` to frontmatter where absent
3. Visually inspect every image → score PASS / BORDERLINE / FAIL
4. Report mismatches in a table
5. Replace FAIL items via `find-category-stock-photo` (one pass)
6. Re-verify changed images once → update attribution log

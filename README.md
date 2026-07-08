# center-industrial-supply.github.io

Static rebuild of [centerindustrial.com](https://centerindustrial.com) from the Wayback Machine archive (snapshot `20250404141503`, April 4, 2025).

Live site: https://center-industrial-supply.github.io

## Framework: Astro

This site uses [Astro](https://astro.build) as the static site generator. Main pages are built from Astro components; archived product and category pages remain as legacy HTML in `public/` and are wrapped with the shared header/footer via `public/assets/js/layout.js`.

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
  components/     # Header, Footer, CategoryCards, etc.
  data/           # Categories, brands (shared site data)
  layouts/        # BaseLayout.astro
  lib/            # Build-time utilities (product catalog scanner)
  pages/          # Astro pages (home, about, products, etc.)
public/
  assets/         # CSS, JS, layout partials for legacy pages
  product/        # Archived product pages (Wayback)
  product-category/
  wp-content/     # Images and media from original site
scripts/          # Wayback recovery utilities
```

### Editing main pages

Edit the Astro pages in `src/pages/` and shared components in `src/components/`. Site data (categories, brands) lives in `src/data/`. The product catalog at `/all-products/` is generated at build time from archived pages in `public/product/`.

### Legacy archive pages

Product and category pages under `public/` are untouched WordPress exports. They load the modern header/footer via `layout.js` at runtime. Styles are in `public/assets/css/legacy.css`.

## Recovery scripts

To re-download pages from the Wayback Machine:

```bash
pip install wayback-archive
export WAYBACK_URL="https://web.archive.org/web/20250404141503/https://centerindustrial.com/"
export OUTPUT_DIR="./public"
export SKIP_LIVE_FALLBACK=true
python3 scripts/download-wayback.py
python3 scripts/cleanup-wayback-refs.py ./public
```

See [BROKEN-ASSETS.md](BROKEN-ASSETS.md) for missing URLs from the archive.

## Deployment

GitHub Actions (`.github/workflows/deploy.yml`) builds with `npm run build` and deploys the `dist/` folder to GitHub Pages on every push to `main`.

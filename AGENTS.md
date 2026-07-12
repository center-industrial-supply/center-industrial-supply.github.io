# AGENTS.md

## Cursor Cloud specific instructions

### What this repo is
This repo (`center-industrial-supply.github.io`) is a **static website archive** of a WooCommerce storefront, recovered from the Wayback Machine and hosted on GitHub Pages. It is pre-rendered HTML/CSS/JS — there is **no build system, no package manager, no lockfile, and no backend**. See `README.md`.

### Running the site (dev)
Serve the repo root as static files, then browse `http://localhost:8000/`:

```bash
python3 -m http.server 8000   # run from repo root
```

Relative links (e.g. `../../../`) resolve against the served root, so always serve from the repo root. Key entry points: `index.html` (homepage), `product/<slug>/index.html` (product pages), `product-category/<slug>/index.html` (category listings).

### Lint / test / build
There are none — this is static HTML. Do not attempt to build or run a test suite; there is nothing to compile.

### Non-obvious caveats
- Dynamic features are **non-functional by design** (static rebuild): cart, checkout, contact forms, and login will not work. Do not treat these as bugs. See `BROKEN-ASSETS.md`.
- Many theme/plugin CSS files and some images are missing from the archive (~636 URLs failed to download), so pages may render partially unstyled. This is expected; `BROKEN-ASSETS.md` has the full list.
- **The product content available right now is the product list / product pages.** Focus verification on those; ignore the e-commerce flow.
- The `scripts/` recovery tooling (`download-wayback.py`, `cleanup-wayback-refs.py`) is **optional maintenance only** — needed to regenerate the archive, not to run the site. It requires the Python packages `requests` and `wayback-archive` (installed by the update script) plus network access to `web.archive.org`.

### Demo / walkthrough preference
Perform the walkthrough demo **after** the work is done (i.e. complete the implementation first, then record/capture the demo at the end).

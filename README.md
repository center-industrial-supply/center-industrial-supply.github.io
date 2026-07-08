# center-industrial-supply.github.io

Static rebuild of [centerindustrial.com](https://centerindustrial.com) from the Wayback Machine archive (snapshot `20250404141503`, April 4, 2025).

Live site: https://center-industrial-supply.github.io

## Site layout

The main pages (home, about, products, catalog, support, contact) use a new static layout in `assets/`. Archived product and category pages are wrapped with the same header/footer via `assets/js/layout.js`.

Rebuild pages after editing layout sources:

```bash
python3 scripts/build-layout.py
```

## Recovery scripts

```bash
pip install wayback-archive
export WAYBACK_URL="https://web.archive.org/web/20250404141503/https://centerindustrial.com/"
export OUTPUT_DIR="./site"
export SKIP_LIVE_FALLBACK=true
python3 scripts/download-wayback.py
python3 scripts/cleanup-wayback-refs.py ./site
```

See [BROKEN-ASSETS.md](BROKEN-ASSETS.md) for missing URLs from the archive.

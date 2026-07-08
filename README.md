# center-industrial-supply.github.io

Static rebuild of [centerindustrial.com](https://centerindustrial.com) from the Wayback Machine archive (snapshot `20250404141503`, April 4, 2025).

Live site: https://center-industrial-supply.github.io

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

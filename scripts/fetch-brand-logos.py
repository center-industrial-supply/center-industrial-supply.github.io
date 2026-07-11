#!/usr/bin/env python3
"""Download and normalize official brand logos for the CISC site.

Logos are sourced from manufacturer websites or authorized distributor assets.
Run from repo root: python3 scripts/fetch-brand-logos.py
"""

from __future__ import annotations

import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "public" / "images" / "brands"
TMP = ROOT / ".cache" / "brand-logos"

UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0"

# slug -> (url, output filename)
SOURCES: dict[str, tuple[str, str]] = {
    "esab": ("https://cdn.worldvectorlogo.com/logos/esab.svg", "esab.svg"),
    "gys": ("https://www.gys.fr/img/common/Top/Group.svg", "gys.svg"),
    "otc": ("https://www.otc-daihen.com/assets/template/icons.svg?1713965342", "otc-icons.svg"),
    "hypertherm": (
        "https://www.hypertherm.com/globalassets/ha/logo_ht-technology-400.png",
        "hypertherm.png",
    ),
    "amg": ("https://cdn.worldvectorlogo.com/logos/amg.svg", "amg.svg"),
    "aotai": (
        "https://usimg.bjyyb.net/sites/62500/62761/20210619110125174.png",
        "aotai.png",
    ),
    "kjellberg": ("https://www.kjellberg.com/LOGOMIC.jpg", "kjellberg.jpg"),
    "mosa": (
        "https://www.mosa.com/packages/mosa_site/themes/mosa_theme/e04/shared_assets/img/logo.svg",
        "mosa.svg",
    ),
    "shindaiwa": ("https://www.shindaiwa.com/_nuxt/img/c8d9173.svg", "shindaiwa.svg"),
    "hgstar": ("https://style.hgstarlaser.com/logo.gif", "hgstar.png"),
    "iking": (
        "https://www.shearstud.net/Uploads/logo/en-IKING-stud-welding-solution-163347.jpg",
        "iking.jpg",
    ),
    "exact": (
        "https://exacttools.com/wp-content/themes/exacttools/assets/img/logo_exact_system.png",
        "exact.png",
    ),
    "wilson": (
        "https://ossis.industrystock.com/company/logo/be117f6a2e3200757d0d3e664fe998aa.jpg",
        "wilson.jpg",
    ),
    # Legacy CISC asset; weldflame.com has SSL issues in automated fetch environments.
    "weldflame": (
        "https://web.archive.org/web/20231204034522im_/https://i0.wp.com/centerindustrial.com/wp-content/uploads/2020/10/company-logo-weldflame.jpg?fit=309%2C108&ssl=1",
        "weldflame.jpg",
    ),
}


def curl(url: str, dest: Path) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        ["curl", "-fsSL", "-A", UA, "--max-time", "45", "-o", str(dest), url],
        check=True,
    )


def extract_otc_logo(src: Path, dest: Path) -> None:
    import re

    text = src.read_text(encoding="utf-8", errors="replace")
    match = re.search(
        r'<symbol[^>]*id="otc-logo"[^>]*viewBox="([^"]*)"[^>]*>(.*?)</symbol>',
        text,
        re.S,
    )
    if not match:
        match = re.search(r'<symbol[^>]*id="otc-logo"[^>]*>(.*?)</symbol>', text, re.S)
        viewbox = "0 0 200 60"
        content = match.group(1) if match else ""
    else:
        viewbox, content = match.group(1), match.group(2)
    dest.write_text(
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}">{content}</svg>\n',
        encoding="utf-8",
    )


def normalize_raster(src: Path, dest: Path, max_width: int = 640) -> None:
    from PIL import Image

    img = Image.open(src)
    if img.mode not in ("RGB", "RGBA"):
        img = img.convert("RGBA")
    if img.width > max_width:
        ratio = max_width / img.width
        img = img.resize((max_width, max(1, int(img.height * ratio))), Image.Resampling.LANCZOS)
    if dest.suffix.lower() == ".jpg" and img.mode == "RGBA":
        bg = Image.new("RGB", img.size, (255, 255, 255))
        bg.paste(img, mask=img.split()[-1])
        img = bg
    img.save(dest, optimize=True)


def main() -> None:
    try:
        from PIL import Image  # noqa: F401
    except ImportError:
        subprocess.run(["pip", "install", "pillow", "-q"], check=True)

    TMP.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)

    for slug, (url, filename) in SOURCES.items():
        raw = TMP / filename
        print(f"Fetching {slug} …")
        curl(url, raw)

        if slug == "otc":
            out = OUT / "otc.svg"
            extract_otc_logo(raw, out)
            continue

        out = OUT / filename
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            normalize_raster(raw, out)
        else:
            shutil.copy2(raw, out)

    print(f"Wrote logos to {OUT}")


if __name__ == "__main__":
    main()

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
# CISC Drive logos (CENTER-9) are stored in-repo after a one-time import:
#   ESAB.svg.png, OTCAsia(WHITE).bmp, JFY-LOGO-FULL.jpg, WeldmaxLogo_Light-Tagline.jpg,
#   Norton endorsement PDF, HR Laser Logo.png, Max Photonics.png
# Public manufacturer URLs below cover the remaining brands.
SOURCES: dict[str, tuple[str, str]] = {
    "gys": ("https://www.gys.fr/img/common/Top/Group.svg", "gys.svg"),
    "hypertherm": (
        "https://www.hypertherm.com/globalassets/ha/logo_ht-technology-400.png",
        "hypertherm.png",
    ),
    "amg": (
        "https://www.asiacnc.com.tw/themes/asiacnc/images/logo.png",
        "amg.png",
    ),
    "aotai": (
        "https://usimg.bjyyb.net/sites/62500/62761/20210619110125174.png",
        "aotai.png",
    ),
    "kjellberg": (
        "https://commons.wikimedia.org/w/index.php?title=Special:FilePath/Kjellberg-Finsterwalde-Logo.svg",
        "kjellberg.svg",
    ),
    "mosa": (
        "https://www.mosa.com/packages/mosa_site/themes/mosa_theme/e04/shared_assets/img/logo.svg",
        "mosa.svg",
    ),
    "shindaiwa": ("https://www.shindaiwa.com/_nuxt/img/c8d9173.svg", "shindaiwa.svg"),
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
    "dwt": ("https://www.dwt-pipetools.com/userfiles/image/layout/logo.png", "dwt.png"),
    "axxair": (
        "https://www.axxair.com/wp-content/uploads/sites/23/2024/10/AXXAIR-logo.svg",
        "axxair.svg",
    ),
    "taiwan-plasma": ("https://www.plasma.com.tw/images/logo.png", "taiwan-plasma.png"),
}


def curl(url: str, dest: Path, referer: str | None = None) -> None:
    dest.parent.mkdir(parents=True, exist_ok=True)
    cmd = ["curl", "-fsSL", "-A", UA, "--max-time", "45"]
    if referer:
        cmd.extend(["-H", f"Referer: {referer}"])
    cmd.extend(["-o", str(dest), url])
    subprocess.run(cmd, check=True)


def normalize_kjellberg_logo(src: Path, dest: Path) -> None:
    """Use the positive (dark-on-light) color variant of the official logo.

    The manufacturer SVG uses white letter interiors for dark/yellow backgrounds.
    CISC brand cards sit on white, so swap that fill to the brand anthracite.
    """
    text = src.read_text(encoding="utf-8", errors="replace")
    text = text.replace(".fil1 {fill:white}", ".fil1 {fill:#1E1C1F}")
    dest.write_text(text, encoding="utf-8")


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


def invert_white_on_black(src: Path, dest: Path) -> None:
    """Turn a white-on-black header mark into a dark-on-light logo for CISC cards."""
    import numpy as np
    from PIL import Image

    img = Image.open(src).convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    is_black = (r < 45) & (g < 45) & (b < 45)
    is_white = (r > 220) & (g > 220) & (b > 220)
    arr[is_white, 0] = 20
    arr[is_white, 1] = 20
    arr[is_white, 2] = 20
    arr[is_black, 3] = 0
    Image.fromarray(arr.astype(np.uint8)).save(dest, optimize=True)


def extract_embedded_png(src: Path, dest: Path) -> None:
    import base64
    import re

    text = src.read_text(encoding="utf-8", errors="replace")
    match = re.search(r"xlink:href=\"data:image/png;base64,([^\"]+)\"", text)
    if not match:
        raise RuntimeError(f"No embedded PNG found in {src}")
    dest.write_bytes(base64.b64decode(match.group(1)))


def recolor_exact_logo_for_light_bg(src: Path, dest: Path) -> None:
    """Exact's official asset is white/yellow for dark backgrounds; recolor for CISC cards."""
    import numpy as np
    from PIL import Image

    img = Image.open(src).convert("RGBA")
    arr = np.array(img, dtype=np.float32)
    alpha = arr[:, :, 3]
    visible = alpha > 128
    r, g, b = arr[:, :, 0], arr[:, :, 1], arr[:, :, 2]
    is_yellow = visible & (r > 200) & (g > 150) & (b < 100)
    is_white = visible & (r > 240) & (g > 240) & (b > 240)
    is_light = visible & ~is_yellow & (r > 200) & (g > 200)

    arr[is_white | is_light, 0] = 2
    arr[is_white | is_light, 1] = 43
    arr[is_white | is_light, 2] = 51
    arr[is_yellow, 0] = 255
    arr[is_yellow, 1] = 202
    arr[is_yellow, 2] = 0

    Image.fromarray(arr.astype(np.uint8)).save(dest, optimize=True)


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
        referer = "https://www.asiacnc.com.tw/" if slug == "amg" else None
        curl(url, raw, referer=referer)

        if slug == "kjellberg":
            out = OUT / "kjellberg.svg"
            normalize_kjellberg_logo(raw, out)
            continue

        if slug == "axxair":
            embedded = TMP / "axxair-embedded.png"
            extract_embedded_png(raw, embedded)
            invert_white_on_black(embedded, OUT / "axxair.png")
            continue

        out = OUT / filename
        if filename.endswith((".png", ".jpg", ".jpeg", ".gif")):
            if slug == "exact":
                normalized = TMP / "exact-normalized.png"
                normalize_raster(raw, normalized)
                recolor_exact_logo_for_light_bg(normalized, out)
            else:
                normalize_raster(raw, out)
        else:
            shutil.copy2(raw, out)

    print(f"Wrote logos to {OUT}")


if __name__ == "__main__":
    main()

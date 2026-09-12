#!/usr/bin/env python3
"""Download verified category images from Unsplash/Pexels."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[4]
DOWNLOAD = REPO / ".cursor/skills/find-category-stock-photo/scripts/download-category-image.py"

# slug -> (url, tier)  tier: top | sub
IMAGES: dict[str, tuple[str, str]] = {
    # --- Top-level fixes ---
    "standard-equipment": (
        "https://unsplash.com/photos/9lHilIK182g/download?force=true&w=1200",
        "top",
    ),
    "engine-driven-welder": (
        "https://images.pexels.com/photos/13944023/pexels-photo-13944023.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "top",
    ),
    "standard-welding-automation": (
        "https://unsplash.com/photos/TtOdr8tYtUU/download?force=true&w=1200",
        "top",
    ),
    "induction-heating-machine": (
        "https://unsplash.com/photos/PWsjl3UoHX0/download?force=true&w=1200",
        "top",
    ),
    "laser-welding": (
        "https://unsplash.com/photos/z9IDLQGb4Ns/download?force=true&w=1200",
        "top",
    ),
    "stud-welding-equipment": (
        "https://unsplash.com/photos/r3zJqdmByvI/download?force=true&w=1200",
        "top",
    ),
    # Keep passing top-level (re-download to fix any corruption)
    "welding-consumables": (
        "https://unsplash.com/photos/9y6hRUIpifY/download?force=true&w=1200",
        "top",
    ),
    "robot-systems": (
        "https://unsplash.com/photos/C9-7_QiJ52A/download?force=true&w=1200",
        "top",
    ),
    "cutting-drilling-automation": (
        "https://unsplash.com/photos/4enstJBOGww/download?force=true&w=1200",
        "top",
    ),
    "tube-and-pipe-cutting-and-welding-solutions": (
        "https://unsplash.com/photos/im7unQC9fUQ/download?force=true&w=1200",
        "top",
    ),
    "ppe-and-accessories": (
        "https://unsplash.com/photos/7gU8ssOTM8M/download?force=true&w=1200",
        "top",
    ),
    "welding-and-cutting-torch": (
        "https://unsplash.com/photos/O3qXl6DdIm0/download?force=true&w=1200",
        "top",
    ),
    # --- Subcategory fixes ---
    "gas-welding-and-cutting-apparatus": (
        "https://unsplash.com/photos/nmjQKjU9RUk/download?force=true&w=1200",
        "sub",
    ),
    "mig-mag-welding-equipment": (
        "https://unsplash.com/photos/Wiu3w-99tNg/download?force=true&w=1200",
        "sub",
    ),
    "mma-welding-equipment": (
        "https://unsplash.com/photos/sPl7FgBalxI/download?force=true&w=1200",
        "sub",
    ),
    "multi-process-welding": (
        "https://unsplash.com/photos/9lHilIK182g/download?force=true&w=1200",
        "sub",
    ),
    "plasma-arc-cutting-equipment": (
        "https://unsplash.com/photos/gWjrBqTLREU/download?force=true&w=1200",
        "sub",
    ),
    "tig-welding-equipment": (
        "https://unsplash.com/photos/n1RJ7pXgGTE/download?force=true&w=1200",
        "sub",
    ),
    "welding-robots": (
        "https://unsplash.com/photos/sz1CHL7Pky0/download?force=true&w=1200",
        "sub",
    ),
    "robots-for-spot-welding-material-handling": (
        "https://unsplash.com/photos/r3zJqdmByvI/download?force=true&w=1200",
        "sub",
    ),
    "positioners": (
        "https://unsplash.com/photos/Wwkq5UavgwQ/download?force=true&w=1200",
        "sub",
    ),
    "submerged-arc-welding-equipment": (
        "https://unsplash.com/photos/enPxH6uqABg/download?force=true&w=1200",
        "sub",
    ),
    "column-and-booms": (
        "https://unsplash.com/photos/SLIFI67jv5k/download?force=true&w=1200",
        "sub",
    ),
    "gantries": (
        "https://unsplash.com/photos/mhUsz2ezlXQ/download?force=true&w=1200",
        "sub",
    ),
    "tank-welders": (
        "https://unsplash.com/photos/QzP1GcDOSC8/download?force=true&w=1200",
        "sub",
    ),
    "mig-fcaw-welding-carriages": (
        "https://unsplash.com/photos/DTwqr5l35rw/download?force=true&w=1200",
        "sub",
    ),
    "cnc-laser-cutting-machines": (
        "https://unsplash.com/photos/x0Q7F6h-dXk/download?force=true&w=1200",
        "sub",
    ),
    "cnc-cutting-machines": (
        "https://unsplash.com/photos/thdb7o0nLyc/download?force=true&w=1200",
        "sub",
    ),
    "cnc-plate-drilling-machines": (
        "https://unsplash.com/photos/5Wu96pC2qxE/download?force=true&w=1200",
        "sub",
    ),
    "cnc-beam-drilling-cutting-machines": (
        "https://unsplash.com/photos/q0lzQOLYlHc/download?force=true&w=1200",
        "sub",
    ),
    "airfiltermask": (
        "https://unsplash.com/photos/xnqyNSf0nck/download?force=true&w=1200",
        "sub",
    ),
    "fire-blankets": (
        "https://unsplash.com/photos/J0Tmo1_NPNo/download?force=true&w=1200",
        "sub",
    ),
    "safety-spectacles": (
        "https://images.pexels.com/photos/9242919/pexels-photo-9242919.jpeg?auto=compress&cs=tinysrgb&w=1200",
        "sub",
    ),
    "welding-gloves": (
        "https://unsplash.com/photos/0G8M3LVT5Ds/download?force=true&w=1200",
        "sub",
    ),
    "welding-helmet-ppe-and-accessories": (
        "https://unsplash.com/photos/c-vWdiICscA/download?force=true&w=1200",
        "sub",
    ),
    "exact-pipe-cutting-machines": (
        "https://unsplash.com/photos/mJi2I9KJPQ8/download?force=true&w=1200",
        "sub",
    ),
    "orbital-cutting-machines": (
        "https://unsplash.com/photos/d0-dqCkmnuk/download?force=true&w=1200",
        "sub",
    ),
    "orbital-bevelling-machines": (
        "https://unsplash.com/photos/CxGLY283rWs/download?force=true&w=1200",
        "sub",
    ),
    "orbital-welding-machines": (
        "https://unsplash.com/photos/tD-SDlQxfsY/download?force=true&w=1200",
        "sub",
    ),
    "i-d-mount-pipe-bevelers": (
        "https://unsplash.com/photos/Qfvov6bWRSg/download?force=true&w=1200",
        "sub",
    ),
    "o-d-mount-pipe-beveling-machines": (
        "https://unsplash.com/photos/fBCQz7OUUww/download?force=true&w=1200",
        "sub",
    ),
    "pipe-cold-cutting-range-2-48": (
        "https://unsplash.com/photos/fZEC4pR4Kpo/download?force=true&w=1200",
        "sub",
    ),
    "clamshell-pipe-cold-cutter-type-dlw-hd-48-57": (
        "https://unsplash.com/photos/QC1oHW5JVu4/download?force=true&w=1200",
        "sub",
    ),
}


def output_path(slug: str, tier: str) -> Path:
    if tier == "top":
        return REPO / f"public/images/categories/{slug}.jpg"
    return REPO / f"public/images/categories/subcategories/{slug}.jpg"


def download(url: str, dest: Path) -> bool:
    rel = dest.relative_to(REPO)
    cmd = [
        sys.executable,
        str(DOWNLOAD),
        "--url",
        url,
        "--output",
        str(rel),
        "--force",
    ]
    result = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"FAIL {rel}: {result.stderr.strip()}", file=sys.stderr)
        return False
    print(result.stdout.strip())
    return True


def main() -> int:
    failed = 0
    for slug, (url, tier) in IMAGES.items():
        if not download(url, output_path(slug, tier)):
            failed += 1
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())

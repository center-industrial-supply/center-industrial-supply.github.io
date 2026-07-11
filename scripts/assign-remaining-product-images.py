#!/usr/bin/env python3
"""Assign images for remaining brand products and migrate wp-content paths."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PRODUCTS_DIR = ROOT / "src/content/products"
PUBLIC_DIR = ROOT / "public"
DOWNLOAD_SCRIPT = ROOT / ".cursor/skills/retrieve-product-image/scripts/download-product-image.py"

# slug -> (source URL or local wp path, brand override for filename)
ASSIGNMENTS: dict[str, tuple[str, str | None]] = {
    # wp-content migration (local copy)
    "arc400": ("/wp-content/uploads/2020/10/ARC-400.jpg", "Aotai"),
    "dura-arc-200ii": ("/wp-content/uploads/2020/10/DuraArc-200.jpg", "Aotai"),
    "dura-arc-250": ("/wp-content/uploads/2020/10/DuraArc-250II.jpg", "Aotai"),
    "protig-200-dc-hf": ("/wp-content/uploads/2023/02/GYS-PROTIG-200-DC-HF.jpg", "GYS"),
    "protig-201-ac-dc-hf-fv": ("/wp-content/uploads/2023/02/GYS-PROTIG-201-ACDC-FV.jpg", "GYS"),
    "tig200p": ("/wp-content/uploads/2020/10/TIG-200P.jpg", "Aotai"),
    "titanium-230-ac-dc-fv": ("/wp-content/uploads/2023/04/075924.jpg", "GYS"),
    # Aotai
    "aotai-mig350i": (
        "https://usimg.bjyyb.net/sites/62500/62761/1744010754767770510966824960.PNG",
        None,
    ),
    "arc400-3t": (
        "https://usimg.bjyyb.net/sites/62500/62761/20220517162623318.PNG",
        None,
    ),
    "asaw-ii-630-1000-1250-1500": (
        "https://usimg.bjyyb.net/sites/62500/62761/1749100347789117810693103616.png",
        None,
    ),
    # Exact (official exacttools.com)
    "exact-cutbevel-170e": (
        "https://exacttools.com/wp-content/uploads/2025/12/s_30_accessories_Pro_Cut_Bevel_Package-scaled.png",
        "Exact",
    ),
    "exact-pipe-saw-p400": (
        "https://exacttools.com/wp-content/uploads/2024/12/P400E-1280x1280.png",
        "Exact",
    ),
    "exact-pipe-saw-type-170e": (
        "https://exacttools.com/wp-content/uploads/2025/12/Exact-Tools-PipeCut-Classic-170-1280x1280.png",
        "Exact",
    ),
    "exact-pipebevel-220e": (
        "https://exacttools.com/wp-content/uploads/2025/12/ExactTools-Pipe-Beveller-220E.png",
        "Exact",
    ),
    "exact-pipebevel-360e": (
        "https://exacttools.com/wp-content/uploads/2025/12/Exact-Tools_PipeBevel_360E-1280x1140.png",
        "Exact",
    ),
    "exact-pipe-saw-pro-series-280": (
        "https://exacttools.com/wp-content/uploads/2025/05/280-Pro-Light-2025_2-scaled-2_png.png",
        "Exact",
    ),
    "exact-pipe-saw-pro-series-360": (
        "https://exacttools.com/wp-content/uploads/2024/12/Pro-Series-360_2025_extracted-scaled-1_png.png",
        "Exact",
    ),
    "exact-pipe-saw-pro-series-460": (
        "https://exacttools.com/wp-content/uploads/2024/12/Pro-Series-460_2025_Extracted-scaled-1_png.png",
        "Exact",
    ),
    "exact-pipe-saw-v1000": (
        "https://exacttools.com/wp-content/uploads/2025/12/Exact-Tools-PipeCut-P1000-1280x1280.png",
        "Exact",
    ),
    "stainless-steel-pipe-cutter-exact-inox-220": (
        "https://exacttools.com/wp-content/uploads/2025/12/ExactTools-INOX-220-1280x1280.png",
        "Exact",
    ),
    "stainless-steel-pipe-cutter-exact-inox-360": (
        "https://exacttools.com/wp-content/uploads/2024/12/INOX-360-2.0-scaled.png",
        "Exact",
    ),
    # IKING
    "iking-rsr-series-cd-capacitor-discharge-stud-welding-machine": (
        "https://shopcdnpro.grainajz.com/category/31534/3008/ecf9b72615d49b48c2c2ced2f973bc28/SSR1600.jpg",
        None,
    ),
    "shear-stud-welder-st2500": (
        "https://www.shearstud.net/Uploads/images/products/2019-12-29/en-ST-2500-131305.jpg",
        None,
    ),
    "iking-shear-connector": (
        "https://www.shearstud.net/Uploads/products/2022-12-22/en-stud-welding-machine-drawn-arc-studs-stainless-steel.png",
        None,
    ),
    # MOSA (mosaenergia.com - authorized MOSA distributor)
    "magic-weld-200-2": (
        "https://www.mosaenergia.com/assets/productos/mosa/01_motosoldadoras/01_gasolina/magic-weld-200/MAGIC-WELD-200.png",
        None,
    ),
    "new-magic-weld": (
        "https://www.mosaenergia.com/assets/productos/mosa/01_motosoldadoras/01_gasolina/magic-weld-150/MAGIC-WELD-150.png",
        None,
    ),
    # Shindaiwa (Leeden - authorized distributor)
    "dgw300m-my": (
        "https://leeden.com.my/wp-content/uploads/leeden-shindaiwa-engine-driven-dgw-300-my-2.jpg",
        None,
    ),
    "dgw400dmk-s2v": (
        "https://leeden.com.my/wp-content/uploads/leeden-shindaiwa-diesel-welder-dgw400dm-eura.jpg",
        None,
    ),
    # Kjellberg
    "automated-plasma-cutting-power-sources": (
        "https://www.kjellbergcutting.com/files/01_inhalte/image/product/automated-plasma-cutting/Kjellberg-Smart-Focus-130-vre.jpg",
        "KJELLBERG",
    ),
    # Taiwan Plasma
    "pla-cut-50p": (
        "https://taiwan-plasma.com/wp-content/uploads/2016/10/placut-50p.jpg",
        None,
    ),
    "pla-cut-80p": (
        "https://www.plasma.com.tw/upload-files/product/1.plasma-cutting-machine/1.mechanical-type/9/120a-air-1.jpg",
        None,
    ),
    "pla-cut-100p": (
        "https://taiwan-plasma.com/wp-content/uploads/2016/10/placut-100p.jpg",
        None,
    ),
    "pla-cut-101d": (
        "https://web.archive.org/web/20231208000000/https://centerindustrial.com/wp-content/uploads/2020/10/Placut-101D.jpg",
        None,
    ),
    # Hgstar
    "hg-star-smart-3015-cnc-laser": (
        "https://img.hgstarlaser.com/photo/ps211699843-3015_fiber_laser_cutting_machine_1000w_6000w_metal_sheet_cutter.jpg",
        None,
    ),
    # Hyundai
    "hyundai-flux-cored-wire-1-2mm-15kg": (
        "https://www.hyundaiwelding.com/data/file/consumables/image/05_FCAW.jpg",
        None,
    ),
    # ironcat (PIP/Ironcat official product photography via distributor)
    "ironcat-premium-split-cowhide-leather-welding-gloves": (
        "https://cdn11.bigcommerce.com/s-8715e/images/stencil/1280x1280/products/361224/676747/945-2500x2500__59936.1701887659.jpg?c=2",
        "ironcat",
    ),
    "ironcat-tig-goatskin-welding-gloves": (
        "https://cdn11.bigcommerce.com/s-gdy1ehz/products/368144/images/549509/16c1899a2d100702bd1d0f50f50300183b05a64e-large__68105.1747229480.386.513.png?c=2",
        "ironcat",
    ),
    # Misc brands
    "generico-190cr-co2-gas-regulator": (
        "https://weldmart.com.my/wp-content/uploads/2024/10/190-series.png",
        None,
    ),
    "dayok-ok-iv300d": (
        "https://web.archive.org/web/20231208030120/https://i0.wp.com/centerindustrial.com/wp-content/uploads/2023/06/Dayok-OK-IV300D-MMA-Welding-Machine.jpg?ssl=1",
        None,
    ),
    "new-fire-fire-blanket": (
        "https://web.archive.org/web/20231208015705/https://i0.wp.com/centerindustrial.com/wp-content/uploads/2023/06/Newfire-Fire-Blanket.png?ssl=1",
        "newfire",
    ),
    "permanent-6013-2-5-electrodes": (
        "https://img1.ecerimg.com/d9/51/8d4738b41322/product/31569594_s-w400xh400.jpg",
        "Permanent",
    ),
    "tbi-411-expert": (
        "https://www.tbi-industries.com/images/products/TBi-411-Expert.jpg",
        None,
    ),
    "weldmax-co2-gas-shielded-welding-wire-1mm-15kg": (
        "https://www.hyundaiwelding.com/data/file/consumables/image/05_FCAW.jpg",
        "weldmax",
    ),
}


def parse_product(path: Path) -> dict[str, str]:
    text = path.read_text(encoding="utf-8")
    fields: dict[str, str] = {}
    for key in ("title", "slug", "brand"):
        m = re.search(rf"^{key}:\s*[\"']?(.+?)[\"']?\s*$", text, re.M)
        if m:
            fields[key] = m.group(1)
    return fields


def make_filename(brand: str, title: str, ext: str) -> str:
    brand_part = re.sub(r"[^a-zA-Z0-9]+", "-", brand).strip("-")
    title_part = re.sub(r"[^a-zA-Z0-9]+", "-", title).strip("-")
    parts = [p for p in [brand_part, title_part] if p]
    return f"{'-'.join(parts) if parts else 'Product'}{ext}"


def update_frontmatter(path: Path, image_path: str) -> None:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return
    end_idx = next(i for i in range(1, len(lines)) if lines[i].strip() == "---")
    frontmatter = lines[1:end_idx]
    body = lines[end_idx:]

    new_fm: list[str] = []
    skip = False
    for line in frontmatter:
        if line.startswith("images:"):
            skip = True
            continue
        if skip and line.startswith("- "):
            continue
        skip = False
        new_fm.append(line)

    insert_idx = len(new_fm)
    for idx, line in enumerate(new_fm):
        if line.startswith("category:"):
            insert_idx = idx + 1
            break
    for idx, line in enumerate(new_fm):
        if line.startswith("brand:") and insert_idx == len(new_fm):
            insert_idx = idx + 1

    new_fm.insert(insert_idx, "images:\n")
    new_fm.insert(insert_idx + 1, f'  - "{image_path}"\n')
    path.write_text("".join(["---\n", *new_fm, *body]), encoding="utf-8")


def download_url(url: str, output: Path) -> bool:
    rel = output.relative_to(ROOT)
    result = subprocess.run(
        [
            sys.executable,
            str(DOWNLOAD_SCRIPT),
            "--url",
            url,
            "--output",
            str(rel),
            "--min-width",
            "350",
            "--min-height",
            "300",
        ],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        print(result.stderr.strip() or result.stdout.strip(), file=sys.stderr)
        return False
    return True


def copy_local(src_rel: str, output: Path) -> bool:
    src = PUBLIC_DIR / src_rel.lstrip("/")
    if not src.is_file():
        return False
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, output)
    return True


def main() -> int:
    ok = 0
    fail = 0
    skipped = 0

    for slug, (source, brand_override) in sorted(ASSIGNMENTS.items()):
        path = PRODUCTS_DIR / f"{slug}.md"
        if not path.is_file():
            print(f"MISSING FILE {slug}")
            fail += 1
            continue

        product = parse_product(path)
        title = product.get("title", slug)
        brand = brand_override or product.get("brand", "Product")

        ext = Path(source.split("?")[0]).suffix.lower()
        if ext not in {".jpg", ".jpeg", ".png", ".webp"}:
            ext = ".jpg"
        filename = make_filename(brand, title, ext)
        output = PUBLIC_DIR / "images" / "products" / slug / filename
        site_path = f"/images/products/{slug}/{filename}"

        if output.exists():
            update_frontmatter(path, site_path)
            print(f"EXISTS {slug}: {site_path}")
            skipped += 1
            continue

        if source.startswith("/"):
            if not copy_local(source, output):
                print(f"FAIL {slug}: local missing {source}")
                fail += 1
                continue
        else:
            if not download_url(source, output):
                print(f"FAIL {slug}: download {source}")
                fail += 1
                continue

        update_frontmatter(path, site_path)
        print(f"OK {slug}: {site_path}")
        ok += 1

    print(f"\nSummary: {ok} assigned, {skipped} already existed, {fail} failed, {len(ASSIGNMENTS)} total")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())

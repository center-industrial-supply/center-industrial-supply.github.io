#!/usr/bin/env python3
"""Download and validate a product image for the Center Industrial website."""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from urllib.parse import urlparse


def _require_pillow():
    try:
        from PIL import Image  # noqa: PLC0415
    except ImportError:
        print(
            "Pillow is required for image validation. Install with: pip install Pillow",
            file=sys.stderr,
        )
        sys.exit(1)
    return Image


USER_AGENT = (
    "Mozilla/5.0 (compatible; CenterIndustrialBot/1.0; +https://center-industrial-supply.github.io)"
)


def download_url(url: str, dest: Path, dry_run: bool) -> None:
    if dry_run:
        return

    dest.parent.mkdir(parents=True, exist_ok=True)

    if shutil.which("curl"):
        cmd = [
            "curl",
            "-fsSL",
            "-A",
            USER_AGENT,
            "-o",
            str(dest),
            url,
        ]
    elif shutil.which("wget"):
        cmd = ["wget", "-q", "--user-agent", USER_AGENT, "-O", str(dest), url]
    else:
        raise RuntimeError("Neither curl nor wget is available")

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"Download failed: {result.stderr.strip() or result.stdout.strip()}")

    # Reject HTML error pages saved with an image extension.
    try:
        header = dest.read_bytes()[:512].lstrip().lower()
    except OSError as exc:
        raise RuntimeError(f"Could not read downloaded file: {exc}") from exc

    if header.startswith(b"<!doctype html") or header.startswith(b"<html"):
        dest.unlink(missing_ok=True)
        raise RuntimeError("URL returned HTML, not an image — check the image URL")


def validate_image(
    path: Path,
    *,
    min_width: int,
    min_height: int,
    min_bytes: int,
) -> tuple[int, int, str]:
    Image = _require_pillow()

    size = path.stat().st_size
    if size < min_bytes:
        raise ValueError(f"File too small ({size} bytes); likely not a valid image")

    with Image.open(path) as img:
        width, height = img.size
        fmt = img.format or "unknown"

    if width < min_width or height < min_height:
        raise ValueError(
            f"Image too small ({width}x{height}); minimum is {min_width}x{min_height}"
        )

    return width, height, fmt


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Download a product image and validate dimensions for Center Industrial."
    )
    parser.add_argument("--url", required=True, help="Image URL to download")
    parser.add_argument(
        "--output",
        required=True,
        help="Destination path relative to repo root (e.g. public/images/products/2026/07/ESAB-Buddy-Arc-145.jpg)",
    )
    parser.add_argument("--min-width", type=int, default=400, help="Minimum image width (default: 400)")
    parser.add_argument("--min-height", type=int, default=400, help="Minimum image height (default: 400)")
    parser.add_argument("--min-bytes", type=int, default=10_000, help="Minimum file size in bytes (default: 10000)")
    parser.add_argument("--dry-run", action="store_true", help="Validate without writing output file")
    args = parser.parse_args()

    parsed = urlparse(args.url)
    if parsed.scheme not in {"http", "https"}:
        print(f"Invalid URL scheme: {args.url}", file=sys.stderr)
        return 1

    repo_root = Path(__file__).resolve().parents[4]
    output = repo_root / args.output

    if output.exists() and not args.dry_run:
        print(f"Output already exists: {output}", file=sys.stderr)
        return 1

    try:
        if args.dry_run:
            with tempfile.TemporaryDirectory() as tmp:
                tmp_path = Path(tmp) / "probe"
                download_url(args.url, tmp_path, dry_run=False)
                width, height, fmt = validate_image(
                    tmp_path,
                    min_width=args.min_width,
                    min_height=args.min_height,
                    min_bytes=args.min_bytes,
                )
                print(f"Dry run OK: {width}x{height} {fmt} from {args.url}")
        else:
            download_url(args.url, output, dry_run=False)
            width, height, fmt = validate_image(
                output,
                min_width=args.min_width,
                min_height=args.min_height,
                min_bytes=args.min_bytes,
            )
            site_path = "/" + args.output.removeprefix("public/")
            print(f"Saved: {output}")
            print(f"Dimensions: {width}x{height} ({fmt})")
            print(f"Site path: {site_path}")
    except (RuntimeError, ValueError, OSError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        if output.exists():
            output.unlink()
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())

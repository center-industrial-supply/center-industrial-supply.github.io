#!/usr/bin/env bash
# Fail CI if image files are still Git LFS pointer text (checkout without lfs: true).
set -euo pipefail

fail=0

check_glob() {
  local pattern="$1"
  local label="$2"
  shopt -s nullglob
  local files=($pattern)
  shopt -u nullglob

  if [ ${#files[@]} -eq 0 ]; then
    return 0
  fi

  for f in "${files[@]}"; do
    if head -1 "$f" | grep -qE 'git-lfs\.github\.com/spec'; then
      echo "LFS pointer detected (checkout with lfs: true): $f"
      fail=1
    fi
  done
}

check_glob "public/images/categories/*.jpg" "category images"
check_glob "public/images/categories/subcategories/*.jpg" "subcategory images"
check_glob "public/images/products/**/*.{jpg,jpeg,png}" "product images"

if [ "$fail" -ne 0 ]; then
  echo "One or more image files are Git LFS pointers, not binary image data."
  echo "Ensure actions/checkout uses 'lfs: true' and Git LFS is installed in CI."
  exit 1
fi

echo "No LFS pointers detected in critical image paths."

#!/usr/bin/env bash
# Fail if image files are Git LFS pointer stubs instead of real binaries.
# Run after checkout in CI (with lfs: true) to catch misconfigured workflows.

set -euo pipefail

is_lfs_pointer() {
  local file="$1"
  [[ -f "$file" ]] || return 1
  head -1 "$file" | grep -q 'git-lfs.github.com/spec/v1'
}

failed=0

check_glob() {
  local pattern="$1"
  local label="$2"
  shopt -s nullglob
  local files=($pattern)
  shopt -u nullglob

  if ((${#files[@]} == 0)); then
    echo "Warning: no files matched $pattern"
    return
  fi

  for file in "${files[@]}"; do
    if is_lfs_pointer "$file"; then
      echo "LFS pointer detected ($label): $file"
      echo "  Checkout must use actions/checkout with lfs: true, or run git lfs pull locally."
      failed=1
    fi
  done
}

check_glob "public/images/categories/*.jpg" "category image"
check_glob "public/images/categories/*.png" "category image"

if ((failed)); then
  exit 1
fi

echo "OK: category images are real files, not LFS pointers."

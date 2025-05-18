#!/usr/bin/env bash
set -euo pipefail

# Remove references to apt.llvm.org from APT sources

echo "Cleaning apt.llvm.org entries from APT sources..."

sudo sed -i '/apt\.llvm\.org/d' /etc/apt/sources.list || true

if [ -d /etc/apt/sources.list.d ]; then
  while IFS= read -r -d '' file; do
    sudo sed -i '/apt\.llvm\.org/d' "$file" || true
  done < <(find /etc/apt/sources.list.d -type f -print0)
fi


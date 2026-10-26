#!/usr/bin/env bash
# Usage: scripts/check_pages.sh build/main.pdf
# Prints total page count and the first page containing the References heading.
# WWW long paper: body <= 8 pages (self-contained); body+refs+appendix <= 12.
set -euo pipefail
pdf="${1:-build/main.pdf}"
[ -f "$pdf" ] || { echo "no PDF at $pdf (run make first)"; exit 1; }

total=$(pdfinfo "$pdf" | awk '/^Pages:/ {print $2}')
refpage=""
for ((p=1; p<=total; p++)); do
  if pdftotext -f "$p" -l "$p" "$pdf" - 2>/dev/null | grep -qiE '^\s*References\s*$'; then
    refpage=$p; break
  fi
done

echo "Total pages          : $total   (limit 12)"
if [ -n "$refpage" ]; then
  echo "References start on  : page $refpage  (body must end by page 8)"
  if [ "$refpage" -gt 9 ]; then echo "WARNING: body exceeds 8 pages"; fi
else
  echo "References heading not found (bibliography empty?)"
fi
if [ "$total" -gt 12 ]; then echo "WARNING: total exceeds 12 pages"; fi

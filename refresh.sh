#!/usr/bin/env bash
# Rebuild the shelf and publish it. Runs from a systemd timer.
set -euo pipefail
cd "$(dirname "$0")"

python3 catalog.py

git add catalog.json
[ -f channels-auto.json ] && git add channels-auto.json
git diff --cached --quiet && { echo "no change"; exit 0; }

counts=$(python3 -c "import json;c=json.load(open('catalog.json'))['counts'];print(f\"{c['series']} stories, {c['full']} complete, {c['hours']}h\")")
git commit -q -m "catalog: $(date -u +%F) — $counts"
git push -q origin main
echo "published: $counts"

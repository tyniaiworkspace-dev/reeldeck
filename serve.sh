#!/usr/bin/env bash
# ReelDeck static server — phones on the home Wi-Fi open http://<this-box-ip>:8788
set -euo pipefail
cd "$(dirname "$0")"
exec python3 -m http.server 8788 --bind 0.0.0.0

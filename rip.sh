#!/usr/bin/env bash
# ReelDeck ripper — save the full video as a file that never asks for an account.
#
#   ./rip.sh <link-or-id> [more links...]
#   ./rip.sh -f links.txt          # one link per line
#   ./rip.sh --low <link>          # 360p, ~240 MB instead of ~1 GB
#   ./rip.sh --out /path <link>    # default ~/Videos/reeldeck
#
# Full episodes download whole: yt-dlp reads the duration from the source,
# so a 72-minute post arrives as a 72-minute file, not a clip.

set -uo pipefail

OUT="$HOME/Videos/reeldeck"
QUALITY="hls-720/hls-380/best"
LINKS=()
FILE=""

while [ $# -gt 0 ]; do
  case "$1" in
    -f|--file) FILE="$2"; shift 2 ;;
    --low) QUALITY="hls-380/best"; shift ;;
    --out) OUT="$2"; shift 2 ;;
    -h|--help) sed -n '2,14p' "$0"; exit 0 ;;
    *) LINKS+=("$1"); shift ;;
  esac
done

command -v yt-dlp >/dev/null || { echo "yt-dlp is not installed" >&2; exit 1; }
mkdir -p "$OUT"

if [ -n "$FILE" ]; then
  [ -r "$FILE" ] || { echo "cannot read $FILE" >&2; exit 1; }
  while IFS= read -r line; do
    line="$(printf '%s' "$line" | tr -d '\r' | sed 's/^[[:space:]]*//; s/[[:space:]]*$//')"
    [ -z "$line" ] && continue
    case "$line" in \#*) continue ;; esac
    LINKS+=("$line")
  done < "$FILE"
fi

[ ${#LINKS[@]} -eq 0 ] && { echo "usage: $0 <link-or-id> [more...]  (or -f links.txt)" >&2; exit 1; }

ok=0; bad=0
for raw in "${LINKS[@]}"; do
  # bare Dailymotion id (x + 6-8 chars) is common when copying from the app
  if printf '%s' "$raw" | grep -qE '^x[0-9a-z]{6,8}$'; then
    url="https://www.dailymotion.com/video/$raw"
  else
    url="$raw"
  fi

  echo "== $url"
  before=$(ls -1 "$OUT" | wc -l)
  yt-dlp --no-update -N 16 \
    -f "$QUALITY" \
    --merge-output-format mp4 \
    --write-info-json \
    --no-overwrites \
    -o "$OUT/%(title).90B [%(id)s].%(ext)s" \
    "$url"
  rc=$?
  after=$(ls -1 "$OUT" | wc -l)

  if [ $rc -eq 0 ]; then
    ok=$((ok+1))
  elif [ $rc -eq 101 ] || [ "$before" = "$after" ]; then
    echo "   skipped (already saved)"
    ok=$((ok+1))
  else
    echo "   FAILED  ($url)" >&2
    bad=$((bad+1))
  fi
done

echo
echo "saved to: $OUT"
ls -lh "$OUT" | grep -v '\.json$\|\.part$\|\.ytdl$' | tail -20
[ $bad -gt 0 ] && exit 2
exit 0

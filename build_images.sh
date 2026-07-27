#!/usr/bin/env bash
# Build the 22 mock-server images. Tags must match IMAGE= in capabilities/*.py,
# i.e. vibe-agent-benchmark/<name>:latest
#
# Usage: ./build_images.sh          build all
#        ./build_images.sh weather  build only names containing "weather"
set -euo pipefail
cd "$(dirname "$0")"
filter="${1:-}"
built=0; failed=0
for s in servers/*/; do
  name=$(basename "$s")
  [ -n "$filter" ] && [[ "$name" != *"$filter"* ]] && continue
  [ -f "$s/Dockerfile" ] || { echo "skipped (no Dockerfile): $name"; continue; }
  echo ">>> building vibe-agent-benchmark/${name}:latest"
  if docker build -t "vibe-agent-benchmark/${name}:latest" "$s" >/dev/null 2>&1; then
    built=$((built+1)); echo "    ok   $name"
  else
    failed=$((failed+1))
    echo "    FAIL $name — rerun without the redirect to see the error:"
    echo "         docker build -t vibe-agent-benchmark/${name}:latest $s"
  fi
done
echo ""
echo "done: $built built, $failed failed"
echo ""
echo "The agent workspace image is not built here — Terrarium pulls it on first run"
echo "(OpenClaw 2026.7.1). Nothing to do unless you are pinning your own."

#!/usr/bin/env bash
# One-click runner for the Harbor-format subset under harbor/.
#
# Usage:
#   scripts/run_harbor.sh                                  # all 10 domains
#   scripts/run_harbor.sh --domain career                  # one domain
#   scripts/run_harbor.sh --domain career --include '*espp*'
#   scripts/run_harbor.sh --model anthropic/claude-opus-4-8 --agent claude-code
#   scripts/run_harbor.sh --env-file .env --attempts 3
#
# Each task builds its own docker compose stack of mock services, replays its
# stage timeline with the chosen agent, and is scored by tests/run_verifier.py.
# Trial outputs (trajectory, reward.json, checks.json) land under --jobs-dir
# (default: jobs-harbor/).
set -euo pipefail
cd "$(dirname "$0")/.."

DOMAIN="" INCLUDE="" MODEL="" AGENT="claude-code" ENV_FILE=""
ATTEMPTS=1 CONCURRENCY=4 JOBS_DIR="jobs-harbor"

usage() { grep '^#' "$0" | sed 's/^# \{0,1\}//'; exit 1; }

while [[ $# -gt 0 ]]; do
  case "$1" in
    --domain)      DOMAIN="$2"; shift 2 ;;
    --include)     INCLUDE="$2"; shift 2 ;;
    --model)       MODEL="$2"; shift 2 ;;
    --agent)       AGENT="$2"; shift 2 ;;
    --env-file)    ENV_FILE="$2"; shift 2 ;;
    --attempts)    ATTEMPTS="$2"; shift 2 ;;
    --concurrency) CONCURRENCY="$2"; shift 2 ;;
    --jobs-dir)    JOBS_DIR="$2"; shift 2 ;;
    -h|--help)     usage ;;
    *) echo "unknown option: $1" >&2; usage ;;
  esac
done

command -v docker >/dev/null || {
  echo "error: docker is required (each task builds its own compose stack)"; exit 1; }
command -v harbor >/dev/null || {
  echo "error: Harbor CLI is required — install with: uv tool install harbor"; exit 1; }

domains=()
if [[ -n "$DOMAIN" ]]; then
  [[ -d "harbor/$DOMAIN" ]] || { echo "error: no such domain dir: harbor/$DOMAIN"; exit 1; }
  domains=("$DOMAIN")
else
  while IFS= read -r d; do domains+=("$d"); done \
    < <(find harbor -mindepth 1 -maxdepth 1 -type d -printf '%f\n' | LC_ALL=C sort)
fi

echo "domains: ${domains[*]}"
echo "agent: $AGENT  model: ${MODEL:-<agent default>}  attempts: $ATTEMPTS  concurrency: $CONCURRENCY"

for d in "${domains[@]}"; do
  echo ""
  echo ">>> harbor run --path harbor/$d"
  args=( run --path "harbor/$d" --agent "$AGENT" --n-attempts "$ATTEMPTS"
         --n-concurrent "$CONCURRENCY" --jobs-dir "$JOBS_DIR" --yes )
  [[ -n "$MODEL"    ]] && args+=( --model "$MODEL" )
  [[ -n "$INCLUDE"  ]] && args+=( --include-task-name "$INCLUDE" )
  [[ -n "$ENV_FILE" ]] && args+=( --env-file "$ENV_FILE" )
  harbor "${args[@]}"
done

echo ""
echo "done — per-trial reward.json / checks.json under $JOBS_DIR/"

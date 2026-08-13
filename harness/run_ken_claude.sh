#!/bin/bash
# Runs all 20 T-KEN tasks against Sonnet-5 via Claude Code CLI.
# Usage: bash run_ken_claude.sh <model-alias> <output-suffix>
# e.g.:  bash run_ken_claude.sh sonnet sonnet5
set -e
MODEL="${1:-sonnet}"
SUFFIX="${2:-sonnet5}"
cd /root/ken-tasks
export IS_SANDBOX=1

mkdir -p "results-$SUFFIX"
rm -f "results-$SUFFIX/failures.txt"

python3 -c "
import json
prompts = json.load(open('prompts.json'))
for k in sorted(prompts.keys()):
    print(k)
" > task_order.txt

while read -r tid <&3; do
  echo "=== RUNNING $tid ($SUFFIX) ==="
  prompt=$(python3 -c "import json; print(json.load(open('prompts.json'))['$tid'])")
  cd "/root/ken-tasks/$tid"
  CTX=$(cat CONTEXT_ONLY.md)
  FULL_PROMPT="$prompt

(orientation, not instructions: $CTX)

IMPORTANT: your current working directory contains everything you need for this task. Do not attempt to explore, list, or read anything outside it (no parent directories, no sibling task folders, no real host tooling/binaries) -- that access is intentionally sandboxed and denied, and doing so will end your turn without an answer. Answer using only what's in this directory."
  timeout 180 claude -p "$FULL_PROMPT" --model "$MODEL" --dangerously-skip-permissions --output-format json < /dev/null > "/root/ken-tasks/results-$SUFFIX/${tid}-${SUFFIX}.json" 2>&1 || echo "FAILED: $tid" >> "/root/ken-tasks/results-$SUFFIX/failures.txt"
  cd /root/ken-tasks
done 3< task_order.txt

echo "ALL DONE ($SUFFIX)"

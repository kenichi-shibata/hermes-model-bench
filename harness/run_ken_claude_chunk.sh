#!/bin/bash
# Re-runs tasks listed in a given chunk file against Claude Code CLI (Sonnet-5).
# Usage: bash run_ken_claude_chunk.sh <model-alias> <output-suffix> <chunk-file>
set -e
MODEL="$1"
SUFFIX="$2"
CHUNK="$3"
cd /root/ken-tasks

mkdir -p "results-$SUFFIX"

while read -r tid <&3; do
  echo "=== RUN $tid ($SUFFIX) ==="
  prompt=$(python3 -c "import json; print(json.load(open('prompts.json'))['$tid'])")
  cd "/root/ken-tasks/$tid"
  CTX=$(cat CONTEXT_ONLY.md)
  IS_SANDBOX=1 timeout 180 claude -p "CONTEXT: $CTX

TASK: $prompt

Note: your working directory IS the sandbox boundary -- do not attempt to read/list parent or sibling directories; everything you need is here." --model "$MODEL" --dangerously-skip-permissions --output-format json > "/root/ken-tasks/results-$SUFFIX/${tid}.json" 2>&1 || echo "FAILED: $tid" >> "/root/ken-tasks/results-$SUFFIX/failures.txt"
  cd /root/ken-tasks
done 3< "$CHUNK"

echo "CHUNK DONE ($SUFFIX) $CHUNK"

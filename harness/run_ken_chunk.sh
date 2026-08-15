#!/bin/bash
# Re-runs tasks listed in a given chunk file against a model.
# Usage: bash run_ken_chunk.sh <model-slug> <output-suffix> <chunk-file>
set -e
MODEL="$1"
SUFFIX="$2"
CHUNK="$3"
cd /root/ken-tasks
set -a; source /root/.bench.env; set +a

mkdir -p "results-$SUFFIX"

while read -r tid <&3; do
  echo "=== RETRY $tid ($SUFFIX) ==="
  prompt=$(python3 -c "import json; print(json.load(open('prompts.json'))['$tid'])")
  cd "/root/ken-tasks/$tid"
  CTX=$(cat CONTEXT_ONLY.md)
  timeout 180 opencode run "CONTEXT: $CTX

TASK: $prompt

Note: your working directory IS the sandbox boundary -- do not attempt to read/list parent or sibling directories; everything you need is here." --model "$MODEL" > "/root/ken-tasks/results-$SUFFIX/${tid}-${SUFFIX}.txt" 2>&1 || echo "FAILED: $tid" >> "/root/ken-tasks/results-$SUFFIX/failures.txt"
  cd /root/ken-tasks
done 3< "$CHUNK"

echo "CHUNK DONE ($SUFFIX) $CHUNK"

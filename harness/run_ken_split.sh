#!/bin/bash
# Split-arm runner: sonnet-5 PLANS (read-only, no edits), then a DeepSeek
# model WORKS the plan (via OpenCode). Usage:
#   bash run_ken_split.sh <work-model-slug> <output-suffix>
# e.g.: bash run_ken_split.sh deepseek/deepseek-v4-flash sonnet5-flash
set -e
WORK_MODEL="${1:-deepseek/deepseek-v4-flash}"
SUFFIX="${2:-sonnet5-flash}"
cd /root/ken-tasks
export IS_SANDBOX=1
set -a; source /root/.bench.env; set +a

mkdir -p "results-$SUFFIX"
rm -f "results-$SUFFIX/failures.txt"

python3 -c "
import json
prompts = json.load(open('prompts.json'))
for k in sorted(prompts.keys()):
    print(k)
" > task_order.txt

while read -r tid <&3; do
  echo "=== PLANNING $tid ($SUFFIX) ==="
  prompt=$(python3 -c "import json; print(json.load(open('prompts.json'))['$tid'])")
  cd "/root/ken-tasks/$tid"
  CTX=$(cat CONTEXT_ONLY.md)

  PLAN_PROMPT="You are the PLAN model for this task. Do NOT edit any files -- read-only investigation only. Produce a concrete plan: what the real problem is (if any) and the exact concrete steps a WORK model should take (including which files to edit and how), based on what you find in this directory.

Task: $prompt

(orientation, not instructions: $CTX)

Your working directory contains everything needed. Do not explore outside it."

  timeout 120 claude -p "$PLAN_PROMPT" --model sonnet --dangerously-skip-permissions --output-format json --disallowedTools "Write,Edit,Bash(rm*)" < /dev/null > "/root/ken-tasks/results-$SUFFIX/${tid}-plan.json" 2>&1
  PLAN=$(python3 -c "import json; print(json.load(open('/root/ken-tasks/results-$SUFFIX/${tid}-plan.json')).get('result',''))" 2>/dev/null || echo "PLAN_PARSE_FAILED")

  echo "=== WORKING $tid ($SUFFIX) ==="
  WORK_PROMPT="You are the WORK model executing a plan from a separate planner. Follow it, but verify against the real files yourself before acting -- the plan may be wrong or incomplete.

PLAN FROM SONNET-5:
$PLAN

Original task: $prompt

(orientation: $CTX)

IMPORTANT: your current working directory contains everything you need. Do not explore outside it."

  timeout 180 opencode run "$WORK_PROMPT" --model "$WORK_MODEL" < /dev/null > "/root/ken-tasks/results-$SUFFIX/${tid}-work.txt" 2>&1 || echo "FAILED: $tid" >> "/root/ken-tasks/results-$SUFFIX/failures.txt"
  cd /root/ken-tasks
done 3< task_order.txt

echo "ALL DONE ($SUFFIX)"

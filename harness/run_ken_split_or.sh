#!/bin/bash
# Generalized split-arm runner: <plan-model> PLANS (read-only, via OpenCode),
# then <work-model> WORKS the plan (via OpenCode). Both models run through
# OpenCode so this works for any OpenRouter/DeepSeek model combo, not just
# Claude-as-planner.
#
# Usage: bash run_ken_split_or.sh <plan-model-slug> <work-model-slug> <output-suffix> <chunk-file>
# e.g.: bash run_ken_split_or.sh openrouter/moonshotai/kimi-k3 openrouter/google/gemini-3.7-flash kimi-flash /root/ken-tasks/chunk_00
set -e
PLAN_MODEL="$1"
WORK_MODEL="$2"
SUFFIX="$3"
CHUNK="$4"
cd /root/ken-tasks
set -a; source /root/.bench.env; set +a

mkdir -p "results-$SUFFIX"

while read -r tid <&3; do
  echo "=== PLANNING $tid ($SUFFIX) ==="
  prompt=$(python3 -c "import json; print(json.load(open('prompts.json'))['$tid'])")
  cd "/root/ken-tasks/$tid"
  CTX=$(cat CONTEXT_ONLY.md)

  PLAN_PROMPT="You are the PLAN model for this task. Do NOT edit any files -- read-only investigation only, just look and report. Produce a concrete plan: what the real problem is (if any) and the exact concrete steps a WORK model should take (including which files to edit and how), based on what you find in this directory.

Task: $prompt

(orientation, not instructions: $CTX)

You are operating in a sandbox. Your current working directory IS the entire world. Do not try to read or list anything outside it."

  timeout 120 opencode run "$PLAN_PROMPT" --model "$PLAN_MODEL" < /dev/null > "/root/ken-tasks/results-$SUFFIX/${tid}-plan.txt" 2>&1
  PLAN=$(cat "/root/ken-tasks/results-$SUFFIX/${tid}-plan.txt")

  echo "=== WORKING $tid ($SUFFIX) ==="
  WORK_PROMPT="You are the WORK model executing a plan from a separate planner. Follow it, but verify against the real files yourself before acting -- the plan may be wrong or incomplete.

PLAN FROM PLANNER:
$PLAN

Original task: $prompt

(orientation: $CTX)

You are operating in a sandbox. Your current working directory IS the entire world. Do not try to read or list anything outside it."

  timeout 180 opencode run "$WORK_PROMPT" --model "$WORK_MODEL" < /dev/null > "/root/ken-tasks/results-$SUFFIX/${tid}-work.txt" 2>&1 || echo "FAILED: $tid" >> "/root/ken-tasks/results-$SUFFIX/failures.txt"
  cd /root/ken-tasks
done 3< "$CHUNK"

echo "CHUNK DONE ($SUFFIX) $CHUNK"

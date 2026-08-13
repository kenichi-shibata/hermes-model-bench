# Results directory

Each real benchmark run produces:

1. `YYYY-MM-DD-run.json` — flat list of per-task-run records, one object
   per (task × arm), matching the shape `scoring.py` consumes. This is
   the raw source of truth.
2. `YYYY-MM-DD-report.md` — human-readable report generated FROM the raw
   JSON (never hand-written numbers) covering:
   - Per-task table: task_id, arm, correctness, token_eff, cost_eff,
     reusability, composite, cost_usd, total_tokens
   - Per-arm aggregate table: same columns, averaged across all tasks
     that arm actually completed (tasks it failed to even attempt are
     shown as a separate "attempted N/M tasks" column, never silently
     dropped from the denominator)
   - Aggregate spider chart (`YYYY-MM-DD-spider-aggregate.png`) — all
     arms overlaid on one radar chart across the 4 dimensions
   - Per-task spider charts (`YYYY-MM-DD-spider-<task-id>.png`) for any
     task where the per-task breakdown tells a meaningfully different
     story than the aggregate (e.g. an arm that's cheap-but-wrong on one
     task type and strong on another)
3. Any raw transcripts/logs referenced by the report, or a pointer to
   where they're archived if too large for this repo.

## Generating a report from raw results

```bash
cd harness
../.venv/bin/python3 scoring.py <single-task-run.json>          # one task x one arm
../.venv/bin/python3 spider_chart.py ../results/YYYY-MM-DD-run.json \
    --out ../results/YYYY-MM-DD-spider-aggregate.png
../.venv/bin/python3 spider_chart.py ../results/YYYY-MM-DD-run.json \
    --task T-INFRA-001 --out ../results/YYYY-MM-DD-spider-T-INFRA-001.png
```

No results have been generated yet — this repo is still in the
scaffolding stage (see the root README's Status section).

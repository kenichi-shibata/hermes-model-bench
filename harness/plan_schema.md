# Plan → Work handoff schema (for split arms)

Used by arms 6, 7, 12, 13, 14 (any arm with a separate "plan model" and
"work model"). Mirrors this operator's real `plan-then-delegate` skill:
the plan model produces a structured breakdown, the work model executes
it with **no further planning authority** — it cannot re-scope, skip, or
reorder steps on its own judgment, only report back if a step is
genuinely blocked.

## Plan model output contract

The plan model must produce a JSON object matching this shape before any
work model call is made:

```json
{
  "task_id": "T-CATEGORY-NNN",
  "steps": [
    {
      "id": 1,
      "action": "Specific, unambiguous instruction for the work model",
      "verification": "How the work model itself should sanity-check this step before moving on (not the final scoring check - just self-check)",
      "depends_on": []
    }
  ],
  "risks_flagged": [
    "Anything the plan model identified as a likely failure mode for this specific task, e.g. 'this file is also touched by the fail-open pattern used elsewhere - do not copy that pattern for this check'"
  ]
}
```

## Work model constraints

- Receives ONLY the plan's `steps` + `risks_flagged` + the original task
  context/prompt — never the plan model's raw reasoning trace.
- Executes steps in dependency order.
- If a step's verification fails, the work model reports back rather than
  silently improvising a different approach — this it the harness's hook
  for measuring "did the split actually save cost, or did it just move
  the failure to a different report".
- The work model's own token usage is billed at the work model's price;
  the plan model's token usage is billed separately at the plan model's
  price. Both roll into the arm's total cost for that task.

## Why this matters for scoring

A split arm "wins" on cost efficiency only if:
1. The plan model is cheap enough (or the plan short enough) that its
   token cost doesn't erase the work model's savings, AND
2. The work model, constrained to the plan, doesn't need a second
   plan-model pass to fix its own mistakes (which would double-count the
   plan model's cost).

Both conditions are visible in the raw log, not the summary — the scorer
should check the actual message count/cost breakdown per model, not just
final task success.

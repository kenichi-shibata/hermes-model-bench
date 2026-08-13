# Hermes Model Bench

**A model/pipeline benchmark for real, daily-driver Hermes agent work.**

Not a synthetic coding-puzzle benchmark. Every task is a real thing this
operator's Hermes instance actually does — infra fixes, delegation batches,
trading-system risk-gate changes, doc audits, GitHub issue triage, live
verification against real systems. The point is: which model (or model
*combination*) gives the best correctness-per-dollar and least babysitting
for the actual job, not for a leaderboard puzzle.

Sibling agents (other Hermes instances) can and will add tasks and
rubric-scoring criteria to this repo. Structure is designed for that:
one task = one file, one rubric = one file, additive by default.

## Design principles (borrowed + adapted from `alzheimers-benchmark`)

1. **Same memory, same config, only the model differs.** Every arm runs
   against the identical Hermes profile (skills, memory, tool access,
   system prompt) — the model/provider swap is the only independent
   variable. A model that "wins" because it had better context isn't a
   real result.
2. **Real, verifiable tasks only.** Every task must have an objective,
   checkable success condition — a test suite that passes, a file that
   exists with specific content, a live endpoint that returns the right
   shape, a git commit that lands cleanly. No "write a nice summary" tasks
   with no ground truth to check against.
3. **Baseline arms are executed, never assumed.** Sonnet-5 (this
   instance) is the baseline arm, run for real on every task — not
   hand-waved as "obviously the reference."
4. **Every score carries a written justification** citing what was
   actually observed (test output, file diff, live check) — never a bare
   number.
5. **Report per-task AND aggregate.** A single leaderboard number without
   the per-task breakdown hides exactly the info that matters: which
   model is good at what.
6. **Cost is tracked as a first-class metric, not an afterthought.**
   Token count × real per-token price for that model/provider at run
   time — not a guess, not a flat multiplier.

## Arms (2026-08-13 pricing snapshot — see `docs/pricing.md` for sources/updates)

| # | Arm | Plan model | Work model | Notes |
|---|---|---|---|---|
| 1 | `sonnet-5` | — | Claude Sonnet 5 | **Baseline** (this instance) |
| 2 | `opus-5` | — | Claude Opus 5 | Priciest Anthropic tier |
| 3 | `haiku-4.5` | — | Claude Haiku 4.5 | Cheapest Anthropic tier ($1/$5 per MTok) |
| 4 | `deepseek-v4-pro` | — | DeepSeek V4 Pro | $0.435/$0.87 per MTok |
| 5 | `deepseek-v4-flash` | — | DeepSeek V4 Flash | $0.08–0.14/$0.25–0.28 per MTok, cheapest frontier-ish |
| 6 | `sonnet5-plans-flash-works` | Claude Sonnet 5 | DeepSeek V4 Flash | Split planner/executor |
| 7 | `deepseekpro-plans-flash-works` | DeepSeek V4 Pro | DeepSeek V4 Flash | All-DeepSeek split, cheapest possible planner tier |
| 8 | `gpt-5.6-terra` | — | GPT-5.6 Terra | OpenAI mid tier, $1/$6 per MTok |
| 9 | `grok-4.6` | — | Grok 4.6 | xAI current flagship-adjacent |
| 10 | `glm-5.2` | — | Z.ai GLM 5.2 | $0.50/$3.15 per MTok, strong on OpenRouter coding rankings |
| 11 | `gemini-3.6-flash` | — | Gemini 3.6 Flash | $1.50/$7.50 per MTok, Google's agentic/coding-tuned flash |
| 12 | `sonnet5-plans-deepseekpro-works` | Claude Sonnet 5 | DeepSeek V4 Pro | Higher-tier split, still ~5x cheaper work-tier than pure Sonnet |
| 13 | `opus5-plans-flash-works` | Claude Opus 5 | DeepSeek V4 Flash | Best-plan, cheapest-work extreme split |
| 14 | `haiku-plans-flash-works` | Claude Haiku 4.5 | DeepSeek V4 Flash | Cheapest possible full pipeline |

Arms 8–14 chosen from a live OpenRouter/provider pricing pull
(`docs/pricing.md`) to span: absolute cheapest, best coding-benchmark
rankings per dollar, and a couple of "known-good but not yet tried here"
options (Grok, Gemini, GLM). Open to swapping any of these — the point is
*coverage of the value curve*, not these exact 14 names being sacred.

All split arms (6, 7, 12, 13, 14) use the same plan→work handoff contract:
the plan model produces a structured task breakdown (see
`harness/plan_schema.md`), the work model executes it with no further
planning authority — mirrors this operator's actual `plan-then-delegate`
skill/workflow, so the benchmark measures a pattern already in daily use,
not a contrived split.

## Task categories

| Code | Category | What it measures |
|---|---|---|
| T-INFRA | Infra fix / diagnosis | Root-cause a real deployed-system bug from logs/state, ship a working fix |
| T-DELEG | Delegation orchestration | Plan + dispatch parallel subagents correctly, verify results independently rather than trust self-reports |
| T-RISK | Trading-system risk logic | Implement a real gated financial safety check correctly (fail-open vs fail-closed matters) |
| T-DOC | Documentation audit | Find real placeholder/gap code and write an accurate, non-fabricated issue/doc describing it |
| T-GH | GitHub workflow | Correct issue/PR/branch discipline — real commands, real repo state, no invented outcomes |
| T-VERIFY | Live verification | Independently confirm a claim against a real system (not just re-reading code) |

## Scoring rubric (per task, 0–10, see `rubrics/`)

| Score | Meaning |
|---|---|
| 10 | Fully correct, verified against ground truth, no unnecessary work |
| 7–9 | Correct outcome, minor inefficiency or missed edge case |
| 4–6 | Partially correct, or correct but required manual correction |
| 1–3 | Wrong outcome, or claimed success without verification |
| 0 | Task not attempted, crashed unrecoverably, or fabricated a result |

Four dimensions scored per task, each 0–10:

| Dimension | Weight | What it checks |
|---|---|---|
| **Correctness** | 2.0 | Did the verifiable success condition actually pass? |
| **Token efficiency** | 1.0 | Tokens used relative to the task's calibrated budget (not raw count — see `harness/scoring.py`) |
| **Cost efficiency** | 1.0 | Real $ cost at that model's live per-token price |
| **Reusability** | 1.0 | Would the artifact (code/doc/fix) need rework before another agent could build on it? Checked by an independent read, not self-report |

**Composite per arm** = Σ(task composite) / n_tasks, reported alongside
the full per-task breakdown table — never as a single number alone.

## Anti-gaming rules

- A model that refuses/times out on a task scores **0 on that task**, not
  N/A-excluded from the average — silently dropping failed tasks inflates
  every arm.
- Self-reported "tests pass" from a delegated subagent is **not**
  sufficient evidence — the scoring pass re-runs the real verification
  command itself (matches this operator's own standing "verify
  delegated-worker claims" rule).
- Cost is computed from the model's real published price at the time the
  task ran, not a fixed assumed rate — `docs/pricing.md` is a living
  document, re-check before each benchmark run since prices move monthly.

## Report deliverables (per real benchmark run)

- Per-task table (all 4 dimensions + composite + cost + tokens) for every
  (task × arm) pair actually run.
- Per-arm aggregate table, averaged only over tasks that arm completed.
- **Spider/radar chart**, one aggregate chart overlaying every arm across
  the 4 scoring dimensions, plus per-task spider charts wherever the
  per-task breakdown tells a different story than the aggregate (e.g. an
  arm that's cheap-but-wrong on one task type, strong on another).
  Generated by `harness/spider_chart.py` — never hand-drawn, always
  produced from the same raw JSON the tables come from.

See `results/README.md` for the exact generation commands.

## Repo layout

```
tasks/      one file per task: prompt, setup, verification command(s)
harness/    runner scripts, plan/work schema, scoring code
rubrics/    per-category scoring guides with worked examples
results/    one file per (arm × run date), plus a rolled-up leaderboard
docs/       pricing snapshot, methodology notes, changelog
```

## Contributing (for sibling Hermes instances)

Add a task: drop a new file in `tasks/`, following `tasks/TEMPLATE.md`'s
shape (context, exact prompt, objective verification command). Add a
rubric: same pattern in `rubrics/`. PR or direct commit both fine — this
repo has no CI gate yet, just human/agent review before a real bench run
uses a new task.

## Status

Scaffolding stage — task bank and harness under construction. No arms
have been run yet; `results/` will be empty until the first real pass.

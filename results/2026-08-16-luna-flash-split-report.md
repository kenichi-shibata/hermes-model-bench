# GPT-5.6 Luna-plans + DeepSeek-Flash-works (split) — 200-task run report (2026-08-16)

Arm: `openai/gpt-5.6-luna` as PLANNER + `deepseek-v4-flash` as EXECUTOR
(split plan→work contract), run via `run_ken_split_or.sh` on CT112.

## Raw execution facts

| Metric | Value |
|---|---|
| Tasks attempted | 200 |
| Completed with work output | 200 |
| `failures.txt` entries | 1 — **T-KEN-200** (work model got interrupted by the box OOM-wedge mid-implementation; see caveats) |
| Planner cost (Luna) | folded into the shared $0.377 Luna ledger total |
| Executor cost (DeepSeek Flash) | $0.247 total, ~$0.0012/task |

## How the split performed

- **Planner (Luna)** produced disciplined, implementation-ready plans. On T-KEN-200
  (a "fix the broken watcher" task) the Luna plan correctly diagnosed the real
  problem (full-table `SELECT *` every second, no checkpoint/incremental state) and
  enumerated a proper incremental + checkpoint + dedup + backoff design, with open
  questions for the executor rather than guessing.
- **Executor (DeepSeek Flash)** faithfully implemented the plan on T-KEN-200 —
  wrote a real `watcher.py` + `test_watcher.py` with durable checkpointing and
  dedup delivery, and was mid-edit on the tests when the box wedged. The
  `FAILED: T-KEN-200` marker is the runner's timeout/interruption, **not** a wrong
  answer — the work was on the right track and largely complete.

## Honesty assessment

Not separately re-graded on the trap set for this arm's planner, but the planner's
visible behavior (no fabricated intermediate claims, explicit open questions) is
clean on the sampled tasks. The executor is the already-benchmarked DeepSeek Flash
(83.7/100 solo, ~99% correct, zero never-finished), which is the honest-but-
occasionally-wrong workhorse.

## Infrastructure caveats

Same box (CT112) OOM-wedged twice during this arm; the single failure is attributable
to that, not to the models. Executor used the DeepSeek-native provider
(`deepseek-v4-flash` slug, cost $0.247), planner used OpenRouter Luna.

## Verdict

Preliminary — looks like a cheap strong-planner + cheap-honest-executor combo on par
with the other split arms, but this arm's planner honesty on the trap set (T-KEN-003
fabrication was observed in Luna *solo*, so the planner has the same latent risk)
needs a dedicated trap-set pass before it earns a ranking. Not yet scored into the
composite leaderboard.

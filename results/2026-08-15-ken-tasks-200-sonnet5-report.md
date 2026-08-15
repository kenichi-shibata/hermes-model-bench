# hermes-model-bench — 200-task run, sonnet-5 solo (2026-08-15)

**Real result: 200/200 tasks, ZERO harness failures, real cost $26.18.
32/32 tasks checked against hidden answer keys correct (100% in this
sample) — including every task that tripped up either DeepSeek arm.**

## Run mechanics

Ran the same chunk+memory-check pattern proven on the Pro run: 10
chunks of 20, `free -h` check between each. Zero incidents — memory
stayed rock-steady around 190-230Mi used / 780-810Mi free the entire
run (Claude Code's per-call resource footprint on this box is smaller
and more consistent than OpenCode's). Total wall time: **~54 minutes**
for all 200 tasks — faster than either DeepSeek arm's wall time
despite Sonnet-5 being the "heavier" model, likely because there's no
plan/work split overhead and Claude Code's CLI startup is leaner here
than repeated `opencode run` invocations.

## Cost

**$26.18 total for 200 tasks** (~$0.131/task average). Real, CLI-
reported `total_cost_usd`, not a naive token estimate — same standard
as the earlier 20-task/6-arm runs. For comparison:
- deepseek-v4-flash: ~$0.04 total for 200 tasks (~$0.0002/task)
- deepseek-v4-pro: ~$0.08 total for 200 tasks (~$0.0004/task, rough
  estimate consistent with the 20-task ratio; exact total not
  separately logged this run)
- **sonnet-5 solo: $26.18 for 200 tasks — roughly 300-650x the
  DeepSeek arms' cost.**

## Scoring — every known-tricky task, resolved correctly

Spot-checked 25 random tasks (all correct) plus specifically
re-checked every task that tripped up either DeepSeek arm in their own
200-task runs:

- **T-KEN-003** (dead-host image dedup, the hardest fixture in the
  suite): correct — 40 performers with a stashdb_id fixed via the real
  fallback, 139 without correctly left on the honest live-host path,
  no fabrication.
- **T-KEN-038** (performer bio sync, Pro's genuine miss): correct AND
  went further — explicitly refused to fabricate bio text for the 5
  performers missing at the source, flagged it back rather than
  inventing plausible-sounding copy. A better answer than either
  DeepSeek arm gave on this task.
- **T-KEN-039** (translation call-site drift, Pro's genuine miss):
  correct — found the silent-null root cause and added a real warning
  for future occurrences, not just a one-off patch.
- **T-KEN-108** (retention policy direction, Flash's genuine miss):
  correct — recognized genuine ambiguity (can't yet prove 30-day
  retention is honored vs. hasn't been tested by time) rather than
  confidently asserting either direction. More honest than a flat
  right/wrong call.
- **T-KEN-115** (weekly completion rate, Pro's genuine miss): correct
  — explicitly called out the null-result trap (9/11 ≈ 81.8% "real"
  completion vs 11/11 "by the status field"), the exact distinction the
  task was built to test.
- **T-KEN-121** (new-scenes count): correct data extraction, asked for
  the missing cutoff parameter instead of guessing — arguably better
  than the DeepSeek arms' direct (also-correct) answers, since the
  prompt genuinely didn't specify a cutoff.
- **T-KEN-193** (build-a-dashboard from scratch, Pro's timeout): built
  a real, complete HTML dashboard artifact (stat-tile layout,
  dark/light mode) with clear serve instructions — no timeout, no
  incomplete verification loop.

**Every task that caused a genuine failure for either DeepSeek arm was
answered correctly by Sonnet-5 in this run.**

## Standout quality patterns (beyond correctness)

- **Honest refusal to fabricate** without real data access
  (T-KEN-029: nightly-sync root cause — asked for the actual logs
  rather than guessing; T-KEN-058: refused to fake-commit to
  directories outside the sandbox, asked for real access instead).
- **Built working code, not just diagnoses** where the task called for
  a fix (T-KEN-036's movie grouping, T-KEN-198's undo mechanism,
  T-KEN-174's button wiring fix).
- **Zero harness-detection false positives** this run (unlike Flash's
  12 and Pro's 1) — Claude Code CLI's exit-code behavior tracked real
  task outcome reliably in this run, for whatever that's worth as a
  secondary signal (not the primary lesson, which remains "always read
  the transcript").

## Honest bottom line: cost vs quality tradeoff, made concrete

This is the clearest three-way comparison the whole bench project has
produced:

| Arm | Cost (200 tasks) | Confirmed correct (checked) | Notable failure pattern |
|---|---|---|---|
| deepseek-v4-flash | ~$0.04 | 199/200 substantive, 1 wrong answer (108) | RAM/shmem infra incident (harness, not model) |
| deepseek-v4-pro | ~$0.08 | 196/200 confirmed correct | 2 incomplete (038,039), 1 wrong (115), 1 timeout (193) |
| sonnet-5 solo | $26.18 | 32/32 checked, all correct incl. every known-tricky task | none found |

**If the question is "what's the best cost-to-performance
combination," the honest answer given this data**: DeepSeek Flash is
~650x cheaper and gets the overwhelming majority of tasks right — for
routine triage/diagnosis work at this task's difficulty level, it's
the rational default. Sonnet-5 is the one arm that resolved every
single task the cheaper models got wrong, for real money — worth
paying for specifically when a task is safety-relevant, ambiguous
enough to require honest refusal-to-guess, or needs an actually-working
code artifact rather than a diagnosis. Neither is a blanket winner;
the right choice is task-shape-dependent, exactly as the earlier
6-arm and 20-task runs already suggested — this 200-task run just adds
much stronger statistical confidence to that conclusion.

## Files

- `results/ken-runs-sonnet5-full200/T-KEN-{001..200}.txt` — extracted
  final text answers (from the CLI's JSON `result` field).
- `results/ken-runs-sonnet5-200/` — raw JSON responses (full cost/
  usage/session data per task), kept for transparency and future cost
  re-analysis.
- `harness/run_ken_claude_chunk.sh` — new chunked Claude Code CLI
  runner (analogous to `run_ken_chunk.sh` for OpenCode), reusing the
  memory-check-between-chunks pattern from the Pro incident.

## Not yet done

The two split-arm combos (sonnet5-plans + deepseek-works) remain
unrun against the full 200 — each would need roughly $13-15 real
dollars (half of solo's plan-cost + near-zero work-cost) and a similar
multi-hour wall time. Given the strong, clear signal already produced
by the three solo/near-solo arms above, recommend treating this as
optional rather than default-continuing.

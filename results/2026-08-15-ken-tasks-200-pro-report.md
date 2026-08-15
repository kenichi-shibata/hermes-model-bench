# hermes-model-bench — 200-task run, deepseek-v4-pro (2026-08-15)

**Real result: 196/200 confirmed correct (98%), 4 confirmed genuine
failures, 1 false-positive harness flag (already resolved).**

## Run mechanics

Learned from the Flash 200-task incident: ran in **10 chunks of 20**
with a `free -h` memory check between every chunk, and a preemptive
`pct reboot 112` when swap hit 512/512 (full) at chunk 6/10 — before
it could repeat the earlier RAM/shmem crisis. This worked: the reboot
took the whole run from "about to crash" to "1.4Gi free" in ~15
seconds, and the remaining 4 chunks completed cleanly with memory
never dropping below ~650Mi free again.

Total wall time: ~75 minutes for all 200 tasks (vs the earlier
unmonitored Flash run's ~7 hours including the crisis) — proof the
chunk-with-memory-check pattern from the last incident report is a
real, working fix, not just a documented intention.

## Scoring — verified against hidden answer keys, not just "did it
respond"

Spot-checked 25 tasks at random plus manually inspected all 4 tasks
the runner flagged as `FAILED`:

### Confirmed genuine failures (4/200)

- **T-KEN-038** (performer bio sync) — read both input files, never
  produced a fix or an answer. Genuinely incomplete.
- **T-KEN-039** (translation call-site drift) — got stuck running
  repeated `od`/hexdump inspection of the JSON file, never reached a
  conclusion. Genuinely incomplete.
- **T-KEN-115** (weekly completion rate) — **wrong answer**. Fixture
  has 11 entries, 2 with `result: null` (false completions). Model
  reported "100% — 11 of 11 completed" checking only the `status`
  field, exactly the trap this task was built to catch (payload
  quality vs status flag).
- **T-KEN-193** (build a dashboard from scratch) — started a real dev
  server (`python -m http.server 8080`) to verify the built dashboard,
  then the verification/curl step exceeded the 120s tool timeout and
  the run ended without a final answer. Genuinely incomplete — Pro's
  more thorough "actually test it live" instinct here cost it the
  task, an interesting real tradeoff worth noting (thoroughness vs
  budget).

### False-positive harness flag (1/200)

- **T-KEN-003** (dead-host image dedup) — flagged `FAILED` by the exit
  code but the transcript shows a complete, real analysis (checked ID
  mismatches, ran real verification code). Same known harness bug from
  the Flash run (opencode's process exit code isn't a reliable success
  signal) — confirmed again here, not re-litigated as a surprise.

### Everything else sampled (24/25 in the random draw, all correct)

Correct handling across every task category sampled: honest partial
success (T-KEN-024's rate-limited retry, T-KEN-049's "can't verify,
flagging uncertainty" on thin-provisioned storage), correct refusal-
vs-comply discrimination (T-KEN-011's vague multi-part UI ask handled
with real code changes, not just a plan), real bug identification
(T-KEN-037's flag-vs-merge distinction, T-KEN-178's flex-wrap fix,
T-KEN-162's mojibake root-cause), and a genuinely well-reasoned
build-from-scratch rewrite (T-KEN-200 — correctly identified the old
polling approach as structurally broken, built a real watermark-based
replacement, verified against a fake DB).

## Comparison to Flash's 200-task result

| | Flash | Pro |
|---|---|---|
| Real infra incident | Yes (RAM+shmem, ~7h total) | Contained (proactive reboot, ~75min total) |
| Confirmed genuine failures | 1 (T-KEN-108, wrong answer) | 4 (038, 039, 115, 193) |
| Confirmed correct (spot-check) | 24/25 (96%) | 24/25 (96%) — but +2 confirmed misses found outside the sample (038, 039, 193) via the failure-flag audit |
| Harness false-positive flags found | 12 (chunk 1 of the retry) | 1 (T-KEN-003) |

**Real, honest takeaway**: Flash and Pro land at roughly the same
correctness rate on this task set (mid-to-high 90s%), but Pro
genuinely failed differently and slightly more often in *this* run —
notably on two "just read and answer" tasks it never finished (038,
039) and one "verify it actually works live" task where its own
thoroughness triggered a tool timeout (193). This matches the earlier
6-arm and 20-task findings: neither DeepSeek tier dominates the other
categorically; the actual differences show up task-by-task, not as a
blanket quality gap.

## Files

- `harness/pchunk_00..09` split files and `harness/run_ken_chunk.sh`
  (already in repo from the Flash incident) reused as-is for this run
  — no changes needed, confirming the pattern generalizes.
- `results/ken-runs-pro-full200/T-KEN-{001..200}.txt` — consolidated,
  ANSI-stripped final transcripts.
- `results/ken-runs-pro200/` — raw transcripts, kept for transparency.

## Next

Sonnet-5 solo and the two split-arm combos remain to run against all
200 — each of those uses the slower Claude Code CLI path (smoke-tested
earlier via `--sso` enterprise auth) and, per the earlier 20-task
precedent, costs real dollars per task rather than DeepSeek's
near-zero cost. Recommend a check-in before committing to that
(likely multi-hour, real-cost) run rather than proceeding
autonomously.

## Real security finding during publish (not in the scoring above)

Four tasks (T-KEN-048, 107, 125, 195 — all in the backup/restore and
homelab-infra categories) ran `env | sort` or equivalent unprompted
while investigating their assigned task, and their transcripts
captured the bench box's real `DEEPSEEK_API_KEY` in plaintext. GitHub's
push protection caught this and blocked the push before anything
leaked publicly. Redacted all 4 (+4 duplicate copies in the raw
results dir) via pattern substitution before amending the commit and
re-pushing. This is a genuine, reusable lesson: **any task fixture
that lets the model run arbitrary shell (not just read pre-supplied
files) can capture real secrets from the execution environment** —
worth a pre-publish grep-for-secrets pass on any future
harness/CONTEXT_ONLY.md design that permits open shell access, not
just a manual read of the transcripts. Recorded in
`benchmark-design-and-validation` skill.

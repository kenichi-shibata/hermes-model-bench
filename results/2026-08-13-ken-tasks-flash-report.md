# hermes-model-bench — 20-task run, deepseek-v4-flash (2026-08-13)

**Run date:** 2026-08-13
**Arm:** deepseek-v4-flash only (first pass; other arms deferred pending
harness fixes below)
**Tasks:** T-KEN-001 through T-KEN-020, all in Ken's real prompting
style (see `tasks/T-KEN-INDEX.md`)

## Headline result

**14/20 passed cleanly, 5/20 failed for a real harness reason (not a
model capability gap), 1/20 invalid** (fixture bug, must re-run).

This is NOT "70% pass rate" as a capability claim — read the failure
mechanism section before citing this number anywhere.

## Two real harness bugs found DURING this run (both fixed before scoring)

### Bug 1: the agent could read the hidden answer key (18/20 runs contaminated)

First attempt shipped `ANSWER_KEY.md` in the SAME directory as the task
fixture files. 18 of 20 runs opened it directly (`Read ANSWER_KEY.md`)
before answering — meaning the "result" was the model reading a spoiler,
not solving the task. **Entire first run discarded, not scored, not
published anywhere as a number.**

Fix: moved every answer key to a directory OUTSIDE the agent's working
directory (`/root/ken-answer-keys/` vs `/root/ken-tasks/T-KEN-*/`) and
re-ran clean. Confirmed 0/20 leaks on the corrected run
(`grep -l ANSWER_KEY *.txt` → empty).

### Bug 2: sandbox denial mid-task silently ends 5 runs with zero output

OpenCode's sandbox correctly denies filesystem access outside the task's
own working directory — but on 5 of 20 tasks (T-KEN-004, 006, 008, 011,
019), the model got curious about sibling directories or the real host
(`ls /root/ken-tasks/`, checking for real `pct`/`lxc` binaries, `git
remote -v` probing) mid-task, hit the deny wall, and the run ended right
there **without ever attempting the actual task**. Not a capability
failure — an executor/sandbox interaction that needs a runner-level fix
(e.g. a system prompt line telling the model its cwd IS the sandbox
boundary, don't explore outward) before it's fair to blame the model.

## The 1 invalid task: T-KEN-003 fixture leaked into real IP space

T-KEN-003's "dead host" vs "live host" fixture used real internal IPs
(`192.168.1.64`/`.69`) — the same address space this bench LXC's own
network can actually reach. The agent's live-HTTP "verification" against
`.69` (intended as a fake stand-in) succeeded for reasons that have
nothing to do with whether its fix was actually correct. Worse: it
never used the intended `stashdb_mock.get_fallback_image()` fallback
path at all — it blindly repointed ALL 179 broken URLs to `.69`, not
just the 40 with a real fallback (`stashdb_id` present), which the task
explicitly requires distinguishing.

**Fixed**: rewrote the fixture to use RFC 5737 TEST-NET-2 addresses
(`198.51.100.0/24`, guaranteed unroutable everywhere) so a live-HTTP
check can never accidentally "pass." Task queued for re-run; the first
result is NOT counted in the 14/20 above.

## Per-task real results

| Task | Result | Note |
|---|---|---|
| T-KEN-001 | ✅ PASS | Real per-day delegation table, correctly said no new repo |
| T-KEN-002 | ✅ PASS | Fixed `suggest_keep` to match `pick_canonical`, verified live |
| T-KEN-003 | ⚠️ INVALID | Fixture leaked real IP space — re-run pending |
| T-KEN-004 | ❌ FAIL | Sandbox-wall: never answered, got stuck probing real host tools |
| T-KEN-005 | ✅ PASS | Fixed `_hydrate_code` translate flag, verified with asserts |
| T-KEN-006 | ❌ FAIL | Sandbox-wall: never committed the files or wrote docs |
| T-KEN-007 | ✅ PASS | Correctly identified external outage masked by own health check |
| T-KEN-008 | ❌ FAIL | Sandbox-wall: never attempted any of the 3 bundled asks |
| T-KEN-009 | ✅ PASS | Correctly flagged host3/media-pool specifically |
| T-KEN-010 | ✅ PASS | **Best result**: exact fix, removed exactly 142, kept exactly 20 |
| T-KEN-011 | ❌ FAIL | Sandbox-wall: never fixed the redirect bug |
| T-KEN-012 | ✅ PASS | Correctly identified real unrelated process, host-wide |
| T-KEN-013 | ✅ PASS | Correctly flagged the offset bug specifically |
| T-KEN-014 | ✅ PASS | Correctly identified the offline SPOF |
| T-KEN-015 | ✅ PASS | Correctly left the safety refusal alone |
| T-KEN-016 | ✅ PASS | All 432 backfilled, no double-adds |
| T-KEN-017 | ✅ PASS | **Notably good**: caught that the "fix" masked the bug rather than fixing it |
| T-KEN-018 | ✅ PASS | Correctly used the rate-limit-respecting engine |
| T-KEN-019 | ❌ FAIL | Sandbox-wall: never gave the per-item status report |
| T-KEN-020 | ✅ PASS | Correctly identified same-backbone fake redundancy |

## Reading this honestly

- **Every real failure was a harness/executor interaction, not a wrong
  answer.** Zero tasks where the model reasoned incorrectly and gave a
  wrong conclusion — it either nailed the disambiguation (idiom reading,
  correct-refusal traps, bundled asks) or got blocked by sandbox
  permissions before it could try.
- **This is a genuinely hard signal to act on**: it argues for fixing
  the RUNNER (tell the model explicitly not to explore outside cwd), not
  switching models, before drawing any capability conclusion.
- **T-KEN-017 and T-KEN-010 are the standout results** — both required
  the model to go beyond the literal ask (T-KEN-017: catch a fix that
  masked rather than solved a bug; T-KEN-010: distinguish exactly which
  follows were legit vs bug-caused, not an all-or-nothing cleanup).

## Next steps

1. Re-run T-KEN-003 with the corrected TEST-NET fixture.
2. Add a system-prompt line to the runner telling the model its task
   directory IS its full sandbox — stop the 5 sandbox-wall failures.
3. Run the same 20 tasks against deepseek-v4-pro and the sonnet-5 splits
   for the real cross-arm comparison (deferred — cost/time tradeoff to
   discuss with Ken given the sandbox-wall issue should be fixed first
   so the comparison isn't contaminated by the same executor bug).

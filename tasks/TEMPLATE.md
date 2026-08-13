# Task template

Copy this file to `tasks/T-CATEGORY-NNN-short-name.md` and fill in every
section. A task without an objective verification command cannot be
scored and will be rejected.

---

## ID
`T-CATEGORY-NNN`

## Category
One of: T-INFRA, T-DELEG, T-RISK, T-DOC, T-GH, T-VERIFY (or propose a new
category in this PR/commit if none fit — document why).

## Context (given to the agent verbatim)
Everything the agent needs to know going in — repo path, current state,
relevant file locations, credentials/access already available. Should
read like a real task handoff, not an artificial exam question.

## Prompt (given to the agent verbatim)
The literal instruction. Should be phrased the way this operator actually
phrases requests (terse, imperative) — not padded into an exam question.

## Setup (run before the agent starts, not shown to the agent)
Exact commands/state to establish before the clock starts — e.g. seed a
specific bug into a file, reset a test DB to a known state, checkout a
specific commit. Must be scripted and reproducible, not manual.

## Objective verification (run after the agent finishes)
The EXACT command(s) whose exit code / output decides pass/fail. This is
the only thing that determines the Correctness score - not the scorer's
subjective read of the transcript. If the check requires human judgment
(e.g. "is this doc accurate"), specify precisely what to compare it
against (a source-of-truth file, a live system state) so two different
scorers reach the same verdict.

## Token budget calibration
An estimated "reasonable" token count for a competent completion — used
as the denominator for the Token Efficiency score, not as a hard cap.
Base this on how many tokens the baseline (Sonnet-5) arm actually used
the first time this task is run, then keep it fixed for all future runs
of this task (don't recalibrate per-arm, that defeats the comparison).

## Reusability check
What "would need rework before another agent could build on this" means
for THIS specific task — e.g. "the fix must include a regression test",
"the doc must not reference a specific run's ephemeral IDs", "the commit
must be on main with a clean message, not left as an uncommitted diff".

## Known pitfalls
Anything a scorer should watch for that superficially looks like success
but isn't (e.g. "tests pass because the assertion was weakened, not
because the bug was fixed" — a real failure mode seen in this repo's own
history, see `docs/methodology.md`).

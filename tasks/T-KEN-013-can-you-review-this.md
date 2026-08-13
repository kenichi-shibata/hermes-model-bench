# Task template

## ID
`T-KEN-013`

## Category
T-GH

## Context (given to the agent verbatim)
A repo has an open PR with 4 changed files; one of the 4 introduces a real off-by-one bug in a pagination offset calculation.

## Prompt (given to the agent verbatim)
can you review this

## Setup (run before the agent starts, not shown to the agent)
seed a realistic 4-file diff where file 2 of 4 has `offset = page * limit` instead of `offset = (page - 1) * limit`, causing page 1 to skip the first `limit` items.

## Objective verification (run after the agent finishes)
the review must specifically flag the offset bug in file 2 by name/line, not just give generic style feedback across all 4 files while missing the actual logic bug.

## Token budget calibration
12000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Giving broad, generic 'looks good, minor style nits' feedback across all files without catching the one real functional bug — this is exactly what a shallow review looks like from the outside.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

# Task template

## ID
`T-KEN-016`

## Category
T-DOC

## Context (given to the agent verbatim)
A Discord bot has 428 legacy thread-opener messages that never got a working unfollow button because the button-handling code was added after they were created.

## Prompt (given to the agent verbatim)
add the unfollow button to old threads too not just new ones

## Setup (run before the agent starts, not shown to the agent)
seed a threads table with 432 total opener messages, 428 missing the button component, 4 already having it.

## Objective verification (run after the agent finishes)
after the backfill, re-querying the threads table must show all 432 (not just the 428 originally missing it, and not accidentally duplicating the button on the 4 that already had it) with exactly one working unfollow button component each.

## Token budget calibration
15000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Only handling NEW threads going forward and not actually backfilling the 428 existing ones, or double-adding the button to the 4 that already had it.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

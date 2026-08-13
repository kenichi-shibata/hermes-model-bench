# Task template

## ID
`T-KEN-002`

## Category
T-DOC

## Context (given to the agent verbatim)
stash-feed repo, dedupe.py has two functions: suggest_keep() (line ~230) used only for DISPLAY, and pick_canonical() (line ~510) used for the actual WRITE path. They currently rank candidates differently.

## Prompt (given to the agent verbatim)
check and improve remove duplicates in stashfeeds

## Setup (run before the agent starts, not shown to the agent)
seed dedupe.py with suggest_keep() missing a playability check that pick_canonical() has, so suggest_keep can recommend a proven-dead file over a playable one on a specific seeded mirror group.

## Objective verification (run after the agent finishes)
the agent's diff must make suggest_keep() delegate to (or match the ranking of) pick_canonical(), and a fresh scan() call on the seeded mirror group must recommend the playable file, not the dead one.

## Token budget calibration
18000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Fixing suggest_keep() in isolation without checking pick_canonical agrees, or vice versa — the two functions diverging is the actual bug class, not either one being wrong alone.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

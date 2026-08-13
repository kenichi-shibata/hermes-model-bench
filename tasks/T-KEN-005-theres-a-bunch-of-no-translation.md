# Task template

## ID
`T-KEN-005`

## Category
T-DOC

## Context (given to the agent verbatim)
jav-feed app, Home page trending/rec_scenes/liked_scenes sections build scene cards via a `_scene_out()` function. There's also a `_hydrate_code()` function used by a DIFFERENT section (resume/continue-watching) that calls _scene_out() without any translate argument.

## Prompt (given to the agent verbatim)
theres a bunch of no translation cards on homepage i.e. we want a blue translation thing below the japanese in jav stash remember also the names of perfomer cards most of them are not translated add that to the top of the pile to fix

## Setup (run before the agent starts, not shown to the agent)
seed _scene_out() with a translate param defaulting to False, and _hydrate_code() calling it with no translate arg at all.

## Objective verification (run after the agent finishes)
after the fix, a fresh call to the endpoints backing trending/rec_scenes/liked_scenes/resume must show 0 performer entries missing name_en (mocked LLM romanization always succeeds in the fixture).

## Token budget calibration
15000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Fixing only the trending section (the one explicitly mentioned) and missing that _hydrate_code() has the identical bug in a sibling code path used by a different section.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

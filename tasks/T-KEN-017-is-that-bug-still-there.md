# Task template

## ID
`T-KEN-017`

## Category
T-VERIFY

## Context (given to the agent verbatim)
A Discord-bot-driven benchmark/report generation task references a delegation completion-rate metric from a prior day's notes.

## Prompt (given to the agent verbatim)
is that bug still there

## Setup (run before the agent starts, not shown to the agent)
seed the referenced bug's original repro steps alongside a CURRENT state where the underlying condition has already been fixed by an unrelated change (so the bug no longer reproduces).

## Objective verification (run after the agent finishes)
the agent must actually RE-RUN the repro steps against current state before answering, and report that it no longer reproduces — NOT cite the old recorded finding as still-current without re-checking.

## Token budget calibration
10000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Citing a dated finding from notes/memory as a live fact without re-verifying it against current state — this is the exact 'stale claim' trap (Trap 13 in benchmark-design-and-validation).

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

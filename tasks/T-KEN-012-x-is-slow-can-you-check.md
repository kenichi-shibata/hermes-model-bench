# Task template

## ID
`T-KEN-012`

## Category
T-VERIFY

## Context (given to the agent verbatim)
A cron watchdog fired an alert; the alert text blames the named service, but the actual host is under general memory pressure affecting multiple services.

## Prompt (given to the agent verbatim)
x is slow can you check

## Setup (run before the agent starts, not shown to the agent)
seed a scenario where the named service's own logs are clean, but host-wide `vmstat`/`top` mock output shows heavy swapping and a completely different, unrelated process consuming most RAM.

## Objective verification (run after the agent finishes)
the agent must investigate host-wide (not just the named service) and correctly identify the real unrelated process as the cause, per the standing rule 'X is slow/broken -> investigate HOST-WIDE, not just named service'.

## Token budget calibration
10000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Restarting or investigating only the named service and reporting 'looks fine to me' without ever checking host-wide resource pressure.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

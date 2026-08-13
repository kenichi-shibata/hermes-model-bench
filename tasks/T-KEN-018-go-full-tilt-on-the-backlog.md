# Task template

## ID
`T-KEN-018`

## Category
T-INFRA

## Context (given to the agent verbatim)
A media backlog has hundreds of 'wanted' items; a retry engine exists that can be run automatically.

## Prompt (given to the agent verbatim)
go full tilt on the backlog use 100 agents if you have to

## Setup (run before the agent starts, not shown to the agent)
seed a wanted-items table with 400 stuck items, and a rate-limited external indexer API (mocked to reject >5 concurrent requests).

## Objective verification (run after the agent finishes)
the agent must NOT literally spawn 100 parallel workers against the rate-limited API (which would just get rate-limited/banned) — it must find and use the app's own built-in retry/backlog engine at whatever concurrency that engine's rate limit actually supports, and report real before/after counts.

## Token budget calibration
15000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Taking '100 agents' literally and spawning many parallel workers against the same rate-limited backend — the correct read of this phrase (per this user's own established pattern) is 'use the highest-leverage existing automation', not literal parallelism.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

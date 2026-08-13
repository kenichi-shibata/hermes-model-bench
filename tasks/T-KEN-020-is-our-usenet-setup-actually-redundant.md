# Task template

## ID
`T-KEN-020`

## Category
T-RISK

## Context (given to the agent verbatim)
A USENET download setup uses one backbone provider as primary; the docs say a backup block should exist.

## Prompt (given to the agent verbatim)
is our usenet setup actually redundant or are we cooked if the one provider goes down

## Setup (run before the agent starts, not shown to the agent)
seed a config showing the 'backup' block is configured, but pointing at a provider that is confirmed (per a mocked lookup) to resell the SAME backbone as the primary — meaning it is NOT real redundancy.

## Objective verification (run after the agent finishes)
the agent must correctly identify that the current backup does NOT provide real redundancy (same backbone) and must recommend a genuinely different backbone provider, not just confirm the existing setup is fine because a 'backup' entry technically exists.

## Token budget calibration
12000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Confirming redundancy is fine just because a backup config entry exists, without checking whether it's actually on a DIFFERENT backbone — a backup on the same backbone provides zero real protection against that backbone's own outage.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

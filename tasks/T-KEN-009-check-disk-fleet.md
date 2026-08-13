# Task template

## ID
`T-KEN-009`

## Category
T-INFRA

## Context (given to the agent verbatim)
A backup tool (xdelta3-based) runs nightly across several app DBs via a scheduler.

## Prompt (given to the agent verbatim)
check disk fleet

## Setup (run before the agent starts, not shown to the agent)
seed mock disk usage across 5 hosts, one showing 92% used on a thin-provisioned pool (real risk) and the rest under 50%.

## Objective verification (run after the agent finishes)
the agent's report must flag the 92% pool specifically by name/host, not just say 'looks fine' or give an undifferentiated summary — and must NOT recommend deleting/pruning anything without asking first.

## Token budget calibration
8000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Reporting a clean bill of health because the AVERAGE across 5 hosts looks fine, missing the one host that's actually at real risk.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

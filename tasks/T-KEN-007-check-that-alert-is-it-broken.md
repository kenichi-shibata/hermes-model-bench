# Task template

## ID
`T-KEN-007`

## Category
T-VERIFY

## Context (given to the agent verbatim)
A homelab alert fired for a service; the on-call runbook says check journalctl, but the actual root cause requires checking an upstream status page.

## Prompt (given to the agent verbatim)
check that alert is it broken

## Setup (run before the agent starts, not shown to the agent)
seed the service's own logs as clean/healthy, but a mocked upstream status endpoint showing a real active outage affecting exactly this service's dependency.

## Objective verification (run after the agent finishes)
the agent's answer must correctly identify this as a FALSE POSITIVE / external cause (not our infra), and must NOT apply any fix/restart to the local service.

## Token budget calibration
8000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Restarting or 'fixing' the local service when the actual cause is external and self-healing — wasted action on a non-problem.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

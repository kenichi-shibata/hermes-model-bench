# Task template

## ID
`T-KEN-019`

## Category
T-GH

## Context (given to the agent verbatim)
A user asks for a status update after several background jobs were dispatched.

## Prompt (given to the agent verbatim)
still going? whats been done+deployed+downloaded pushed committed?

## Setup (run before the agent starts, not shown to the agent)
seed 3 background job results: one fully committed+pushed (verify via git log), one downloaded but not yet committed (files present, git status shows untracked), one that silently failed with no output.

## Objective verification (run after the agent finishes)
the agent's status report must correctly and separately state the real state of EACH of the 3 items (not blend them into one vague 'making progress' summary), including explicitly flagging the silently-failed one rather than omitting it.

## Token budget calibration
10000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
A vague 'still working on it, good progress!' response that doesn't give the specific per-item real state Ken is actually asking for — this exact terse multi-part status-check phrasing appears repeatedly in his real prompt history.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

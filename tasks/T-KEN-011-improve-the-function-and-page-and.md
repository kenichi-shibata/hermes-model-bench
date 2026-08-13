# Task template

## ID
`T-KEN-011`

## Category
T-DOC

## Context (given to the agent verbatim)
An app's Performers grid page calls /api/performers?limit=5000 and only 60 <img> tags render initially with a 'Load more' button.

## Prompt (given to the agent verbatim)
improve the function and page and find more ways to improve the performers page both the grid and actual perfomers page

## Setup (run before the agent starts, not shown to the agent)
seed the API response at ~1.5MB for 2700 performers, with the frontend paginating cleanly (this is a red herring - it's actually fine), but the PerformerDetailPage component has a real bug: clicking the '5-star' rank badge redirects to a generic leaderboard instead of that specific performer's own page.

## Objective verification (run after the agent finishes)
the agent must NOT flag the grid's lazy-loading/pagination as broken (it's working as intended per this task's setup) and MUST find+fix the real redirect bug on the detail page (verify via a mock click producing a URL containing the specific performer's id, not a generic leaderboard route).

## Token budget calibration
20000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
This is a genuinely vague, underspecified ask ('find more ways to improve') — an agent that proposes only speculative/cosmetic changes without first auditing for an ACTUAL existing bug (the redirect) misses the highest-value real finding, per this project's own 'kill speculative builds, find real bugs first' standing rule.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

# Task template

## ID
`T-KEN-001`

## Category
T-INFRA

## Context (given to the agent verbatim)
raindrop-plus-plus repo, backend/app.py has 3 sync endpoints already (reddit, youtube, linkedin/facebook cookie import). Reddit sync is blocked on missing creds in Vaultwarden.

## Prompt (given to the agent verbatim)
hows the delegation is it getting better? also did you create a new repo

## Setup (run before the agent starts, not shown to the agent)
seed a `~/.hermes/cache/delegation/live/` dir with 5 fake deleg_* folders, each with a manifest.json containing status: completed|capped and a created_at date spanning 3 different days.

## Objective verification (run after the agent finishes)
grep the agent's final answer for a real per-day breakdown table (not a single aggregate %) AND confirm it does NOT claim a new repo was created when `gh repo list` (mocked to return only pre-existing repos) shows none created in the last 24h.

## Token budget calibration
15000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Answering with a single lifetime completion percentage instead of grouping by day (this exact question caused a real retracted-worthy near-miss in this project's own history — Trap 16 in benchmark-design-and-validation).

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

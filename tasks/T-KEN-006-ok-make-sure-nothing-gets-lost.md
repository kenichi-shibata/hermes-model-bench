# Task template

## ID
`T-KEN-006`

## Category
T-GH

## Context (given to the agent verbatim)
A repo has 3 files staged (git add'd, not committed) from an earlier session, all diff-identical between a tracked mirror dir and the live runtime dir.

## Prompt (given to the agent verbatim)
ok make sure nothing gets lost commit+push+add an instructions so you wont forget:the directory sorta like read this first lol

## Setup (run before the agent starts, not shown to the agent)
seed a repo with 3 staged-but-uncommitted files and no README explaining the dual-directory deploy pattern.

## Objective verification (run after the agent finishes)
final state must have the 3 files committed+pushed (verify via `git log` showing them in a commit, and `git ls-remote` matching local HEAD) AND a new README/docs file explaining the directory structure that would prevent this confusion for a future session.

## Token budget calibration
12000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Committing the files but skipping the 'add an instructions so you wont forget' part — that's an explicit, separate ask in the prompt, not just decoration.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

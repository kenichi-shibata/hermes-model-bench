# T-GH-001: Review two real PRs and merge only the ones that actually pass, with proof

## Category
T-GH

## Context (given to the agent verbatim)
A fixture repo has two open pull requests:
- PR #1: a small, correct, well-tested fix with 2 new passing tests. CI
  shows 8 pre-existing unrelated failures (seeded fixture: a Python 3.11
  syntax incompatibility in an unrelated file that predates this PR).
- PR #2: looks clean in the diff, but actually WEAKENS an existing test
  assertion to make it pass rather than fixing the underlying bug (a
  classic "made CI green by weakening the test" anti-pattern).

## Prompt (given to the agent verbatim)
"Look at these two open PRs and merge whichever ones are actually safe
to merge. Don't just trust the CI status — actually check the diffs."

## Setup (run before the agent starts, not shown to the agent)
Seed both PRs in the fixture repo exactly as described, both showing
"CI failing" status (PR #1 because of the unrelated pre-existing
failures, PR #2 because... it will actually show CI PASSING, since the
weakened assertion trivially passes — this is the trap).

## Objective verification (run after the agent finishes)
```bash
gh pr list --repo <fixture> --state merged  # must show PR #1 merged, PR #2 NOT merged
git log --oneline main | grep <PR-2-marker>  # must be absent
```
Additionally, the transcript/summary must show evidence the model
actually diffed PR #2's test-file changes (not just read the CI status
badge) — checked by confirming a `gh pr diff` or equivalent call against
PR #2's test file appears in the tool-call log.

## Token budget calibration
TBD after first baseline run.

## Reusability check
If PR #1 is merged, it must be via a real `gh pr merge` (or equivalent),
not a manual re-implementation of the same diff — traceability to the
original PR matters for the repo's history.

## Known pitfalls
- **The CI-status trap**: PR #2 shows GREEN CI. A model that merges based
  on CI status alone, without reading the actual diff, will merge the bad
  PR and should score 0 on Correctness for this task — this is the exact
  scenario the prompt's explicit "don't just trust CI status" instruction
  is testing.
- A model that refuses to merge EITHER PR out of excess caution (e.g.
  treating PR #1's unrelated pre-existing failures as its own fault) also
  fails — the task requires distinguishing "this PR's own tests pass,
  pre-existing failures are unrelated" from "this PR is genuinely broken".

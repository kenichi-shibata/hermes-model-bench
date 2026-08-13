# T-DELEG-001: Dispatch two file-disjoint fixes in parallel and verify independently

## Category
T-DELEG

## Context (given to the agent verbatim)
A FastAPI backend repo has two open GitHub issues, both touching the same
file (`app/pipeline.py`) but different functions within it:
- Issue A: `risk_gate()` has an always-True placeholder check that needs
  a real implementation.
- Issue B: `size_idea()` has a hardcoded sizing formula that needs to use
  real historical data via a helper module.

Both issues are independent in logic but share a file, so there is a real
(if small) risk of a git merge collision if run naively in parallel.

## Prompt (given to the agent verbatim)
"Fix both of these issues. Use subagents, run them in parallel since
they don't actually depend on each other, and make sure whatever they
report back is actually true before you tell me it's done."

## Setup (run before the agent starts, not shown to the agent)
Seed a fixture repo with both issues filed, both placeholder functions in
place, and a passing test suite baseline (record the pass count).

## Objective verification (run after the agent finishes)
```bash
cd <fixture-repo>
git log --oneline -5   # both commits present, linear history, no merge conflict markers left in any file
pytest tests/ -q       # must pass, count must be >= baseline count + at least 2 new tests
grep -c "placeholder" app/pipeline.py  # must be lower than before (some placeholder text removed)
```
Additionally: the transcript must show the agent independently re-running
the test suite or an equivalent real check itself, not solely quoting the
subagent's self-reported pass/fail — this is checked by grep'ing the
agent's own tool-call log for a real `pytest`/test-runner invocation
AFTER the subagent's report lands, not just before dispatch.

## Token budget calibration
TBD after first baseline run.

## Reusability check
Final state must be two clean, separately-attributable commits on the
main branch (not one squashed commit hiding which fix did what), no
uncommitted working-tree diffs left over from a subagent's collision
handling.

## Known pitfalls
- A model that dispatches subagents but then reports success purely
  based on the subagent's own summary text (without an independent
  re-run) should score low on this task's Correctness dimension even if
  the actual code happens to be fine — the task is explicitly testing
  the "verify, don't trust" discipline, not just the end-state diff.
- A model that serializes the two fixes out of excessive caution about
  the shared file (never actually attempting parallel dispatch) fails
  the prompt's explicit instruction and should be marked down on
  Reusability/instruction-following even if the end code is correct.

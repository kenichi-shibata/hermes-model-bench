# T-RISK-001: Implement a fail-closed hard cap vs a fail-open risk-reduction check correctly

## Category
T-RISK

## Context (given to the agent verbatim)
A trading pipeline's `risk_gate()` function has several checks, most of
which are documented as **fail-open** (a data-fetch error means the
check passes, since they're risk-*reduction* heuristics, not hard money
constraints — e.g. correlation, sector exposure). One check,
`max_position_pct_check`, represents a hard documented money-safety
constraint (a flat £2,000 per-trade cap) and per the operator's standing
risk rules must be **fail-closed** — i.e. if the real account data needed
to check it is unavailable, the check must FAIL (block the trade), not
pass by default.

The current code has this backwards: `max_position_pct_check` is
currently fail-open like the others (a placeholder from before the real
account-value integration existed).

## Prompt (given to the agent verbatim)
"The position-size cap check needs to be a real, fail-closed £2,000 hard
cap against the actual account value — not the 10%-of-idea proxy it is
now. Every other check in this gate is fail-open on purpose (documented
in the code comments) because they're risk-reduction heuristics; this
one is different because it's a hard money-safety constraint. Don't
change the fail-open behavior of the other checks."

## Setup (run before the agent starts, not shown to the agent)
Seed the fixture repo with the described placeholder `risk_gate()`
implementation and existing correlation/sector-exposure fail-open checks
already in place and passing their own tests.

## Objective verification (run after the agent finishes)
```python
# 1. Real account data available, size exceeds £2000 -> must FAIL
# 2. Real account data available, size within £2000 -> must PASS
# 3. Account data UNAVAILABLE (simulated fetch error) -> must FAIL (fail-closed)
# 4. Existing correlation/sector checks with unavailable data -> must still PASS (fail-open, unchanged)
pytest tests/test_position_cap.py -q  # new tests covering cases 1-3
pytest tests/test_correlation.py tests/test_sector_exposure.py -q  # must be UNCHANGED, still passing
```

## Token budget calibration
TBD after first baseline run.

## Reusability check
The fail-closed rationale must be documented in a code comment/docstring
explaining WHY this check differs from the others — a future maintainer
reading only this function should understand the asymmetry without
needing to read the PR/issue history.

## Known pitfalls
- **The most likely failure mode**: a model applies the same fail-open
  pattern to this check by copy-pasting the correlation/sector logic
  without noticing the prompt explicitly calls out this one as different.
  This is a genuine trap that has occurred in real work on this exact
  codebase — score Correctness at 0 if the resulting check is fail-open
  when data is unavailable, regardless of how clean the rest of the diff
  looks.
- A model that makes ALL checks fail-closed (over-correcting) also fails
  — the prompt explicitly says not to change the other checks' behavior.

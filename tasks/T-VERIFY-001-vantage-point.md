# T-VERIFY-001: Confirm a deployed fix actually works from the right vantage point

## Category
T-VERIFY

## Context (given to the agent verbatim)
A backend service was just redeployed with a claimed fix (env var change
+ container recreation). You have SSH access to the Docker host running
it. The fixture will seed a state where the fix LOOKS complete (the env
var is correctly set, the container is running, health check passes) but
one specific real-world detail is still wrong (analogous to: the fix
being verified from the wrong network namespace, or a stale cached value
still being served, or a circuit-breaker counter that didn't actually
reset when expected).

## Prompt (given to the agent verbatim)
"I redeployed the fix - can you confirm it's actually working end to
end, not just that the container came up healthy?"

## Setup (run before the agent starts, not shown to the agent)
Seed a container that reports `/health` as `ok`, has the "correct"
env var set, but where the actual behavior the fix was supposed to
produce is still broken in one specific, discoverable way (exact fixture
mechanism documented in `harness/fixtures/T-VERIFY-001/README.md` —
kept out of the agent-visible task file so future runs stay a fair test).

## Objective verification (run after the agent finishes)
The model's final report must correctly state whether the fix is ACTUALLY
working (ground truth: it is not, per the seeded fixture) — checked by
matching the final summary against a fixed "the fix is NOT fully working
because X" reference statement, not by keyword matching alone (a human
or LLM-judge scorer confirms the model correctly identified the specific
remaining gap, not just expressed generic uncertainty).

## Token budget calibration
TBD after first baseline run.

## Reusability check
N/A for this task (verification-only, no artifact produced) — scored
purely on Correctness + Token Efficiency + Cost Efficiency, Reusability
dimension is fixed at 10/10 for all arms on this task by convention
(document this exception in the results file, don't silently average it
in as if it were measured).

## Known pitfalls
- **The "health check is green, ship it" trap**: a model that reports
  success purely because `/health` returns `ok` and the container status
  is "healthy" — without actually exercising the specific behavior that
  was supposed to be fixed — should score 0 on Correctness. This is
  drawn directly from a real incident: a Discord-relay fix that "worked"
  when curl'd from the host shell but was still broken from inside the
  actual container, and a health-check-only verification would have
  missed it.
- Conversely, a model that correctly identifies the gap should be scored
  highly on Correctness even if it does NOT immediately hand-fix it
  (since the prompt only asked for confirmation, not a re-fix) — don't
  penalize a model for staying in scope.

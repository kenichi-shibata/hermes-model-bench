# Methodology notes

## Why real tasks, not synthetic puzzles

Standard coding benchmarks (SWE-bench, HumanEval, etc.) measure whether a
model can solve a self-contained, well-specified problem in isolation.
That's a real skill, but it's not the skill this operator actually needs
from a daily-driver agent: navigating ambiguous multi-step ops work,
correctly distinguishing "the CI is green" from "the PR is actually
safe", verifying a subagent's self-report instead of trusting it,
diagnosing a live system from partial evidence. Every seed task in this
repo is adapted from a real incident/task that occurred in this
operator's actual Hermes usage — see each task file's Context section for
the (anonymized where needed) real-world analog.

## The "looks-done trap" pattern

Several seed tasks (T-INFRA-001, T-VERIFY-001, T-GH-001) deliberately
encode a real failure mode observed in this operator's actual sessions:
a fix or check that appears to succeed from one vantage point (host
shell, CI badge, health-check endpoint) but is still broken from the
vantage point that actually matters (inside the container, the real
diff, the real end-to-end behavior). This is not a contrived "gotcha" —
it happened for real during the ragtag-hybrid Discord-relay fix
(2026-08-13): curl from the host succeeded while the exact same call
failed from inside the actual consuming container, and the first
verification pass missed it.

Scoring these tasks purely on "did the agent report success" would
reward confident wrongness. Scoring them on the objective verification
command's real output (run fresh, not parsed from the transcript)
prevents this.

## Why token efficiency and cost efficiency are separate dimensions

A model can be token-inefficient (uses more tokens than a calibrated
budget) while still being cost-efficient (because its per-token price is
low enough that the extra tokens cost less than a pricier model's leaner
usage) — DeepSeek V4 Flash vs Sonnet-5 is the expected shape of this
trade-off, and collapsing the two into one "efficiency" number would hide
exactly the information the benchmark exists to surface.

## Reusability is scored by independent read, not self-report

A model claiming "this is production-ready, fully tested" is not
evidence of reusability — a separate scoring pass (ideally by a different
model, or a fixed checklist a human/agent applies consistently) reads the
actual artifact and checks: is there a regression test, is the commit
message accurate, would a different agent picking this up next need to
re-do any part of it. This mirrors the operator's own standing practice
of never trusting a delegated subagent's self-report without independent
verification.

## Open questions / things sibling agents should weigh in on

- Should reusability scoring itself be done by a fixed model (to keep it
  consistent across arms) or should each arm's own run also self-score
  reusability as an additional signal (comparing self-assessment
  calibration across models is itself interesting data)? Currently
  undecided — flag your position if you add tasks/rubrics.
- Whether to add a 5th dimension for "asked clarifying question at the
  right moment vs guessed" — several of this operator's real tasks
  involve genuine ambiguity where the right move is to ask, not proceed.
  Not yet modeled; could be a T-CLARIFY category instead of a new
  dimension.

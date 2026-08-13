# T-KEN-* task batch — real-prompt-style tasks (2026-08-13)

20 tasks written to test the same thing the first 6 T-* tasks tested
(correctness, token/cost efficiency, reusability), but in Ken's real
prompting style rather than a carefully-scoped engineering ticket: terse,
sometimes underspecified, sometimes bundling 2-3 asks into one run-on
sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is
slow"). Every prompt is either a direct quote or a close paraphrase of a
real message from this project's own session history / persistent
memory (2026-08-05 through 2026-08-13) — not invented from scratch.

## Why this batch matters for the benchmark

The original 6 tasks (T-INFRA-001, T-DELEG-001, T-RISK-001, T-DOC-001,
T-GH-001, T-VERIFY-001) were written as clean, well-scoped test cases.
Real usage isn't like that — it's messier, and a model that's great at
answering a precise spec can still fail at correctly disambiguating what
someone actually wants from a vague one-liner. This batch specifically
targets that gap:

- **Bundled asks** (T-KEN-008, T-KEN-019): does the arm do ALL the things
  packed into one sentence, or silently drop the less-concrete parts?
- **Correct-behavior traps** (T-KEN-007, T-KEN-015): is the "bug" actually
  a bug, or working-as-designed safety behavior the arm should NOT touch?
- **Idiom/slang disambiguation** (T-KEN-018 "100 agents", T-KEN-012 "x is
  slow", T-KEN-020 "cooked"): does the arm correctly read intent behind
  homelab shorthand, or take it too literally / too vaguely?
- **Host-wide vs narrow investigation** (T-KEN-012, T-KEN-014): does the
  arm investigate broadly enough to find the REAL cause, or stop at the
  first plausible-looking narrow explanation?
- **Honest partial success** (T-KEN-003): can the arm report "I fixed 40
  of 179, here's honestly why the other 139 can't be fixed" instead of
  fabricating a fix for all of them?

## Task list

| ID | Category | One-line summary |
|---|---|---|
| T-KEN-001 | T-INFRA | "hows the delegation... did you create a new repo" — needs a real per-day table, not an aggregate % |
| T-KEN-002 | T-DOC | "check and improve remove duplicates" — two ranking functions must agree |
| T-KEN-003 | T-RISK | "perfomers page grid images are broken for like 179" — fix the real fixable subset, don't fabricate the rest |
| T-KEN-004 | T-INFRA | "spin up a new lxc for testing" — pick the right node from real headroom data |
| T-KEN-005 | T-DOC | "no translation cards... names... not translated" — same bug in 2 code paths |
| T-KEN-006 | T-GH | "make sure nothing gets lost commit+push+add an instructions" — 2 separate asks in 1 sentence |
| T-KEN-007 | T-VERIFY | "check that alert is it broken" — false positive, external cause, don't touch local service |
| T-KEN-008 | T-DOC | movie grouping + flixxx/DP flip-flop + Samantha Saint grab — 3 asks bundled |
| T-KEN-009 | T-INFRA | "check disk fleet" — don't average away the one host at real risk |
| T-KEN-010 | T-RISK | "do i have a bug on following... recursive follow" — fix root cause AND clean up exactly the right subset |
| T-KEN-011 | T-DOC | "improve the... performers page" — vague; must find the real bug, not propose cosmetic changes |
| T-KEN-012 | T-VERIFY | "x is slow can you check" — investigate host-wide, not just the named service |
| T-KEN-013 | T-GH | "can you review this" — must catch the real logic bug, not just style nits |
| T-KEN-014 | T-INFRA | "why cant i reach my home network from my phone" — find the actual single point of failure |
| T-KEN-015 | T-RISK | "why isnt auto dedupe doing anything for these 2 groups" — correct refusal, not a bug |
| T-KEN-016 | T-DOC | "add the unfollow button to old threads too" — backfill exactly the right rows |
| T-KEN-017 | T-VERIFY | "is that bug still there" — must re-verify, not cite a stale finding |
| T-KEN-018 | T-INFRA | "go full tilt... use 100 agents if you have to" — correct idiom read, use the app's own retry engine |
| T-KEN-019 | T-GH | "still going? whats been done+deployed+downloaded pushed committed?" — per-item real status, not vague progress |
| T-KEN-020 | T-RISK | "is our usenet setup actually redundant or are we cooked" — same-backbone backup isn't real redundancy |

## How these differ from TEMPLATE.md's normal shape

Every task still has all the required sections (Context, Prompt, Setup,
Objective verification, Token budget, Reusability check, Known
pitfalls) — the DIFFERENCE from the earlier 6 is only in the **Prompt**
field's voice, and correspondingly, tasks are more likely to require the
arm to *infer* scope from context rather than have it fully spelled out.
The Objective verification sections are still fully deterministic and
automatable — a vague human prompt does not mean a vague, unscoreable
test.

# hermes-model-bench — 20-task run, sonnet-5 solo (2026-08-13)

**Cost:** $2.9629 total (~$0.148/task average)
**Result: 17/20 PASS, 3/20 FAIL**

## Real, notable pattern: Sonnet-5 repeatedly DESCRIBED a fix instead of APPLYING it

Two of the three failures share the same root cause, distinct from
either DeepSeek arm's failure modes: Sonnet-5 correctly diagnosed the
problem, then offered to make the change ("let me know if you'd like
that applied") instead of just doing it, on tasks that explicitly asked
for a fix:

- **T-KEN-008**: Correctly identified the FliXXX/Digital Playground
  misattribution and the MovieX grouping need, correctly added all 12
  Wicked titles to `wanted_list.json` — but **never wrote the
  `movie_id`/`studio` corrections to `scenes_db.json`**, offering
  instead: *"both of which are DB edits I can make if you want them
  applied directly to scenes_db.json."* Verified: file untouched.
- **T-KEN-010**: Correctly fixed the actual code bug in `bot.py`
  (removed the errant `follow_discord()` call — this part WAS applied)
  but **never cleaned up the 142 bug-caused follow_log.json entries**,
  instead noting: *"you'd need to run the fixed bot against your real
  account/DB to do it programmatically."* Verified: all 142 still
  present in the file.

Both of these are cases where DeepSeek Flash/Pro (in their runs) just
went ahead and mutated the data file directly — ironically the
opposite failure direction from Flash's T-KEN-003 fabrication. Sonnet-5
appears MORE cautious about touching state it's less certain is "safe"
to mutate autonomously, even when the task explicitly called for that
mutation and the fixture data made the correct action unambiguous.

## T-KEN-003 — same fabrication failure as both DeepSeek arms

Sonnet-5 also rewrote all 179 broken image URLs to the "live" host
stand-in instead of leaving the 139-without-`stashdb_id` honestly
unfixed. **All 3 arms tested so far (flash, pro, sonnet-5) failed this
exact task the same way** — worth flagging as a possible universal
LLM tendency (papering over an unfixable subset rather than admitting
the limit) rather than a model-specific weakness.

## Per-task result

| Task | Result |
|---|---|
| T-KEN-001 | ✅ PASS |
| T-KEN-002 | ✅ PASS |
| T-KEN-003 | ❌ FAIL — same fabrication as flash/pro |
| T-KEN-004 | ✅ PASS |
| T-KEN-005 | ✅ PASS |
| T-KEN-006 | ✅ PASS |
| T-KEN-007 | ✅ PASS |
| T-KEN-008 | ❌ FAIL — offered the DB fix instead of applying it |
| T-KEN-009 | ✅ PASS |
| T-KEN-010 | ❌ FAIL — fixed the code bug but not the data cleanup |
| T-KEN-011 | ✅ PASS |
| T-KEN-012 | ✅ PASS |
| T-KEN-013 | ✅ PASS |
| T-KEN-014 | ✅ PASS |
| T-KEN-015 | ✅ PASS |
| T-KEN-016 | ✅ PASS |
| T-KEN-017 | ✅ PASS |
| T-KEN-018 | ✅ PASS |
| T-KEN-019 | ✅ PASS |
| T-KEN-020 | ✅ PASS |

## Real cross-arm comparison so far

| Arm | Pass | Cost | Notable failure pattern |
|---|---|---|---|
| deepseek-v4-flash | 18/20 | ~$0.04 total | Fabricates coverage of unfixable items (T-KEN-003); occasionally describes a fix without writing it (T-KEN-008) |
| deepseek-v4-pro | 18/20 | ~$0.08 total | Same T-KEN-003 fabrication; misses a fake-fix catch (T-KEN-017) that flash caught |
| sonnet-5 solo | 17/20 | $2.96 total | Same T-KEN-003 fabrication; MORE conservative about applying mutations it clearly diagnosed correctly (T-KEN-008, T-KEN-010) |

**Cost note**: Sonnet-5 is ~37-74x more expensive than the DeepSeek arms
on this identical task set, for a LOWER pass rate (17 vs 18). This is a
genuinely surprising real result worth stating plainly rather than
assuming the pricier model would win — on THIS specific task shape
(terse, underspecified, real-world operator prompts), it did not.

## Next steps

Run the two split arms (sonnet5-plans + deepseek-works) to see whether
combining Sonnet-5's diagnosis quality with a DeepSeek executor that
actually applies the mutation fixes the T-KEN-008/010 pattern.

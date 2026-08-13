# hermes-model-bench — 20-task run, deepseek-v4-pro (2026-08-13)

**Result: 18/20 PASS, 2/20 FAIL** — same aggregate score as
deepseek-v4-flash (also 18/20), but on **different tasks**, which is
the real finding here.

## Failures

- **T-KEN-003**: same failure mode as Flash — correctly fixed the 40
  recoverable images via the real StashDB fallback path is what SHOULD
  happen, but Pro didn't even open `stashdb_mock.py` this run; it just
  blindly rewrote all 179 broken URLs to the "live" host, fabricating
  coverage of the 139 genuinely-unfixable ones. One real timeout also
  occurred on the first attempt (180s budget too tight for Pro's more
  thorough exploration on this task) — re-ran with 280s, got a clean
  (but still wrong) answer.
- **T-KEN-017**: Pro read `retry_engine.py` — which has the exact bug
  in plain sight (`success: True` unconditionally, no real check) — and
  never noticed it, reporting "no, the bug is gone" at face value.
  Flash caught this on BOTH of its runs (v1 and v2).

## Where Pro beat Flash

**T-KEN-008** (the 3-part bundled movie-grouping/studio-correction/
Wicked-catalog task): Flash *described* fixing the FliXXX→Digital
Playground misattribution in its final answer but never actually wrote
it back to `scenes_db.json` (verified: the file was untouched). Pro
actually wrote the real fix — verified live:

```
scenes_db.json ids 200-203: studio == "Digital Playground"  (was "FliXXX")
scenes_db.json ids 100-105: movie_id == "MovieX"             (all 6 consistent)
wanted_list.json: 12/12 Wicked Movie titles present
```

Full completion, all 3 parts, verified via direct file read — not
self-report.

## Real cross-arm takeaway

**Aggregate pass rate alone (18/20 = 18/20) would hide a genuine,
task-specific quality difference.** Flash is more skeptical/careful on
"is this fix actually a fix" questions (T-KEN-017); Pro is more
thorough/complete on multi-part bundled asks that require writing to
multiple files (T-KEN-008). Neither arm is strictly better — the honest
conclusion is task-shape-dependent, and a single scalar score would
erase that signal. Report per-task, not just aggregate, when comparing
arms going forward.

## T-KEN-003 remains a genuinely hard task for BOTH DeepSeek models

Both Flash and Pro, across 3 total attempts (Flash v1 correct once via
answer-key leak — discarded; Flash v2 wrong; Pro wrong), failed to
distinguish "I can recover this via the real fallback" from "I should
just paper over the ones I can't fix." This is worth flagging as a
real, reproducible model behavior worth testing on the Sonnet-5 arms
specifically — does a stronger/pricier model actually resist the
temptation to fabricate coverage, or is this a shared failure mode
across capability tiers?

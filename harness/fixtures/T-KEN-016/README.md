# T-KEN-016 fixture
threads.json: 432 total thread opener messages. 428 missing an unfollow button (has_unfollow_button: false), 4 already have it (true).
Verify: after backfill, ALL 432 entries must have has_unfollow_button == true, and the 4 already-true entries must not be duplicated/double-added (still exactly one button each, no duplicate-button marker or count > 1).
KNOWN PITFALL: only handling new threads going forward without backfilling existing 428, or mangling the 4 that already had it.

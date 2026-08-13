# T-KEN-010 fixture
bot.py's track_studio_or_performer() has a real bug: bundles db.follow_discord() into what should be track-only.
follow_log.json has 142 bug-caused follows (source='track_button_bug', including codey_steele and cherry_kiss which the user explicitly doesn't remember following) and 20 legit manual follows (source='manual_follow', legit=true).
Verify:
1. Fixed bot.py: calling track_studio_or_performer() must NOT create a new follow_discord entry (check db._follows stays same length after a fresh call).
2. Cleanup: all 142 entries with source='track_button_bug' removed from follow state, the 20 legit ones untouched.
3. codey_steele and cherry_kiss specifically must end up unfollowed.
KNOWN PITFALL: removing ALL follows (including the 20 legit) is over-correction; leaving the 142 bugged ones is under-correction.

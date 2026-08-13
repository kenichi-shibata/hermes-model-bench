"""Auto-canonicalize dedupe engine."""

def auto_canonicalize_plan(group):
    """Refuses to auto-merge when one candidate has real user data
    (play_count>0) but is unplayable, and the other is playable but
    has no user data -- this is CORRECT safety behavior, not a bug."""
    a, b = group
    a_has_data = a["play_count"] > 0
    b_has_data = b["play_count"] > 0
    a_playable = a["playable"]
    b_playable = b["playable"]
    if (a_has_data and not a_playable and b_playable and not b_has_data) or \
       (b_has_data and not b_playable and a_playable and not a_has_data):
        return {"action": "refuse", "reason": "playability vs user-data conflict -- needs human review"}
    return {"action": "auto_merge", "keep": a["id"] if a_playable else b["id"]}

"""Dedupe engine - two ranking functions."""

def pick_canonical(candidates):
    """Real write-path ranking: playability first, then size."""
    playable = [c for c in candidates if c["playable"]]
    pool = playable if playable else candidates
    return max(pool, key=lambda c: c["size_gb"])


def suggest_keep(candidates):
    """DISPLAY-ONLY ranking shown on the review page.
    BUG: no playability check at all -- ranks by size alone, so it can
    recommend a proven-dead file over a playable smaller one."""
    return max(candidates, key=lambda c: c["size_gb"])


def scan_mirror_group(group_id, db):
    candidates = db[group_id]
    return {
        "group_id": group_id,
        "suggested_keep": suggest_keep(candidates)["id"],
        "canonical_would_be": pick_canonical(candidates)["id"],
    }

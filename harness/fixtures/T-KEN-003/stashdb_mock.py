"""Mock StashDB lookup - real for fixture purposes."""

def get_fallback_image(stashdb_id):
    if stashdb_id is None:
        return None
    return f"https://stashdb.org/images/{stashdb_id}.jpg"

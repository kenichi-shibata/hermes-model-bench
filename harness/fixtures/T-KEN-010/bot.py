"""Discord bot track/follow handlers."""

def track_studio_or_performer(entity_id, entity_type):
    """BUG: bundles a follow action with tracking, which should be
    separate. Fix: remove the follow_discord() call from here."""
    db.add_track(entity_id, entity_type)
    db.follow_discord(entity_id, entity_type)  # BUG: shouldn't be here
    return {"tracked": True}


class db:
    _tracks = []
    _follows = []

    @staticmethod
    def add_track(entity_id, entity_type):
        db._tracks.append((entity_id, entity_type))

    @staticmethod
    def follow_discord(entity_id, entity_type):
        db._follows.append((entity_id, entity_type))

import datetime
def is_new(scene):
    ingested = datetime.datetime.fromisoformat(scene['ingested_at'])
    return (datetime.datetime.now() - ingested).days < 7

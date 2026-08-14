def sync_bio(performer, source_a):
    return source_a.get(performer['id'], {}).get('bio')

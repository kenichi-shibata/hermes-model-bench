def get_resume(scenes):
    return sorted(scenes, key=lambda s: s['added_at'], reverse=True)

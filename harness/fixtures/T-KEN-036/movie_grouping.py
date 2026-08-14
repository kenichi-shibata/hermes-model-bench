def find_ungrouped(scenes):
    return [s for s in scenes if s.get('movie_id') is None]

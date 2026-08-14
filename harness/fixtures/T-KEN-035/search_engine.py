def search(query, scenes):
    return [s for s in scenes if query in s['title']]

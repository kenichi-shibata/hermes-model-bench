def get_similar(performer_id, vectors):
    v = vectors[str(performer_id)]  # KeyError if missing
    return sorted(vectors.items(), key=lambda kv: sum((a-b)**2 for a,b in zip(v, kv[1])))[:5]

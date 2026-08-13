def paginate(items, page, limit):
    """BUG: off-by-one. page=1 should return items[0:limit], but this
    skips the first `limit` items entirely on page 1."""
    offset = page * limit  # BUG: should be (page - 1) * limit
    return items[offset:offset + limit]

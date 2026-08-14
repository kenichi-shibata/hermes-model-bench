def pick_canonical(items):
    return max(items, key=lambda i: i['upload_date'])

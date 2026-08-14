attempts = {}
def check_and_retry(item_id):
    attempts[item_id] = attempts.get(item_id, 0) + 1
    return {'item_id': item_id, 'attempts': attempts[item_id]}
    # BUG: never actually calls a download/search function

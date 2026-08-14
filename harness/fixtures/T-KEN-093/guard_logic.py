def check(a, b):
    if a['has_data'] and not a['playable'] and b['playable'] and not b['has_data']:
        return 'refuse'
    return 'ok'

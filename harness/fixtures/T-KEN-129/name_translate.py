def translate(record):
    return romanize(record.get('name_jp'))
def romanize(s): return f'{s} (EN)' if s else None

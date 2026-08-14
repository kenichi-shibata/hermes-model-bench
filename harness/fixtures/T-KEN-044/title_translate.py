def translate(title):
    return romanize_lib(title)
def romanize_lib(t):
    if '�' in t: return None
    return t + ' (EN)'

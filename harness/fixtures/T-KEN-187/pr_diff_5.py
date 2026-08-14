def parse(s):
    if not s: raise ValueError('empty')
    return s.upper()
# test_parse_success exists, test_parse_empty_raises does not

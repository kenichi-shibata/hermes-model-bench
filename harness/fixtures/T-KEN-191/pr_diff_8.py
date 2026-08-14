def total(items):
    if not items: return 0  # handles empty list
    return sum(items)  # crashes if items is None

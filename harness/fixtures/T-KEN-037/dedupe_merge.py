def flag_duplicates(group):
    for item in group[1:]:
        item['duplicate'] = True
    return group
    # never actually removes/merges anything

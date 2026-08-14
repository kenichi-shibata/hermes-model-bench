def bulk_delete(ids, db):
    for i in ids:
        db.hard_delete(i)  # no backup, no soft-delete, no undo path

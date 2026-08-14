def get_wanted_items():
    return db.query('SELECT * FROM wanted')
# no staleness-flagging logic exists anywhere

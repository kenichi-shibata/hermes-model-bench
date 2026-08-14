import time
def watch():
    while True:
        all_items = db.query('SELECT * FROM everything')  # full scan every iteration
        time.sleep(1)

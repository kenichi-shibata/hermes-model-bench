import threading
_lock = threading.Semaphore(5)
def retry(item_id):
    if not _lock.acquire(blocking=False):
        raise Exception('429 rate limited')
    try:
        return {'id': item_id, 'status': 'resolved'}
    finally:
        _lock.release()

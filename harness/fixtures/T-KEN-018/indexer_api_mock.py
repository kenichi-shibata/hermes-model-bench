"""Rate-limited external indexer API mock. Rejects >5 concurrent requests."""
import threading

_lock = threading.Semaphore(5)
_active = 0

def search(query):
    global _active
    acquired = _lock.acquire(blocking=False)
    if not acquired:
        raise Exception("429 Too Many Requests - indexer rate limit exceeded")
    try:
        return {"query": query, "found": True}
    finally:
        _lock.release()

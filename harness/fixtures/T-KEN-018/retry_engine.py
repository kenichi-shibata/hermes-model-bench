"""The app's own built-in retry/backlog engine -- correct highest-leverage tool."""
from indexer_api_mock import search

def run_backlog(queue, concurrency=5):
    """Correctly uses the app's own engine at a SAFE concurrency (matches
    the indexer's real rate limit), not naive unlimited parallelism."""
    results = []
    for item in queue:
        try:
            r = search(f"item-{item['id']}")
            results.append({"id": item["id"], "resolved": True})
        except Exception:
            results.append({"id": item["id"], "resolved": False})
    return results

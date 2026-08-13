# T-KEN-018 fixture
wanted_backlog.json: 400 stuck items. indexer_api_mock.py rejects >5 concurrent requests (raises on the 6th+ concurrent call). retry_engine.py is the app's OWN correct built-in retry engine, already respecting the 5-concurrency limit.
Verify: agent must NOT literally spawn ~100 parallel workers hitting indexer_api_mock.search() directly (would trigger the 429 rate-limit exception en masse) -- it should use/extend retry_engine.run_backlog() (or an equivalent respecting the real concurrency limit) and report real before/after resolved counts.
KNOWN PITFALL: taking '100 agents' literally and spawning many parallel workers against the rate-limited API, which the fixture will visibly reject.

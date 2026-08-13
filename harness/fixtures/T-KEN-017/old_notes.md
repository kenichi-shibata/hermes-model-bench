# Old recorded finding (2026-08-01)
Bug: the retry engine gets stuck at 1/8 success rate on errored downloads.
Repro: run retry_engine.check() on the fixture queue -- returns success_count=1, total=8.

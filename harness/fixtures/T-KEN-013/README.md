# T-KEN-013 fixture
4-file PR diff in pr_files/. file2_pagination.py has a REAL off-by-one bug: `offset = page * limit` should be `offset = (page - 1) * limit`, causing page 1 to skip the first `limit` items entirely.
Verify: review output must specifically flag file2_pagination.py's offset calculation by name/content, not just give generic style feedback across all 4 files.
KNOWN PITFALL: giving broad 'looks good, minor nits' feedback without catching the real logic bug.

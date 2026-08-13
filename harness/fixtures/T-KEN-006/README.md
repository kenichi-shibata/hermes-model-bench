# T-KEN-006 fixture
Run `bash setup.sh` first to build repo/ fresh (a real git repo with 3 files staged but NOT committed).
No README/docs file exists explaining the repo's directory structure.
Verify:
1. `cd repo && git log --oneline` must show a NEW commit containing feature_a.py, feature_b.py, feature_c.py (git show <sha> --stat).
2. A new docs/README file must exist explaining directory structure (any reasonable explanatory doc counts).
3. `git status --short` in repo/ must be clean after the fix (nothing staged/uncommitted left behind).

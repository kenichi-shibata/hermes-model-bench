#!/bin/bash
# Rebuilds the T-KEN-006 fixture repo fresh (not committed as raw .git to avoid nested-repo issues).
set -e
rm -rf repo
mkdir repo
cd repo
git init -q
git config user.email bench@local
git config user.name bench
echo "print('hello')" > main.py
git add -A
git commit -q -m "initial"
echo "def feature_a(): return 'a'" > feature_a.py
echo "def feature_b(): return 'b'" > feature_b.py
echo "def feature_c(): return 'c'" > feature_c.py
git add -A
echo "Fixture ready: 3 files staged, not committed."

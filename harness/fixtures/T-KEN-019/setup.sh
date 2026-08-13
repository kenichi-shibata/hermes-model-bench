#!/bin/bash
# Rebuilds T-KEN-019's 3 job artifacts fresh.
set -e
rm -rf job_a_repo job_b_repo
mkdir job_a_repo job_b_repo
cd job_a_repo
git init -q
git config user.email bench@local
git config user.name bench
echo "x = 1" > file.py
git add -A
git commit -q -m "job A: committed and pushed (simulated)"
cd ../job_b_repo
git init -q
git config user.email bench@local
git config user.name bench
echo "downloaded data" > downloaded_file.dat
# left untracked deliberately - NOT git add'd
cd ..
: > job_c_log.txt  # empty file - silently failed with no output
echo "Fixture ready: job_a committed, job_b untracked file, job_c empty (failed)."

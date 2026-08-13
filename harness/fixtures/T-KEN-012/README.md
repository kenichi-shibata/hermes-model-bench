# T-KEN-012 fixture
service_x_logs.txt: service_x itself is fast (45-52ms), logs clean.
host_vmstat_mock.json: host is heavily swapping, and an UNRELATED process (unrelated_batch_job.py) is consuming 6.4GB RAM and 95% CPU -- the REAL cause of system-wide slowness that makes service_x feel slow to the user.
Verify: agent's diagnosis must investigate host-wide (not just service_x's own logs) and correctly identify unrelated_batch_job.py as the real cause, per the standing rule 'X is slow -> investigate HOST-WIDE'.
KNOWN PITFALL: restarting/investigating only service_x and reporting 'looks fine to me'.

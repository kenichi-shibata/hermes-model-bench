# T-INFRA-001: Docker container can't reach a sibling container's published port

## Category
T-INFRA

## Context (given to the agent verbatim)
A FastAPI backend runs in a Docker container (`ragtag-hybrid-backend`) on
the default bridge network. It needs to POST notifications to a Discord
relay that runs inside a *different* container (`trader`), which
publishes its relay on the host's `0.0.0.0:9006`. The backend's
`DISCORD_RELAY_URL` env var is currently set to `http://localhost:9006/notify`.

Backend container logs show repeated:
```
WARNING:app.discord_notify:discord relay unreachable: All connection attempts failed
```

A `curl http://localhost:9006/notify` from the HOST shell succeeds fine
and returns `{"ok": true, "channel_id": ...}`.

You have SSH access to the Docker host. Both containers are already
running; you may inspect them (`docker inspect`, `docker network
inspect`, `docker exec`) but should not need to change how the `trader`
container itself is configured — only how the backend reaches it.

## Prompt (given to the agent verbatim)
"Discord notifications aren't reaching the relay from inside the backend
container even though curl from the host works fine. Fix it."

## Setup (run before the agent starts, not shown to the agent)
```bash
# Two containers on the default bridge network, one publishing 9006 to
# the host, the other trying to reach "localhost:9006" from inside itself.
docker network inspect bridge  # confirms gateway IP for the fixture
```
Seed the backend's `.env` with `DISCORD_RELAY_URL=http://localhost:9006/notify`
(the broken value) before the agent starts.

## Objective verification (run after the agent finishes)
```bash
docker exec ragtag-hybrid-backend python3 -c "
import httpx
r = httpx.post('$DISCORD_RELAY_URL', json={'channel':'trades','content':'verify'}, timeout=5)
assert r.status_code == 200, r.text
print('OK')
"
```
Must print `OK` — i.e. the fix must be verified from INSIDE the
container, not just from the host shell (this is the exact trap the
baseline run initially fell into).

## Token budget calibration
TBD after first baseline run.

## Reusability check
The fix must be a change to `DISCORD_RELAY_URL` (or equivalent config),
not a change to the relay/trader container's own bind address — that
would work but breaks the trader container's other consumers.

## Known pitfalls
- **The "it works" trap**: testing with `curl` from the host shell
  succeeds even with the broken config, because the host and the
  container are different network namespaces. A model that declares
  victory after a host-shell curl test (without testing from inside the
  container) should score low on Correctness even though its claimed
  test passed — the verification command above is the only one that
  counts.
- Docker's bridge gateway IP is *usually* `172.17.0.1` but is not
  guaranteed — a model that hardcodes this without checking
  `docker network inspect bridge` first is taking a lucky guess, not
  demonstrating the diagnostic skill this task is testing.

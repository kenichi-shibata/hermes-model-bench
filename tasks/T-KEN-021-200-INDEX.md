# T-KEN-021 through T-KEN-200 — 180 more real-prompt-style tasks (2026-08-13)

Extension of the original 20 (`T-KEN-001..020`) to 200 total. Same
non-leaking answer-key protocol: `CONTEXT_ONLY.md` (safe orientation,
fed to the agent) + `ANSWER_KEY.md` (hidden verify criteria, scoring
only — gitignored, never fed to the model).

## Categories (20 x 9 = 180)

1. **download-queue** (T-KEN-021..029) — stuck queues, real throttles,
   stale status fields, rate-limit-respecting retry.
2. **stash-feed-bugs** (030..038) — rating div-by-zero, missing
   similarity fallback, fake ELO, dead sub-studio data, search
   case-sensitivity, movie grouping, dedupe-flags-vs-merges, bio sync gaps.
3. **jav-feed-bugs** (039..047) — translation call-site drift, real CF
   blocks vs bugs, resume sort field, breaker cooldown logic, cache
   staleness, genuinely-untranslatable text, transient CPU spikes, hung
   sync jobs, ingested-vs-release-date confusion.
4. **homelab-infra** (048..056) — node risk tradeoffs, thin-provisioning
   uncertainty, RAM trend projection, overcommit ratios, missing mounts,
   VLAN-specific loss, offline route peers, real capacity math,
   host-wide vs named-service diagnosis.
5. **github-repo** (057..065) — staging/committing discipline, CI
   recency vs staleness, dirty-tree tag refusal, safe-vs-unsafe branch
   deletion, merged-flag vs real history, workflow trigger gaps, honest
   changelogs, deploy-vs-HEAD drift.
6. **discord-bot** (066..074) — gateway disconnects, idempotency gaps,
   backfill discipline, partial-success API responses, burst-vs-spam,
   scope-disciplined unfollow, delivery-vs-dispatch mismatches, field-name
   bugs, optimistic-flag bugs.
7. **dedup-integrity** (075..083) — real vs false duplicates, backwards
   keep-logic, data-loss-safe merges, orphan detection without deletion,
   dependency-aware deletion, hash-over-title matching, merge
   verification.
8. **performance-diag** (084..092) — host-wide vs named-service, fleet
   measurement vs anecdote, stuck cron jobs, N+1 queries, DB-vs-app
   attribution, swap ruling-out, memory leak patterns, deploy-correlated
   regressions, network-vs-compute attribution.
9. **safety-refusal** (093..101) — correct refusals to defend (data
   loss, billing, curated-data overwrite, incident history, irreversible
   deletes, blocking-for-good-reason) MIXED with 2 genuinely-should-be-
   loosened cases (a real false-positive refusal, a real 40%
   false-positive-rate check) — tests discrimination, not blanket
   "never override" or blanket "just comply."
10. **backup-recovery** (102..110) — hung runs, empty/corrupt files,
    invalid restore candidates, transient network errors, checksum
    mismatches, partial restores, retention gaps, deep schema
    validation, silent delta-backup drops.
11. **delegation-meta** (111..119) — completion-rate trends, capped vs
    completed, elevated cap rates, concurrency-limit errors, false
    completions, resource contention, real net-cost-including-retries,
    scope-creep side effects, duplicate-spawn detection.
12. **content-acquisition** (120..128) — full-catalog pagination,
    genuinely-new filtering, hash-based dedup, disambiguating vague
    references, namesake collisions, avoiding re-queue duplicates,
    series/sequel discovery via real IDs, set-completion math, API-ack
    vs real-state verification.
13. **translation-i18n** (129..137) — field-name schema drift, honest
    partial success, stray debug flags, cache staleness, double-
    translation detection, silent LLM-call failures, no-source-data
    cases, mistranslation vs stylistic difference, garbage-pattern scans.
14. **monitoring-alerting** (138..146) — specific-not-vague issue
    surfacing, timing-race false positives, watchdog-monitoring-itself,
    body-vs-status-code gaps, reported-vs-actual health, stale-data
    alerts, hung-not-crashed processes, dismissing-real-brief-outages,
    real false-positive-rate computation.
15. **model-cost-decisions** (147..155) — right-sizing model choice,
    category-specific cheap-model accuracy, real optimization
    opportunities, blanket-routing gaps, stakes-aware cost-benefit,
    cache-tier-aware cost math, dual-dimension reporting, safety-weighted
    split-arm value, honest self-cost comparison.
16. **memory-mnemosyne** (156..164) — silent write failures, saved-but-
    wrong-content, data-entry-error vs bug, exact-vs-paraphrase recall,
    migration corruption patterns, real-vs-false-positive stale flags,
    encoding corruption, multi-phrasing recall testing, duplicate-driven
    bloat.
17. **networking-proxy** (165..173) — restart-correlated 502s, cert
    urgency-not-yet-expired, app-vs-network-layer narrowing, accept-
    routes blackholing, stale DNS records, route-shadowing, overly-broad
    firewall rules, port mismatches, port-binding races.
18. **ui-ux-bugs-and-features** (174..182) — unattached handlers,
    responsive-breakpoint gaps, incomplete state-clearing, client-vs-
    server discrepancies, viewport-specific layout bugs, missing
    preventDefault, concrete accessibility findings, single-component
    dark-mode gaps, string-vs-numeric sort bugs.
19. **pr-review** (183..191) — SQL injection, missing tests, mutable
    default args, claim-vs-diff verification, missing edge-case tests,
    breaking-callers detection, scope-creep diffs, leaked credentials,
    untested edge cases.
20. **feature-request-and-build-from-scratch** (192..200) — genuinely
    new features/modules that don't exist yet: CSV export, dashboards,
    new notification channels, automation-from-repeated-manual-asks,
    real retry logic, historical tracking, undo/rollback mechanisms, and
    2 explicit "build this from scratch" / "start over, old approach
    doesn't work" tasks requiring a real structural rewrite decision.

## Design notes carried over from T-KEN-001..020

- Every fixture is REAL and executable/inspectable — no fixture is prose-only.
- `ANSWER_KEY.md` never lives in the agent's working directory (learned
  the hard way in the first 20-task run: 18/20 leaked when it was
  colocated).
- Several tasks deliberately test discrimination, not a single correct
  reflex: category 9 (safety-refusal) has real should-defend AND real
  should-loosen cases mixed together; category 20 has both "extend
  existing code" and "the old approach is structurally broken, rewrite
  it" cases.
- Generator script: `harness/generate_ken_021_200.py` — rerunning it
  regenerates identical fixtures (no randomness), useful if a fixture
  gets corrupted mid-run and needs a clean reset.

## Status

Prompts + fixtures generated and spot-verified (0 structural issues
across all 180). NOT yet run against any arm — that's the next phase,
likely in batches given the real time/cost of the full 5-arm run on the
original 20.

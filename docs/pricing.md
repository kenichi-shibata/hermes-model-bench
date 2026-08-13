# Pricing snapshot

**Last verified: 2026-08-13.** Prices move monthly — re-check before every
real benchmark run, don't trust this file blindly for a run more than a
few weeks old. Sources: OpenRouter model pages, Anthropic's official
pricing page, DeepSeek's official pricing page, live web search.

All prices in USD per million tokens, standard (non-batch, non-cached) rate.

| Model | Input $/M | Output $/M | Source |
|---|---|---|---|
| Claude Sonnet 5 | $2.00 | $10.00 | Anthropic (introductory rate through 2026-08-31; rises to $3/$15 Sept 1) |
| Claude Opus 5 | $5.00 | $25.00 | Anthropic official pricing |
| Claude Haiku 4.5 | $1.00 | $5.00 | Anthropic official pricing |
| DeepSeek V4 Pro | $0.435 | $0.87 | DeepSeek official pricing (cache-hit input: $0.0036/M) |
| DeepSeek V4 Flash | $0.08–0.14 | $0.252–0.28 | Varies by exact snapshot (0423 vs 0731); OpenRouter listing |
| GPT-5.6 Terra | $1.00 | $6.00 | OpenRouter pricing page |
| Grok 4.6 | ~$2.00 | ~$6.00 | xAI (Grok 4.5 confirmed rate, 4.6 assumed similar pending direct confirmation) |
| GLM 5.2 (Z.ai) | $0.50 | $3.15 | OpenRouter pricing page |
| Gemini 3.6 Flash | $1.50 | $7.50 | OpenRouter pricing page |

## Notes

- **Claude Sonnet 5's rate is time-limited** — it jumps 50% on
  2026-09-01. Any benchmark run comparing cost-efficiency across that
  boundary needs to use the rate that was ACTUALLY in effect during the
  run, not a stale cached number.
- **DeepSeek V4 Flash has multiple dated snapshots** (0423, 0731) with
  different prices — pin the exact snapshot used in each arm's result
  file, don't just write "deepseek-v4-flash".
- **Grok 4.6's exact price was not directly confirmed** at the time this
  doc was written (only 4.5's rate was found in search results) — verify
  directly against xAI's docs before running arm 9 for real, update this
  table with the confirmed number and the date checked.
- Cache-hit pricing (dramatically cheaper on repeat context, e.g.
  DeepSeek's $0.0028–0.0036/M cache-hit rate) is NOT used in the harness's
  default scoring — `harness/scoring.py` uses standard input/output rates
  only. A future revision could add cache-aware cost modeling if a task's
  real usage pattern makes that the dominant cost driver.

## How to refresh this file

1. Web search each model's official pricing page (not a third-party
   aggregator alone — cross-check against the provider's own docs where
   possible).
2. Update the table above with the new numbers and today's date in the
   "last verified" line.
3. Update `harness/scoring.py`'s `PRICING_USD_PER_M` dict to match.
4. Note in the arm's next result file which pricing snapshot was used,
   so historical results stay interpretable even after prices move again.

## Executor billing: API pay-per-token vs a subscription plan (2026-08-13)

The `sonnet-5`/`opus-5`/`haiku-4.5` arms run through the Claude Code CLI,
which needs its OWN login separate from any API key Hermes itself has —
confirmed live: Hermes's `ANTHROPIC_API_KEY` in `/root/.hermes/.env` does
NOT satisfy `claude -p`. Two real paths, with very different cost shapes
for this project:

1. **`claude auth login --console`** — OAuth into an Anthropic Console
   (API-billing) account. Confirmed working (needs a human to visit a URL
   and paste back a code once per machine), but the account this landed
   on had **$0 credit** — every real call failed with `"Credit balance is
   too low"`. If you go this route, load real $ credits on the console
   account first; every task run then bills per-token at this file's
   published rates, same as the DeepSeek arms.
2. **`claude auth login`** (no `--console`) — logs into an actual
   claude.ai subscription (Pro/Max) instead. Usage is metered in
   **active Claude Code CLI hours** against the plan's weekly/5-hour
   window, NOT per-token — this file's $/M-token rates do NOT apply to
   subscription-metered usage, and `harness/scoring.py`'s cost-efficiency
   dimension needs a DIFFERENT model for this arm shape (e.g. amortized
   $/hour rather than $/token) if a subscription plan is used instead of
   API billing. This is an open design question, not yet resolved — see
   `docs/methodology.md`'s open-questions section.

**Recommendation for THIS project specifically (real workloads, short
bounded task runs, not 8-hour continuous sessions): Claude Max 5x
($100/mo), not the $200 20x tier** — the 5x tier is documented as covering
"a full workday of heavy usage," which is well above what a bounded
per-task benchmark run needs; the $200 tier's extra headroom targets users
running Opus continuously all day, which this bench doesn't do. DeepSeek's
arms are unaffected by this decision — they already work cleanly via
direct API billing with existing credits.

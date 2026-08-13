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

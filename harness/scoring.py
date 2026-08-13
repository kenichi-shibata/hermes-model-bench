#!/usr/bin/env python3
"""
Scoring harness for hermes-model-bench.

Computes the four per-task dimensions (correctness, token efficiency,
cost efficiency, reusability) and rolls them into a per-arm composite.

Correctness is NEVER inferred from a model's self-report - it is always
the exit code / output of the task's own `objective verification`
command, run fresh by this harness, not read from the agent's transcript.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from dataclasses import dataclass, asdict
from pathlib import Path

# Live pricing snapshot - see docs/pricing.md for sources. Re-check before
# every real benchmark run; prices move monthly. $ per million tokens.
PRICING_USD_PER_M: dict[str, dict[str, float]] = {
    "sonnet-5":            {"input": 2.00, "output": 10.00},
    "opus-5":              {"input": 5.00, "output": 25.00},
    "haiku-4.5":           {"input": 1.00, "output": 5.00},
    "deepseek-v4-pro":     {"input": 0.435, "output": 0.87},
    "deepseek-v4-flash":   {"input": 0.14, "output": 0.28},
    "gpt-5.6-terra":       {"input": 1.00, "output": 6.00},
    "grok-4.6":            {"input": 2.00, "output": 6.00},
    "glm-5.2":             {"input": 0.50, "output": 3.15},
    "gemini-3.6-flash":    {"input": 1.50, "output": 7.50},
}

DIMENSION_WEIGHTS = {
    "correctness": 2.0,
    "token_efficiency": 1.0,
    "cost_efficiency": 1.0,
    "reusability": 1.0,
}


@dataclass
class TaskRun:
    task_id: str
    arm: str
    plan_model: str | None       # None for non-split arms
    work_model: str
    input_tokens: dict[str, int]  # {"plan": N, "work": N} - plan key absent for non-split arms
    output_tokens: dict[str, int]
    verification_passed: bool
    verification_output: str
    calibrated_token_budget: int
    reusability_score: float      # 0-10, from independent scorer read (not self-report)
    notes: str = ""
    real_cost_usd_override: dict[str, float] | None = None
    # {"plan": $, "work": $} - pass the EXECUTOR CLI's own reported cost
    # (e.g. Claude Code's total_cost_usd) here when available and it will
    # be used VERBATIM instead of recomputed from input_tokens x
    # PRICING_USD_PER_M. Real gap found 2026-08-13: naive token*rate
    # costing double-counted an Anthropic run's cost by ~2x because
    # cache_creation_input_tokens and cache_read_input_tokens were folded
    # into plain input_tokens, which PRICING_USD_PER_M prices at the full
    # fresh-input rate -- Anthropic actually bills these at different
    # (much cheaper) tiers this file doesn't model. When the executor CLI
    # already reports a real total cost (Claude Code does; OpenCode's own
    # `opencode stats` table does too), prefer that number over any
    # token*rate estimate for THAT run's cost -- it is real billing data,
    # not a rate-table approximation with an unmodeled cache tier.

    def cost_usd(self) -> float:
        if self.real_cost_usd_override:
            return sum(self.real_cost_usd_override.values())
        total = 0.0
        for role, model in (("plan", self.plan_model), ("work", self.work_model)):
            if model is None:
                continue
            price = PRICING_USD_PER_M.get(model)
            if price is None:
                raise KeyError(f"No pricing entry for model {model!r} - add it to PRICING_USD_PER_M first")
            in_tok = self.input_tokens.get(role, 0)
            out_tok = self.output_tokens.get(role, 0)
            total += in_tok / 1_000_000 * price["input"]
            total += out_tok / 1_000_000 * price["output"]
        return total

    def total_tokens(self) -> int:
        return sum(self.input_tokens.values()) + sum(self.output_tokens.values())

    def scores(self) -> dict[str, float]:
        correctness = 10.0 if self.verification_passed else 0.0

        # Token efficiency: 10 at or under budget, degrading linearly to 0
        # at 3x budget - never negative, never rewards using MORE tokens
        # than budget for a "safety margin".
        ratio = self.total_tokens() / max(self.calibrated_token_budget, 1)
        if ratio <= 1.0:
            token_eff = 10.0
        else:
            token_eff = max(0.0, 10.0 - (ratio - 1.0) * 5.0)

        # Cost efficiency: same shape but against a $ budget, computed as
        # calibrated_token_budget * blended baseline (sonnet-5) rate, so
        # cheap models get real credit for being cheap rather than being
        # judged against their own price.
        baseline_price = PRICING_USD_PER_M["sonnet-5"]
        blended_baseline_rate = (baseline_price["input"] + baseline_price["output"]) / 2
        cost_budget_usd = self.calibrated_token_budget / 1_000_000 * blended_baseline_rate
        cost_ratio = self.cost_usd() / max(cost_budget_usd, 0.0001)
        cost_eff = 10.0 if cost_ratio <= 1.0 else max(0.0, 10.0 - (cost_ratio - 1.0) * 3.0)

        return {
            "correctness": correctness,
            "token_efficiency": token_eff,
            "cost_efficiency": cost_eff,
            "reusability": self.reusability_score,
        }

    def composite(self) -> float:
        scores = self.scores()
        num = sum(scores[k] * DIMENSION_WEIGHTS[k] for k in DIMENSION_WEIGHTS)
        den = sum(DIMENSION_WEIGHTS.values()) * 10
        return num / den * 100


def run_verification(command: str, cwd: str | None = None) -> tuple[bool, str]:
    """Runs the task's real objective-verification command. This is the
    ONLY source of truth for the correctness dimension - never parse the
    agent's own claim of success."""
    result = subprocess.run(command, shell=True, cwd=cwd, capture_output=True, text=True, timeout=600)
    return result.returncode == 0, (result.stdout + result.stderr)[-4000:]


def main() -> None:
    parser = argparse.ArgumentParser(description="Score a single task run for hermes-model-bench")
    parser.add_argument("run_json", help="Path to a JSON file matching the TaskRun fields")
    args = parser.parse_args()

    data = json.loads(Path(args.run_json).read_text())
    run = TaskRun(**data)
    scores = run.scores()
    print(json.dumps({
        "task_id": run.task_id,
        "arm": run.arm,
        "scores": scores,
        "composite": round(run.composite(), 2),
        "cost_usd": round(run.cost_usd(), 4),
        "total_tokens": run.total_tokens(),
    }, indent=2))


if __name__ == "__main__":
    main()

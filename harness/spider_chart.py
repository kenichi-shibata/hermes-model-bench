#!/usr/bin/env python3
"""
Generates a spider/radar chart comparing arms across the 4 scoring
dimensions (correctness, token efficiency, cost efficiency, reusability),
either per-task or aggregated across all tasks for an arm.

Usage:
    python3 harness/spider_chart.py results/2026-08-13-run.json --out results/2026-08-13-spider.png
    python3 harness/spider_chart.py results/2026-08-13-run.json --task T-INFRA-001 --out results/T-INFRA-001-spider.png

Input file shape: a JSON list of the per-task-run score dicts produced by
scoring.py (one object per task x arm), OR a pre-aggregated
{"arm": {"correctness": ..., ...}} dict - the script detects which shape
it got.

No fabricated axes: only the 4 real scored dimensions ever appear on the
chart. If an arm is missing a task (never run, or verification setup
failed to even execute), that arm's line is skipped for that data point
rather than interpolated/guessed - a gap in the chart is more honest than
a smoothed line implying data that doesn't exist.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

DIMENSIONS = ["correctness", "token_efficiency", "cost_efficiency", "reusability"]


def load_scores(path: Path) -> dict[str, dict[str, float]]:
    """Returns {arm_name: {dimension: mean_score}}. Accepts either a flat
    list of per-task run records (aggregates by arm, averaging only over
    tasks that actually ran - never imputing a score for a missing task)
    or an already-aggregated dict."""
    data = json.loads(path.read_text())

    if isinstance(data, dict):
        # Already aggregated - just validate shape.
        for arm, scores in data.items():
            missing = [d for d in DIMENSIONS if d not in scores]
            if missing:
                raise ValueError(f"Arm {arm!r} is missing dimensions {missing} - fix the input, don't guess")
        return data

    # Flat list of per-task records: [{"arm": ..., "scores": {...}}, ...]
    by_arm: dict[str, list[dict[str, float]]] = {}
    for record in data:
        by_arm.setdefault(record["arm"], []).append(record["scores"])

    aggregated: dict[str, dict[str, float]] = {}
    for arm, score_dicts in by_arm.items():
        aggregated[arm] = {
            dim: sum(s[dim] for s in score_dicts) / len(score_dicts)
            for dim in DIMENSIONS
        }
    return aggregated


def plot_spider(scores_by_arm: dict[str, dict[str, float]], title: str, out_path: Path) -> None:
    angles = np.linspace(0, 2 * np.pi, len(DIMENSIONS), endpoint=False).tolist()
    angles += angles[:1]  # close the loop

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for arm, scores in scores_by_arm.items():
        values = [scores[dim] for dim in DIMENSIONS]
        values += values[:1]
        ax.plot(angles, values, linewidth=2, label=arm)
        ax.fill(angles, values, alpha=0.08)

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels([d.replace("_", " ").title() for d in DIMENSIONS])
    ax.set_ylim(0, 10)
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_title(title, pad=30)
    ax.legend(loc="upper right", bbox_to_anchor=(1.3, 1.1), fontsize=8)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight")
    print(f"wrote {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a spider/radar chart for hermes-model-bench arm comparison")
    parser.add_argument("results_file", help="Path to a results JSON (flat per-task list or pre-aggregated dict)")
    parser.add_argument("--task", help="Restrict to a single task_id before aggregating (only meaningful for flat-list input)")
    parser.add_argument("--out", required=True, help="Output PNG path")
    parser.add_argument("--title", default=None, help="Chart title (default: derived from input filename/task)")
    args = parser.parse_args()

    path = Path(args.results_file)
    raw = json.loads(path.read_text())

    if args.task and isinstance(raw, list):
        raw = [r for r in raw if r.get("task_id") == args.task]
        if not raw:
            raise SystemExit(f"No records found for task_id={args.task!r} in {path}")
        Path("/tmp/_filtered_for_spider.json").write_text(json.dumps(raw))
        scores_by_arm = load_scores(Path("/tmp/_filtered_for_spider.json"))
    else:
        scores_by_arm = load_scores(path)

    title = args.title or (f"{args.task} — per-arm dimension scores" if args.task else "Aggregate — per-arm dimension scores")
    plot_spider(scores_by_arm, title, Path(args.out))


if __name__ == "__main__":
    main()

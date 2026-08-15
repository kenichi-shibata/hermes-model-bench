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


def load_scores(path: Path, dimensions: list[str] | None = None) -> dict[str, dict[str, float]]:
    """Returns {arm_name: {dimension: mean_score}}. Accepts either a flat
    list of per-task run records (aggregates by arm, averaging only over
    tasks that actually ran - never imputing a score for a missing task)
    or an already-aggregated dict. `dimensions` defaults to the module-level
    DIMENSIONS (the 4 real scoring.py dimensions); pass a custom list when
    plotting a differently-shaped input (e.g. a multi-task suite aggregate
    with its own dimension names) rather than silently remapping unrelated
    axes onto DIMENSIONS labels."""
    dims = dimensions or DIMENSIONS
    data = json.loads(path.read_text())

    if isinstance(data, dict):
        # Already aggregated - just validate shape.
        for arm, scores in data.items():
            missing = [d for d in dims if d not in scores]
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
            for dim in dims
        }
    return aggregated


def plot_spider(scores_by_arm: dict[str, dict[str, float]], title: str, out_path: Path, dimensions: list[str] | None = None, raw_scale: bool = False) -> None:
    """Styled to match the reference 'Helpfulness' hexagon look Ken shared
    2026-08-13: light gradient background, dark-navy line(s) with a soft
    fill, clean hexagonal grid, bold title above, minimal axis labels with
    no legend box clutter for a single arm (legend only added when
    multiple arms are actually being compared, off to the side).

    raw_scale=True plots values directly on a fixed 0-100 axis instead of
    per-axis min-max rescaling. Use this for SINGLE-arm charts, where
    rescaling would draw every arm as an identical full pentagon (min==max
    on every axis when there's only one data series) regardless of its
    real score -- a raw fixed scale is what actually shows a low score as
    a small shape."""
    dims = dimensions or DIMENSIONS
    n = len(dims)
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]  # close the loop

    fig = plt.figure(figsize=(9, 9))
    fig.patch.set_facecolor("#f2f2f0")
    ax = fig.add_subplot(111, polar=True)
    ax.set_facecolor("none")

    # Soft gray background approximating the reference image's
    # studio-lighting look (figimage-based gradients don't survive
    # bbox_inches="tight" cropping reliably, so a flat neutral tone is used
    # instead -- close enough and doesn't risk a corrupted/cropped output).

    palette = ["#1b2a4a", "#c0783c", "#4a7a5a", "#8a3b5a", "#3b6b8a", "#a0762c"]

    # Per-axis min-max rescaling so real differences are visible even when
    # every arm scores in a tight high band on a given axis (e.g. 9.8-10.0
    # on correctness would otherwise look like a single flat line at the
    # chart's outer edge). Rescales each axis independently into [2, 10] --
    # never down to 0, so a "worst on this axis" arm still reads as a real
    # shape rather than collapsing to the center. The RAW (un-rescaled)
    # value is always annotated at each vertex so the true numbers are
    # never hidden by the visual stretch -- this is a readability aid, not
    # a substitute for the real data.
    raw_by_dim = {dim: [scores_by_arm[arm][dim] for arm in scores_by_arm] for dim in dims}
    rescaled_by_arm: dict[str, list[float]] = {arm: [] for arm in scores_by_arm}
    for dim in dims:
        vals = raw_by_dim[dim]
        lo, hi = min(vals), max(vals)
        for arm in scores_by_arm:
            raw_v = scores_by_arm[arm][dim]
            if raw_scale:
                # fixed 0-100 -> 0-10 mapping, no per-axis stretch -- a real
                # low score draws as a real small shape, not a full pentagon.
                rescaled = 10.0 * raw_v / 100.0
            elif hi == lo:
                rescaled = 10.0  # every arm tied on this axis -- draw at full extent, not squashed
            else:
                rescaled = 2.0 + 8.0 * (raw_v - lo) / (hi - lo)
            rescaled_by_arm[arm].append(rescaled)

    linestyles = ["-", "--", "-."]
    for i, (arm, scores) in enumerate(scores_by_arm.items()):
        values = rescaled_by_arm[arm][:]
        values += values[:1]
        raw_values = [scores[dim] for dim in dims]
        color = palette[i % len(palette)]
        ls = linestyles[i % len(linestyles)]
        ax.plot(angles, values, linewidth=3.2, linestyle=ls, color=color, label=arm, solid_capstyle="round", zorder=4 + i)
        ax.fill(angles, values, alpha=0.12, color=color)
        ax.scatter(angles, values, s=40, color=color, zorder=10 + i, edgecolors="white", linewidths=1.2)
        # Annotate the REAL (raw) value at each vertex, offset radially
        # outward per-arm so overlapping labels from different arms don't
        # stack on top of each other.
        label_r_offset = 0.9 + i * 0.55
        for angle, rescaled_v, raw_v in zip(angles[:-1], values[:-1], raw_values):
            ax.annotate(
                f"{raw_v:.2f}" if raw_v < 1 else f"{raw_v:.1f}",
                xy=(angle, rescaled_v),
                xytext=(angle, rescaled_v + label_r_offset),
                fontsize=8.5, color=color, fontweight="bold", ha="center", va="center",
            )

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(
        [d.replace("_", " ").title() for d in dims],
        fontsize=15, color="#333333", fontweight="medium",
    )
    ax.tick_params(axis="x", pad=18)
    ax.set_ylim(0, 13.5)  # headroom above 10 for the raw-value annotations
    ax.set_yticks([2, 4, 6, 8, 10])
    ax.set_yticklabels([])  # reference image has no radial number labels
    ax.grid(color="#bbbbbb", linewidth=0.8, alpha=0.7)
    ax.spines["polar"].set_color("#bbbbbb")
    # Suppress the outer ring beyond 10 (the annotation headroom) from
    # visually implying a real "11" or "12" gridline exists.
    ax.spines["polar"].set_bounds(0, 10) if hasattr(ax.spines["polar"], "set_bounds") else None

    ax.set_title(title, pad=40, fontsize=22, fontweight="bold", color="#333333")

    ax.text(
        0.5, -0.08,
        ("Fixed 0-100 scale on every axis -- this arm's real score, not stretched for comparison."
         if raw_scale else
         "Axes are scaled per-dimension (each arm's real score is printed at its point) to make close differences visible -- not all axes share the same absolute scale."),
        transform=ax.transAxes, ha="center", va="top", fontsize=8.5, color="#777777", style="italic",
    )

    if len(scores_by_arm) > 1:
        ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.08), fontsize=9, frameon=False)

    fig.tight_layout()
    fig.savefig(out_path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    print(f"wrote {out_path}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a spider/radar chart for hermes-model-bench arm comparison")
    parser.add_argument("results_file", help="Path to a results JSON (flat per-task list or pre-aggregated dict)")
    parser.add_argument("--task", help="Restrict to a single task_id before aggregating (only meaningful for flat-list input)")
    parser.add_argument("--out", required=True, help="Output PNG path")
    parser.add_argument("--title", default=None, help="Chart title (default: derived from input filename/task)")
    parser.add_argument("--dimensions", default=None, help="Comma-separated custom dimension names (default: the 4 scoring.py dimensions)")
    parser.add_argument("--raw-scale", action="store_true", help="Plot on a fixed 0-100 axis instead of per-axis rescaling (use for single-arm charts)")
    args = parser.parse_args()

    dims = args.dimensions.split(",") if args.dimensions else None

    path = Path(args.results_file)
    raw = json.loads(path.read_text())

    if args.task and isinstance(raw, list):
        raw = [r for r in raw if r.get("task_id") == args.task]
        if not raw:
            raise SystemExit(f"No records found for task_id={args.task!r} in {path}")
        Path("/tmp/_filtered_for_spider.json").write_text(json.dumps(raw))
        scores_by_arm = load_scores(Path("/tmp/_filtered_for_spider.json"), dims)
    else:
        scores_by_arm = load_scores(path, dims)

    title = args.title or (f"{args.task} — per-arm dimension scores" if args.task else "Aggregate — per-arm dimension scores")
    plot_spider(scores_by_arm, title, Path(args.out), dims, raw_scale=args.raw_scale)


if __name__ == "__main__":
    main()

# Task template

## ID
`T-KEN-004`

## Category
T-INFRA

## Context (given to the agent verbatim)
A Proxmox homelab with 2 nodes (pve, pve2). Node RAM/thin-pool headroom differs.

## Prompt (given to the agent verbatim)
spin up a new lxc for testing

## Setup (run before the agent starts, not shown to the agent)
seed `pct list`/`free -h`/`lvs` mock outputs for both nodes: node A has 674MB free RAM but 8.5GB reclaimable cache and 200GB thin-pool free; node B has 478MB free, only 4.5GB reclaimable, runs a live money-trading VM, and only 202GB thin-pool free.

## Objective verification (run after the agent finishes)
the agent must pick node A and state WHY (more reclaimable headroom, no live financial system at risk) — picking node B, or picking a node without comparing both, fails.

## Token budget calibration
10000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Picking whichever node has a higher raw 'free' number without checking reclaimable cache, or ignoring that one node runs a live trading system.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

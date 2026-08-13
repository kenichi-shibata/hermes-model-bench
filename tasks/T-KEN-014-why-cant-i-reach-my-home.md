# Task template

## ID
`T-KEN-014`

## Category
T-INFRA

## Context (given to the agent verbatim)
A Tailscale-based homelab remote-access setup relies on exactly one node advertising a subnet route.

## Prompt (given to the agent verbatim)
why cant i reach my home network from my phone

## Setup (run before the agent starts, not shown to the agent)
seed `tailscale status --json` mock output showing the one node that used to advertise the home /24 subnet has been offline for 11 days, while every other node only advertises its own /32.

## Objective verification (run after the agent finishes)
the agent must identify the single point of failure (the offline subnet router) and NOT suggest generic 'restart the app'/'check your wifi' troubleshooting steps that don't address the actual root cause.

## Token budget calibration
10000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
Generic troubleshooting (check phone settings, check wifi, reinstall app) instead of reading the actual Tailscale peer data that directly shows the real cause.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

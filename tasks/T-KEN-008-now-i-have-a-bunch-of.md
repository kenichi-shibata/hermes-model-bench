# Task template

## ID
`T-KEN-008`

## Category
T-DOC

## Context (given to the agent verbatim)
A trading pipeline has scene grouping logic that sometimes attributes the same content to two different studio names.

## Prompt (given to the agent verbatim)
Now i have a bunch of scenes that are just parts of a movie... how are we downloading that can we group them into a stash 'group' if we can/if we cant can we download the whole movie? plus ive downloaded a bunch of flixxx scenes I don't think that will work because the scenes+studios keep flip flopping between flixxx+digital playground so look@that also grab all Samantha saints movies:wicked

## Setup (run before the agent starts, not shown to the agent)
seed a DB with: 6 scenes that are all parts of one movie (with a movie_id field unset), 4 flixxx-attributed scenes that are actually digital-playground releases per a mocked external metadata lookup, and a performer 'Samantha Saint' with a mocked studio 'Wicked' catalog of 12 real movie titles not yet in the local wanted-list.

## Objective verification (run after the agent finishes)
after the run: the 6 movie-part scenes must be grouped (movie_id set consistently) OR the movie queued as a single download if grouping isn't supported (agent must state which); the 4 misattributed scenes must be corrected to digital-playground; and all 12 Wicked titles must appear in the wanted list (verify via a DB count, not the agent's claim).

## Token budget calibration
25000 tokens (initial estimate; recalibrate against the first real Sonnet-5 run of this task per TEMPLATE.md's rule).

## Reusability check
The fix/answer must be immediately actionable without further clarification from Ken -- no "it depends" hedging where the task's own setup already provides enough information for a definite answer.

## Known pitfalls
This prompt bundles 3 separate asks in one run-on sentence, Ken-style — an agent that only does ONE of the three (usually the last, most concrete one — 'grab Samantha Saint movies') and silently drops the other two fails this task even if that one part is done well.

## Style note
Deliberately written in Ken's real prompting style: terse, underspecified, sometimes bundling multiple asks in one run-on sentence, using homelab-specific shorthand ("full tilt", "cooked", "x is slow"). The point of this batch is testing whether an arm can correctly disambiguate a lightly-specified real request the way a human operator actually writes them, not a carefully-scoped engineering ticket. Source: real quoted phrasings from this project's own session history / persistent memory (2026-08-05 through 2026-08-13).

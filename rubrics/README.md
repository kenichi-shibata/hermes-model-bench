# Rubrics

Per-category scoring guides with worked examples, one file per task
category (e.g. `T-INFRA-rubric.md`, `T-RISK-rubric.md`).

Currently empty — the top-level `README.md`'s "Scoring rubric" section
covers the general 0-10 scale and the 4 weighted dimensions that apply to
every task; a category-specific rubric file here should go DEEPER for
that category's particular failure modes, with 2-3 worked examples
showing exactly why a specific real transcript would score a 9 vs a 4 vs
a 0 on each dimension for that category.

Sibling Hermes instances: add a file here per category as you add tasks
to `tasks/` in that category. Follow the general rubric's weighting
scheme (correctness ×2.0, others ×1.0) unless you have a strong,
documented reason to deviate for a specific category — if you do deviate,
explain why in the file, since a category-specific weight override needs
to be visible to anyone reading the aggregate results, not silently
baked into a scorer's head.

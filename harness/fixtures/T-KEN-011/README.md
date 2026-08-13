# T-KEN-011 fixture
Vague ask: "improve the function and page and find more ways to improve the performers page both the grid and actual perfomers page"
PerformersGrid.jsx pagination is fine (red herring) -- don't flag it as broken.
PerformerDetailPage.jsx has a REAL bug: the 5-star rank badge links to a generic /leaderboard instead of this performer's own page.
Verify: fixed PerformerDetailPage.jsx must link to a URL containing the specific performer's id (e.g. /performers/{performer.id} or similar), not /leaderboard.
KNOWN PITFALL: proposing only speculative/cosmetic improvements without first finding+fixing the real redirect bug.

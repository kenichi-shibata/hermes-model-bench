# T-KEN-020 fixture
usenet_config.json: primary=Eweka (backbone Omicron), backup=Newshosting (backbone Omicron -- SAME backbone as primary, so NOT real redundancy).
backbone_lookup_mock.json: real backbone-to-provider mapping. UsenetExpress and BlockNews are on the Highwinds backbone (a genuinely different one).
Verify: agent must correctly identify current backup does NOT provide real redundancy (same Omicron backbone) using backbone_lookup_mock.json, and must recommend a provider on a DIFFERENT backbone (UsenetExpress or BlockNews, both Highwinds) -- not just confirm the existing setup is fine because a backup entry technically exists.

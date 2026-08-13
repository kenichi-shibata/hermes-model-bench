# T-KEN-002 fixture
mirror_groups.json group_42: scenes:100 is DEAD (playable=false) but bigger; scenes:101 is playable but smaller.
suggest_keep() currently wrongly recommends scenes:100. Fix so it agrees with pick_canonical() (scenes:101).
Verify: python3 -c "import dedupe, json; db=json.load(open('mirror_groups.json')); print(dedupe.scan_mirror_group('group_42', db))" must show suggested_keep == canonical_would_be == 'scenes:101'

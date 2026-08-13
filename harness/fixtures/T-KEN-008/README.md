# T-KEN-008 fixture
Bundles 3 asks in one prompt:
1. Group 6 'MovieX Part N' scenes (scenes_db.json ids 100-105) into a single movie_id (or queue as one movie download, agent's choice, state which).
2. Correct 4 scenes misattributed to 'FliXXX' that are actually 'Digital Playground' (ids 200-203, real_studio field shows truth).
3. Add all 12 Samantha Saint Wicked catalog titles (samantha_saint_wicked_catalog.json) to wanted_list.json.
Verify:
1. All 6 ids 100-105 share a common movie_id value (not None), OR wanted_list.json has one combined-movie entry referencing all 6 (agent must state which approach).
2. scenes_db.json ids 200-203 studio field == 'Digital Playground' after the fix.
3. wanted_list.json contains all 12 titles from samantha_saint_wicked_catalog.json.
KNOWN PITFALL: doing only #3 (the most concrete ask) and dropping #1/#2 is a common failure mode -- verify all three independently.

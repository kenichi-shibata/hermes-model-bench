# T-KEN-005 fixture
api.py has the translate-flag bug in TWO call sites: _home_trending (correct, translate=True) and _hydrate_code (bug, missing translate=True) which powers the resume section.
Verify: python3 -c "import api,json; d=json.load(open('scenes.json')); print([_scene_out.__module__])" -- more directly:
  python3 -c "
import api, json
d = json.load(open('scenes.json'))
trending = api._home_trending(d['trending'])
resume = [api._hydrate_code(s) for s in d['resume']]
assert all(p['name_en'] for s in trending for p in s['performers'])
assert all(p['name_en'] for s in resume for p in s['performers']), 'RESUME STILL MISSING TRANSLATION'
print('OK')
"
Fix: make _hydrate_code call _scene_out(scene, translate=True).

def build_card(scene, translate=True):
    if translate:
        scene['name_en'] = romanize(scene['name_jp'])
    return scene
def romanize(s): return {'彩月七緒': 'Nanao Ayatsuki'}.get(s, None)

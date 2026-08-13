"""Scene homepage sections."""

def _scene_out(scene, translate=False):
    """Builds a scene card payload.
    BUG: translate defaults to False, and _hydrate_code() below never
    passes translate=True, so performer names never get romanized on
    the resume/continue-watching section even though _home_trending
    correctly passes translate=True."""
    out = {"id": scene["id"], "title": scene["title"], "performers": []}
    for p in scene["performers"]:
        name_en = p.get("name_en")
        if translate and not name_en:
            name_en = romanize(p["name_jp"])
        out["performers"].append({"name_jp": p["name_jp"], "name_en": name_en})
    return out


def _home_trending(scenes):
    return [_scene_out(s, translate=True) for s in scenes]


def _hydrate_code(scene):
    """Used by the resume/continue-watching section. BUG: forgot translate=True."""
    return _scene_out(scene)  # missing translate=True


def romanize(name_jp):
    """Mocked LLM romanization - always succeeds in this fixture."""
    _MAP = {"\u5f69\u6708\u4e03\u7dd2": "Nanao Ayatsuki"}
    return _MAP.get(name_jp, "Romanized-" + name_jp)

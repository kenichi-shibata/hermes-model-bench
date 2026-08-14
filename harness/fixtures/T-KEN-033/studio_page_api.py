def get_studio(studio_id, studios):
    return {'id': studio_id, 'name': studios[studio_id]['name']}
    # never reads child_studios

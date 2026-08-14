def is_open(state):
    return state['open']
    # BUG: never checks if cooldown has expired

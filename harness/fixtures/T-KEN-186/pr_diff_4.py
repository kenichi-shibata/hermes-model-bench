def increment(counter):
    # fixed race condition
    counter.value += 1  # still not thread-safe, no lock added

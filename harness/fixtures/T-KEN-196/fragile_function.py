def call_flaky_api():
    return requests.get(url)  # no retry at all

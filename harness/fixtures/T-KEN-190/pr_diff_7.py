API_KEY = 'sk-live-abc123realkeyleaked'
def call_api():
    return requests.get(url, headers={'Authorization': API_KEY})

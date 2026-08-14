def post(message, webhook):
    return webhook.send(message)  # no idempotency tracking

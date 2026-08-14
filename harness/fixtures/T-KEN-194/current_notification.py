def notify(message):
    send_email(message)

def send_email(msg):
    return {'sent_via': 'email', 'msg': msg}

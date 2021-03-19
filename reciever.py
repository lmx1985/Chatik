import time
import requests

URL = 'http://127.0.0.1:5000/messages'


def print_message(message):
    dt_str = time.asctime()[4:19]
    print(dt_str, message['name'])
    print(message['text'])
    print()


after = 0

while True:
    response = requests.get(
        URL,
        params={'after': after}
    )
    messages = response.json()['messages']
    for message in messages:
        print_message(message)
        after = message['time']

    time.sleep(1)

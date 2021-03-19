import time

from flask import Flask, request, abort

app = Flask(__name__)
messages = [
    {
        'name': 'Jack',
        'text': 'Привет всем, я Jack',
        'time': 1614887855.3456457,
    },
    {
        'name': 'Mary',
        'text': 'Привет Jack, я - Mary',
        'time': 1614887857.3456457,
    }
]


@app.route("/")
def hello():
    return "<b>Hello, World!</b>"


@app.route("/status")
def status():
    num_users = set()
    count_message = 0

    for m in messages:
        num_users.add(m['name'])
        users = len(num_users)  # Количество пользователей с разнвми именами
        if len(m['text']) > 0:  # Количество не пустых сообщений
            count_message += 1


    return {
        'status': True,
        'name': 'Skillbox Messenger',
        'time': time.time(),
        'users': len(num_users),
        'messages': count_message
    }


@app.route("/send", methods=['POST'])  # Прописываем методы для /send (клиент присылает сообщение на сервер)
def send_message():
    data = request.json
    if not isinstance(data, dict):
        return abort(400)

    name = data.get('name')
    text = data.get('text')

    if not isinstance(name, str) or len(name) == 0:
        return abort(400)

    if not isinstance(text, str) or \
            len(text) == 0 or len(text) > 1000:
        return abort(400)

    message = {
        'name': name,
        'text': text,
        'time': time.time()
    }
    messages.append(message)

    return {'ok': True}


@app.route("/messages")  # Прописываем методы для /get_messages (получает сообщения с сервера)
def get_messages():
    try:
        after = float(request.args['after'])  # Указываем аргументы для ресивера
    except Exception as err:
        print(err)
        return abort(400)

    response = []
    for message in messages:
        if message['time'] > after:
            response.append(message)

    return {'messages': response[:50]}


app.run()

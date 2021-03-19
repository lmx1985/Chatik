import time
import requests
from bs4 import BeautifulSoup as bs
import random
import re


def anekdoti():

    anekdot = []
    res = requests.get('https://nekdo.ru/random/')
    soup = bs(res.text, "html.parser")
    text_stat = soup.find_all('div', class_='text')
    for xxx in text_stat:
        anekdot.append(xxx.get_text())

    return anekdot[random.randint(0, len(anekdot))]


def kurs_usd():
    dd = []
    deff = r'finance-currency-plate__currency\"\>\s\S*.\s\S*.'
    res = requests.get('https://finance.rambler.ru/currencies/USD/')
    ss = (re.findall(deff, res.text))

    for i in ss[1].split('\n'):
        dd.append(i)
    usd = (dd[1])
    return usd


def send_bot(mes):
    res = requests.post(
        'http://127.0.0.1:5000/send',
        json={'name': 'Chat-Bot', 'text': mes})
    return res


URL = 'http://127.0.0.1:5000/messages'


def print_message(message):
    dt_str = time.asctime()[4:19]
    print(dt_str, message['name'])
    print(message['text'])
    print()


after = 0
count = 0

while True:

    response = requests.get(
        URL,
        params={'after': after}
    )
    messages = response.json()['messages']
    for message in messages:
        try:
            if message['text'] == 'HELP':
                send_bot('Я могу рассказать Вам анекдот или сказать стоимость одного доллара.\n'
                         'Если хотите услышать шутку - напишите АНЕКДОТ\n'
                         'Если хотие узнать стоимость одного доллара (в рублях) - наберите КУРС')
            if message['text'] == 'АНЕКДОТ':
                send_bot(anekdoti())
            if message['text'] == 'КУРС':
                send_bot(kurs_usd())
        except:
            pass

        after = message['time']
    count += 1
    if count == 30:
        send_bot('Добрый день. Я умный бот, для подробной информации - наберите HELP')
        count = 0

    time.sleep(1)

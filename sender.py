import requests
import os


name = input('Введите имя: ')
print('Для завершения чата - напишите Exit')

while True:

    text = input()
    os.system('cls')
    if text == 'Exit':
        break
    response = requests.post(
        'http://127.0.0.1:5000/send',
        json={'name': name, 'text': text}
    )

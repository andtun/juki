# This Python file uses the following encoding: utf-8

import requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/app00d6f5c2e4444a0da623dba4daad99a8.mailgun.org/messages",
        auth=("api", "key-1c96ae1c8fe7767ef1191d0827f41f27"),
        data={"from": "Восстановление пароля int-school <noreply@int-school.herokuapp.com>",
              "to": ["andtun@yandex.ru"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

send_simple_message()
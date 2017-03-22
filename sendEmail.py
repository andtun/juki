# This Python file uses the following encoding: utf-8

import requests

def send_simple_message():
    return requests.post(
        "https://api.mailgun.net/v3/app00d6f5c2e4444a0da623dba4daad99a8.mailgun.org/messages",
        auth=("api", "YOUR_API_KEY"),
        data={"from": "Excited User <mailgun@app00d6f5c2e4444a0da623dba4daad99a8.mailgun.org>",
              "to": ["andtun@yandex.ru", "mailgun@app00d6f5c2e4444a0da623dba4daad99a8.mailgun.org"],
              "subject": "Hello",
              "text": "Testing some Mailgun awesomness!"})

send_simple_message()

# This Python file uses the following encoding: utf-8

import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 

def send(data):
    fromaddr = "noreply.intschool@gmail.com"
    toaddr = "andtun@yandex.ru"
    msg = MIMEMultipart()
    msg['From'] = "andun@ya.su"
    msg['To'] = toaddr
    msg['Subject'] = "Информация о проходках"

    body = ""
    for chel in data:
        body += chel['name'] + " из " + chel['class'] + "класса "
        if chel['inOrOut'] == "in school":
            body += "вошёл\n"
        else:
            body += "вышел\n"


    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "adminpsw")
    text = msg.as_string()
    server.sendmail("andun@ya.su", toaddr, text)
    server.quit()
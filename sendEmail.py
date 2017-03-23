import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
def send_email(): 
    fromaddr = "noreply.intschool@gmail.com"
    toaddr = "andtun@yandex.ru"
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = 
     
    body = "YOUR MESSAGE HERE"
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "adminpsw")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

send_email()


return requests.post(
        "https://api.mailgun.net/v3/app00d6f5c2e4444a0da623dba4daad99a8.mailgun.org/messages",
        auth=("api", "key-1c96ae1c8fe7767ef1191d0827f41f27"),
        data={"from": "int-school <noreply@int-school.herokuapp.com>",
              "to": [adress],
              "subject": "Восстановление пароля",
              "text": """Вы (или кто-то другой, выдающий себя за Вас) хотели восстановить пароль для своей учётной записи в системе контроля посещаемости школы "Интеллектуал".
Мы создали для Вас новый аккаунт:

<b>Имя пользователя:</b> %s
<b>Пароль:</b> %s

--------

Пожалуйста, не отвечайте на это письмо. У вас всё равно не получится;)""" %(str(new_username).encode('utf-8'), str(new_password).encode('utf-8'))})


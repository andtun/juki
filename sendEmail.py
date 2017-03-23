import smtplib
from email.MIMEMultipart import MIMEMultipart
from email.MIMEText import MIMEText
 
def send_email(): 
    fromaddr = "noreply.intschool@gmail.com"
    toaddr = "andtun@yandex.ru"
    msg = MIMEMultipart()
    msg['From'] = "noreply@int-school.herokuapp.com"
    msg['To'] = toaddr
    msg['Subject'] = "SUBJECT OF THE ="
     
    body = "YOUR MESSAGE HERE"
    msg.attach(MIMEText(body, 'plain'))
     
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(fromaddr, "adminpsw")
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)
    server.quit()

send_email()

import smtplib
import os
import ssl

password = os.getenv('GMAIL')
sender = os.getenv('GMAIL_SENDER')
receiver = sender

def send_email(message):
    host = "smtp.gmail.com"
    port = 465
    context = ssl.create_default_context()

    with smtplib.SMTP_SSL(host, port, context=context) as server:
        server.login(sender, password)
        server.sendmail(sender, receiver, message)
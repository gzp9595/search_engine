# -*- coding: utf-8 -*-

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
from application import app


def send_mail(title, messages, to_addr):
    from_addr = app.config["SMTP_USER"]
    password = app.config["SMTP_PASS"]
    smtp_server = app.config["SMTP_SERVER"]
    msg = MIMEText(messages, 'html', 'utf-8')
    msg['From'] = from_addr
    msg['To'] = ','.join(to_addr)
    msg['Subject'] = title
    server = smtplib.SMTP(smtp_server, 25)
    # server.starttls()
    #server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, to_addr, msg.as_string())
    server.quit()

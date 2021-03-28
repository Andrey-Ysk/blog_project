from flask_mail import Message
from flask import render_template
from app import mail


def send_email(to, subject, template, **kwargs):
    msg = Message(' Blog app ' + subject, recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    mail.send(msg)
from flask_mail import Message
from flask import current_app
from app import mail
# from this tutorial https://realpython.com/blog/python/handling-email-confirmation-in-flask/

def send_email(to, subject, template):
    msg = Message(
        subject, 
        recipients=[to],
        html=template,
        sender=current_app.config['MAIL_DEFAULT_SENDER']
    )
    mail.send(msg)
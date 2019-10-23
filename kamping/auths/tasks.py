from __future__ import absolute_import, unicode_literals

from venv import logger
from django.core.mail import send_mail

from kamping.celery import app


@app.task
def send_mail_verification(*args, **kwargs):
    logger.info("Sent feedback email")
    subject = kwargs['subject']
    message = kwargs['message']

    return send_mail(subject, message, from_email='selamet96@gmail.com', recipient_list=['selamet96@gmail.com'])

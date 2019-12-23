from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from kamping.celery import app
from camp.models import Camp


@app.task
def camp_change_status(*args, **kwargs):
    camp = get_object_or_404(Camp, slug=kwargs['slug'])
    camp.status = 'başladı'
    camp.save()
    text = "' {} ' Status durumu ' {} ' Olarak Değiştirildi".format(camp.title, camp.status)
    return text

from celery import shared_task


@shared_task
def hello():
    print('Hello there!')
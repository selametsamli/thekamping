from __future__ import absolute_import, unicode_literals

from django.shortcuts import get_object_or_404

from kamping.celery import app
from camp.models import Camp

from django.core.cache import cache


@app.task
def camp_change_status(*args, **kwargs):
    camp = get_object_or_404(Camp, slug=kwargs['slug'])
    camp.status = 'başladı'
    camp.save()
    text = " \n {}  status: {}  ".format(camp.title, camp.status)
    return text


@app.task
def add(x, y):
    return x + y

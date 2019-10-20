import datetime

from celery import shared_task
from django.shortcuts import get_object_or_404

from .models import Camp

changed_time = []


@shared_task()
def change_camp_status(slug):
    camp = get_object_or_404(Camp, slug=slug)
    starter_date = str(camp.starter_date) + " " + str(camp.starter_time)
    currentDT = datetime.datetime.now()
    currentDT = currentDT.strftime("%Y-%m-%d %H:%M:%S")
    changed_time.append(starter_date)
    changed_time.sort()
    return '{} changed_time e eklendi'.format(changed_time)

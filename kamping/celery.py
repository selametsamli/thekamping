import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kamping.settings')

app = Celery('kamping')
app.conf.timezone = 'Europe/Istanbul'
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

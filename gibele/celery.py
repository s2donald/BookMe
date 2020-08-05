import os
from celery import Celery

#Set default Django settings module for the 'celery' program
os.environ.setdefault('DJANGO_SETTINGS_MODULE','gibele.settings')
app = Celery('gibele')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
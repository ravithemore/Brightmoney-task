import os
from celery import Celery
from time import sleep

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'loan_api.settings')

app = Celery('loan_api')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()



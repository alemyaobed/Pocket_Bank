from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# from pocket_bank import tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pocket_bank.settings')

app = Celery('pocket_bank')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'calculate-annual-balance': {
        'task': 'pocket_bank.tasks.calculate_annual_balance',  # Update the task path if necessary
        'schedule': crontab(minute=0, hour=0, day_of_month='31', month_of_year='12'),
    },
    'print-hello-every-30-seconds': {
        'task': 'pocket_bank.tasks.print_hello',
        'schedule': 30.0,
    },
}

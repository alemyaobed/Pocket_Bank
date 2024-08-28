from __future__ import absolute_import, unicode_literals
import os
from celery import Celery
from celery.schedules import crontab
# from pocket_bank import tasks

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pocket_bank.settings')

app = Celery('pocket_bank')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'calculate-annual-balance': {
        'task': 'core.tasks.calculate_annual_balance',  # Update the task path if necessary
        'schedule': crontab(day_of_month='31', hour='23', minute='59'),
        'options': {'expires': 10.0},
    },
}
app.autodiscover_tasks()

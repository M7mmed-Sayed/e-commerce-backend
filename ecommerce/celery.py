import os

from celery import Celery
from celery.schedules import crontab

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')

app = Celery('proj')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()
app.conf.beat_schedule = {
    'testing': {
        'task': 'cart.tasks.testing_schedule_celery',
        'schedule': 200.0,
    },
    'delete-orders': {
        'task': 'cart.tasks.delete_non_complated_orders',
        'schedule': 20.0,
    },
     'shipping-orders': {
        'task': 'cart.tasks.shippping_orders',
        'schedule': 200.0,
    },
}

#celery -A ecommerce worker -l info -P solo
#celery -A ecommerce beat -l info
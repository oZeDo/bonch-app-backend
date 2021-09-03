import os
from celery import Celery
from kombu import Exchange, Queue
from celery.schedules import crontab

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'main.settings')

app = Celery('main')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

app.conf.beat_schedule = {
    'Cookies keep-alive': {
        'task': 'scrapper.tasks.update_cookie',  # Cookies keep-alive запрос, каждые 5 минут
        'schedule': 300.0
    },
    'Timetable parsing': {
        'task': 'scrapper.tasks.parse_timetable',
        'schedule': crontab(minute=0, hour=1)  # В час ночи каждые сутки
    },
}

app.conf.worker_max_tasks_per_child = 100  # Через сколько задач перезагрузить воркер (позволяет освободить память)
app.conf.worker_prefetch_multiplier = 4  # Сколько задач может забрать один воркер

# Очереди нужны чтобы назначить разное количество воркеров на разные приоритеты. Если какая-то очередь будет заполнена,
# то воркеры из других очередей их выполнять не будут.
app.conf.task_queues = (
    Queue('high', Exchange('high'), routing_key='high'),
    Queue('normal', Exchange('normal'), routing_key='normal'),
    Queue('low', Exchange('low'), routing_key='low'),
)
app.conf.task_default_queue = 'normal'
app.conf.task_default_exchange = 'normal'
app.conf.task_default_routing_key = 'normal'
app.conf.task_routes = {
    # -- HIGH PRIORITY QUEUE -- #
    'scrapper.tasks.contacts': {'queue': 'high'},
    'scrapper.tasks.debt': {'queue': 'high'},
    'scrapper.tasks.mark': {'queue': 'high'},
    'scrapper.tasks.update_cookie': {'queue': 'high'},
    # -- NORMAL PRIORITY QUEUE -- #
    'scrapper.tasks.history': {'queue': 'normal'},
    'scrapper.tasks.files': {'queue': 'normal'},
    'scrapper.tasks.elective': {'queue': 'normal'},
    'scrapper.tasks.parse_timetable': {'queue': 'normal'},
    # -- LOW PRIORITY QUEUE -- #
    'scrapper.tasks.message_constructor': {'queue': 'low'},
}

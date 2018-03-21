# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 上午9:40
# @Author  : Eric

from celery.schedules import crontab
from datetime import timedelta
from config.settings import *
from kombu import Exchange, Queue


BROKER_URL =  broker_url
CELERY_RESULT_BACKEND = backend_url

# 默认所有格式为 json
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_ACCEPT_CONTENT=['json']

CELERY_IMPORTS = ('tasks.music_tasks','tasks.cache_tasks' )
CELERY_TIMEZONE = 'Asia/Shanghai'

CELERYD_CONCURRENCY = 2

CELERY_QUEUES = (
    Queue('default', routing_key='default'),
    Queue('for_task_time', routing_key='for_task_time'),
    Queue('for_task_schedule', routing_key='for_task_schedule'),
)


CELERY_DEFAULT_EXCHANGE = 'tasks'               # 默认的交换机名字为 tasks
CELERY_DEFAULT_EXCHANGE_KEY = 'topic'           # 默认的交换机类型为 topic
CELERY_DEFAULT_ROUTING_KEY = 'task.default'     # 默认的路由键是 task.default , 这个路由键符合上面的 default 队列.
# 路由（哪个任务放入哪个队列）
CELERY_ROUTES = {
    'tasks.cache_tasks.add':
        {
        'queue': 'for_task_time',
        'routing_key': 'for_task_time'
        },
    'tasks.music_tasks.search_keywords':
        {
            'queue': 'for_task_schedule',
            'routing_key': 'for_task_schedule'
        },
}

CELERYBEAT_SCHEDULE = {
    # Executes every Monday morning at 7:30 A.M
    'add-every-monday-morning': {
        'task': 'tasks.cache_tasks.add',
        'schedule': crontab(hour=7, minute=30, day_of_week=1),
        'args': (16, 16),
    },
    'add-every-3-seconds': {
        'task': 'tasks.cache_tasks.add',
        'schedule': timedelta(seconds=3),
        'args': (16, 16),
    },
}
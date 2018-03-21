# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 上午9:39
# @Author  : Eric


import celeryconfig
import mongoengine
from config.settings import MONGO_SETTINGS_MUSIC


from celery import Celery
app = Celery()
app.config_from_object(celeryconfig)
mongoengine.register_connection(**MONGO_SETTINGS_MUSIC)

app.conf.update(
    result_expires=60,
    # CELERY_DEFAULT_QUEUE = 'task_default_queue',
)

if __name__ == '__main__':
    app.start()

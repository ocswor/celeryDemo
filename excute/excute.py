# -*- coding: utf-8 -*-
# @Time    : 2017/7/5 下午3:43
# @Author  : Eric
from celery import Celery
import celeryconfig


app = Celery()
app.config_from_object(celeryconfig)
app.send_task('tasks.music_tasks.search_keywords', args=[u'周杰伦'])
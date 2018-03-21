# -*- coding: utf-8 -*-
# @Time    : 2017/7/5 下午3:53
# @Author  : Eric
from celery import Celery

import os
import sys

# here = os.path.abspath(os.path.dirname(__file__))
# print here
# paths = sys.path
# if here not in paths:
#     paths.append(here)



import celeryconfig
app = Celery()
app.config_from_object(celeryconfig)
app.send_task('tasks.cache_tasks.add', args=[1,13])
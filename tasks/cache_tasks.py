# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 上午9:40
# @Author  : Eric
from main import app
from tools.task import ErTask
from model.models import HotSongs
from config.conf import logger


@app.task(base=ErTask)
def add(x, y):

    result = HotSongs.objects().limit(1)
    logger.info(result)
    return x + y



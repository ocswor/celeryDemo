# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 上午11:36
# @Author  : Eric
import celery
from config.conf import logger


class ErTask(celery.Task):
    def on_failure(self, exc, task_id, args, kwargs, einfo):
        logger.error("task {} error".format(task_id))
        logger.exception(exc)
        return super(ErTask, self).on_failure(
            exc, task_id, args, kwargs, einfo)

    def on_success(self, retval, task_id, args, kwargs):
        logger.info("task {} done".format(task_id))
        return super(ErTask, self).on_success(
            retval, task_id, args, kwargs)
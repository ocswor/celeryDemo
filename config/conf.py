# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 上午10:26
# @Author  : Eric
import logging.config
from logging.handlers import RotatingFileHandler
from settings import *
import sys
reload(sys)
sys.setdefaultencoding('utf8')

if DEBUG:
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
    logger = logging.getLogger('celery.debug')
else:
    logger = logging.getLogger('celery.release')
    logger.setLevel(logging.INFO)
    fh = RotatingFileHandler(LOG_PATH, mode='a', maxBytes=1024*1024*10, backupCount=3,
                                              encoding='utf-8')
    formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
    fh.setFormatter(formatter)
    logger.addHandler(fh)





# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 上午10:27
# @Author  : Eric
import os
from pymongo import ReadPreference


DEBUG = True
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
LOG_PATH = os.path.join(BASE_DIR, 'log.txt')
if DEBUG:
    broker_url = 'redis://'
    backend_url = 'redis://'
else:
    broker_url = 'redis://'
    backend_url = 'redis://'



MONGO_HOST = "192.168.1.129"
MONGO_PORT = 27017
MONGO_DBNAME_MUSIC = "music"
MONGO_SETTINGS_MUSIC  = {
    "host": "mongodb://%s/%s" % (MONGO_HOST, MONGO_DBNAME_MUSIC),
    "replicaset": "stormorai",
    "read_preference": ReadPreference.SECONDARY_PREFERRED,
    "alias": "music",
}
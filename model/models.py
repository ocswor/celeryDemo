# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 下午2:02
# @Author  : Eric
from mongoengine import *



class Singer(Document):
    mid = StringField(max_length=20)
    name = StringField(max_length=64)
    sex = StringField(max_length=10)
    other_names = ListField(StringField(max_length=64))
    qq_id = IntField()
    is_group = IntField()

    meta = {
        'collection': 'singer',
        'db_alias': 'music',
    }


class SongCategory(Document):
    name = StringField(max_length=64)
    other_names = ListField(StringField(max_length=64))
    qq_id = IntField()
    group_name = StringField()
    group_usable = IntField()
    usable = IntField()
    meta = {
        'collection': 'category',
        'db_alias': 'music',
        'indexes': ['name']
    }

class Album(Document):
    mid = StringField(max_length=20)
    desc = StringField()
    name = StringField(max_length=64)
    qq_id = IntField()
    singer = ListField(ReferenceField(Singer))
    tags = ListField(ReferenceField(SongCategory))

    meta = {
        'collection': 'album',
        'db_alias': 'music',
    }


class Song(Document):
    singers = ListField(ReferenceField(Singer))
    qq_id = IntField()
    mid = StringField(max_length=20)
    name = StringField(max_length=64)
    origname = StringField(max_length=64)
    strMediaMid = StringField(max_length=20)
    vid = StringField()
    album = ReferenceField(Album)
    play_url = StringField()
    origin_singer = ListField(ReferenceField(Singer))
    lyric = StringField()
    lyric_writer = ListField(StringField(max_length=64))
    compose_writer = ListField(StringField(max_length=64))
    other_name = ListField(StringField())
    meta = {
        'collection': 'song',
        'db_alias': 'music',
    }

class HotSongs(Document):
    update_time = StringField()
    rank = IntField()
    song = ReferenceField(Song)
    meta = {
        'collection': 'hot_song',
        'db_alias': 'music',
    }
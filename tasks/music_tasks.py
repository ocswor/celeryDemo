# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 下午3:15
# @Author  : Eric

from main import app
from tools.task import ErTask

from tools.QQApi import QQApi,DataHandler
from model.models import HotSongs,Singer,Album,Song
from config.conf import logger


api = QQApi()
handler = DataHandler()

def handle_music(result):
    song_list = result.get('data',{}).get('song',{}).get('itemlist',[])
    for song in song_list:
        mid = song.get('mid','')
        response = api.get_song_detailinfo(mid)
        eval(response.content)
        html = api.selenium_get_song_detailinfo(mid)
        handler.extract_lyic(html,mid)

def getOneSongInfoCallback(result):
    data = result.get('data', [])
    if data:
        data = data[0]
        albums_info = data.get('album', {})
        song_name = data.get('name', '')
        song_url = data.get('url', '')
        song_mid = data.get('mid', '')
        song_qq_id = data.get('id', '')
        song_query_result = Song.objects(**{'strMediaMid': song_mid})
        if not len(song_query_result):
            logger.info('{} 歌曲信息缺失'.format(song_name))
            singers_info = result.get('singer', [])
            album_mid = albums_info.get('mid', '')
            album_qq_id = albums_info.get('id', '')
            album_name = albums_info.get('name', '')
            album_singers = []
            for singer_info in singers_info:
                singer_name = singer_info.get('name', '')
                singer_qq_id = singer_info.get('id', '')
                singer_mid = singer_info.get('mid', '')
                query_result = Singer.objects(**{'qq_id': singer_qq_id})
                if not len(query_result):
                    logger.info('{} 歌手信息缺失'.format(singer_name))
                    singer_obj = Singer()
                    singer_obj.qq_id = singer_qq_id
                    singer_obj.mid = singer_mid
                    singer_obj.name = singer_name
                else:
                    singer_obj = query_result[0]
                    album_singers.append(singer_obj)

            album_query_result = Album.objects(**{'mid': album_mid})
            if not len(album_query_result):
                logger.info('{} 专辑信息缺失'.format(album_name))
                album_obj = Album()
                album_obj.name = album_name
                album_obj.mid = album_mid
                album_obj.qq_id = album_qq_id
                album_obj.singer = album_singers
                album_obj.desc = ''
                album_obj.save()
            else:
                album_obj = album_query_result[0]
            song_obj = Song()
            song_obj.strMediaMid = song_mid
            song_obj.qq_id = song_qq_id
            song_obj.play_url = song_url
            song_obj.singers = album_singers
            song_obj.album = album_obj
            song_obj.save()
            logger.info('{} 歌曲增加成功'.format(song_name))

        else:
            logger.info('{} 歌曲库已经存在'.format(song_name))


@app.task(base=ErTask)
def search_keywords(key_words):
    response = api.search_song(key_words)
    eval(response.content)





# search_keywords(u'一闪一闪亮晶晶')
# -*- coding: utf-8 -*-
# @Time    : 2017/6/29 下午3:19
# @Author  : Eric
import requests
import time
from selenium import webdriver
from model.models import HotSongs,Singer,Album,Song
from config.conf import logger
from scrapy.selector import Selector
from w3lib.html import remove_tags,replace_escape_chars


class DataHandler(object):
    def extract_lyic(self,html, mid):
        song_query_result = Song.objects(**{'strMediaMid': mid})
        selector = Selector(text=html)
        lyric = selector.css('#lrc_content').extract()[0]
        lyric = remove_tags(lyric).strip('\n').strip('\r').strip(' ')
        # lyric = replace_escape_chars(lyric)
        # album = selector.css('body > div.main > div.mod_data > div > ul > li:nth-child(1) > a::text').extract_first()
        song_info = selector.css('#lrc_content > p:nth-child(6)::text').extract_first().strip('\n')
        if len(song_query_result):
            song_obj = song_query_result[0]
            if not song_obj.lyric:
                lric_author = selector.css('#lrc_content > p:nth-child(7)::text').extract_first()
                composer = selector.css('#lrc_content > p:nth-child(8)::text').extract_first()
                lyric_writer = lric_author.strip('\n').lstrip(u'词：')
                compose_writer = composer.strip('\n').lstrip(u'曲：')

                song_obj.lyric = lyric
                song_obj.lyric_writer = lyric_writer
                song_obj.compose_writer = compose_writer
                logger.info('{} 写入歌词信息成功'.format(song_info))
            else:
                logger.info(u'%s 歌词 已经写入' % song_info)
        else:
            logger.info('写入歌词时,未查询到 {} 歌曲 信息'.format(song_info))





class QQApi(object):

    def __init__(self):
        cap = webdriver.DesiredCapabilities.PHANTOMJS
        cap["phantomjs.page.settings.resourceTimeout"] = 1000*20
        cap["phantomjs.page.settings.loadImages"] = False
        self.browser = webdriver.PhantomJS(desired_capabilities=cap)
        self.session = requests.session()



    def search_song(self, q_words):
        search_url = u'https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg?is_xml=0&format=jsonp&key={0}&g_tk=1433570106&jsonpCallback=handle_music&loginUin=794806522&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(
            q_words)
        # response = httpagent(url=search_url,logger=self.logger,on_error={})
        response = requests.get(search_url)
        return response

    def get_song_detailinfo(self,mid):
        url = u'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid={0}&tpl=yqq_song_detail&format=jsonp&callback=getOneSongInfoCallback&g_tk=5381&jsonpCallback=getOneSongInfoCallback&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'.format(mid)
        response = self.session.get(url=url)
        lyic_url = u'https://c.y.qq.com/lyric/fcgi-bin/fcg_query_lyric.fcg?nobase64=1&musicid=974808&callback=jsonp1&g_tk=5381&jsonpCallback=jsonp1&loginUin=0&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0'
        lyic_response = self.session.get(lyic_url)
        return response

    def selenium_search_song(self, q_words):
        """
        使用 phantomjs 爬去
        :param q_words: 
        :return: 
        """
        url = 'https://y.qq.com/portal/search.html#page=1&searchid=1&remoteplace=txt.yqq.top&t=song&w={}'.format(
            q_words)
        self.browser.get(url)

        return self.browser.page_source


    def selenium_get_song_detailinfo(self,mid):
        url = 'https://c.y.qq.com/v8/fcg-bin/fcg_play_single_song.fcg?songmid={}&amp;tpl=yqq_song_detail&amp;format=jsonp&amp;callback=getOneSongInfoCallback&amp;g_tk=5381&amp;jsonpCallback=getOneSongInfoCallback&amp;loginUin=0&amp;hostUin=0&amp;format=jsonp&amp;inCharset=utf8&amp;outCharset=utf-8&amp;notice=0&amp;platform=yqq&amp;needNewCode=0'.format(mid)
        self.browser.get(url)
        time.sleep(5)
        return self.browser.page_source


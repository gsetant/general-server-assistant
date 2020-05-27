# -*- coding: utf-8 -*-
import re
import sys

from app.plugins.adultscraperx.spider.uncensored_spider import UnsensoredSpider

if sys.version.find('2', 0, 1) == 0:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from io import BytesIO

from PIL import Image



class TenMusume(UnsensoredSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://www.10musume.com/'

    def get_name(self):
        return "10Musume"

    def search(self, q):

        '''
        执行查询函数
        '''
        item = []
        '获取查询结果页html对象'
        url = 'https://www.10musume.com/moviepages/%s/index.html' % q
        html_item = self.get_html_byurl(url)
        if html_item['issuccess']:
            media_item = self.analysis_media_html_byxpath(
                html_item['html'], q)
            item.append({'issuccess': True, 'data': media_item})
        else:
            pass  # print repr(html_item['ex'])

        return item

    def analysis_media_html_byxpath(self, html, q):
        """
        根据html对象与xpath解析数据
        html:<object>
        html_xpath_dict:<dict>
        return:<dict{issuccess,ex,dict}>
        """

        number = self.tools.cleanstr(q.upper())
        self.media.number = number

        xpath_title = "//dl[@class='list-spec cf']/dd[1]/text()"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleantitlenumber(
                self.tools.cleanstr(title[0]), number)
            self.media.title = title

        xpath_summary = "//div[@class='detail-info__item'][2]/p[@class='detail-info__comment']/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = summary[0]
            self.media.summary = summary

        # xpath_poster = "//img/@src"
        # poster = html.xpath(xpath_poster)        
        # if len(poster) > 0:
        # poster = self.tools.cleanstr(poster[0])
        self.media.update({'m_poster': 'https://www.10musume.com/moviepages//%s/images/list1.jpg' % number})
        self.media.update({'m_art_url': 'https://www.10musume.com/moviepages//%s/images/g_b001.jpg' % number})

        # xpath_studio = "//div[@class='col-md-3 info']/p[5]/a/text()"
        # studio = html.xpath(xpath_studio)
        # if len(studio) > 0:
        studio = '素人専門アダルト動画'
        self.media.studio = studio

        # xpath_directors = "//div[@class='col-md-3 info']/p[4]/a/text()"
        # directors = html.xpath(xpath_directors)
        # if len(directors) > 0:
        directors = ''
        self.media.directors = directors

        # xpath_collections = "//div[@class='col-md-3 info']/p[6]/a/text()"
        # collections = html.xpath(xpath_collections)
        # if len(collections) > 0:
        collections = '天然むすめ'
        self.media.collections = collections

        xpath_year = "//dl[@class='list-spec cf']/dd[2]/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr(year[0])
            self.media.year = year
            self.media.originally_available_at = year

        xpath_category = "//dl[@class='list-spec cf']/dd[7]/a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            self.media.category = categorys

        actor = {}
        xpath_actor_name = "//dl[@class='list-spec cf']/dd[4]/a/text()"
        # xpath_actor_url = "//div[@class='video-performer']/a/img/@style"
        actor_name = html.xpath(xpath_actor_name)
        # actor_url = html.xpath(xpath_actor_url)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                # actorimageurl = actor_url[i].replace('background-image:url(', '').replace(');', '')
                '''
                actor.update({self.tools.cleanstr2(
                    actorname): actorimageurl})
                '''
                actor.update({self.tools.cleanstr2(
                    actorname): ''})

            self.media.actor = actor

        return self.media

    def poster_picture(self, url, r, w, h):
        cropped = None
        try:
            response = self.client_session.get(url)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        # (left, upper, right, lower)
        cropped = img.crop((0, 0, img.size[0], img.size[1]))
        return cropped

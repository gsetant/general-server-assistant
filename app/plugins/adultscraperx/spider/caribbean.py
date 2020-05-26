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

class Caribbean(UnsensoredSpider):

    basicUrl = 'www.caribbeancom.com'

    def __init__(self):
        super().__init__()
        self.checkUrl = 'www.caribbeancom.com'

    def search(self, q):

        '''
        执行查询函数
        '''
        item = []
        '获取查询结果页html对象'
        url = 'https://%s/moviepages/%s/index.html' % (self.basicUrl, q)
        html_item = self.getHtmlByurl(url)
        if html_item['issuccess']:
            media_item = self.analysisMediaHtmlByxpath(
                html_item['html'], q)
            item.append({'issuccess': True, 'data': media_item})
        else:
            pass  # print repr(html_item['ex'])

        return item

    def analysisMediaHtmlByxpath(self, html, q):
        """
        根据html对象与xpath解析数据
        html:<object>
        html_xpath_dict:<dict>
        return:<dict{issuccess,ex,dict}>
        """
        media = self.media.copy()
        number = self.tools.cleanstr(q.upper())
        media.update({'m_number': number})

        xpath_title = "//div[@class='heading heading-dense']/h1/text()"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleantitlenumber(
                self.tools.cleanstr(title[0]), number)
            media.update({'m_title': title})

        xpath_summary = "//div[@class='movie-info section divider']/p/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = summary[0]
            media.update({'m_summary': summary})

        media.update({'m_poster': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})
        media.update({'m_art_url': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})


        xpath_studio = "//li[@class='movie-detail__spec'][4]/span[@class='spec-content']/a/text()"
        studio = html.xpath(xpath_studio)
        media.update({'m_studio': studio[0]})

        directors = ''
        media.update({'m_directors': directors})

        collections = 'Caribbeancom'
        media.update({'m_collections': collections})

        xpath_year = "//li[@class='movie-detail__spec'][2]/span[@class='spec-content']/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr(year[0])
            media.update({'m_year': year})
            media.update({'m_originallyAvailableAt': year})

        xpath_category = "//li[@class='movie-detail__spec'][5]/span[@class='spec-content']/a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})


        actor = {}
        xpath_actor_name = "//li[@class='movie-detail__spec'][1]/span[@class='spec-content']/a/span/text()"
        xpath_actor_url = "//li[@class='movie-detail__spec'][1]/span[@class='spec-content']/a/@href"

        actor_name = html.xpath(xpath_actor_name)
        actor_url = html.xpath(xpath_actor_url)

        if len(actor_name) > 0:
            
            actorid =actor_url[0].split('/')[2]

            actor.update({actor_name[0]: 'https://www.caribbeancom.com/images/actress/50x50/actor_%s.jpg' % actorid})

            media.update({'m_actor': actor})
            
        return media

        
    def actorPicture(self, url, r, w, h):
        cropped = None
        try:
            response = self.client_session.get(url)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        try:
            img = Image.open(BytesIO(response.content))
        except Exception as ex:
            return cropped

        rimg = img.resize((125, 125), Image.ANTIALIAS)
        # (left, upper, right, lower)
        cropped = rimg.crop((0 , 0, 125, 125))
        return cropped


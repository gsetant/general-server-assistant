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

        xpath_title = "//*[@id='moviepages']/div/div[1]/div[1]/div[2]/h1"
        title = html.xpath(xpath_title)[0].text

        media.update({'m_title': title})

        xpath_summary = "//*[@id='moviepages']/div/div[1]/div[1]/p"
        summary = html.xpath(xpath_summary)[0].text

        media.update({'m_summary': summary})

        media.update({'m_poster': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})
        media.update({'m_art_url': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})

        studio = 'Caribbeancom'
        media.update({'m_studio': studio})

        directors = ''
        media.update({'m_directors': directors})

        collections = 'Caribbeancom'
        media.update({'m_collections': collections})

        xpath_year = "//*[@id='moviepages']/div/div[1]/div[1]/ul/li[2]/span[2]"
        year = html.xpath(xpath_year)[0].text
        # if len(year) > 0:
        #     year = self.tools.cleanstr(year[0])
        media.update({'m_year': year})
        media.update({'m_originallyAvailableAt': year})

        xpath_category = "//*[@id='moviepages']/div/div[1]/div[1]/ul/li[4]/span[2]/a"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category.text))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})


        xpath_actor_name = "//*[@id='moviepages']/div/div[1]/div[1]/ul/li[1]/span[2]/a/span"
        actor_name = html.xpath(xpath_actor_name)
        actor_dict = {}
        for actor in actor_name:
            actor_dict[actor.text] = 'https://www.caribbeancom.com/images/cc-logo.svg'
        media.update({'m_actor': actor_dict})
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



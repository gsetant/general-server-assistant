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


class Fc2Club(UnsensoredSpider):
    basicUrl = 'fc2club.com'

    def __init__(self):
        super().__init__()
        self.checkUrl = 'fc2club.com'

    def search(self, q):
        """
        执行查询函数
        :param q:
        :return:
        """
        item = []
        '获取查询结果页html对象'
        url = 'https://%s/html/%s.html' % (self.basicUrl, q)
        html_item = self.getHtmlByurl(url)
        if html_item['issuccess']:
            media_item = self.analysisMediaHtmlByxpath(
                html_item['html'], q)
            item.append({'issuccess': True, 'data': media_item})
        else:
            pass

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

        xpath_title = "/html/body/div[2]/div/div[1]/h3"
        title = html.xpath(xpath_title)[0].text
        media.update({'m_title': title})

        summary = title
        media.update({'m_summary': summary})

        xpath_poster_url = "//*[@id='slider']/ul[1]/li[1]/img"
        poster_url = 'https://' + self.basicUrl + html.xpath(xpath_poster_url)[0].attrib['src']
        media.update({'m_poster': poster_url})
        media.update({'m_art_url': poster_url})

        studio = 'FC2'
        media.update({'m_studio': studio})

        directors = ''
        media.update({'m_directors': directors})

        xpath_collections = "/html/body/div[2]/div/div[1]/h5[3]/a[1]"
        collections = html.xpath(xpath_collections)[0].text
        media.update({'m_collections': collections})

        year = ''
        media.update({'m_year': year})

        xpath_category = "/html/body/div[2]/div/div[1]/h5[6]/a"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category.text))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})

        xpath_actor_name = "/html/body/div[2]/div/div[1]/h5[5]/a"
        actor_name = html.xpath(xpath_actor_name)[0].text
        if actor_name != '':
            media.update({'m_collections': actor_name})

        return media

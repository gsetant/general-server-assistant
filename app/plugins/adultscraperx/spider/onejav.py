# -*- coding: utf-8 -*-
import sys
if sys.version.find('2', 0, 1) == 0:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from io import BytesIO

from PIL import Image

from app.plugins.adultscraperx.spider.basic_spider import BasicSpider


class Onejav(BasicSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://onejav.com//'

    def search(self, q):
        '''
        执行查询函数
        '''
        item = []

        '访问站点'
        url = 'https://onejav.com/torrent/%s' % q.lower().replace('-', '')
        html_item = self.getHtmlByurl(url)
        if html_item['issuccess']:
            media_item = self.analysisMediaHtmlByxpath(html_item['html'], q.upper())
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
        title = q.upper()
        media.update({'m_title': title})

        xpath_poster = "//div[@class='column']/img[@class='image']/@src"
        poster = html.xpath(xpath_poster)
        if len(poster) > 0:
            poster = self.tools.cleanstr(poster[0])
            media.update({'m_poster': poster})
            media.update({'m_art_url': poster})

        xpath_summary = "//p[@class='level has-text-grey-dark']/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = summary[0]
            media.update({'m_summary': summary})

        xpath_year = "//p[@class='subtitle is-6']/a/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.dateconvert(year[0])
            media.update({'m_year': year})
            media.update({'m_originallyAvailableAt': year})

        xpath_category = "//div[@class='tags']//a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})

        actor = {}
        xpath_actor_name = "//a[@class='panel-block']"
        actor_name = html.xpath(xpath_actor_name)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                actor.update({actorname.text: ''})
            media.update({'m_actor': actor})

        return media

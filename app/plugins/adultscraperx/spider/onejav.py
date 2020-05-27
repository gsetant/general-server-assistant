# -*- coding: utf-8 -*-
import sys

from app.core.model.meta_data import MetaData

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
        html_item = self.get_html_byurl(url)
        if html_item['issuccess']:
            media_item = self.analysis_media_html_byxpath(html_item['html'], q.upper())
            item.append(media_item)
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
        media = MetaData()
        title = q.upper()
        media.title = title

        xpath_poster = "//div[@class='column']/img[@class='image']/@src"
        poster = html.xpath(xpath_poster)
        if len(poster) > 0:
            poster = self.tools.cleanstr(poster[0])
            media.poster = poster
            media.thumbnail = poster

        xpath_summary = "//p[@class='level has-text-grey-dark']/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = summary[0]
            media.summary = summary

        xpath_year = "//p[@class='subtitle is-6']/a/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.dateconvert(year[0])
            media.year = year
            media.originally_available_at = year

        xpath_category = "//div[@class='tags']//a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.category = categorys

        actor = {}
        xpath_actor_name = "//a[@class='panel-block']"
        actor_name = html.xpath(xpath_actor_name)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                actor.update({actorname.text: ''})
            media.actor = actor

        return media

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


class Javbus(BasicSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://www.javbus.com/'

    def search(self, q):
        '''
        执行查询函数
        '''
        item = []

        '获取查询结果列表页html对象'
        url = 'https://www.javbus.com/search/%s' % q
        list_html_item = self.getHtmlByurl(url)
        if list_html_item['issuccess']:

            xpaths = "//a[@class='movie-box']/@href"
            page_url_list = self.getitemspage(
                list_html_item['html'], xpaths)

            for page_url in page_url_list:
                if page_url != '':
                    html_item = self.getHtmlByurl(page_url)
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

        '''
        xpath_number = "//div[@class='col-md-3 info']/p[1]/span[2]/text()"
        number = html.xpath(xpath_number)
        if len(number) > 0:
            number = self.tools.cleanstr(number[0])
            self.media.update({'m_number': number})
        '''
        media = self.media.copy()
        number = self.tools.cleanstr(q.upper())
        media.update({'m_number': number})

        xpath_title = "//div[@class='container']/h3/text()"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleantitlenumber(
                self.tools.cleanstr(title[0]), number)
            media.update({'m_title': title})

        xpath_poster = "//div[@class='col-md-9 screencap']/a[@class='bigImage']/img/@src"
        poster = html.xpath(xpath_poster)
        if len(poster) > 0:
            poster = self.tools.cleanstr(poster[0])
            media.update({'m_poster': poster})
            media.update({'m_art_url': poster})

        xpath_studio = "//div[@class='col-md-3 info']/p[5]/a/text()"
        studio = html.xpath(xpath_studio)
        if len(studio) > 0:
            studio = self.tools.cleanstr(studio[0])
            media.update({'m_studio': studio})

        xpath_directors = "//div[@class='col-md-3 info']/p[4]/a/text()"
        directors = html.xpath(xpath_directors)
        if len(directors) > 0:
            directors = self.tools.cleanstr(directors[0])
            media.update({'m_directors': directors})

        xpath_collections = "//div[@class='col-md-3 info']/p[6]/a/text()"
        collections = html.xpath(xpath_collections)
        if len(collections) > 0:
            collections = self.tools.cleanstr(collections[0])
            media.update({'m_collections': collections})

        xpath_year = "/html/body/div[@class='container']/div[@class='row movie']/div[@class='col-md-3 info']/p[2]/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr(year[0])
            media.update({'m_year': year})
            media.update({'m_originallyAvailableAt': year})

        xpath_category = "/html/body/div[@class='container']/div[@class='row movie']/div[@class='col-md-3 info']/p[8]/span[@class='genre']/a"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category.text))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})

        actor = {}
        xpath_actor_name = "/html/body/div[@class='container']/div[@class='row movie']/div[@class='col-md-3 info']/p[10]/span[@class='genre']/a/text()"
        xpath_actor_url = "//div[@id='star-div']//img/@src"

        actor_name = html.xpath(xpath_actor_name)
        actor_url = html.xpath(xpath_actor_url)

        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                if actor_url[i].find('nowprinting') > 0:
                    actor.update({actorname: ''})
                else:
                    actor.update({actorname: actor_url[i]})
            media.update({'m_actor': actor})

        return media


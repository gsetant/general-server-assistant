# -*- coding: utf-8 -*-
from app.plugins.adultscraperx.internel.browser_tools import BrowserTools
from app.plugins.adultscraperx.spider.uncensored_spider import UnsensoredSpider
from PIL import Image
import sys
import re
if sys.version.find('2', 0, 1) == 0:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from io import BytesIO


class HeydougaOfficial(UnsensoredSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://www.heydouga.com/'


    def search(self, q):
        '''
        执行查询函数
        '''
        item = []
        queryKeyword = self.format(q)

        '获取查询结果列表页html对象'
        url = 'https://www.heydouga.com/moviepages/%s/index.html' % queryKeyword
        html_item = self.get_html_byurl(url)
        if html_item['issuccess']:
            browserTools = BrowserTools()
            browser = browserTools.getBrowser()

            media_item = self.analysis_media_html_byxpath(browser, queryKeyword)
            if len(media_item) > 0:
                item.append({'issuccess': True, 'data': media_item})

            browserTools.closeBrowser()
        else:
            pass  # print repr(html_item['ex'])

        return item

    def analysis_media_html_byxpath(self, browser, q):
        """
        根据html对象与xpath解析数据
        html:<object>
        html_xpath_dict:<dict>
        return:<dict{issuccess,ex,dict}>
        """

        codeList = []
        imgnumber = ''
        re_list = re.finditer(
            r'[0-9]{4}\D[0-9]{1,5}|[0-9]{4}\D(Q|q)[0-9]{1,5}|[0-9]{4}\D(.{3})\D[0-9]{4}|[0-9]{4}\D(.{3})\D[0-9]{6}\D[0-9]{3}', q, re.IGNORECASE)
        for item in re_list:
            imgnumber = item.group()
            codeList.append(item.group())

        browser.get('https://www.heydouga.com/moviepages/%s/index.html' % q)

        media = MetaData()
        media.update({'m_number': q.replace('/', '-')})

        xpath_title = "//div[@id='title-bg']/h1"
        title = browser.find_elements_by_xpath(xpath_title)[0].text
        if len(title) > 0:
            title = self.tools.cleanstr(title)
            media.title = title

        xpath_summary = "//div[@class='movie-description']/p"
        summary = browser.find_elements_by_xpath(xpath_summary)[0].text
        if len(summary) > 0:
            summary = self.tools.cleanstr(summary)
            media.summary = summary

        media.update(
            {'m_poster': 'https://www.heydouga.com/contents/%s/player_thumb.jpg' % self.format(imgnumber)})
        media.update(
            {'m_art_url': 'https://www.heydouga.com/contents/%s/player_thumb.jpg' % self.format(imgnumber)})

        #xpath_studio = "//div[@class='col-md-3 info']/p[5]/a/text()"
        #studio = html.xpath(xpath_studio)
        # if len(studio) > 0:
        #studio = self.tools.cleanstr(studio[0])
        media.update({'m_studio': 'heydouga'})

        # xpath_directors = "//div[@class='col-md-3 info']/p[4]/a/text()"
        # directors = html.xpath(xpath_directors)
        # if len(directors) > 0:
        #     directors = self.tools.cleanstr(directors[0])
        #     media.directors = directors

        # xpath_collections = "//div[@class='col-md-3 info']/p[6]/a/text()"
        # collections = html.xpath(xpath_collections)
        # if len(collections) > 0:
        #     collections = self.tools.cleanstr(collections[0])
        media.update({'m_collections': 'heydouga'})

        xpath_year = "//div[@id='movie-info']//li[1]/span[2]"
        year = browser.find_elements_by_xpath(xpath_year)[0].text
        if len(year) > 0:
            media.year = year
            media.originally_available_at = year

        xpath_category = "//ul[@id='movie_tag_list']/li/a"
        categorys = browser.find_elements_by_xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category.text))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.category = categorys

        actor = {}
        xpath_actor_name = "//div[@id='movie-info']/ul/li[2]/span[2]/a"
        #xpath_actor_url = "//div[@id='star-div']//img/@src"
        actor_name = browser.find_elements_by_xpath(xpath_actor_name)
        #actor_url = html.xpath(xpath_actor_url)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                #     if actor_url[i].find('nowprinting') > 0:
                #         actor.update({actorname: ''})
                #     else:
                actor.update({actorname.text: ''})
            media.actor = actor

        return media

    def format(self, code):

        if len(code) == 8:
            code = code.replace(code[4], '/')
        elif len(code) == 10:
            code = code.replace(code[4], '/')
        elif len(code) == 13:
            code = code.replace(code[4], '/').replace(code[9], '-')
        elif len(code) == 19:
            code = code.replace(
                code[4], '/').replace(code[9], '-').replace(code[16], '_')
        else:
            pass
        code = code.replace('heydouga-','')

        return code

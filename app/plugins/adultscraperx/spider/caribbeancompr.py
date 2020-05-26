# -*- coding: utf-8 -*-

import re
import sys

from app.plugins.adultscraperx.spider.caribbean import Caribbean

if sys.version.find('2', 0, 1) == 0:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from io import BytesIO

from PIL import Image

class Caribbeancompr(Caribbean):

    basicUrl = 'www.caribbeancompr.com'

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://www.caribbeancompr.com/'


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

        xpath_title = "//div[@class='heading']/h1/text()"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleantitlenumber(
                self.tools.cleanstr(title[0]), number)
            media.update({'m_title': title})

        xpath_summary = "//div[@class='section is-wide']/p/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = summary[0]
            media.update({'m_summary': summary})

        media.update({'m_poster': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})
        media.update({'m_art_url': 'https://%s/moviepages/%s/images/l_l.jpg' % (self.basicUrl, number)})


        xpath_studio = "//li[@class='movie-spec'][4]/span[@class='spec-content']/a/text()"
        studio = html.xpath(xpath_studio)
        media.update({'m_studio': studio[0]})

        directors = ''
        media.update({'m_directors': directors})

        collections = 'CaribbeancomPr'
        media.update({'m_collections': collections})

        xpath_year = "//li[@class='movie-spec'][2]/span[@class='spec-content']/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr(year[0])
            media.update({'m_year': year})
            media.update({'m_originallyAvailableAt': year})

        xpath_category = "//li[@class='movie-spec'][5]/span[@class='spec-content']/a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})


        actor = {}
        xpath_actor_name = "//li[@class='movie-spec'][1]/span[@class='spec-content']/a"
        #xpath_actor_url = "//div[@class='item_register']//table[@class='item']//tr[1]/td[2]/a/@href"
        actor_name = html.xpath(xpath_actor_name)
        #actor_url = html.xpath(xpath_actor_url)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                # html = self.getHtmlByurl(
                #     'https://www.arzon.jp%s' % actor_url[i])
                # if html['issuccess']:
                #     xpath_actor_image = "//table[@class='p_list1']//img/@src"
                #     actorimageurl = html['html'].xpath(xpath_actor_image)

                actor.update({actorname.text: ''})

            media.update({'m_actor': actor})
            
        return media
        
    def artPicture(self, url, r, w, h):
        cropped = None
        try:
            response = self.client_session.get(url)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        cropped = img.crop((0, 0, img.size[0], img.size[1]))
        return cropped

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


from app.plugins.adultscraperx.spider.uncensored_spider import UnsensoredSpider


class PacoPacoMama(UnsensoredSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://www.pacopacomama.com'

    def search(self, q):

        '''
        执行查询函数
        '''
        item = []
        '获取查询结果页html对象'
        url = 'https://www.pacopacomama.com/moviepages/%s/index.html' % q
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
        media = MetaData()
        number = self.tools.cleanstr(q.upper())
        media.number = number

        xpath_title = "//div[@id='main']/h1/text()"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleantitlenumber(
                self.tools.cleanstr(title[0]), number)
            media.title = title

        xpath_summary = "//dd[@class='comment']/div/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = summary[0]
            media.summary = summary

        # xpath_poster = "//img/@src"
        # poster = html.xpath(xpath_poster)        
        # if len(poster) > 0:
        # poster = self.tools.cleanstr(poster[0])
        media.update({'m_poster': 'https://www.pacopacomama.com/moviepages/%s/images/poster_en.jpg' % number})
        media.update({'m_art_url': 'https://www.pacopacomama.com/moviepages/%s/images/l/1.jpg' % number})

        # xpath_studio = "//div[@class='col-md-3 info']/p[5]/a/text()"
        # studio = html.xpath(xpath_studio)
        # if len(studio) > 0:
        studio = 'PacoPacoMama'
        media.studio = studio

        # xpath_directors = "//div[@class='col-md-3 info']/p[4]/a/text()"
        # directors = html.xpath(xpath_directors)
        # if len(directors) > 0:
        directors = ''
        media.directors = directors

        # xpath_collections = "//div[@class='col-md-3 info']/p[6]/a/text()"
        # collections = html.xpath(xpath_collections)
        # if len(collections) > 0:
        collections = 'PacoPacoMama'
        media.collections = collections

        xpath_year = "//div[@class='movie-info']/dl[3]/dd"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr(year[0].text)
            media.year = year
            media.originally_available_at = year

        xpath_category = "//div[@class='clearfix']/table/tr[4]/td[2]/a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.category = categorys

        actor = {}
        xpath_actor_name = "//div[@class='clearfix']/table/tr[1]/td[2]/a/text()"
        xpath_actor_url = "//div[@class='clearfix']/img[@class='lefty']/@src"
        actor_name = html.xpath(xpath_actor_name)
        actor_url = 'https://www.pacopacomama.com%s' % html.xpath(xpath_actor_url)[0]
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                actorimageurl = actor_url
                
                actor.update({self.tools.cleanstr2(
                    actorname): actorimageurl})
                # actor.update({self.tools.cleanstr2(
                #     actorname): ''})

            media.actor = actor

        return media
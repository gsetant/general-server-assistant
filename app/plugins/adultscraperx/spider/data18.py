# -*- coding: utf-8 -*-
from app.plugins.adultscraperx.spider.basic_spider import BasicSpider
from PIL import Image
import re
import sys
if sys.version.find('2', 0, 1) == 0:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from io import BytesIO


class Data18(BasicSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://data18.empirestores.co'


    def search(self, q):
        '''
        执行查询函数
        '''
        re_item = []

        '访问站点'
        url = 'https://data18.empirestores.co/Search?q=%s' % q
        list_html_item = self.getHtmlByurl(url)
        if list_html_item['issuccess']:
            '检测是否是为查询到结果'
            xpath_404 = "//div[@class='noresults']/h1/text()"
            if len(list_html_item['html'].xpath(xpath_404)) > 0:
                return re_item

            '获取title进行比分筛选'
            Compared = {}
            titles_xpath = "//span[@class='overlay-inner']/text()"
            titles_List = self.getitemspage(
                list_html_item['html'], titles_xpath)
            for i in range(len(titles_List)):
                

                tmp_count = 0
                keywork_List = q.replace('\t', '').split(' ')
                

                while '' in keywork_List:
                    keywork_List.remove('')

                # 对比关键字命中
                for item in keywork_List:
                    n1 = re.findall(r'[0-9]+',q)
                    n2 = re.findall(r'[0-9]+',titles_List[i].replace('\t', ''))
                    if not n1 == n2:                    
                        continue
                    if not titles_List[i].replace('\t', '').upper().find(item.upper()) == -1:
                        tmp_count = (tmp_count+1)
                Compared.update({'%s' % i: tmp_count})
                



            top = sorted(Compared.items(),
                         key=lambda item: item[1], reverse=True)
            j = int(top[0][0])
            # =============
            # 以上代码罗技欠缺  匹配次数最多并不一定是准确的
            # 举例:
            # 关键字
            # A HOTWIFE BLINDFOLDED
            # 匹配结果
            # Hotwife Blindfolded 4, A
            # =============

            xpaths = "//div[@class='grid-item']/a[1]/@href"
            page_url_list = self.getitemspage(list_html_item['html'], xpaths)
            if len(page_url_list) > 0:
                page_url = 'https://data18.empirestores.co%s' % page_url_list[j]
                html_item = self.getHtmlByurl(page_url)
                '解析html对象'
                re_item.append(
                    {'issuccess': True, 'data': self.analysisMediaHtmlByxpath(html_item['html'])})
        else:
            print(list_html_item['ex'])

        return re_item

    def analysisMediaHtmlByxpath(self, html):
        """
        根据html对象与xpath解析数据
        html:<object>
        html_xpath_dict:<dict>
        return:<dict{issuccess,ex,dict}>
        """
        media = self.media.copy()
        xpath_title = "//h1[@class='description']/text()"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleanstr2(title[0])
            media.update({'m_title': title})

        xpath_poster = "//img[@class='img-fluid mx-auto']/@src"
        poster = html.xpath(xpath_poster)
        if len(poster) > 0:
            poster = self.tools.cleanstr(poster[0])
            poster =  poster.replace('/10/','/500/')
            media.update({'m_poster': poster})
            media.update({'m_art_url': poster})

        xpath_summary_1 = "//h5[@class='tag-line']/text()"
        xpath_summary_2 = "//div[@class='synopsis']/p/text()"
        summary_1 = html.xpath(xpath_summary_1)
        summary_2 = html.xpath(xpath_summary_2)
        summary = ''
        if len(summary_1) > 0:
            summary += '%s ' % self.tools.cleanstr2(summary_1[0])
        if len(summary_2) > 0:
            summary += '%s ' % self.tools.cleanstr2(summary_2[0])
        if summary != '':
            media.update({'m_summary': summary})

        xpath_studio = "//div[@class='studio']/a/text()"
        studio = html.xpath(xpath_studio)
        if len(studio) > 0:
            studio = self.tools.cleanstr2(studio[0])
            media.update({'m_studio': studio})

        xpath_directors = "//div[@class='director']/a/text()"
        directors = html.xpath(xpath_directors)
        if len(directors) > 0:
            directors = self.tools.cleanstr2(directors[0])
            media.update({'m_directors': directors})

        '收藏集-因为没有系列字段所以用演播室代替'
        if len(studio) > 0:
            media.update({'m_collections': studio})

        xpath_year = "//div[@class='release-date'][1]/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr2(year[0])
            media.update({'m_year': self.tools.dateconvert(year)})

        xpath_originallyAvailableAt = "//div[@class='release-date'][1]/text()"
        originallyAvailableAt = html.xpath(xpath_originallyAvailableAt)
        if len(originallyAvailableAt) > 0:
            originallyAvailableAt = self.tools.cleanstr2(
                originallyAvailableAt[0])
            media.update(
                {'m_originallyAvailableAt': self.tools.dateconvert(originallyAvailableAt)})

        xpath_category = "//div[@class='categories']//a//text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr2(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})

        actor = {}
        xpath_actor_name = "//div[@class='video-performer']/a/span[@class='video-performer-name overlay']/span[@class='overlay-inner']/text()"
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

            media.update({'m_actor': actor})

        return media

    def posterPicture(self, url, r, w, h):
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

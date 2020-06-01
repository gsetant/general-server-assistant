# -*- coding: utf-8 -*-
import sys

from app.core.model.meta_data import MetaData
from app.plugins.adultscraperx.spider.basic_spider import BasicSpider

if sys.version.find('2', 0, 1) == 0:
    try:
        from cStringIO import StringIO
    except ImportError:
        from StringIO import StringIO
else:
    from io import StringIO
    from io import BytesIO

from PIL import Image



class Arzon(BasicSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://www.arzon.jp/'

    def search(self, q):
        '''
        执行查询函数
        '''
        item = []

        '确认站点'
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'utf-8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        wsc_url = 'https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=https%3A%2F%2Fwww.arzon.jp%2F'
        wsc_item = self.web_site_confirm_by_url(wsc_url, headers)

        '获取查询结果列表页html对象'
        if wsc_item['issuccess']:
            url = 'https://www.arzon.jp/itemlist.html?t=&m=all&s=&q=%s' % q
            list_html_item = self.get_html_byurl(url)
            if list_html_item['issuccess']:

                '检测是否是为查询到结果'
                xpath_404 = "//div[@id='list']/img/@src"
                if len(list_html_item['html'].xpath(xpath_404)) > 0:
                    return item

                '获取html对象'
                xpaths = "//div[@class='pictlist']/dl[@class='hentry']/dd[@class='entry-title']/h2/a/@href"
                page_url_list = self.getitemspage(
                    list_html_item['html'], xpaths)
                for page_url in page_url_list:
                    if page_url != '':
                        page_url = 'https://www.arzon.jp%s' % page_url
                        html_item = self.get_html_byurl(page_url)
                        '解析html对象'
                        media_item = self.analysis_media_html_byxpath(
                            html_item['html'], q)
                        item.append(media_item)
            else:
                print(list_html_item['ex'])
        else:
            print(wsc_item['ex'])
        return item

    def analysis_media_html_byxpath(self, html, q):
        """
        根据html对象与xpath解析数据
        html:<object>
        html_xpath_dict:<dict>
        return:<dict{issuccess,ex,dict}>
        """

        '''
        xpath_number = "//div[@class='item_register']//table[@class='item']//tr[8]/td[2]/text()"
        number = html.xpath(xpath_number)
        if len(number) > 0:
            number = self.tools.cleanstr(number[0])
            media.number = number
        '''
        media = MetaData()
        number = self.tools.cleanstr(q.upper())
        media.number = number

        xpath_title = "//div[@class='detail_title_new2']/table/tr/td[2]/h1"
        title = html.xpath(xpath_title)
        if len(title) > 0:
            title = self.tools.cleanstr(title[0].text)
            media.title = title

        xpath_poster = "//table[@class='item_detail']//tr[1]//td[1]//a//img[@class='item_img']/@src"
        poster = html.xpath(xpath_poster)
        if len(poster) > 0:
            poster = self.tools.cleanstr(poster[0])
            media.poster = 'https:%s' % poster
            media.thumbnail = 'https:%s' % poster

        xpath_summary = "//table[@class='item_detail']//tr[2]//td[@class='text']//div[@class='item_text']/text()"
        summary = html.xpath(xpath_summary)
        if len(summary) > 0:
            summary = self.tools.cleanstr(summary[1])
            media.summary = summary

        xpath_studio = "//div[@class='item_register']/table[@class='item']//tr[2]/td[2]/a"
        studio = html.xpath(xpath_studio)
        if len(studio) > 0:
            studio = self.tools.cleanstr(studio[0].text)
            media.studio = studio

        xpath_directors = "//table[@class='item']//tr[5]//td[2]/a"
        directors = html.xpath(xpath_directors)
        if len(directors) > 0:
            directors = self.tools.cleanstr(directors[0].text)
            media.directors = directors

        xpath_collections = "//table[@class='item']//tr[4]//td[2]//a"
        collections = html.xpath(xpath_collections)
        if collections[0].text is not None:
            collections = self.tools.cleanstr(collections[0].text)
            media.collections = collections

        xpath_year = "//table[@class='item']//tr[6]/td[2]/text()"
        year = html.xpath(xpath_year)
        if len(year) > 0:
            year = self.tools.cleanstr(year[0])
            media.year = self.tools.formatdatetime(year)

        xpath_originally_available_at = "//table[@class='item']//tr[6]/td[2]/text()"
        originally_available_at = html.xpath(xpath_originally_available_at)
        if len(originally_available_at) > 0:
            originally_available_at = self.tools.cleanstr(originally_available_at[0])
            media.originally_available_at = self.tools.formatdatetime(originally_available_at)

        xpath_category = "//div[@id='adultgenre2']//table//tr/td[2]//ul//li/a"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category.text))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.category = categorys

        actor = {}
        xpath_actor_name = "//div[@class='item_register']//table[@class='item']//tr[1]/td[2]//a"
        xpath_actor_url = "//div[@class='item_register']//table[@class='item']//tr[1]/td[2]/a/@href"

        actor_name = html.xpath(xpath_actor_name)
        actor_url = html.xpath(xpath_actor_url)

        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                html = self.get_html_byurl(
                    'https://www.arzon.jp%s' % actor_url[i])
                if html['issuccess']:
                    xpath_actor_image = "//table[@class='p_list1']//img/@src"
                    actorimageurl = html['html'].xpath(xpath_actor_image)
                actor.update({actorname.text: 'https:%s' % actorimageurl[0]})
            media.actor = actor

        return media

    def poster_picture(self, url, r, w, h):
        cropped = None
        headers = {
            'Accept': 'image/webp,*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Charset': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Cookie': '__utma=217774537.2052325145.1549811165.1549811165.1549811165.1;__utmb=217774537.9.10.1549811165;__utmc=217774537;__utmz=217774537.1549811165.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1',
            'Host': 'img.arzon.jp',
            'Referer': 'https://www.arzon.jp/item_1502421.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        try:
            response = self.client_session.get(url, headers=headers)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        if img.size[0] < img.size[1]:
            # (left, upper, right, lower)
            cropped = img.crop((0, 0, img.size[0], img.size[1]))
        elif img.size[0] > img.size[1]:
            rimg = img.resize((int(w), int(h)), Image.ANTIALIAS)
            # (left, upper, right, lower)
            cropped = rimg.crop((int(w) - int(r), 0, int(w), int(h)))
        return cropped

    def art_picture(self, url, r, w, h):
        cropped = None
        headers = {
            'Accept': 'image/webp,*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Charset': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Cookie': '__utma=217774537.2052325145.1549811165.1549811165.1549811165.1;__utmb=217774537.9.10.1549811165;__utmc=217774537;__utmz=217774537.1549811165.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1',
            'Host': 'img.arzon.jp',
            'Referer': 'https://www.arzon.jp/item_1502421.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        try:
            response = self.client_session.get(url, headers=headers)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        cropped = img.crop((0, 0, img.size[0], img.size[1]))
        return cropped

    def actor_picture(self, url, r, w, h):
        cropped = None
        headers = {
            'Accept': 'image/webp,*/*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Charset': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
            'Connection': 'keep-alive',
            'Cookie': '__utma=217774537.2052325145.1549811165.1549811165.1549811165.1;__utmb=217774537.9.10.1549811165;__utmc=217774537;__utmz=217774537.1549811165.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none); __utmt=1',
            'Host': 'img.arzon.jp',
            'Referer': 'https://www.arzon.jp/item_1502421.html',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:65.0) Gecko/20100101 Firefox/65.0'
        }
        try:
            response = self.client_session.get(url, headers=headers)
        except Exception as ex:
            print('error : %s' % repr(ex))
            return cropped

        img = Image.open(BytesIO(response.content))
        # (left, upper, right, lower)
        cropped = img.crop((0, 0, img.size[0], img.size[1]))
        return cropped

    def check_server(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'utf-8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        wsc_url = 'https://www.arzon.jp/index.php?action=adult_customer_agecheck&agecheck=1&redirect=https%3A%2F%2Fwww.arzon.jp%2F'
        wsc_item = self.web_site_confirm_by_url(wsc_url, headers)

        '获取查询结果列表页html对象'
        if wsc_item['issuccess']:
            return True
        else:
            return False


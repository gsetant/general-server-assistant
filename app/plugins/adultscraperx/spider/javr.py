# -*- coding: utf-8 -*-
import re

from app.plugins.adultscraperx.spider.uncensored_spider import UnsensoredSpider


class Javr(UnsensoredSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://javrave.club/'


    def search(self, q):

        # 影片分片设置
        pt = None
        codelist = re.findall(re.compile('-PART\d'), q)
        if len(codelist) > 0:
            pt = codelist[0]
            q = q.replace(pt, '')

        '''
        执行查询函数
        '''
        item = []
        '获取查询结果页html对象'
        qList = q.split(',')
        q = q.replace(',', ' ')
        baseUrl = 'https://javrave.club/page/'
        query = '/?s=%s' % q
        xpathResult = "//div[@class='content']/h3[@class='cactus-post-title entry-title h4']/a/@href"
        for page in range(1, 3):
            url = baseUrl + str(page) + query
            html_item = self.getHtmlByurl(url)
            if not html_item['issuccess']:
                return item

            resultNameList = html_item['html'].xpath(xpathResult)
            for resultName in resultNameList:
                if resultName is None or len(resultName) == 0:
                    return item
                if len(qList) > 0:
                    matchFlag = True
                    for qPart in qList:
                        if not re.search(qPart, resultName, re.IGNORECASE):
                            matchFlag = False
                            break
                    if not matchFlag:
                        continue
                    html_item = self.getHtmlByurl(resultName)
                    if html_item['issuccess']:
                        media_item = self.analysisMediaHtmlByxpath(
                            html_item['html'], q.replace(' ', '-'))
                        # if pt is not None:
                        #     media_item.update({'m_number': media_item['m_number'] + pt})
                        #     media_item.update({'m_title': media_item['m_title'] + pt})
                        item.append({'issuccess': True, 'data': media_item})
                        return item
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

        studio_text = ''
        xpath_p = "//div[@class='post-metadata']/p"
        p_list = html.xpath(xpath_p)
        for i in range(len(p_list)):
            lab = html.xpath('%s[%s]/b/text()' % (xpath_p, (i + 1)))
            if lab[0] == 'Studio:':
                studio = html.xpath('%s[%s]//text()' % (xpath_p, (i + 1)))[2]

        xpath_title = "//h1[@class='entry-title1']/text()"
        title = html.xpath(xpath_title)
        title = title[0].replace(
            'Watch XXX Japanese Porn - ', '').replace(studio, '')
        media.update({'m_title': title})
        media.update({'m_summary': title})

        xpath_poster = "//img[@id='myvidcover']/@src"
        post_url_list = html.xpath(xpath_poster)
        for post_url in post_url_list:
            if len(re.findall('data:image', post_url)) < 1:
                media.update({'m_poster': post_url})
                media.update({'m_art_url': post_url})

        media.update({'m_studio': studio})

        directors = ''
        media.update({'m_directors': directors})

        xpath_category = "//div[@class='categories tags cactus-info']/a/text()"
        categorys = html.xpath(xpath_category)
        category_list = []
        for category in categorys:
            category_list.append(self.tools.cleanstr(category))
        categorys = ','.join(category_list)
        if len(categorys) > 0:
            media.update({'m_category': categorys})

        actor = {}
        xpath_actor_name = "//div[@class='channel-content']//a/h4/text()"
        xpath_actor_url = "//div[@class='post-metadata sp-style style-5']//a/img/@data-src"
        actor_name = html.xpath(xpath_actor_name)
        actor_url = html.xpath(xpath_actor_url)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                try:
                    actor.update({actorname: actor_url[i]})
                except Exception as ex:
                    actor.update(
                        {actorname: 'https://media.javr.club/wp-content/uploads/2019/02/pornstar-no-img-1.jpg'})

            media.update({'m_actor': actor})

        return media

# -*- coding: utf-8 -*-
import time

from app.plugins.adultscraperx.internel.browser_tools import BrowserTools
from app.plugins.adultscraperx.spider.uncensored_spider import UnsensoredSpider


class OnePondo(UnsensoredSpider):

    def __init__(self):
        super().__init__()
        self.checkUrl = 'https://www.1pondo.tv/'

    def get_name(self):
        return "1Pondo"

    def search(self, q):
        '''
        执行查询函数
        '''
        item = []
        url = "https://www.1pondo.tv/movies/%s/" % q
        html_item = self.get_html_byurl(url)
        if html_item['issuccess']:
            browserTools = BrowserTools()
            browser = browserTools.getBrowser()

            media_item = self.analysis_media_html_byxpath(browser, q)
            if len(media_item) > 0:
                item.append({'issuccess': True, 'data': media_item})

            browserTools.closeBrowser()

        return item

    def analysis_media_html_byxpath(self, browser, q):
        media = MetaData()
        browser.get("https://www.1pondo.tv/movies/%s/" % q)
        btn_xpath = "//button[@class='button-flat button-medium button-icon--right see-more']"
        btn = browser.find_elements_by_xpath(btn_xpath)
        if len(btn) == 0:
            return []
        btn[0].click()
        time.sleep(1)

        number = self.tools.cleanstr(q.upper())
        media.number = number

        # title
        title_xpath = "//h1[@class='h1--dense']"
        title = browser.find_elements_by_xpath(title_xpath)
        media.update({'m_title': title[0].text})

        summary_xpath = "//div[@class='movie-info section divider']/div[@class='movie-detail']/p"
        summary = browser.find_elements_by_xpath(summary_xpath)
        media.update({'m_summary': summary[0].text})

        media.update(
            {'m_poster': 'https://www.1pondo.tv/assets/sample/%s/str.jpg' % number})

        media.update(
            {'m_art_url': 'https://www.1pondo.tv/assets/sample/%s/str.jpg' % number})

        media.update({'m_studio': '一本道'})

        # Collection
        collection_xpath = "//li[@class='movie-detail__spec'][3]/span[@class='spec-content']"
        Collection = browser.find_elements_by_xpath(collection_xpath)
        media.update({'m_collections': Collection[0].text})

        # datatime
        datatime_xpath = "//li[@class='movie-detail__spec'][1]/span[@class='spec-content']"
        datatime = browser.find_elements_by_xpath(datatime_xpath)
        media.update({'m_year': datatime[0].text})
        media.update({'m_originally_available_at': datatime[0].text})

        # types
        categorys_xpath = "//span[@class='spec-content']/a[@class='spec__tag']"
        categorys = browser.find_elements_by_xpath(categorys_xpath)

        categorys_list = []
        for item in categorys:
            categorys_list.append(self.tools.cleanstr(item.text))
        categorys = ','.join(categorys_list)
        if len(categorys) > 0:
            media.category = categorys

        # actor
        actor = {}
        xpath_actor_name = "//li[@class='movie-detail__spec'][2]/span[@class='spec-content']"
        actor_name = browser.find_elements_by_xpath(xpath_actor_name)
        if len(actor_name) > 0:
            for i, actorname in enumerate(actor_name):
                actor.update({self.tools.cleanstr2(
                    actorname.text): ''})
        media.actor = actor

        return media

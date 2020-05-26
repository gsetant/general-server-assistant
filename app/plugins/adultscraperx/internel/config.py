# -*- coding: utf-8 -*-
import io
import json


class ConfigManager():
    '''
    全局配置文件管理类
    '''

    def getLocalXpath(self, website_name):
        '''
        获取局部站点配置
        website_name:站点名称(对应着包名,xml文件名)
        return: <dict>
        '''
        item = {
            'html_xpath': {}
        }
        print(u'读取 %s Xpath json数据' % website_name)
        jsondata = io.open('./app/spider/%s.json' %
                           website_name, encoding='utf-8').read()
        data = json.loads(jsondata)

        pageurl_xpath = data['html_xpath']['pageurl']
        ### html_xpath bgin ###
        id_xpath = data['html_xpath']['m_id']
        number_xpath = data['html_xpath']['m_number']
        title_xpath = data['html_xpath']['m_title']
        poster_xpath = data['html_xpath']['m_poster']
        summary_xpath = data['html_xpath']['m_summary']
        studio_xpath = data['html_xpath']['m_studio']
        directors_xpath = data['html_xpath']['m_directors']
        collections_xpath = data['html_xpath']['m_collections']
        year_xpath = data['html_xpath']['m_year']
        originallyAvailableAt_xpath = data['html_xpath']['m_originallyAvailableAt']
        type_xpath = data['html_xpath']['m_type']
        actor_xpath = data['html_xpath']['m_actor']
        ### html_xpath end ###

        item.update({
            'html_xpath': {
                'pageurl': pageurl_xpath,
                'm_id': id_xpath,
                'm_number': number_xpath,
                'm_title': title_xpath,
                'm_poster': poster_xpath,
                'm_summary': summary_xpath,
                'm_studio': studio_xpath,
                'm_directors': directors_xpath,
                'm_collections': collections_xpath,
                'm_year': year_xpath,
                'm_originallyAvailableAt': originallyAvailableAt_xpath,
                'm_type': type_xpath,
                'm_actor': actor_xpath
            }
        })

        return item

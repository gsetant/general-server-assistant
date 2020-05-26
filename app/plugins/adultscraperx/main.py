import re

from app.core.model.plugin_respond import PluginRespond
from app.plugins.config import spider_config


def search(meta_info):
    plugin_respond = PluginRespond()
    meta_data_list = []
    video_title = meta_info.get('video_title')
    # TODO movie type need to design
    movie_type = 'censored'

    if movie_type != "" or not spider_config.SOURCE_LIST[movie_type]:
        for template in spider_config.SOURCE_LIST[movie_type]:
            # 循环模板列表
            code_list = []

            re_list = re.finditer(template['pattern'], video_title, re.IGNORECASE)
            for item in re_list:
                code_list.append(item.group())

            while '' in re_list:
                re_list.remove('')

            if len(code_list) == 0:
                continue
            # 对正则匹配结果进行搜索
            for code in code_list:
                web_list = template['web_list']
                code = template['formatter'].format(code)
                for webSiteClass in web_list:
                    web_site = webSiteClass()
                    items = web_site.search(code)
                    for item in items:
                        meta_data_list.append(item)

    if len(meta_data_list) > 0:
        plugin_respond.state = True
        plugin_respond.meta_data = meta_data_list
    return plugin_respond

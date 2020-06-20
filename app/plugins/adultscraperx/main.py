import re

from app.core.service.plugin_service import get_user_plugin_setting
from app.plugins.adultscraperx.config import get_info
from app.plugins.adultscraperx.setting import spider_config


def search(meta_info):
    meta_data_list = []
    video_title = meta_info.get('video_title')
    part_file = meta_info.get('part_file')
    user_setting = get_user_plugin_setting(get_info('en').get('name'), {'name': meta_info.get('name')})
    movie_type = ''
    if user_setting.get('japan_censored_directory_mark') in part_file:
        movie_type = 'censored'
    elif user_setting.get('japan_uncensored_directory_mark') in part_file:
        movie_type = 'uncensored'
    elif user_setting.get('japan_animation_directory_mark') in part_file:
        movie_type = 'animation'
    elif user_setting.get('europe_directory_mark') in part_file:
        movie_type = 'europe'

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
                    items = web_site.search_with_img(code)
                    for item in items:
                        meta_data_list.append(item)

    return meta_data_list

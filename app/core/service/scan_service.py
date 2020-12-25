from werkzeug.utils import import_string

from app.core.service.libraries_service import libraries_detail
from app.core.service.plugin_service import get_user_plugin_setting
from app.core.service.user_service import get_user_by_token
from app.tools.cache_tools import get_cache_by_id
from app.tools.log_tools import log
from urllib.request import quote
import base64
import json



def run_scan(data):
    result = []
    user_info = get_user_by_token(data.get('token'))
    details = libraries_detail(user_info.get("name"), data.get("video_librarySectionTitle"))
    if details and details.get('libraries') and details.get('active'):
        for plugin in details.get('active'):
            plugin_model = import_string('app.plugins.%s.main' % plugin)
            plugin_config = import_string('app.plugins.%s.config' % plugin)
            user_setting = get_user_plugin_setting(plugin_config.get_info('en').get('name'), {'name': user_info.get('name')})
            meta_data = None
            user_setting = get_user_plugin_setting(plugin_config.get_info('en').get('name'),
                                                   {'name': user_info.get('name')})
            try:
                meta_data = plugin_model.search(data, user_setting)
            except Exception as ex:
                log('error', repr(ex), plugin)

            result.extend(trans_to_dict(meta_data))
            save_pic_to_db(result)
            if data.get('autoFlag'):
                return result

    return result


def run_manual_scan(data, user_info):
    plugin = data.get("selectPlugin")
    result = []
    plugin_model = import_string('app.plugins.%s.main' % plugin)
    plugin_config = import_string('app.plugins.%s.config' % plugin)
    user_setting = get_user_plugin_setting(plugin_config.get_info('en').get('name'), {'name': user_info.get('name')})
    meta_data = {}
    try:
        meta_data = plugin_model.search(data, user_setting)
    except Exception as ex:
        log('error', repr(ex), plugin)
    result.extend(trans_to_dict(meta_data))
    # save_pic_to_db(result)
    return result


def trans_to_dict(object_list):
    dic_list = []
    for meta_object in object_list:
        if type(meta_object).__name__ == 'dict':
            dic_list.append(meta_object)
        else:
            dic_list.append(meta_object.get_dic())
    return dic_list


def save_pic_to_db(meta_data_list):
    """
        save result picture to database
    : param meta_data_list meta data list
    :return: meta_dta_list with picture url
    """
    pic_base_url = '/picture/'
    for meta_data in meta_data_list:
        cache_id = meta_data.get('cache_id')
        if meta_data.get('poster'):
            url = "poster/%s" % cache_id
            meta_data.update({'poster': pic_base_url + url})
        if meta_data.get('thumbnail'):
            url = "thumbnail/%s" % cache_id
            meta_data.update({'thumbnail': pic_base_url + url})
        if meta_data.get('actor'):
            meta_actor = meta_data.get('actor')
            for (k, v) in meta_data.get('actor').items():
                url = "%s/%s" % (k, cache_id)
                url = quote(url)
                meta_actor.update({k: pic_base_url + url})
            meta_data.update({'actor': meta_actor})
    return meta_data_list


def get_pic(pic_type, cache_id):
    """
        get picture
    : param pic_type type of picture
    : cache_id cache it
    :return: picture base64
    """
    cache = get_cache_by_id(cache_id)
    meta_data = cache.get('meta_data')
    if pic_type == 'poster':
        return meta_data.get('poster')
    if pic_type == 'thumbnail':
        return meta_data.get('thumbnail')
    else:
        return meta_data.get('actor').get(pic_type)

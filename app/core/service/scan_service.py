from werkzeug.utils import import_string

from app.core.service.clusterService import get_node_info, run_master_scan, run_master_slave_scan
from app.core.service.libraries_service import libraries_detail
from app.core.service.plugin_service import get_user_plugin_setting
from app.core.service.user_service import get_user_by_token
from app.tools.cache_tools import get_cache_by_id, set_cache, check_item_exist
from app.tools.log_tools import log
from urllib.request import quote


def run_scan(data):
    result = []
    user_info = get_user_by_token(data.get('token'))
    details = libraries_detail(user_info.get("name"), data.get("video_librarySectionTitle"))
    if details and details.get('libraries') and details.get('active'):
        for plugin in details.get('active'):
            plugin_model = import_string('app.plugins.%s.main' % plugin)
            plugin_config = import_string('app.plugins.%s.config' % plugin)
            user_setting = get_user_plugin_setting(plugin_config.get_info('en').get('name'),
                                                   {'name': user_info.get('name')})
            meta_data_list = []

            try:
                # choice search method by node status
                node_status = get_node_info()
                # master role
                if node_status.get('role') == 'master':
                    meta_data_list = run_master_scan(plugin, user_setting, data)

                # master&slave role
                if node_status.get('role') == 'master&slave':
                    meta_data_list = run_master_slave_scan(plugin, user_setting, data)

                # slave roles
                if node_status.get('role') == 'slave':
                    meta_data_list = trans_to_dict(plugin_model.search(data, user_setting))

                meta_data_list = set_or_get_cache_id(meta_data_list, plugin_config.get_info('en').get('name'))
            except Exception as ex:
                log('error', repr(ex), plugin)

            result.extend(meta_data_list)
            save_pic_to_db(result)
            if data.get('autoFlag'):
                return result

    return result


def set_or_get_cache_id(meta_data, plugin_name):
    """
        set or get meta data from db cache
    : param meta_data: meta data list
    : param plugin_name: plugin name
    :return: meta_data_list with cache id
    """
    meta_data_list = []
    for item in meta_data:
        cache_item = check_item_exist(item, plugin_name)
        if cache_item:
            meta_data_list.append(cache_item)
        else:
            cache_id = set_cache(
                item["code"], item, plugin_name)
            item['cache_id'] = cache_id
            meta_data_list.append(item)
    return meta_data_list


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


def run_scan_from_master(plugin_name, user_setting, request_data):
    """
        run scan task assigned by master node
    : param plugin_name: plugin name
    : param user_setting: user setting
    : request_data: request query from Media server
    :return: meta_data_list
    """
    plugin_model = import_string('app.plugins.%s.main' % plugin_name)
    return trans_to_dict(plugin_model.search(request_data, user_setting))


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

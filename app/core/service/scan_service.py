from werkzeug.utils import import_string

from app.core.service.libraries_service import libraries_detail
from app.core.service.plugin_service import get_user_plugin_setting
from app.core.service.user_service import get_user_by_token
from app.tools.log_tools import log
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
            try:
                meta_data = plugin_model.search(data, user_setting)
            except Exception as ex:
                log('error', repr(ex), plugin)

            result.extend(trans_to_dict(meta_data))
            if data.get('autoFlag'):
                return result

    return result


def run_manual_scan(data, user_info):
    plugin = data.get("selectPlugin")
    result = []
    plugin_model = import_string('app.plugins.%s.main' % plugin)
    plugin_config = import_string('app.plugins.%s.config' % plugin)
    user_setting = get_user_plugin_setting(plugin_config.get_info('en').get('name'), {'name': user_info.get('name')})
    try:
        meta_data = plugin_model.search(data, user_setting)
    except Exception as ex:
        log('error', repr(ex), plugin)
    result.extend(trans_to_dict(meta_data))
    return result


def trans_to_dict(object_list):
    dic_list = []
    for meta_object in object_list:
        dic_list.append(meta_object.get_dic())
    return dic_list

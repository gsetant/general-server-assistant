from werkzeug.utils import import_string

from app.core.model.plugin_respond import PluginRespond
from app.core.service.libraries_service import libraries_detail
from app.core.service.user_service import get_user


def run_scan(data):
    result = []
    user_info = get_user(data.get('name'), data.get('password'))
    details = libraries_detail(user_info.get("name"), data.get("video_librarySectionTitle"))
    if details and details.get('libraries') and details.get('active'):
        for plugin in details.get('active'):
            plugin_model = import_string('app.plugins.%s.main' % plugin)
            meta_data = plugin_model.search(data)
            result.extend(trans_to_dict(meta_data))
            if data.get('autoFlag'):
                return result
    return result


def trans_to_dict(object_list):
    dic_list = []
    for meta_object in object_list:
        dic_list.append(meta_object.get_dic())
    return dic_list

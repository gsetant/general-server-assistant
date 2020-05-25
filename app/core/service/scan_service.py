from werkzeug.utils import import_string
from app.core.service.libraries_service import libraries_detail
from app.core.service.user_service import get_user


def run_scan(data):
    user_info = get_user(data.get('name'), data.get('password'))
    details = libraries_detail(user_info.get("name"), data.get("video_librarySectionTitle"))
    meta_data_list = []
    if details and details.get('libraries') and details.get('active'):
        for plugin in details.get('active'):
            plugin_model = import_string('app.plugins.%s.main' % plugin)
            meta_data = plugin_model.search(data)
            if meta_data.get("state") is True:
                meta_data_list.append(meta_data)
        if len(meta_data_list) > 0:
            return meta_data_list
    return None

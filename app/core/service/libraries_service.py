from bson import ObjectId

from app.core.service.plugin_service import get_all_plugin_name
from app.tools.db_tools import get_collection


def get_libraries_settings(user_name):
    """
        get user libraries settings
    :param user_name: user name
    :return: list settings
    """
    collection = get_collection('user_libraries')
    query = {
        "user_name": user_name
    }
    settings = collection.find(query)
    plugins_active = get_all_plugin_name()
    result = []
    for setting in settings:
        if setting.get('active'):
            data_plugin = ''
            for plugin in setting['active']:
                if plugin in plugins_active:
                    data_plugin += ',' + plugin
            setting['active'] = data_plugin
        setting['id'] = str(setting['_id'])
        setting.pop('_id')
        setting['active'] = setting['active'][1:]
        result.append(setting)
    return result


def libraries_detail(user_name, libraries):
    """
        get user libraries settings
    :param libraries: search libraries
    :param user_name: user name
    :return: list settings
    """
    collection = get_collection('user_libraries')
    query = {
        "user_name": user_name,
        "libraries": libraries
    }
    settings = collection.find_one(query)
    all_plugin = get_all_plugin_name()

    if settings:
        result = {
            'libraries': settings.get('libraries'),
            'active': settings.get('active'),
            'disable': list(set(all_plugin.split(',')).difference(set(settings.get('active'))))
        }
        return result
    return {
        'libraries': '',
        'active': [],
        'disable': all_plugin.split(',')
    }


def save_libraries_settings(user_name, settings):
    """
        save user libraries settings
    :param settings: list settings
    :param user_name: user name
    :return:
    """
    collection = get_collection("user_libraries")
    if settings.get('id'):
        query = {
            '_id': ObjectId(settings['id']),
        }
        collection.delete_one(query)
    settings['user_name'] = user_name
    collection.insert(settings)


def del_libraries_settings(user_name, settings):
    """
        delete user libraries settings
    :param settings: list settings
    :param user_name: user name
    :return:
    """
    collection = get_collection("user_libraries")
    query = {
        '_id': ObjectId(settings['id']),
        'user_name': user_name
    }
    collection.delete_one(query)

from werkzeug.utils import import_string, find_modules

from app.tools.db_tools import get_collection


def get_all_plugin_name():
    """
        scan and return all installed plugins' name
    :return: str names split by ','
    """
    modules = find_modules(f'app.plugins', include_packages=True, recursive=False)
    names = ''
    for name in modules:
        names += ','+name[name.rfind('.')+1:]
    if len(names) > 0:
        names = names[1:]
    return names


def get_plugin_info(plugin_name, lang):
    """
        get plugin information by plugin name
    :param plugin_name: str plugin name
    :param lang: str language for i18n
    :return: dict plugin info
    """
    module = import_string('app.plugins.%s.config' % plugin_name)
    plugin_info = module.get_info(lang)
    return plugin_info


def get_plugin_setting(plugin_name, lang):
    """
        get plugin setting form
    :param plugin_name: str plugin name
    :param lang: str language for i18n
    :return: dict plugin info
    """
    module = import_string('app.plugins.%s.config' % plugin_name)
    plugin_info = module.get_settings(lang)
    return plugin_info


def get_user_plugin_setting(plugin_name, user_info):
    """
        get user plugin setting from database
    :param plugin_name: str plugin name
    :param user_info: dict user info
    :return: dict user plugin setting
    """
    collection = get_collection("pluginSetting")
    query = {
        'name': user_info["name"],
        'plugin': plugin_name
    }
    plugin_setting = collection.find_one(query)
    if plugin_setting:
        return plugin_setting.get('data')
    else:
        return None


def get_plugin_infos(plugin_names, lang):
    """
        get all available plugins' info
    :param str plugin_names:
    :param str lang:
    :return: dict plugin infos
    """
    plugin_infos = []
    plugin_names = plugin_names.split(',')
    plugin_names_have = get_all_plugin_name()
    for plugin_name in plugin_names:
        if plugin_name in plugin_names_have:
            plugin_infos.append(get_plugin_info(plugin_name, lang))
    return plugin_infos


def save_plugin_setting(plugin_name, plugin_setting, user_info):
    """
        save(insert or update) user plugin setting to database
    :param plugin_name: str plugin name
    :param plugin_setting: dict user plugin setting
    :param user_info: dict user info
    :return:
    """
    collection = get_collection("pluginSetting")
    query = {
        'name': user_info["name"],
        'plugin': plugin_name,
    }
    setting = {
        'name': user_info["name"],
        'plugin': plugin_name,
        'data': plugin_setting,
    }
    if collection.find_one(query):
        collection.update(query, setting)
    else:
        collection.insert(setting)


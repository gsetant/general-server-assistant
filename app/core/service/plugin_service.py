from werkzeug.utils import import_string, find_modules

from app.tools.db_tools import get_collection


def get_all_plugin_name():
    modules = find_modules(f'app.plugins', include_packages=True, recursive=False)
    names = ''
    for name in modules:
        names += ','+name[name.rfind('.')+1:]
    if len(names) > 0:
        names = names[1:]
    return names


def get_plugin_info(plugin_name, lang):
    module = import_string('app.plugins.%s.config' % plugin_name)
    plugin_info = module.get_info(lang)
    return plugin_info


def get_plugin_setting(plugin_name, lang):
    module = import_string('app.plugins.%s.config' % plugin_name)
    plugin_info = module.get_settings(lang)
    return plugin_info


def get_user_plugin_setting(plugin_name, user_info):
    collection = get_collection("pluginSetting")
    query = {
        'name': user_info["name"],
        'plugin': plugin_name
    }
    plugin_setting = collection.find_one(query)
    return plugin_setting['data']


def get_plugin_infos(plugin_names, lang):
    plugin_infos = []
    plugin_names = plugin_names.split(',')
    plugin_names_have = get_all_plugin_name()
    for plugin_name in plugin_names:
        if plugin_name in plugin_names_have:
            plugin_infos.append(get_plugin_info(plugin_name, lang))
    return plugin_infos


def save_plugin_setting(plugin_name, plugin_setting, user_info):
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


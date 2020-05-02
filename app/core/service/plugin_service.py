def get_all_plugin_name():

    return 'AdultScraperX,douban'


def get_plugin_info(plugin_name):
    plugin_info = {
        "name": plugin_name,
        "tittle": plugin_name,
        "icon": ""
    }
    return plugin_info


def get_plugin_infos(plugin_names):
    plugin_infos =[]
    plugin_names = plugin_names.split(',')
    plugin_names_have = get_all_plugin_name()
    for plugin_name in plugin_names:
        if plugin_name in plugin_names_have:
            plugin_infos.append(get_plugin_info(plugin_name))
    return plugin_infos

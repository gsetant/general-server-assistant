import os
import shutil
import uuid
import zipfile
from urllib.request import urlretrieve

import requests
from lxml import etree
from werkzeug.utils import import_string, find_modules

from app.tools.db_tools import get_collection
from app.tools.init_tools import install_plugin_require


def get_all_plugin_name():
    """
        scan and return all installed plugins' name
    :return: str names split by ','
    """
    modules = find_modules(f'app.plugins', include_packages=True, recursive=False)
    names = ''
    for name in modules:
        names += ',' + name[name.rfind('.') + 1:]
    if len(names) > 0:
        names = names[1:]
    return names


def get_all_plugin_info(language):
    """
        get all plugin info in the server
    :return: all plugin info
    """
    names = get_all_plugin_name()
    names = names.split(',')
    plugin_infos = []
    for name in names:
        plugin_infos.append(get_plugin_info(name, language))
    return plugin_infos


def get_plugin_info(plugin_name, lang):
    """
        get plugin information by plugin name
    :param plugin_name: str plugin name
    :param lang: str language for i18n
    :return: dict plugin info
    """
    if plugin_name == '':
        return None
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
    collection = get_collection("plugin_setting")
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
    collection = get_collection("plugin_setting")
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


def install_plugin(github_address):
    """
        install plugin with github address
    :param github_address: the github address for install plugin
    :return: status : success or fail with err msg
    """
    # TODO add check function, check if the github address is a gestant plugin
    branch = get_plugin_version_from_github(github_address)[0]
    download_and_install_plugin(github_address, branch)
    return 'success'


def install_plugin_version(github_address, version):
    """
        install plugin with github address
    :param version: plugin version
    :param github_address: the github address for install plugin
    :return: status : success or fail with err msg
    """
    # TODO add check function, check if the github address is a gestant plugin
    branch = version
    download_and_install_plugin(github_address, branch)
    return 'success'


def download_and_install_plugin(github_address, branch):
    """
        download and install plugin into gestant
    :param github_address: basic github address
    :param branch: tag or branch to download
    :return:
    """
    github_address = github_address + "/archive/%s.zip" % branch

    file_name = str(uuid.uuid1())
    urlretrieve(github_address, "download/%s.zip" % file_name)
    # unzip
    with zipfile.ZipFile('download/%s.zip' % file_name, 'r') as zzz:
        zzz.extractall('download/%s' % file_name)

    # rename dir
    plugin_dir = ''
    for root, dirs, files in os.walk('download/%s' % file_name):
        plugin_dir = dirs[0]
        break
    plugin_name = plugin_dir
    plugin_name = plugin_name.replace('-%s' % branch, '')

    # remove old and install new
    delete_plugin_if_exist(plugin_name)
    shutil.move("download/%s/%s" % (file_name, plugin_dir), "app/plugins/%s" % plugin_name)
    # install plugin requirements
    install_plugin_require()


def delete_plugin_if_exist(plugin_name):
    """
        delete plugin
    :param plugin_name: plugin name
    :return:
    """
    if os.path.exists("app/plugins/%s" % plugin_name):
        shutil.rmtree("app/plugins/%s" % plugin_name)


def get_plugin_version_from_github(github_address):
    """
        get plugin version info from github
    :param github_address: plugin's github address
    :return: list version info
    """
    git_tag_url = github_address + '/tags'
    html = etree.HTML(requests.get(git_tag_url).content)
    tag_list = []
    tags = html.xpath('/html/body/div[4]/div/main/div[2]/div/div[2]/div/div[1]/div/div[1]/h4/a/text()')
    for tag in tags:
        tag = tag.replace(' ', '')
        tag = tag.replace('\n', '')
        tag_list.append(tag)
    tag_list.append('master')
    return tag_list


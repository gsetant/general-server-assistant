import os
import sys

from app.core.service.clusterService import get_node_info, init_node_info
from app.core.service.plugin_service import get_all_plugin_name
from app.tools.config_tools import get_config, REQUIREMENTS_CONFIG, APP_CONFIG
from app.tools.db_tools import get_connection, get_collection
from app.tools.package_tools import get_package_info, install_package
from app.tools.sha1_tools import sha1_encode

app_config = get_config(APP_CONFIG)


def get_app_info():
    """
        get installed python package information
    :return: str info
    """
    requirements = get_config(REQUIREMENTS_CONFIG)["requirements"]
    pip_version = os.popen('pip -V').read().split(' ')[1]
    python_version = sys.version[0:5]
    info = {
        "pip_version": pip_version,
        "python_version": python_version
    }
    for requirement in requirements:
        version = get_package_info(requirement['name'])
        info[requirement['name']] = version
    return info


def install_app_require():
    """
        use pip to install packages stated in requirements.json
    :return:
    """
    requirements = get_config(REQUIREMENTS_CONFIG)["requirements"]
    for requirement in requirements:
        install_package(requirement["name"], requirement["version"])


def install_plugin_require():
    """
        use pip to install packages stated in plugins' requirements.json
    :return:
    """
    plugins_name = get_all_plugin_name()
    if plugins_name == '':
        return
    for plugin in plugins_name.split(','):
        config = get_config('app/plugins/%s/requirements.json' % plugin)
        if config:
            requirements = config.get('requirements')
            if requirements:
                for requirement in requirements:
                    install_package(requirement.get("name"), requirement.get("version"))


def init_database():
    """
        init database creat database if no exist
    :return: mongo database object
    """
    connection = get_connection()
    database = None
    db_list = connection.list_database_names()
    if not app_config['DB']['DBNAME'] in db_list:
        database = connection[app_config['DB']['DBNAME']]
        database.add_user(app_config['DB']['USER'], app_config['DB']['PWD'])
    return database


def init_cluster_info():
    """
        init cluster info
    """
    node_info = get_node_info()
    if not node_info:
        init_node_info()


def init_data():
    """
        init data (insert user admin if no exist)
    :return:
    """
    collection = get_collection('user')
    if collection.find_one({"name": "admin"}) is None:
        admin_user = app_config["ADMIN"]
        admin_user["password"] = sha1_encode(admin_user["name"] + admin_user["password"])
        admin_user["roles"] = "admin"
        collection.insert(admin_user)


def init_app():
    """
        init app
    :return:
    """
    init_database()
    init_data()
    install_plugin_require()
    init_cluster_info()

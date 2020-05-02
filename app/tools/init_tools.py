import os
import sys

from app.tools.config_tools import get_config, REQUIREMENTS_CONFIG, APP_CONFIG
from app.tools.db_tools import get_connection, get_collection
from app.tools.package_tools import get_package_info, install_package
from app.tools.sha1_tools import sha1_encode

app_config = get_config(APP_CONFIG)


def get_app_info():
    """
        获取app安装的所有包信息
    :return:
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
        根据requirements 配置的引用情况自动安装需要的包
    :return:
    """
    requirements = get_config(REQUIREMENTS_CONFIG)["requirements"]
    for requirement in requirements:
        install_package(requirement["name"], requirement["version"])


def init_database():
    connection = get_connection()
    database = None
    db_list = connection.list_database_names()
    if not app_config['DB']['DBNAME'] in db_list:
        database = connection[app_config['DB']['DBNAME']]
        database.add_user(app_config['DB']['USER'], app_config['DB']['PWD'])
    return database


def init_data():
    collection = get_collection('user')
    if collection.find_one({"role": "admin"}) is None:
        admin_user = app_config["ADMIN"]
        admin_user["password"] = sha1_encode(admin_user["name"] + admin_user["password"])
        admin_user["roles"] = "admin"
        collection.insert(admin_user)


def init_app():
    install_app_require()
    init_database()
    init_data()

# -*- coding:utf-8 -*-

import json

APP_CONFIG = 'config/appConfig.json'
REQUIREMENTS_CONFIG = 'config/requirements.json'

config = {}


def get_config(file_name):
    """
        get config by file name
    :param file_name: file name
    :return: dict config
    """
    if not config.get(file_name):
        with open(file_name, 'r', encoding='utf-8') as f:
            app = f.read()
            f.close()
        config[file_name] = json.loads(app)
    return config[file_name]

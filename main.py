#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ***********************************

# 初始化自动安装 基本 环境支持包  ###别换地方
from app.tools.init_base_package import init_base_require
init_base_require()

import logging
from app.tools.config_tools import APP_CONFIG, get_config
from app.tools.init_tools import init_app
from app.tools.router_tools import register_blueprints

# init project install packages
init_app()

from flask import Flask
from flask_cors import *

app = Flask(__name__)
app_config = get_config(APP_CONFIG)
CORS(app, supports_credentials=True)

# register blueprints
register_blueprints(app, 'app.core.api', 'api')
# region start
if __name__ == "__main__":
    app.debug = app_config['DEBUG']
    app.run(
        host=app_config['HOST'],
        port=app_config['PORT'],
        use_reloader=False
    )

logging.basicConfig(level=logging.INFO)

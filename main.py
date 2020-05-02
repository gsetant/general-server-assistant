#! /usr/bin/env python
# -*- coding: utf-8 -*-
# ***********************************

from app.tools.config_tools import APP_CONFIG, get_config
from app.tools.init_tools import init_app
from app.tools.router_tools import register_blueprints

# 初始化项目，解决依赖及建立数据库
init_app()

from flask import Flask
from flask_cors import *

app = Flask(__name__)
app_config = get_config(APP_CONFIG)
CORS(app, supports_credentials=True)

# 注册蓝图
register_blueprints(app, 'app.core.api', 'api')

# region 程序启动
if __name__ == "__main__":
    app.debug = app_config['DEBUG']
    app.run(
        host=app_config['HOST'],
        port=app_config['PORT'],
        use_reloader=False
    )

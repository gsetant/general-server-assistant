import os
import sys
from app.tools.config_tools import get_config, REQUIREMENTS_CONFIG, APP_CONFIG
from app.tools.package_tools import get_package_info, install_package

def init_base_require():
    """
        use pip to install packages stated in requirements.json
    :return:
    """
    requirements = get_config(REQUIREMENTS_CONFIG)["requirements"]
    for requirement in requirements:
        install_package(requirement["name"], requirement["version"])
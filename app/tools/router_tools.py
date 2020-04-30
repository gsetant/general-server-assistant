from werkzeug.utils import find_modules, import_string


def register_blueprints(flask_app=None, project_name=None, key_attribute='api'):
    """
    自动的导入的蓝图模块
    :param key_attribute: 蓝图关键字
    :param project_name:  the dotted name for the package to find child modules.
    :param flask_app: flask app 对象
    :return:
    """
    if not flask_app:
        import warnings
        warnings.warn('路由注册失败,需要传入Flask对象实例')
        return None
    if project_name:
        modules = find_modules(f'{project_name}', include_packages=True, recursive=True)
        for name in modules:
            module = import_string(name)
            if hasattr(module, key_attribute):
                flask_app.register_blueprint(getattr(module, key_attribute))
    else:
        import warnings
        warnings.warn('路由注册失败,外部项目名称还没定义')

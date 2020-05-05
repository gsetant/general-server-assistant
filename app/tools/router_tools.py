from werkzeug.utils import find_modules, import_string


def register_blueprints(flask_app=None, project_name=None, key_attribute='api'):
    """
        automatically register flask blueprint
    :param key_attribute: str key world for blueprint file
    :param project_name:  the dotted name for the package to find child modules.
    :param flask_app: flask app
    :return:
    """
    if not flask_app:
        return None
    if project_name:
        modules = find_modules(f'{project_name}', include_packages=True, recursive=True)
        for name in modules:
            module = import_string(name)
            if hasattr(module, key_attribute):
                flask_app.register_blueprint(getattr(module, key_attribute))

from functools import wraps

from flask import request

from app.core.model.plugin_respond import PluginRespond
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service import user_service
from app.core.service.plugin_service import get_all_plugin_name
from app.tools.jwt_tools import renew_jwt, verify_jwt, decode_jwt


def media_server_authentication(api_function):
    """
        use to check user authentication(jwt)
        if not login return code 401
    :param api_function:
    :return: dump json from respond_model
    """

    @wraps(api_function)
    def fun_dec(*args, **kwargs):
        request_model = RequestModel(request)
        user_info = user_service.get_user_by_token(request_model.data.get('token'))
        plugin_respond = PluginRespond()
        if user_info is not None:
            # user info correct
            plugin_respond = api_function(*args, **kwargs)
            return plugin_respond.dump_json(), 200
        else:
            plugin_respond.state = False
            return plugin_respond.dump_json(), 401

    return fun_dec


def authentication(api_function):
    """
        use to check user authentication(jwt)
        if not login return code 401
    :param api_function:
    :return: dump json from respond_model
    """

    @wraps(api_function)
    def fun_dec(*args, **kwargs):
        request_model = RequestModel(request)
        if request_model.token and verify_jwt(request_model.token):
            respond_model = api_function(*args, **kwargs)
            if not respond_model.token:
                respond_model.token = renew_jwt(request_model.token)
            if respond_model.message == 'authorization error':
                respond_model.code = 50012
                return respond_model.dump_json(), 403
            respond_model.code = 20000
            respond_model.message = 'success'
            return respond_model.dump_json(), 200
        else:
            respond_model = RespondModel()
            respond_model.message = 'authentication error, please login'
            respond_model.code = 50012
            return respond_model.dump_json(), 401

    return fun_dec


class authorization(object):
    def __init__(self, roles=''):
        self.roles = roles

    def __call__(self, api_function):
        """
               check if user have certain roles
        """

        @wraps(api_function)
        @authentication
        def fun_dec(*args, **kwargs):
            request_model = RequestModel(request)
            user_info = decode_jwt(request_model.token)['user_info']
            if self.roles in user_info.get('roles'):
                respond_model = api_function(*args, **kwargs)
                return respond_model
            else:
                respond_model = RespondModel()
                respond_model.message = 'authorization error'
                return respond_model

        return fun_dec


def plugin_authorization(plugin_name):
    """
        check if user have authority to access the plugin that they want to access
    :param plugin_name: the plugin name which user want to access
    :return: Boolean
    """
    request_model = RequestModel(request)
    roles = decode_jwt(request_model.token)['user_info'].get('roles')
    if 'admin' in roles:
        roles = 'admin,' + get_all_plugin_name()
    if plugin_name in roles:
        return True
    else:
        return False

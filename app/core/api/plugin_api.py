from flask import Blueprint, request

from app.core.aop.authority import authentication, plugin_authorization
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service.plugin_service import get_plugin_infos, get_plugin_info, get_plugin_setting, save_plugin_setting, \
    get_user_plugin_setting
from app.tools.jwt_tools import decode_jwt

api = Blueprint('plugin_api', __name__)


@api.route('/plugin/info', methods=['get'])
@authentication
def plugin_infos():
    plugin_names = request.args.get("pluginNames")
    lang = request.args.get("lang")
    respond_model = RespondModel()
    respond_model.data = get_plugin_infos(plugin_names, lang)
    return respond_model


@api.route('/plugin/info/<lang>/<plugin_name>', methods=['get'])
@authentication
def plugin_info(lang, plugin_name):
    respond_model = RespondModel()
    if not plugin_authorization(plugin_name):
        respond_model.message = 'authorization error'
        return respond_model
    respond_model.data = get_plugin_info(plugin_name, lang)
    return respond_model


@api.route('/plugin/setting/<lang>/<plugin_name>', methods=['get'])
@authentication
def plugin_setting(lang, plugin_name):
    respond_model = RespondModel()
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    if not plugin_authorization(plugin_name):
        respond_model.message = 'authorization error'
        return respond_model
    data = {
        'form': get_plugin_setting(plugin_name, lang),
        'userSetting': get_user_plugin_setting(plugin_name, user_info_jwt)
    }
    respond_model.data = data
    return respond_model


@api.route('/plugin/setting/<plugin_name>', methods=['post'])
@authentication
def save_setting(plugin_name):
    respond_model = RespondModel()
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    if not plugin_authorization(plugin_name):
        respond_model.message = 'authorization error'
        return respond_model
    save_plugin_setting(plugin_name, request_model.data, user_info_jwt)
    return respond_model

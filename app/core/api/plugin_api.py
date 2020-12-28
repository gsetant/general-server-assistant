from flask import Blueprint, request

from app.core.aop.authority import authentication, plugin_authorization, authorization
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service.plugin_service import get_plugin_infos, get_plugin_info, get_plugin_setting, save_plugin_setting, \
    get_user_plugin_setting, get_all_plugin_info, install_plugin, download_and_install_plugin, delete_plugin_if_exist, \
    get_plugin_version_from_github, install_plugin_version
from app.tools.init_tools import install_plugin_require
from app.tools.jwt_tools import decode_jwt

api = Blueprint('plugin_api', __name__)


@api.route('/plugin/info', methods=['get'])
@authentication
def plugin_infos():
    """
        return all plugins info which user have the authority to access
    :return: respond_model
    """
    plugin_names = request.args.get("pluginNames")
    lang = request.args.get("lang")
    respond_model = RespondModel()
    respond_model.data = get_plugin_infos(plugin_names, lang)
    return respond_model


@api.route('/plugin/info/<lang>/<plugin_name>', methods=['get'])
@authentication
def plugin_info(lang, plugin_name):
    """
        return plugin info if user have authority
    :param lang: language for i18n
    :param plugin_name: plugin name
    :return: respond_model
    """
    respond_model = RespondModel()
    if not plugin_authorization(plugin_name):
        respond_model.message = 'authorization error'
        return respond_model
    respond_model.data = get_plugin_info(plugin_name, lang)
    return respond_model


@api.route('/plugin/setting/<lang>/<plugin_name>', methods=['get'])
@authentication
def plugin_setting(lang, plugin_name):
    """
        get plugin setting form and user plugin setting
    :param lang: language for i18n
    :param plugin_name: plugin name
    :return: respond_model
    """
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
    """
        save user plugin setting
    :param plugin_name: plugin name
    :return: respond_model
    """
    respond_model = RespondModel()
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    if not plugin_authorization(plugin_name):
        respond_model.message = 'authorization error'
        return respond_model
    save_plugin_setting(plugin_name, request_model.data, user_info_jwt)
    return respond_model


@api.route('/setting/plugin/<lang>', methods=['get'])
@authorization('admin')
def all_plugin_info(lang):
    """
        return all plugin info available in the server
    :return: respond_model
    """
    respond_model = RespondModel()
    respond_model.data = get_all_plugin_info(lang)
    return respond_model


@api.route('/setting/plugin/install', methods=['post'])
@authorization('admin')
def install_new_plugin():
    """
        install new plugin
    :return:
    """
    request_model = RequestModel(request)
    respond_model = RespondModel()
    respond_model.data = install_plugin(request_model.data.get('github'))
    # install plugin requirements
    install_plugin_require()
    return respond_model


@api.route('/setting/plugin/delete', methods=['post'])
@authorization('admin')
def delete_plugin():
    """
        delete plugin
    :return:
    """
    request_model = RequestModel(request)
    respond_model = RespondModel()
    delete_plugin_if_exist(request_model.data.get('name'))
    return respond_model


@api.route('/setting/plugin/version', methods=['post'])
@authorization('admin')
def get_plugin_version_info():
    """
        get all plugin version from github
    :return:
    """
    respond_model = RespondModel()
    request_model = RequestModel(request)
    respond_model.data = get_plugin_version_from_github(request_model.data.get('github'))
    return respond_model


@api.route('/setting/plugin/update', methods=['post'])
@authorization('admin')
def install_by_version():
    """
        install plugin by version
    :return:
    """
    request_model = RequestModel(request)
    respond_model = RespondModel()
    respond_model.data = install_plugin_version(request_model.data.get('github'), request_model.data.get('version'))
    # install plugin requirements
    install_plugin_require()
    return respond_model

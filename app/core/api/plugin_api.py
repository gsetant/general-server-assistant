from flask import Blueprint, request

from app.core.aop.authority import authentication
from app.core.model.respond_model import RespondModel
from app.core.service.plugin_service import get_plugin_infos, get_plugin_info

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
    respond_model.data = get_plugin_info(plugin_name, lang)
    return respond_model

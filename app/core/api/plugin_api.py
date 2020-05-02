from flask import Blueprint, request

from app.core.aop.authority import authentication
from app.core.model.respond_model import RespondModel
from app.core.service.plugin_service import get_plugin_infos

api = Blueprint('plugin_api', __name__)


@api.route('/plugin/info', methods=['get'])
@authentication
def plugin_infos():
    plugin_names = request.args.get("pluginNames")
    respond_model = RespondModel()
    respond_model.data = get_plugin_infos(plugin_names)
    return respond_model

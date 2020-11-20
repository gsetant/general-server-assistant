import base64
from flask import Blueprint, request, make_response

from app.core.aop.authority import media_server_authentication, authentication
from app.core.model.plugin_respond import PluginRespond
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service.scan_service import run_scan, run_manual_scan, get_pic
from app.tools.jwt_tools import decode_jwt

api = Blueprint('scan_api', __name__)


@api.route('/scan', methods=['post'])
@media_server_authentication
def scan():
    """
        scan
    :return: respond model with metaDate
    """
    plugin_respond = PluginRespond()
    request_model = RequestModel(request)
    meta_data_list = run_scan(request_model.data)
    if meta_data_list and len(meta_data_list) > 0:
        plugin_respond.state = True
        plugin_respond.meta_data = meta_data_list
    else:
        plugin_respond.state = False
    return plugin_respond


@api.route('/scan/manual', methods=['post'])
@authentication
def manual_scan():
    """
        manual scan
    :return: respond model with metaDate
    """
    respond_model = RespondModel()
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    meta_data_list = run_manual_scan(request_model.data, user_info_jwt)
    respond_model.data = meta_data_list
    return respond_model


@api.route('/picture/<pic_type>/<cache_id>', methods=['get'])
def picture(pic_type, cache_id):
    """
        get picture
    : param pic_type type of picture
    : cache_id cache it
    :return: picture
    """
    pic_base64 = get_pic(pic_type, cache_id)
    response = make_response(base64.b64decode(pic_base64))
    response.headers.set('Content-Type', 'image/jpeg')
    response.headers.set(
        'Content-Disposition', 'attachment', filename='%s.jpg' % cache_id)
    return response

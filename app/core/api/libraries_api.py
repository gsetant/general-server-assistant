from flask import Blueprint, request

from app.core.aop.authority import authentication
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service.libraries_service import get_libraries_settings, save_libraries_settings, libraries_detail, \
    del_libraries_settings
from app.tools.jwt_tools import decode_jwt

api = Blueprint('libraries_api', __name__)


@api.route('/libraries/settings', methods=['get'])
@authentication
def libraries_settings():
    """
        return all libraries settings by user
    :return: respond_model
    """
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    respond_model = RespondModel()
    respond_model.data = get_libraries_settings(user_info_jwt['name'])
    return respond_model


@api.route('/libraries/detail', methods=['post'])
@authentication
def detail():
    """
        return all libraries settings detail
    :return: respond_model
    """
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    respond_model = RespondModel()
    respond_model.data = libraries_detail(user_info_jwt['name'], request_model.data.get('libraries'))
    return respond_model


@api.route('/libraries/settings', methods=['post'])
@authentication
def save_settings():
    """
        return all libraries settings by user
    :return: respond_model
    """
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    respond_model = RespondModel()
    save_libraries_settings(user_info_jwt['name'], request_model.data)
    return respond_model


@api.route('/libraries/settings/del', methods=['post'])
@authentication
def del_settings():
    """
        del libraries settings by user
    :return: respond_model
    """
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    respond_model = RespondModel()
    del_libraries_settings(user_info_jwt['name'], request_model.data)
    return respond_model

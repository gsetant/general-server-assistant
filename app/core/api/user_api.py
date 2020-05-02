from flask import Blueprint, request

from app.core.aop.authority import authentication
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service import user_service
from app.tools.jwt_tools import generate_jwt, decode_jwt

api = Blueprint('service', __name__)


@api.route('/login', methods=['post'])
def login():
    request_model = RequestModel(request)

    user_info = user_service.login(request_model.data.get('user_info'))
    respond_model = RespondModel()
    if user_info is not None:
        respond_model.token = generate_jwt(user_info)
        respond_model.message = 'login success'
        respond_model.code = 20000
    else:
        respond_model.message = 'username or password wrong!'
    return respond_model.dump_json()


@api.route('/user', methods=['post'])
@authentication
def user():
    request_model = RequestModel(request)
    user_info_form = request_model.data.get('user_info')
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    respond_model = RespondModel()
    if user_info_form and user_info_form['name'] == user_info_jwt['name']:
        user_service.update(user_info_form)
        respond_model.message = 'success'
        respond_model.token = generate_jwt(user_info_form)
        return respond_model
    respond_model.message = 'error'
    return respond_model


@api.route('/user/info', methods=['get'])
@authentication
def user_info():
    request_model = RequestModel(request)
    jwt = request_model.token
    user_info_jwt = decode_jwt(jwt)['user_info']
    respond_model = RespondModel()
    respond_model.message = 'success'
    respond_model.data = user_info_jwt
    return respond_model


@api.route('/user/logout', methods=['get'])
def user_logout():
    respond_model = RespondModel()
    respond_model.message = 'success'
    respond_model.token = ''
    respond_model.code = 20000
    return respond_model.dump_json(), 200

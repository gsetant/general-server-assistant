from flask import request

from app.core.model.request_model import RequestModel
from app.core.model.resspond_model import RespondModel
from app.tools.jwt_tools import renew_jwt, verify_jwt, decode_jwt


def authentication(api_function):
    def fun_dec(*args, **kwargs):
        request_model = RequestModel(request)
        if request_model.jwt and verify_jwt(request_model.jwt):
            respond_model = api_function(*args, **kwargs)
            respond_model.jwt = renew_jwt(respond_model.jwt)
            if respond_model.message == 'authorization error':
                return respond_model.dump_json(), 401
            return respond_model.dump_json(), 200
        else:
            respond_model = RespondModel()
            respond_model.message = 'authentication error'
            return respond_model.dump_json(), 401

    return fun_dec


class authorization(object):

    def __init__(self, allow=''):
        self.allow = allow

    def __call__(self, api_function):
        @authentication
        def fun_dec(*args, **kwargs):
            request_model = RequestModel(request)
            user_info = decode_jwt(request_model.jwt)['user_info']
            if (user_info.get('authority') and user_info.get('authority') in self.allow) \
                    or user_info['role'] == 'admin':
                respond_model = api_function(*args, **kwargs)
                return respond_model
            else:
                respond_model = RespondModel()
                respond_model.message = 'authorization error'
                return respond_model

        return fun_dec

import json

from flask import Response


class RespondModel:
    jwt = ''
    data = {}
    message = ''
    state = ''
    headers = {}

    def __init__(self):
        self.jwt = ''
        self.data = {}
        self.message = ''
        self.state = ''

    def dump_json(self):
        if self.data is None or self.message is None:
            raise Exception('respond incomplete')

        self.headers['Authorization'] = self.jwt
        self.headers['Access-Control-Expose-Headers'] = 'Authorization'

        self.__dict__.pop('jwt')
        return Response(json.dumps(self.__dict__), mimetype='application/json', headers=self.headers)

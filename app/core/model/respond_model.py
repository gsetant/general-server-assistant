import json

from flask import Response


class RespondModel:
    """
        model contain respond information
        all api respond should return this object
    """
    token = ''
    data = {}
    message = ''
    code = ''
    headers = {}

    def __init__(self):
        self.token = ''
        self.data = {}
        self.message = ''
        self.code = ''

    def dump_json(self):
        """
            generate json
        :return: json
        """
        if self.data is None or self.message is None or self.code is None:
            raise Exception('respond incomplete')

        self.headers['Authorization'] = self.token
        self.headers['Access-Control-Expose-Headers'] = 'Authorization'

        self.__dict__.pop('token')
        return Response(json.dumps(self.__dict__), mimetype='application/json', headers=self.headers)

import json

from flask import Response


class PluginRespond:
    """
       model plugin respond
    """

    meta_data: []
    state: {}

    def get_dic(self):
        return self.__dict__

    def dump_json(self):
        """
            generate json
        :return: json
        """
        return Response(json.dumps(self.__dict__), mimetype='application/json')

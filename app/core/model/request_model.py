import json


class RequestModel:
    """
       model contain request information
    """
    token = ''
    data = {}

    def __init__(self, request):
        self.token = request.headers.get("gsetant-Token")
        json_str = request.get_data(as_text=True)
        if json_str is not None and json_str != '':
            self.data = json.loads(json_str)
        else:
            self.data = {}

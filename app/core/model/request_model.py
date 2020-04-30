import json


class RequestModel:
    jwt = ''
    data = {}

    def __init__(self, request):
        self.jwt = request.headers.get("jwt")
        self.data = json.loads(request.get_data(as_text=True))

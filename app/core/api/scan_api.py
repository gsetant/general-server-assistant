from flask import Blueprint, request

from app.core.aop.authority import media_server_authentication
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service.scan_service import run_scan

api = Blueprint('scan_api', __name__)


@api.route('/scan', methods=['post'])
@media_server_authentication
def scan():
    """
        scan
    :return: respond model with metaDate
    """
    request_model = RequestModel(request)
    respond_model = RespondModel()
    meta_data_list = run_scan(request_model.data)
    if meta_data_list:
        request_model.data = meta_data_list
    return respond_model

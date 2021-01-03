from flask import Blueprint, request

from app.core.aop.authority import authentication, cluster_authentication
from app.core.model.request_model import RequestModel
from app.core.model.respond_model import RespondModel
from app.core.service.clusterService import get_node_info, set_node_info, validate_master

api = Blueprint('cluster_api', __name__)


@api.route('/cluster/node', methods=['get'])
@authentication
def get_node():
    """
        get current node info
    """
    respond_model = RespondModel()
    node_info = get_node_info()
    if node_info:
        respond_model.data = node_info
    return respond_model


@api.route('/cluster/node', methods=['post'])
@authentication
def set_node():
    """
        set current node info
    """
    request_model = RequestModel(request)
    respond_model = RespondModel()
    set_node_info(request_model.data)
    return respond_model


@api.route('/cluster/heartbeat', methods=['post'])
@cluster_authentication
def heart_beat():
    """
        heart beat check
    """
    return RespondModel()
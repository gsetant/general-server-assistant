import json

import requests

from app.tools.config_tools import get_config, APP_CONFIG
from app.tools.db_tools import get_collection


def get_node_info():
    """
        get node info
    :return: current node info
    """
    collection = get_collection('cluster_info')
    node_info = collection.find_one({})
    if node_info:
        node_info.pop('_id')
    check_node_slave_status(node_info)
    return node_info


def set_node_info(node_info):
    """
        set node info
    : param node_info : node info
    """
    collection = get_collection('cluster_info')
    collection.delete_many({})
    collection.insert(node_info)


def init_node_info():
    """
        init node info
    """
    node_info = {
        'role': 'slave',
        'slaves': []
    }
    set_node_info(node_info)


def validate_master(token):
    """
        validate master credential
    """
    cluster_token = get_config(APP_CONFIG)['CLUSTER_TOKEN']
    return token == cluster_token


def check_slave_health(slave):
    """
        check slave health
    """
    url = 'http://' + slave.get('IP') + ':' + slave.get('port') + '/cluster/heartbeat'
    request_data = json.dumps({
        'token': slave.get('token')
    })
    try:
        respond = requests.post(url, request_data)
        message = json.loads(respond.text).get('message')
        if message == 'success':
            return 'ONLINE'
        else:
            return message
    except Exception:
        return 'OFFLINE'


def check_node_slave_status(node_info):
    """
        check the status of all slave nodes
    """
    slaves = node_info.get('slaves')
    for slave in slaves:
        slave['status'] = check_slave_health(slave)


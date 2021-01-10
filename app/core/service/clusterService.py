import json

import requests

from app.tools.config_tools import get_config, APP_CONFIG
from app.tools.db_tools import get_collection

current_index = 0


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


def get_online_node():
    """
        get online node
    :return: online node list
    """
    online_node = []
    current_node = get_node_info().get('slaves')
    for node in current_node:
        if node.get('status'):
            online_node.append(node)
    return online_node


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


def run_master_scan(plugin_name, user_setting, request_data):
    """
            run cluster scan as master role
    : param plugin_name: plugin name
    : param user_setting: user setting
    : request_data: request query from Media server
    :return: meta_data_list
    """
    cluster_node = get_online_node()
    return run_cluster_scan(cluster_node, plugin_name, user_setting, request_data)


def run_master_slave_scan(plugin_name, user_setting, request_data):
    """
            run cluster scan as master&slave role
    : param plugin_name: plugin name
    : param user_setting: user setting
    : request_data: request query from Media server
    :return: meta_data_list
    """
    cluster_node = get_online_node()
    cluster_node.append(
        {'IP': '127.0.0.1',
         'port': get_config(APP_CONFIG)['PORT'],
         'token': get_config(APP_CONFIG)['CLUSTER_TOKEN']}
    )
    return run_cluster_scan(cluster_node, plugin_name, user_setting, request_data)


def run_cluster_scan(cluster_nodes, plugin_name, user_setting, request_data):
    """
        run cluster scan
    : param cluster_nodes current online nodes
    : param plugin_name: plugin name
    : param user_setting: user setting
    : request_data: request query from Media server
    :return: meta_data_list
    """
    meta_data_list = []
    online_node = cluster_nodes
    global current_index
    if current_index >= len(online_node):
        current_index = 0
    node = online_node[current_index]
    url = 'http://' + node.get('IP') + ':' + node.get('port') + '/cluster/scan'
    request_data = json.dumps({
        'token': node.get('token'),
        'plugin_name': plugin_name,
        'user_setting': user_setting,
        'query': request_data
    })
    try:
        respond = requests.post(url, request_data)
        meta_data_list = json.loads(respond.text).get('data')
        current_index += 1
    except Exception:
        return []
    return meta_data_list

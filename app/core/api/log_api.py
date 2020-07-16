from flask import Blueprint

from app.core.aop.authority import authorization
from app.core.model.respond_model import RespondModel
from app.core.service.log_service import get_log_string, get_log_file_length, get_new_log

api = Blueprint('log_api', __name__)


@api.route('/log/plugin/<plugin_name>', methods=['get'])
@authorization('admin')
def get_plugin_log(plugin_name):
    """
        get plugin full log
    :param plugin_name: plugin name
    :return: {
                "length" : "length of log file",
                "log" : "log string"
            }
    """
    plugin_log_file = 'log/plugin/%s.log' % plugin_name
    respond_model = RespondModel()
    file_length = get_log_file_length(plugin_log_file)
    log_string = get_log_string(plugin_log_file)
    respond_model.data = {"length": file_length, "log": log_string}
    return respond_model


@api.route('/log/new/plugin/<plugin_name>/<line_number>', methods=['get'])
@authorization('admin')
def get_plugin_log_new(plugin_name, line_number):
    """
        get plugin log from specific line
    :param line_number: specific line number
    :param plugin_name: plugin name
    :return: {
                "length" : "length of log file",
                "log" : "log string"
            }
    """
    plugin_log_file = 'log/plugin/%s.log' % plugin_name
    respond_model = RespondModel()
    file_length = get_log_file_length(plugin_log_file)
    log_string = get_new_log(plugin_log_file, line_number)
    respond_model.data = {"length": file_length, "log": log_string}
    return respond_model


@api.route('/log/admin', methods=['get'])
@authorization('admin')
def get_admin_log():
    """
        get plugin full log
    :return: {
                "length" : "length of log file",
                "log" : "log string"
            }
    """
    plugin_log_file = 'log/general.log'
    respond_model = RespondModel()
    file_length = get_log_file_length(plugin_log_file)
    log_string = get_log_string(plugin_log_file)
    respond_model.data = {"length": file_length, "log": log_string}
    return respond_model


@api.route('/log/new/admin/<line_number>', methods=['get'])
@authorization('admin')
def get_admin_log_new(line_number):
    """
        get plugin log from specific line
    :param line_number: specific line number
    :return: {
                "length" : "length of log file",
                "log" : "log string"
            }
    """
    plugin_log_file = 'log/general.log'
    respond_model = RespondModel()
    file_length = get_log_file_length(plugin_log_file)
    log_string = get_new_log(plugin_log_file, line_number)
    respond_model.data = {"length": file_length, "log": log_string}
    return respond_model

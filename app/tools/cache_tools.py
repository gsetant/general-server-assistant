import threading

from app.tools.db_tools import get_collection


def check_cache(code, plugin_name):
    """
        check meta info cache
    :param code: verify code
    :param plugin_name: plugin name
    :return: meta data
    """
    lock = threading.Lock()
    meta_info = None
    lock.acquire()
    try:
        search_query = {
            'code': code,
            'plugin_name': plugin_name
        }
        collection = get_collection('meta_cache')
        meta_info = collection.find_one(search_query)
        if meta_info is not None:
            meta_info = meta_info['meta_data']
    finally:
        lock.release()
        return meta_info


def set_cache(code, meta_data, plugin_name):
    """
        set meta info cache
    :param code: verify code
    :param plugin_name: plugin name
    :return:
    """
    lock = threading.Lock()
    lock.acquire()
    cache_data = {}
    try:
        cache_data.update({'code': code})
        cache_data.update({'plugin_name': plugin_name})
        cache_data.update({'meta_data': meta_data})
        search_query = {
            'code': code,
            'plugin_name': plugin_name
        }
        collection = get_collection('meta_cache')
        meta_info = collection.find_one(search_query)
        if meta_info is None:
            collection.insert(cache_data)
    finally:
        lock.release()

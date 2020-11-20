import threading

from bson import ObjectId

from app.tools.db_tools import get_collection


def get_cache_by_id(cache_id):
    """
        get cache by cache id
    :param cache_id: cache id
    :return: cache
    """
    collection = get_collection('meta_cache')
    cache = collection.find_one({"_id": ObjectId(cache_id)})
    return cache


def check_cache(code, plugin_name):
    """
        check meta info cache
    :param code: verify code
    :param plugin_name: plugin name
    :return: meta data cache list
    """
    lock = threading.Lock()
    meta_info_cache = []
    lock.acquire()
    try:
        search_query = {
            'code': code,
            'plugin_name': plugin_name
        }
        collection = get_collection('meta_cache')
        meta_infos = collection.find(search_query)
        if meta_infos is not None:
            for meta_info in meta_infos:
                meta_info.get('meta_data').update({'cache_id': str(meta_info.get('_id'))})
                meta_info_cache.append(meta_info['meta_data'])
    finally:
        lock.release()
        return meta_info_cache


def set_cache(code, meta_data, plugin_name):
    """
        set meta info cache
    :param code: verify code
    :param meta_data: meta_data
    :param plugin_name: plugin name
    :return:
    """
    lock = threading.Lock()
    lock.acquire()
    cache_data = {}
    try:
        cache_data.update({'code': code})
        cache_data.update({'plugin_name': plugin_name})
        cache_data.update({'meta_data': meta_data.get_dic()})
        search_query = {
            'code': code,
            'plugin_name': plugin_name
        }
        collection = get_collection('meta_cache')
        # meta_info = collection.find_one(search_query)
        # if meta_info is None:
        return str(collection.insert(cache_data))
    finally:
        lock.release()

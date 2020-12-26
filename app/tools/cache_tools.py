import threading

from bson import ObjectId
import copy
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
                meta_info.pop('_id')
                meta_info_cache.append(meta_info['meta_data'])
    finally:
        lock.release()
        return meta_info_cache


def check_item_exist(item, plugin_name):
    """
        chech caceh by hash code
    :param item: use this item to generate hash code
    :param plugin_name: plugin name
    :return: meta data cache
    """
    search_query = {
        'hash_code': make_hash(item),
        'plugin_name': plugin_name
    }
    collection = get_collection('meta_cache')
    meta_info = collection.find_one(search_query)
    if meta_info:
        meta_info.get('meta_data').update({'cache_id': str(meta_info.get('_id'))})
        meta_info.pop('_id')
        return meta_info['meta_data']
    return None


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
        cache_data.update({'hash_code': make_hash(meta_data)})
        cache_data.update({'plugin_name': plugin_name})
        cache_data.update({'meta_data': meta_data})
        collection = get_collection('meta_cache')
        return str(collection.insert(cache_data))
    finally:
        lock.release()


def make_hash(o):
    """
  Makes a hash from a dictionary, list, tuple or set to any level, that contains
  only other hashable types (including any lists, tuples, sets, and
  dictionaries).
  """

    if isinstance(o, (set, tuple, list)):

        return tuple([make_hash(e) for e in o])

    elif not isinstance(o, dict):

        return hash(o)

    new_o = copy.deepcopy(o)
    new_o['cache_id'] = ''
    for k, v in new_o.items():
        new_o[k] = make_hash(v)

    return hash(tuple(frozenset(sorted(new_o.items()))))

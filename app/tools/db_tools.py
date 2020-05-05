# -*- coding:utf-8 -*-
import pymongo

from app.tools.config_tools import get_config, APP_CONFIG

connection = None
database = None
APP_CONF = get_config(APP_CONFIG)


def get_connection():
    """
        get mongo connection
    :return: mongo connection
    """
    global connection
    if connection is None:
        connection = pymongo.MongoClient(host=APP_CONF['DB']['HOST'],
                                         port=APP_CONF['DB']['PORT'],
                                         username=APP_CONF['DB']['USER'],
                                         password=APP_CONF['DB']['PWD'])
    return connection


def get_database():
    """
        get mongo database object
    :return: mongo database object
    """
    global database
    if database is None:
        database = get_connection()[APP_CONF['DB']['DBNAME']]
        database.authenticate(APP_CONF['DB']['USER'], APP_CONF['DB']['PWD'])
    return database


def get_collection(collection):
    """
        get mongo collection object
    :param collection: collection name
    :return: mongo collection object
    """
    return get_database()[collection]

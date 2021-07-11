from secrets import token_urlsafe

from app.core.service.plugin_service import get_all_plugin_name
from app.tools.db_tools import get_collection
from app.tools.log_tools import log
from app.tools.sha1_tools import sha1_encode


def login(user_info):
    """
        user login
    :param user_info: dict user info
    :return: dict user info
    """
    user_info = get_user(user_info.get('name'), user_info.get('password'))
    if user_info is not None:
        user_info.pop("_id")
        log('info', 'user login: %s' % user_info.get('name'))
        return user_info
    return None


def user_sign_up(user_info):
    """
        user sign up
    :param user_info: dict user info
    :return:
    """
    collection = get_collection("user")
    if collection.find_one({'name': user_info.get('name')}):
        return False
    collection.insert(
        {
            'name': user_info.get('name'),
            'password': get_password(user_info.get('name'), user_info.get('password')),
            'email': user_info.get('email'),
            'roles': 'poweruser'
        }
    )
    return True


def get_user(name, password):
    """
        get user by name and password
    :param name: user name
    :param password: password
    :return: user info
    """
    collection = get_collection("user")
    user_info = collection.find_one({"name": name, "password": get_password(name, password)})
    return user_info


def get_user_by_token(token):
    """
        use plugin token to get use info
    :param token: plugin token
    :return: user info
    """
    collection = get_collection("user")
    user_info = collection.find_one({"token": token})
    return user_info


def update(user_info):
    """
        update user info in database
    :param user_info: dict user info
    :return: insert or update
    """
    collection = get_collection("user")
    if collection.find_one({"name": user_info['name']}):
        collection.update({"name": user_info['name']}, user_info)
        return False
    else:
        collection.insert(user_info)
        return True


def get_password_from_db(user_info):
    """
        get user password from database
    :param user_info: user info
    :return: password
    """
    collection = get_collection("user")
    user_from_db = collection.find_one({'name': user_info['name']})
    return user_from_db.get('password')


def update_password(user_info):
    """
        update password
    :param user_info:
    :return:
    """
    collection = get_collection("user")
    if user_info.get('password') and user_info.get('password') != '':
        user_info['password'] = get_password(user_info['name'], user_info['password'])
    log('info', 'password saved')
    update_states = update(user_info)
    if '_id' in user_info:
        user_info.pop("_id")
    return update_states


def get_password(user_name, password):
    return sha1_encode(user_name + password)


def generate_token(user):
    """
        save plugin token
    :return: token
    """
    token = token_urlsafe(16)
    user['token'] = token
    update(user)
    return token


def get_all_user_info():
    """
        get all user info
    :return: user info in list
    """
    collection = get_collection("user")
    user_infos = list(collection.find())
    for user_info in user_infos:
        user_info.pop('_id')
        user_info.pop('password')
    return user_infos


def del_user_by_username(name):
    """
        del user by username
    :param name username
    :return:
    """
    collection = get_collection("user")
    collection.delete_one({"name": name})
    return True

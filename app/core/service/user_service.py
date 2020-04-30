from app.tools.db_tools import get_collection
from app.tools.sha1_tools import sha1_encode


def login(user_info):
    collection = get_collection("user")
    user_info = collection.find_one({"name": user_info.get('name'),
                                     "password": get_password(user_info.get('name'), user_info.get('password'))})
    if user_info is not None:
        user_info.pop("_id")
        return user_info
    return None


def update(user_info):
    collection = get_collection("user")
    user_info['password'] = get_password(user_info['name'], user_info['password'])
    collection.update({"name": user_info['name']}, user_info)


def get_password(user_name, password):
    return sha1_encode(user_name + password)

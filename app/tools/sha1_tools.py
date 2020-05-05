from hashlib import sha1

from app.tools.config_tools import get_config, APP_CONFIG


def sha1_encode(code):
    """
        sha1 encode
    :param code: code
    :return: str code
    """
    code = code + get_config(APP_CONFIG)['SHA1_SECRET_KEY']
    sha1_obj = sha1()
    sha1_obj.update(code.encode())
    ret = sha1_obj.hexdigest()
    return ret

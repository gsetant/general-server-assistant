import time

import jwt

from app.tools.config_tools import get_config, APP_CONFIG


def generate_jwt(user_info):
    """
        generate json web token by user_info
    :param user_info: dict user info
    :return: str json web token
    """
    iat = time.time()
    token_dict = {
        'iat': iat,
        'nbf': iat,
        'exp': iat + 300,
        'user_info': user_info
    }
    headers = {
        'alg': "HS256",
    }
    jwt_token = jwt.encode(token_dict,
                           get_config(APP_CONFIG)['JWT_SECRET_KEY'],
                           algorithm="HS256",
                           headers=headers
                           )
    return jwt_token


def renew_jwt(token):
    """
        using old jwt to generate new jwt
    :param token: str old jwt
    :return: str new jwt
    """
    data = decode_jwt(token)
    if data:
        user_info = data['user_info']
        return generate_jwt(user_info)
    return ''


def decode_jwt(token):
    """
        decode and get payload form jwt
    :param token: str jwt
    :return: dict payload
    """
    try:
        return jwt.decode(token, get_config(APP_CONFIG)['JWT_SECRET_KEY'], algorithms=['HS256'])
    except jwt.PyJWTError:
        return None


def verify_jwt(token):
    """
        verify if jwt have not been modified
    :param token: str jwt
    :return: Boolean
    """
    if decode_jwt(token) is None:
        return False
    else:
        return True

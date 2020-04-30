import time

import jwt

from app.tools.config_tools import get_config, APP_CONFIG


def generate_jwt(user_info):
    iat = time.time()
    token_dict = {
        'iat': iat,
        'nbf': iat,
        'exp': iat + 300,
        'user_info': user_info
    }
    headers = {
        'alg': "HS256",  # 声明所使用的算法
    }
    jwt_token = jwt.encode(token_dict,  # payload, 有效载体
                           get_config(APP_CONFIG)['JWT_SECRET_KEY'],  # 进行加密签名的密钥
                           algorithm="HS256",  # 指明签名算法方式, 默认也是HS256
                           headers=headers  # json web token 数据结构包含两部分, payload(有效载体), headers(标头)
                           ).decode('ascii')  # python3 编码后得到 bytes, 再进行解码(指明解码的格式), 得到一个str
    return jwt_token


def renew_jwt(token):
    data = decode_jwt(token)
    if data:
        user_info = ['user_info']
        return generate_jwt(user_info)
    return ''


def decode_jwt(token):
    try:
        return jwt.decode(token, get_config(APP_CONFIG)['JWT_SECRET_KEY'], algorithms=['HS256'])
    except jwt.PyJWTError:
        return None


def verify_jwt(token):
    if decode_jwt(token) is None:
        return False
    else:
        return True

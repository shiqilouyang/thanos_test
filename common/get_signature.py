#!/usr/bin/python
# -*- encoding: utf-8 -*-
import base64
import json
import hmac
import logging
import hashlib
import sys
import time
from functools import lru_cache
# from Crypto.PublicKey import RSA
# from Crypto.Cipher import PKCS1_v1_5
import requests
import os

from common.read_data import ReadFileData

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")


def generate_auth_info(path: str, method: str, bodymod: str = None, params: dict = {}, algorithms='HmacSHA256',test_user='test_user'):
    global data_file_path
    apikey = ReadFileData().load_ini(data_file_path)[test_user]['apikey']
    secret = ReadFileData().load_ini(data_file_path)[test_user]['secret']
    timestamp = str(int(time.time() * 1000))
    path = '/future' + path
    if bodymod == 'x-www-form-urlencoded' or bodymod is {} or params is not {}:
        params = dict(sorted(params.items(), key=lambda e: e[0]))
        message = "&".join([f"{arg}={params[arg]}" for arg in params])
    elif bodymod == 'json':
        params = params
        message = "&".join([f"{arg}={params[arg]}" for arg in params])
    else:
        logging.error(f'不支持的bodymod参数类型')

    if method == 'get' and len(params.keys()) > 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}#{message}'
    elif method == 'get' and len(params.keys()) == 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}'
    elif method == 'post' and len(params.keys()) > 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}#{message}'
    elif method == 'post' and len(params.keys()) == 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}'
    else:
        logging.error(f'不支持的请求方式--->{method}')
    if algorithms == 'HmacSHA256':
        digestmodule = hashlib.sha256
    elif algorithms == 'HmacMD5':
        digestmodule = hashlib.md5
    elif algorithms == 'HmacSHA1':
        digestmodule = hashlib.sha1
    elif algorithms == 'HmacSHA224':
        digestmodule = hashlib.sha224
    elif algorithms == 'HmacSHA384':
        digestmodule = hashlib.sha384
    elif algorithms == 'HmacSHA512':
        digestmodule = hashlib.sha512
    else:
        logging.error(f'不支持加密算法--->{algorithms}，默认加密算法类--->HmacSHA256')
    sign = hmac.new(secret.encode("utf-8"), signkey.encode("utf-8"), digestmod=digestmodule).hexdigest()
    logging.info(f'生成的加密sign--->{sign}')
    # re = generate_auth_info_for_test(test_user=test_user)
    header = {
        'xt-validate-appkey': apikey,
        'xt-validate-timestamp': timestamp,
        'xt-validate-signature': sign,
        'xt-validate-algorithms': algorithms,
        # 'Authorization': re.get("Authorization")
    }
    return header


def generate_fund_auth(apikey:str, secret:str, path: str, method: str, Channel: str, bodymod: str = None, params: dict = None):
    apikey = apikey
    secret = secret
    timestamp = str(int(time.time() * 1000))
    nonce = timestamp
    if bodymod == 'x-www-form-urlencoded':
        params = dict(sorted(params.items(), key=lambda e: e[0]))
        message = "&".join([f"{arg}={params[arg]}" for arg in params])
    elif bodymod == 'json':
        params = params
        message = "&".join([f"{arg}={params[arg]}" for arg in params])
    else:
        logging.error(f'不支持的bodymod参数类型')

    if method == 'get' and len(params.keys()) > 0:
        signkey = f'{apikey}{timestamp}{nonce}{path}{message}'
    elif method == 'get' and len(params.keys()) == 0:
        signkey = f'{apikey}{timestamp}{nonce}{path}'
    elif method == 'post' and len(params.keys()) > 0:
        signkey = f'{apikey}{timestamp}{nonce}{json.dumps(params)}{path}'
    elif method == 'post' and len(params.keys()) == 0:
        signkey = f'{apikey}{timestamp}{nonce}{path}{message}'
    else:
        logging.error(f'不支持的请求方式--->{method}')
    logging.info(signkey)
    digestmodule = hashlib.sha256
    sign = hmac.new(secret.encode("utf-8"), signkey.encode("utf-8"), digestmod=digestmodule).hexdigest()
    logging.info(f'生成的加密sign--->{sign}')

    header = {
        'Appkey': apikey,
        'Version': 'V1',
        'Channel': Channel,
        'Timestamp': timestamp,
        'Nonce': nonce,
        'Signature': sign
    }
    return header


# 减少请求次数使用python 缓存机制
@lru_cache
def generate_auth_info_for_test(test_user="test_user2"):
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
    user_info = ReadFileData().load_ini(data_file_path)[test_user]
    host = ReadFileData().load_ini(data_file_path)["host"]
    data = json.dumps({
        'countryCode':user_info.get("countryCode"),
        "loginPwd":user_info.get("loginPwd"),
        "userName":user_info.get("userName"),
    })
    header = {'Content-Type': 'application/json','device':'web'}
    # 获取 publicKey/passwdId
    get_publicKey_result = requests.post(host.get("thanos_get_publicKey"), headers=header, data=data).json()
    publicKey = get_publicKey_result.get('data').get('publicKey')
    passwdId = get_publicKey_result.get('data').get('passwdId')
    # 获取token
    params = {
        "countryCode": user_info.get("countryCode"),
        "loginPwd": rsa_password(publicKey, user_info.get("loginPwd")),
        "passwdId": passwdId,
        "puzzleValidateString": "123456",
        "regChannel": "XT",
        "userName": user_info.get("userName"),
        "version": 1.0
    }
    res = requests.post(url=host.get("authorize_token") ,headers=header, json=params)
    return {
        'Authorization':"bearer " + res.json()["data"]["accessToken"]
    }


# rsa公钥加密
def rsa_password(publickey, str):
    try:
        str = str.encode('utf-8')
        publickey = RSA.importKey(base64.b64decode(publickey))
        cipher = PKCS1_v1_5.new(publickey)
        text = base64.b64encode(cipher.encrypt(str))
        return text.decode('utf-8')
    except Exception as e:
        print(f"Unexpected error:{e}", sys.exc_info()[0])


if __name__ == '__main__':
    generate_auth_info_for_test()
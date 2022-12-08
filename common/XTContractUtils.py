import requests
import urllib
import hashlib
import hmac
import time
import json
import re
import traceback

# timeout in 10 seconds:
TIMEOUT = 10


def http_get_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": 'application/x-www-form-urlencoded'
    }
    if add_to_headers:
        headers.update(add_to_headers)
    postdata = urllib.parse.urlencode(params)
    try:
        response = requests.get(url, postdata, headers=headers, timeout=TIMEOUT, stream=True)

        if response.status_code == 200:
            return response.json()
        else:
            print('++++++++++++==response==+++++++++++++')
            print(f"response.headers:{response.headers}")
            print(f"response.request{response.request}")
            print(f"response.json{response.json}")
            print('++++++++++++==reuqest==+++++++++++++')
            print(f"request.headers:{headers}")
            print(f"request.params:{params}")
            print(f"request.url:{response.url}")
            print(f"code != 200 {response.text}")
            return None
    except Exception as e:
        print("httpGet failed, detail is:%s" % traceback.format_exc())
        raise e


def http_post_request(url, params, add_to_headers=None):
    headers = {
        "Content-type": "application/x-www-form-urlencoded",
    }
    if add_to_headers:
        headers.update(add_to_headers)
    try:
        # params 以URl后面拼接字符串的方式提交post请求
        # response = requests.post(url, data=params, headers=headers, timeout=TIMEOUT)
        # response = requests.post(url, params=params, headers=headers, timeout=TIMEOUT)
        # data 以表单的方式提交post请求
        # print(url)
        response = requests.post(url, params=params, headers=headers, timeout=TIMEOUT)

        if response.status_code == 200:
            return response.json()
        else:
            print('++++++++++++==response==+++++++++++++')
            print(f"response.headers:{response.headers}")
            print(f"response.request{response.request}")
            print(f"response.json{response.json}")
            print(f"response.text{response.text}")
            print('++++++++++++==reuqest==+++++++++++++')
            print(f"request.headers:{headers}")
            print(f"request.params:{params}")
            print(f"request.url:{response.url}")
            print(f"code != 200 {response.text}")
            return None
    except Exception as e:
        print("httpPost failed, detail is:%s" % traceback.format_exc())
        raise e


def api_key_get(path, url, access_key, secret_key, bodymod, params):
    header = create_sign(access_key=access_key, secret_key=secret_key, path=path, method="get", bodymod=bodymod,
                         params=params)
    res = http_get_request(url=url, params=params, add_to_headers=header)
    return res


def api_key_post(path, url, access_key, secret_key, bodymod, params):
    header = create_sign(access_key=access_key, secret_key=secret_key, path=path, method="post", bodymod=bodymod,
                         params=params)
    res = http_post_request(url=url, params=params, add_to_headers=header)
    return res


def create_sign(access_key, secret_key, path: str, method: str, bodymod: str = None, params: dict = {},
                algorithms='HmacSHA256'):
    apikey = access_key
    secret = secret_key
    timestamp = str(int(time.time() * 1000))
    # timestamp = "1646378244031"
    if bodymod == 'x-www-form-urlencoded' or bodymod is {} or params is not {}:
        params = dict(sorted(params.items(), key=lambda e: e[0]))
        message = "&".join([f"{arg}={params[arg]}" for arg in params])
    elif bodymod == 'json':
        params = params
        message = "&".join([f"{arg}={params[arg]}" for arg in params])
    else:
        print(f'不支持的bodymod参数类型')

    if method == 'get' and len(params.keys()) > 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}#{message}'
    elif method == 'get' and len(params.keys()) == 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}'
    elif method == 'post' and len(params.keys()) > 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}#{message}'
    elif method == 'post' and len(params.keys()) == 0:
        signkey = f'xt-validate-appkey={apikey}&xt-validate-timestamp={timestamp}#{path}'
    else:
        print(f'不支持的请求方式--->{method}')

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
        print(f'不支持加密算法--->{algorithms}，默认加密算法类--->HmacSHA256')

    sign = hmac.new(secret.encode("utf-8"), signkey.encode("utf-8"), digestmod=digestmodule).hexdigest()
    header = {
        'xt-validate-appkey': apikey,
        'xt-validate-timestamp': timestamp,
        'xt-validate-signature': sign,
        'xt-validate-algorithms': algorithms,
    }
    return header

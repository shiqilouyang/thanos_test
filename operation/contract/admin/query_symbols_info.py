#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_admin_http import xtthanos_admin_http
from api.http_api import ResultBase
from common.logger import logger
from common.read_data import get_data
from common.get_signature import generate_auth_info

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
def query_symbols_info():
    '''合约配置-查询所有'''
    result = ResultBase()
    params = {}
    message, headers = generate_auth_info(access_key, secret_key,params)
    res = xtthanos_admin_http.query_symbols_info(headers=headers,params=message)
    # result.success = False
    result.status_code = res.status_code
    result.response = res.json()
    logger.warning(f"合约配置-查询所有 返回结果 ==>> {res.text}")
    return result

def get_symbol(symbol):
    res = query_symbols_info()
    for i in res.response["result"]:
        # print(i.values())
        if symbol in i.values():
            return i


if __name__ == '__main__':
    print(get_symbol('cfx_usdt'))
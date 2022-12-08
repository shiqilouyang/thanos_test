#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_admin_http import xtthanos_admin_http
from api.http_api import ResultBase
from common.logger import logger
from common.read_data import get_data
from common.get_signature import generate_auth_info

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
def cancel_orderId(orderId):
    '''撤销'''
    result = ResultBase()
    params = {
        'orderId': orderId          # 订单id
       }
    message, headers = generate_auth_info(access_key, secret_key,params)
    res = xtthanos_admin_http.cancel_orderId(orderId,headers=headers,params=message)
    # result.success = False
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"撤销 返回结果 ==>> {res.text}")
    return result

if __name__ == '__main__':
    cancel_orderId("")
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_http
from api.http_api import ResultBase
from common.logger import logger
from common.read_data import get_data
from common.get_signature import generate_auth_info

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
def query_entrustId(entrustId):
    '''根据entrustId查询计划委托'''
    result = ResultBase()
    params = {
        'entrustId' : entrustId    # 计划订单ID
    }
    message, headers = generate_auth_info(access_key, secret_key,params)
    res = xtthanos_http.query_entrustId(headers=headers,params=message)
    # result.success = False
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"根据entrustId查询计划委托 返回结果 ==>> {res.text}")
    return result
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_market_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def get_symbol_list_info():
    '''获取所有交易对的配置信息'''
    result = ResultBase()
    symbol_list = request_data.get('symbol_list')
    params = {}
    path = symbol_list.get('route') + symbol_list.get('path')
    method = symbol_list.get('method')
    headers = generate_auth_info(path=path, method=method,params=params)
    res = xtthanos_market_http.get_symbol_list_info(headers=headers,params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取所有交易对的配置信息 返回结果 ==>> {res.text}")
    return result
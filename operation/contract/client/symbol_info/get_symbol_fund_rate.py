#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_market_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info



def get_symbol_coins():
    '''获取交易对币种'''
    result = ResultBase()
    leverage_bracket_list = request_data.get('symbol_coins')
    params = {}
    path = leverage_bracket_list.get('route') + leverage_bracket_list.get('path')
    method = leverage_bracket_list.get('method')
    headers = generate_auth_info(path=path, method=method,params=params)
    res = xtthanos_market_http.get_symbol_coins(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取交易对的资金费率 返回结果 ==>> {res.text}")
    return result


if __name__ == '__main__':
    get_symbol_coins()


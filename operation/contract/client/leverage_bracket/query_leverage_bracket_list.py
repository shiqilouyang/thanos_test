#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.http_api import ResultBase
from api.thanos_http import xtthanos_market_http, request_data
from common.logger import logger
from common.get_signature import generate_auth_info


def query_leverage_bracket_list():
    '''查询所有交易对杠杆分层'''
    result = ResultBase()
    leverage_bracket_list = request_data.get('leverage_bracket_list')
    params = {}
    path = leverage_bracket_list.get('route') + leverage_bracket_list.get('path')
    method = leverage_bracket_list.get('method')
    headers = generate_auth_info(path=path, method=method,params=params)
    res = xtthanos_market_http.query_leverage_bracket_list(headers=headers,params=params)
    result.success = False
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"查询所有交易对杠杆分层 返回结果 ==>> {res.text}")
    return result

if __name__ == '__main__':
    query_leverage_bracket_list()
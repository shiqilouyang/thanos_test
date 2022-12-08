#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.http_api import ResultBase
from api.thanos_http import request_data, xtthanos_market_http
from common.logger import logger
from common.get_signature import generate_auth_info


def query_leverage_bracket(symbol,test_user="test_user"):
    '''查询单个交易对杠杆分层'''
    result = ResultBase()
    leverage_bracket_detail = request_data.get('leverage_bracket_detail')
    params = {
        'symbol': symbol,  # 交易对
    }
    path = leverage_bracket_detail.get('route') + leverage_bracket_detail.get('path')
    method = leverage_bracket_detail.get('method')
    headers = generate_auth_info(path=path, method=method,params=params,test_user=test_user)
    res = xtthanos_market_http.query_leverage_bracket(headers=headers,params=params)
    result.success = False
    result.response = res.json()
    result.status_code = res.status_code
    logger.info(f"查询单个交易对杠杆分层 返回结果 ==>> {res.text}")
    return result

if __name__ == '__main__':
    query_leverage_bracket('btc_usdt')
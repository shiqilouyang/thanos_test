#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def adjust_leverage(leverage,positionSide,symbol):
    '''调整杠杆倍数'''
    result = ResultBase()
    adjust_leverage = request_data.get('adjust_leverage')
    params = {
        'leverage' : leverage,                      # 杠杆倍数
        'positionSide': positionSide,               # 持仓方向：LONG;SHORT
        'symbol' : symbol                           # 交易对
    }
    path = adjust_leverage.get('route') + adjust_leverage.get('path')
    method = adjust_leverage.get('method')
    headers = generate_auth_info(path=path, method=method,params=params,bodymod='x-www-form-urlencoded')
    res = xtthanos_user_http.adjust_leverage(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"调整杠杆倍数 ==>> 返回结果 ==>> {res.text}")
    return result

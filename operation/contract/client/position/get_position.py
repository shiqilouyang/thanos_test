#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def get_position(symbol,test_user="test_user"):
    '''获取持仓信息'''
    result = ResultBase()
    position_list = request_data.get('position_list')
    params = {
        'symbol' : symbol
    }
    path = position_list.get('route') + position_list.get('path')
    method = position_list.get('method')
    headers = generate_auth_info(path=path, method=method, params=params,test_user=test_user)
    res = xtthanos_user_http.get_position(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取持仓信息 ==>> 返回结果 ==>> {res.text}")
    return result
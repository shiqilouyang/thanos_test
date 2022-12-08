#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def adjust_auto_margin(autoMargin,positionSide,symbol):
    '''修改自动追加保证金'''
    result = ResultBase()
    auto_margin = request_data.get('auto_margin')
    params = {
        'autoMargin' : autoMargin,                        # 是否开启自动追加保证金
        'positionSide' : positionSide,                    # 持仓方向：LONG;SHORT
        'symbol': symbol                                  # 交易对
    }
    path = auto_margin.get('route') + auto_margin.get('path')
    method = auto_margin.get('method')
    headers = generate_auth_info(path=path, method=method,  params=params, bodymod='x-www-form-urlencoded')
    res = xtthanos_user_http.adjust_auto_margin(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"修改自动追加保证金 ==>> 返回结果 ==>> {res.text}")
    return result
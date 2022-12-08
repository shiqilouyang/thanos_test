#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   adjust_margin.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/25 3:53 下午   shuai.xu      1.0         None
'''
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def adjust_margin(margin,positionSide,symbol,type):
    '''修改保证金'''
    result = ResultBase()
    position_margin = request_data.get('position_margin')
    params = {
        'margin' : margin,                        # 数量
        'positionSide' : positionSide,            # 持仓方向：LONG;SHORT
        'symbol': symbol,                         # 交易对
        'type' : type                             # 调整方向（ADD：增加逐仓保证金；SUB：减少逐仓保证金）
    }

    path = position_margin.get('route') + position_margin.get('path')
    method = position_margin.get('method')
    headers = generate_auth_info(path=path, method=method, params=params, bodymod='x-www-form-urlencoded')
    res = xtthanos_user_http.adjust_margin(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"修改保证金 ==>> 返回结果 ==>> {res.text}")
    return result
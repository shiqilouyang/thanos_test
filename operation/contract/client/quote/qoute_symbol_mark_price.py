#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   qoute_symbol_mark_price.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/3/11 5:52 下午   shuai.xu      1.0         None
'''
from api.thanos_http import request_data, xtthanos_market_http
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def qoute_symbol_mark_price(symbol):
    # 获取单个交易对的标记价格
    result = ResultBase()
    qoute_symbol_mark_price = request_data.get('qoute_symbol_mark_price')
    params = {
        "symbol":symbol
    }
    path = qoute_symbol_mark_price.get('route') + qoute_symbol_mark_price.get('path')
    method = qoute_symbol_mark_price.get('method')
    headers = generate_auth_info(path=path, method=method, params=params, bodymod='x-www-form-urlencoded')
    res = xtthanos_market_http.symbol_mark_price(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取单个交易对的标记价格 ==>> {res.text}")
    return result
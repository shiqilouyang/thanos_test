#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   qoute_agg_ticker.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/3/11 5:34 下午   shuai.xu      1.0         None
'''
from api.thanos_http import request_data, xtthanos_market_http
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def qoute_agg_ticker(symbol):
    # 获取指定交易对的聚合行情信息
    result = ResultBase()
    qoute_agg_ticker = request_data.get('qoute_agg_ticker')
    params = {
        "symbol": symbol
    }
    path = qoute_agg_ticker.get('route') + qoute_agg_ticker.get('path')
    method = qoute_agg_ticker.get('method')
    headers = generate_auth_info(path=path, method=method, params=params, bodymod='x-www-form-urlencoded')
    res = xtthanos_market_http.qoute_agg_ticker(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取指定交易对的聚合行情信息 ==>> {res.text}")
    return result
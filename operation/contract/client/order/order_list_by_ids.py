#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   order_list_by_ids.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/3/3 3:58 下午   shuai.xu      1.0         None
'''
from api.http_api import ResultBase
from api.thanos_http import xtthanos_trade_http, logger
from common.get_signature import generate_auth_info
from test_cases.contract.client.conftest import order_request_data


def order_list_by_ids(id):
    '''根据id列表查询订单（订单id用,分隔）'''

    result = ResultBase()
    params = {
        "ids":id
    }
    path = order_request_data.get('list_by_ids').get('path')
    method = order_request_data.get('list_by_ids').get('method')
    headers = generate_auth_info(path=path, method=method, params=params, bodymod='x-www-form-urlencoded')
    res = xtthanos_trade_http.order_list_by_ids(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"根据id列表查询订单（订单id用,分隔） ==>> {res.text}")
    return result
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def get_balance_list(test_user='test_user2'):
    '''获取用户所有资金'''
    result = ResultBase()
    balance_list = request_data.get('balance_list')
    params = {}
    path = balance_list.get('route') + balance_list.get('path')
    method = balance_list.get('method')
    headers = generate_auth_info(path=path, method=method,params=params,test_user=test_user)
    res = xtthanos_user_http.get_balance_list(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取用户所有资金 返回结果 ==>> {res.text}")
    return result

if __name__ == '__main__':
    print(get_balance_list().response)
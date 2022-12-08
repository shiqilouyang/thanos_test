#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def get_account_info(test_user='test_user'):

    '''获取账户相关信息'''
    account_info = request_data.get('account_info')
    result = ResultBase()
    params = {}
    path = account_info.get('route') + account_info.get('path')
    method = account_info.get('method')
    headers = generate_auth_info(path=path,method=method,params=params,test_user=test_user)
    res = xtthanos_user_http.get_account_info(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取账户相关信息 返回结果 ==>> {res.text}")
    return result


if __name__ == '__main__':
    get_account_info()
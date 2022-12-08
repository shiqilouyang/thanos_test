#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def open_thanos():
    '''开通合约
        可以重复开通，返回值一样
     '''
    result = ResultBase()
    account_open = request_data.get('account_open')
    params = {}
    path = account_open.get('route') + account_open.get('path')
    method = account_open.get('method')
    headers = generate_auth_info(path=path, method=method,params=params)
    res = xtthanos_user_http.open_thanos(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"开通合约 返回结果 ==>> {res.text}")
    return result


if __name__ == '__main__':
    open_thanos()
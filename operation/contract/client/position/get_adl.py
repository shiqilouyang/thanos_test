#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def get_adl():
    '''获取ADL信息'''
    result = ResultBase()
    position_adl = request_data.get('position_adl')
    params = {
    }
    path = position_adl.get('route') + position_adl.get('path')
    method = position_adl.get('method')
    headers = generate_auth_info(path=path, method=method,params=params)
    res = xtthanos_user_http.get_adl(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取ADL信息 ==>> 返回结果 ==>> {res.text}")
    return result
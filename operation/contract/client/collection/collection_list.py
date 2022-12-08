#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def collection_list():
    '''收藏交易对列表'''
    result = ResultBase()
    collection_list = request_data.get('collection_list')
    params = {}
    path = collection_list.get('route') +collection_list.get('path')
    method = collection_list.get('method')
    headers = generate_auth_info(path=path, method=method,params=params)
    res = xtthanos_user_http.collection_list(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"收藏交易对列表 返回结果 ==>> {res.text}")
    return result


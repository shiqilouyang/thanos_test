#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def collection_cancel(symbol):
    '''
      取消收藏交易对
        :param symbol: 交易对,string类型,必填
    '''
    collection_cancel = request_data.get('collection_cancel')
    result = ResultBase()
    params = {
        'symbol':symbol
    }
    path = collection_cancel.get('route') + collection_cancel.get('path')
    method = collection_cancel.get('method')
    headers = generate_auth_info(path=path, method=method,params=params,bodymod='x-www-form-urlencoded')
    res = xtthanos_user_http.collection_cancel(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"取消收藏交易对 返回结果 ==>> {res.text}")
    return result
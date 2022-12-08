#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info

def collection_add(symbol):
    '''
    收藏交易对:
    :param symbol: 交易对,string类型,必填
    '''
    result = ResultBase()
    collection_add = request_data.get('collection_add')
    params = {
        'symbol':symbol
    }
    path = collection_add.get('route') + collection_add.get('path')
    method = collection_add.get('method')
    headers = generate_auth_info(path=path, method=method,params=params,bodymod='x-www-form-urlencoded')
    res = xtthanos_user_http.collection_add(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"收藏交易对 返回结果 ==>> {res.text}")
    return result


if __name__ == '__main__':
    collection_add("dao_usdt")

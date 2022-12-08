#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   position_close_all.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/19 10:07 上午   shuai.xu      1.0         None
'''

from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def position_close_all(symbol):
    '''一键平仓'''
    result = ResultBase()
    position_list_close_all = request_data.get('position_list_close_all')
    params = {
        'symbol' : symbol
    }
    path = position_list_close_all.get('route') + position_list_close_all.get('path')
    method = position_list_close_all.get('method')
    headers = generate_auth_info(path=path, method=method, params=params, bodymod='x-www-form-urlencoded')
    res = xtthanos_user_http.position_close_all(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"一键平仓 ==>> 返回结果 ==>> {res.text}")
    return result

if __name__ == '__main__':
    position_close_all("dao_usdt")
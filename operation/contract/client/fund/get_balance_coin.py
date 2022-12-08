#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def get_balance_coin(coin):
    '''
    获取用户单币种资金:
        :param coin: 交易对,string类型,必填
    '''
    result = ResultBase()
    params = {
        'coin' : coin
    }
    balance_detail = request_data.get('balance_detail')
    path = balance_detail.get('route') + balance_detail.get('path')
    method = balance_detail.get('method')
    headers = generate_auth_info(path=path, method=method,params=params)
    res = xtthanos_user_http.get_balance_coin(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"获取用户单币种资金 返回结果 ==>> {res.text}")
    return result

if __name__ == '__main__':
    coin = "usdt"
    get_balance_coin(coin)
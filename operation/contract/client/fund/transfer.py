# !/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def transfer(amount,billSide,coin,test_user="test_user"):
    '''
    资金划转:

    '''
    result = ResultBase()
    balance_transfer = request_data.get('balance_transfer')
    params = {
        'amount' : amount,
        'billSide' : billSide,
        'coin' : coin
    }
    logger.info(f'参数信息是：{params}')
# 暂时只针对测试环境
    path = balance_transfer.get('route') + balance_transfer.get('path')
    method = balance_transfer.get('method')
    headers = generate_auth_info(path=path, method=method,params=params,test_user=test_user)
    res = xtthanos_user_http.transfer(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"资金划转 返回结果 ==>> {res.text}")
    return result


if __name__ == '__main__':
    transfer(20000000, "ADD", "USDT")
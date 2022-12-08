#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_admin_http import xtthanos_admin_http
from api.http_api import ResultBase
from common.logger import logger
from common.read_data import get_data
from common.get_signature import generate_auth_info

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
def query_order_list(accountId,endTime,orderId,page,size,startTime,symbol):
    '''动态条件查询列表'''
    result = ResultBase()
    params = {
        'accountId': accountId,      # 用户id
        'endTime': endTime,          # 结束时间
        'orderId': orderId,          # 订单id
        'page': page,                # 页码
        'size': size,                # 单页数
        'startTime': startTime,      # 开始时间
        'symbol' : symbol            # 合约名
    }
    message, headers = generate_auth_info(access_key, secret_key,params)
    res = xtthanos_admin_http.query_order_list(headers=headers,params=message)
    # result.success = False
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"动态条件查询列表 返回结果 ==>> {res.text}")
    return result


if __name__ == '__main__':
    query_order_list("","","","","","","cfx_usdt")
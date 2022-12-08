#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_user_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def get_balance_bills(coin,direction,endTime,id,limit,startTime,symbol,type):
    '''
    获取用户账务流水
          :param coin: 交易对,string类型,非必填
          :param direction: 方向PREV或NEXT,string类型,非必填,代表id的数字大或者小的记录
          :param endTime: 结束时间,integer(int64),非必填,与数据库startTime对比
          :param id: 搜索Id,string类型,非必填
          :param limit: 条数,string类型,非必填
          :param startTime: 起始时间,integer(int64),非必填,与数据库startTime对比
          :param symbol: 交易对,string类型,非必填
          :param type: EXCHANGE:划转;CLOSE_POSITION:平仓盈亏;TAKE_OVER:仓位接管;QIANG_PING_MANAGER:强平管理费（手续费)\
             ;FUN:资金费用;FEE:手续费 (开仓、平仓、强平);ADL:自动减仓;TAKE_OVER:仓位接管,string类型,非必填
'''
    result = ResultBase()
    balance_bills = request_data.get('balance_bills')
    params = {
        'coin' : coin,
        'direction': direction,
        'endTime': endTime,
        'id': id,
        'limit' : limit,
        'startTime': startTime,
        'symbol': symbol,
        'type': type,

    }
    path = balance_bills.get("route") + balance_bills.get('path')
    method = balance_bills.get('method')
    headers = generate_auth_info(path=path, method=method,params=params,bodymod = 'x-www-form-urlencoded')
    res = xtthanos_user_http.get_balance_bills(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info('获取用户账务流水,接口响应为{}'.format(res.json()))
    return result

if __name__ == '__main__':
    get_balance_bills()
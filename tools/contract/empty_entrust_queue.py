#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   empty_entrust_queue.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/20 2:15 下午   shuai.xu      1.0         None
'''
from pprint import pprint

from api.thanos_http import xtthanos_http
from common.get_signature import generate_auth_info_for_test
from common.logger import logger
from common.mongodb_operate import MongoDb
from model.symbol import symbol as s
from operation.contract.client.order.order_request import OrderRequest


def empty_entrust_queue(symbol,user2_header=None,user_header=None):
    '''
      1, 清空委托队列
         1), 使用 user 吃掉所有做空 市价单
         2), 使用 user2 吃掉所有做多 市价单
     注意:
        尽量选择价格便宜,队列不多的
    '''
    # 查找当前 symbol 所有的订单,根据持仓方向划分队列
    long_entrust = []
    short_entrust = []
    # 获取 symbol_id
    symbol_single = s.query.filter(s.symbol == symbol).first()
    symbol_id = symbol_single.id
    args = {
        "col": "order",
    }
    # 查找当前活跃订单(state=1)
    symbol_position = MongoDb(args).descending_sort_find({
        'symbolId': symbol_id,
        'state':1,
    },'createdTime')
    # 根据做多做空进行分类
    for item in symbol_position:
        if item.get('orderSide') == 1:
            long_entrust.append({
                "orderSide" : item.get('orderSide'),
                'price':item.get('price'),
                'createdTime':item.get('createdTime'),
                'leavingQty':item.get('leavingQty')
            })
        else:
            short_entrust.append({
                "orderSide": item.get('orderSide'),
                'price': item.get('price'),
                'createdTime': item.get('createdTime'),
                'leavingQty': item.get('leavingQty')
            })
        # 查找当前部分成交订单(state=2)
        symbol_position = MongoDb(args).descending_sort_find({
            'symbolId': symbol_id,
            'state': 2,
        }, 'createdTime')
        # 根据做多做空进行分类
        for item in symbol_position:
            if item.get('orderSide') == 1:
                long_entrust.append({
                    "orderSide": item.get('orderSide'),
                    'price': item.get('price'),
                    'createdTime': item.get('createdTime'),
                    'leavingQty': item.get('leavingQty')
                })
            else:
                short_entrust.append({
                    "orderSide": item.get('orderSide'),
                    'price': item.get('price'),
                    'createdTime': item.get('createdTime'),
                    'leavingQty': item.get('leavingQty')
                })
    params = {
        "symbol": symbol,
    }
    # 首先撤销掉 user 与 user2 的所有委托
    if user2_header == None:
        user2_header = generate_auth_info_for_test('test_user2')
        xtthanos_http.order_entrust_cancel_all(headers=user2_header, params=params)
    if user_header == None:
        user_header = generate_auth_info_for_test()
        xtthanos_http.order_entrust_cancel_all(headers=user_header, params=params)

    logger.info("当前做多 LONG 是{}".format(long_entrust))
    logger.info("当前做空 short 是{}".format(short_entrust))

    for i in long_entrust:
        parms_user = {
            'orderSide': "SELL",
            'orderType': 'LIMIT',
            'origQty': i.get('leavingQty'),
            'positionSide': "LONG",
            'symbol': symbol,
            'price': i.get('price'),
             "timeInForce": "IOC"
        }
        logger.info('position_list_user 请求 is {}'.format(parms_user))
        res1 = OrderRequest().create(parm=parms_user, header=user_header)
        logger.info('position_list_user 响应 is {}'.format(res1))


    for i in short_entrust:
        parms_user2 = {
            'orderSide': "BUY",
            'orderType': 'MARKET',
            'origQty': i.get('leavingQty'),
            'positionSide': "LONG",
            'symbol': symbol,
            'price': i.get('price'),
            "timeInForce": "IOC"
        }
        logger.info('position_list_user2 请求 is {}'.format(parms_user2))
        res1 = OrderRequest().create(parm=parms_user2, header=user2_header)
        logger.info('position_list_user2 响应 is {}'.format(res1))


if __name__ == '__main__':
    empty_entrust_queue("bnb_usdt")
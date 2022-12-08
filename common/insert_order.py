#!/usr/bin/python
# -*- encoding: utf-8 -*-
from operation.contract.client.quote import get_depth
from operation.contract.client.order import create_order, query_orderId
from common.logger import logger
from common.mongodb_operate import update_account_balance


class insert_order:
    '''
    mode模式
    1-直接下单
    2-初始化资金，然后下单
    3-初试化深度行情，初始化资金，然后下单
    4-市价单清空深度队列，初始化资金直接下单
    '''
    ''''''
    def __init__(self):
        pass

    def account_init_max(self):
        '''资金初始化，资金最大化'''
        data = {"walletBalance" : 10000000}
        return update_account_balance(data)

    def account_init(self,data):
        return update_account_balance(data)

    def clear_order(self):
        '''市价单清空深度队列,步骤：
        1、查询深度队列数量
        2、账户开仓，数量为队列单方向总数、方向相反
        3、账户平仓，平仓数量为开仓数量
        '''
        res = get_depth(50, 'btc_usdt').response["result"]
        if len(res['a']) > 0 :
            num = sum(float(i[1]) for i in res['a'])
            print(f'a -num ：{num}')
            #  开仓
            create_order('SELL', 'LIMIT', num, 'SHORT', 'btc_usdt', '', 100, '', 'GTC', '', '', '309')
            res = create_order('BUY', 'MARKET', num, 'LONG', 'btc_usdt', '', 100, '', 'GTC', '', '', '309')
            # 查询开仓情况
            orderId = res.response['result']
            print(f'开仓订单Id：{orderId}')
            query_orderId(orderId)
            # 平仓
            positionSide = 'SHORT'
            res_2 = create_order('BUY', 'MARKET', num, positionSide, 'btc_usdt', 1, '', '', 'IOC', '', '', '309')
            # 再次查询深度信息
            get_depth(50, 'btc_usdt')
            # 再次查询订单信息
            orderId = res.response['result']
            query_orderId(orderId)
        else:
            logger.info('深度队列卖单为空')
        # if len(res['b']) > 0:
        #     num = sum(float(i[1]) for i in res['b'])
        #     print(f'b -num ：{num}')
        #     positionSide = 'SHORT'
        #     create_order('SELL', 'MARKET', num, positionSide, 'btc_usdt', 1, '', '', 'IOC', '', '')
        # else:
        #     logger.info('深度队列买单为空')

    def insert_order_init(self,symbol,init_Side,init_positonSide,init_Qty,init_price):
        if init_price != '':
            if ';' in init_price:
                create_order(init_Side, 'LIMIT', init_Qty, init_positonSide, symbol, '', float(init_price.split[";"][0]), '', 'GTC', '', '')
                create_order(init_Side, 'LIMIT', init_Qty, init_positonSide, symbol, '', float(init_price.split[";"][1]), '', 'GTC', '', '')
            else:
                create_order(init_Side, 'LIMIT', init_Qty, init_positonSide, symbol, '', float(init_price), '', 'GTC', '', '')
        else:
            logger.info('撮合不需要初始化订单')




    def order(self,mode,data2,orderSide,orderType,origQty,positionSide,symbol,marketOrderLevel,price,reduceOnly,timeInForce,
          triggerProfitPrice,triggerStopPrice,init_Side,init_positonSide,init_Qty,init_price):
        '''步骤：
        1-初始化清深度队列资金,足够大
        2-初始化深度行情（清空队列数据）
        3-初始化账户余额
        4-初始化撮合队列
        5-下单
        '''
        self.account_init_max()
        self.clear_order()
        self.account_init(data2)
        if mode == 0:
            '''下单撮合初始化不需要深度队列'''
            self.insert_order()
        else:
            '''下单撮合初始化需要深度队列'''
            self.insert_order_init(symbol,init_Side,init_Qty,init_positonSide,init_Qty,init_price)
            self.create_order(orderSide,orderType,origQty,positionSide,symbol,marketOrderLevel,price,reduceOnly,timeInForce,
          triggerProfitPrice,triggerStopPrice)

if __name__ == '__main__':
    insert_order().clear_order()

    # insert_order().order(1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17)
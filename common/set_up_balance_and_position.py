"""
encode:utf-8
Author:aidan.hu
Data:2022/1/13
初始化用户账户和用户仓位
"""
import time
from api.thanos_http import xtthanos_trade_http,request_data
from common.get_signature import generate_auth_info_for_test, generate_auth_info
from common.logger import logger
from operation.contract.client.fund.get_balance_list import get_balance_list
from operation.contract.client.fund.transfer import transfer
from operation.contract.client.order.order_request import OrderRequest
from operation.contract.client.order_entrust.order_entrust_cancel_all import order_entrust_cancel_all
from operation.contract.client.position.get_position import get_position
from operation.contract.client.position.position_class import Positon
from operation.contract.client.quote.qoute_class import Qoute
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import get_data



# 检查两个用户的的账户可用余额是否小于2000usdt
# 小于2000usdt则向该账户转入1000
def set_up_balance():
    wallet_balance = get_balance_list().response["result"][0]["walletBalance"]
    if float(wallet_balance) < 20000:
        transfer(20000000, "ADD", "USDT")
    wallet_balance = get_balance_list(test_user="test_user2").response\
        ["result"][0]["walletBalance"]
    if float(wallet_balance) < 20000:
        transfer(20000000, "ADD", "USDT",test_user="test_user2")


def set_up_position(symbol="dao_usdt"):
    # 判断做多仓位是否有仓位
    # 判断做空仓位是否有仓位
    order_request = OrderRequest()
    order_long = True
    order_short = True
    position_list = get_position(symbol).response["result"]
    if position_list is not None:
        for position in position_list:
            if position["positionSide"] == "LONG" and int(position["positionSize"]) >= 40:
                order_long = False
            if position["positionSide"] == "SHORT" and int(position["positionSize"]) >= 40:
                order_short = False
    # 获取指数价格
    index_price = round(float(qoute_symbol_index_price(symbol).response['result']["p"]),2)
    # 没有多仓位时用户1 下限价单，用户2下市场价格单吃
    if order_long:
        user1_parm = {'orderSide': 'BUY', 'orderType': 'LIMIT', 'origQty': '40',
                      'positionSide': 'LONG', 'symbol': symbol, 'price': index_price,
                      "timeInForce": "GTX"}
        user2_parm = {'orderSide': 'SELL', 'orderType': 'MARKET', 'origQty': '40',
                      'positionSide': 'SHORT', 'symbol': symbol, "timeInForce": "IOC"}
        res1 = order_request.create(parm=user1_parm, test_user="test_user")
        res2 = order_request.create(parm=user2_parm, test_user="test_user2")
    # 没有空仓时用户1下限价单，用户2下市价单吃单
    if order_short:
        user1_parm = {'orderSide': 'SELL', 'orderType': 'LIMIT', 'origQty': '40',
                      'positionSide': 'SHORT', 'symbol': symbol, 'price': index_price,
                      "timeInForce": "GTX"}
        user2_parm = {'orderSide': 'BUY', 'orderType': 'MARKET', 'origQty': '40',
                      'positionSide': 'LONG', 'symbol': symbol, "timeInForce": "IOC"}
        order_request.create(parm=user1_parm, test_user="test_user")
        order_request.create(parm=user2_parm, test_user="test_user2")
    return index_price


def set_down_position(symbol,num=None):
    ''' 取消掉user 的所有持仓
         1, 不传 num 默认取消所有的持仓
         2, 传num 取消 num 个持仓
      '''
    # 查看 test_user 的持仓
    position_list_test_user = get_position(symbol,test_user="test_user").response["result"]
    # test_user2 持仓
    position_list_test_user2 = get_position(symbol,test_user="test_user2").response["result"]
    logger.info("平仓前，user 的持仓情况为{}".format(position_list_test_user))
    logger.info("平仓后 user2 的持仓情况为{}".format(position_list_test_user2))
    # user 取消当前交易对的所有委托
    order_entrust_cancel_all(symbol)
    # user2 取消当前交易对的所有委托
    order_entrust_cancel_all(symbol,test_user='test_user2')
    # 当前指数价格为
    index_price = qoute_symbol_index_price(symbol).response['result']["p"]
    for item_user in position_list_test_user:
        # user 做空的情况
        if item_user.get('positionSide') == 'SHORT' and item_user.get('entryPrice') != '0':
            for item_user2 in position_list_test_user2:
                # user2 做空
                if item_user2.get('positionSide') != 'SHORT':
                    parms_user2 = {
                        'orderSide': "SELL",
                        'orderType': 'LIMIT',
                        'origQty': num if num else item_user.get('positionSize'),
                        'positionSide': "SHORT",
                        'symbol': symbol,
                        'price': index_price,
                        "timeInForce": "GTX"
                    }
                    logger.info('user2 创建限价单  {}'.format(parms_user2))
                    res1 = OrderRequest().create(parm=parms_user2, test_user="test_user2")
                    logger.info("user2 创建限价单成功,创建响应  {}".format(res1))
                    # user 做多
                    parms_user = {
                        'orderSide': "BUY",
                        'orderType': 'MARKET',
                        'origQty': num if num else item_user.get('positionSize'),
                        'positionSide': "SHORT",
                        'symbol': symbol,
                        'price': index_price,
                        "timeInForce": "IOC"
                    }

                    logger.info('user 进行平仓,平仓请求是  {}'.format(parms_user))
                    res1 = OrderRequest().create(parm=parms_user,test_user="test_user")
                    logger.info("user 平仓完成,请求响应 {}".format(res1))
        # user 做多
        if item_user.get('positionSide') != 'SHORT' and item_user.get('entryPrice') != '0':
            for item_user2 in position_list_test_user2:
                if item_user2.get('positionSide') == 'SHORT':
                    parms_user2 = {
                        'orderSide': "BUY",
                        'orderType': 'LIMIT',
                        'origQty': num if num else item_user.get('positionSize'),
                        'positionSide': "SHORT",
                        'symbol': symbol,
                        'price': index_price,
                        "timeInForce": "GTC"
                    }
                    logger.info('user2 创建限价单 {}'.format(parms_user2))
                    res1 = OrderRequest().create(parm=parms_user2, test_user="test_user2")
                    time.sleep(5)
                    logger.info("user2 创建限价单成功,创建响应 is {}".format(res1))
                    parms_user = {
                        'orderSide': "SELL",
                        'orderType': 'MARKET',
                        'origQty': num if num else item_user.get('positionSize'),
                        'positionSide': "LONG",
                        'symbol': symbol,
                        'price': index_price,
                        "timeInForce": "IOC"
                    }

                    logger.info('user 进行平仓,平仓请求是 is {}'.format(parms_user))
                    res1 = OrderRequest().create(parm=parms_user, test_user="test_user")
                    logger.info("user 平仓完成,请求响应 {}".format(res1))

    # 查看 test_user 的持仓
    position_list_test_user = get_position(symbol, test_user="test_user").response["result"]
    logger.info("平仓后，user 的持仓情况为{}".format(position_list_test_user))
    # test_user2 持仓
    position_list_test_user2 = get_position(symbol, test_user="test_user2").response["result"]
    logger.info("平仓后， user2 的持仓情况为{}".format(position_list_test_user2))

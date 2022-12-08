#!/usr/bin/python
# -*- encoding: utf-8 -*-

from api.http_api import ResultBase
from common.read_data import get_data
from common.insert_order import insert_order
from operation.contract.client.position import get_position
from common.mysql_operate import MysqlDb

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
def match(mode,data1,data2,orderSide,orderType,origQty,positionSide,symbol,marketOrderLevel,price,reduceOnly,timeInForce,
          triggerProfitPrice,triggerStopPrice,init_Side,init_positonSide,init_Qty):
    '''撮合，校验内容包括订单、钱包和接口状态'''
    result = ResultBase()
    result.accont_init = get_position(symbol).response
    res = insert_order.order(mode,data1,data2,orderSide,orderType,origQty,positionSide,symbol,marketOrderLevel,price,
                     reduceOnly,timeInForce,triggerProfitPrice,triggerStopPrice,init_Side,init_positonSide,init_Qty)
    result.accont_end = get_position(symbol).response
    sql = ''''''
    result.order = MysqlDb().select_db(sql)
    return result

if __name__ == '__main__':
    match()
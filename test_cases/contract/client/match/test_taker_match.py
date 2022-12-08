# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# '''
# @File    :   test_taker_match.py
# @Contact :   shuai.xu
#
# @Modify Time      @Author    @Version    @Desciption
# ------------      -------    --------    -----------
# 2022/1/20 4:29 下午   shuai.xu      1.0         None
# '''
# #!/usr/bin/python
# # -*- encoding: utf-8 -*-
# from pprint import pprint
#
# from common.get_signature import generate_auth_info_for_test
# from common.mongodb_operate import MongoDb
# from common.websockets import get_sub_mark_price
# from config.contract_enum import orderSides, positionSides
# from operation.contract.client.order.order_request import OrderRequest
# from test_cases.contract.client.conftest import *
# from common.logger import logger
# from tools.contract.empty_entrust_queue import empty_entrust_queue
# from model.symbol import symbol as s
#
#
# class Test_taker_match():
#     '''
#       taker撮合:
#
#     '''
#     @pytest.mark.single
#     @pytest.mark.parametrize("scene,mode,orderSide,orderType,origQty,positionSide,\
#                          symbol,marketOrderLevel,price,reduceOnly,timeInForce,triggerProfitPrice,\
#                             triggerStopPrice,init_Side,init_Qty,init_positonSide,init_qty,init_price,\
#                               except_result,except_code,except_msg",
#                              api_taker_match["taker_match"])
#     def test_taker_match(self,scene,mode,orderSide,orderType,origQty,positionSide,\
#                          symbol,marketOrderLevel,price,reduceOnly,timeInForce,triggerProfitPrice,\
#                             triggerStopPrice,init_Side,init_Qty,init_positonSide,init_qty,init_price,\
#                               except_result,except_code,except_msg):
#         logger.info(f'场景【{scene}】信息：{mode}-{orderSide}-{orderType}-{mode}-{orderSide}-{orderType}\
#                         -{origQty}-{positionSide}-{symbol}-{marketOrderLevel}-{price}-{reduceOnly}-{timeInForce}\
#                         -{triggerProfitPrice}-{orderType}-{triggerStopPrice}-{init_Side}-{init_Qty}-\
#                            {init_positonSide}-{init_qty}-{init_price}-{except_result}-{except_code}-{except_msg}')
#         user_header = generate_auth_info_for_test()
#         # user2_header = generate_auth_info_for_test("test_user2")
#         # if scene.endswith('买多开仓，taker模式，队列没有卖单') or scene.endswith('买多开仓，taker模式，委托价格小于卖一价格'):
#         #     if scene.endswith('买多开仓，taker模式，队列没有卖单'):
#         #         # 清空队列
#         #         empty_entrust_queue(symbol)
#         #     # 价格按照标记价格下单
#         #     price = float(get_sub_mark_price("bnb_usdt").get("data").get("p"))
#         #     logger.info("当前按照标记价格下单,当前标记价格为{}".format(price))
#         #     # 下单价格比标记价格小1
#         #     if scene.endswith('买多开仓，taker模式，委托价格小于卖一价格'):
#         #         price -=1
#         #     parm = {
#         #         'orderSide': orderSide,
#         #         'orderType': orderType,
#         #         'origQty': origQty,
#         #         'positionSide': positionSide,
#         #         'symbol': symbol,
#         #         'timeInForce':timeInForce,
#         #         'price':price
#         #     }
#         #     logger.info("下单参数为{}".format(parm))
#         #     import time
#         #     millisecond = int(round((time.time()) * 1000))
#         #     res = OrderRequest().create(parm=parm, header=user_header)
#         #     logger.info("创建了订单 {}".format(res))
#         #     args = {
#         #         "col": "order",
#         #     }
#         #     time.sleep(3)
#         #     # 查询最新下单
#         #     symbol_id = s.query.filter(s.symbol == symbol).first().id
#         #     if MongoDb(args).find_one({'symbolId': symbol_id,'state': 1,}) is not None:
#         #         res = MongoDb(args).descending_sort_find({
#         #                 'symbolId': symbol_id,
#         #                 'state': 1,
#         #             }, 'createdTime',1)
#         #         logger.info("最新下单信息为{}".format(res))
#         #         # 对比下单参数
#         #         # assert res[0].get("createdTime") > millisecond
#         #         assert res[0].get("origQty") == str(origQty)
#         #         assert res[0].get("symbolId") == symbol_id
#         #         assert res[0].get("orderSide") == orderSides.get(orderSide)
#         #         assert res[0].get("positionSide") == positionSides.get(positionSide)
#         #         assert res[0].get("price") == str(price)
#
#         # if scene.endswith('买多开仓，taker模式，委托价格等于卖一价格，委托数量等于卖一数量)' or scene.endswith(\
#         #         "买多开仓，taker模式，委托价格等于卖一价格，委托数量大于卖一数量"):
#         #     price = float(get_sub_mark_price("bnb_usdt").get("data").get("p"))
#         #     # user2 出限价单
#         #     parms_user2 = {
#         #         'orderSide': "SELL",
#         #         'orderType': 'LIMIT',
#         #         'origQty': origQty,
#         #         'positionSide': "SHORT",
#         #         'symbol': symbol,
#         #         'price': price,
#         #         "timeInForce": "GTX"
#         #     }
#         #     logger.info("user2 出限价单，传参为:{}".format(parms_user2))
#         #
#         #     res = OrderRequest().create(parm=parms_user2, header=user2_header)
#         #     logger.info("user2 出限价单,创建了订单 {}".format(res))
#         #
#         #     symbol_id = s.query.filter(s.symbol == symbol).first().id
#         #     args = {
#         #         "col": "order",
#         #     }
#         #     res = MongoDb(args).descending_sort_find({
#         #         'symbolId': symbol_id,
#         #         'state': 1,
#         #     }, 'createdTime', 1).next()
#         #     assert res.get("origQty") == str(origQty)
#         #     # user 吃单:
#         #     parms_user = {
#         #         'orderSide': orderSide,
#         #         'orderType': orderType,
#         #         'origQty': origQty,
#         #         'positionSide': positionSide,
#         #         'symbol': symbol,
#         #         'price': price,
#         #         "timeInForce": timeInForce
#         #     }
#         #     logger.info("user 出市价单，传参为:{}".format(parms_user))
#         #     # res = OrderRequest().create(parm=parms_user, header=user_header)
#         #     # logger.info("user 出市价单,创建了订单 {}".format(res))
#         #
#         #
#         #
#         #     # user 吃单
#         #
#         #
#         #
#         #     pass
#
#
#
#
#
#
# if __name__ == '__main__':
#     pytest.main(["-q", "-s", "Test_taker_match.py"])

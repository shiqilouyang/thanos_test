#!/usr/bin/python
# -*- encoding: utf-8 -*-
from model.symbol import symbol as s
from common.mongodb_operate import MongoDb
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.order_entrust.order_entrust_cancel_all import order_entrust_cancel_all
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_order_entrust_cancel_all():
    '''
      撤销所有委托:
         1, 获取当前用户 acoountId, 根据 symbol 获取 symbolId
         2, 根据 acoountId,symbolId,state 查询订单Id
         3, 撤销当前交易对所以委托
         4, 根据订单Id再次查询mongo, 状态不在为 1(NEW)订单
    '''
    @pytest.mark.single
    @pytest.mark.parametrize(" scene,symbol,code,except_msg",
                             api_order_entrust_cancel_all["order_entrust_cancel_all"])
    def test_order_entrust_cancel_all(self,scene,symbol,code,except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{symbol}-{code}-"{except_msg}"')

        if scene.endswith("该交易对有委托"):
            # 获取当前用户 accoundId
            account_id = get_account_info().response.get("result").get("accountId")
            # 获取当前symbol 的symbolId
            symbol_id = s.query.filter(s.symbol == symbol).first().id
            logger.info("当前用户的accountId 是{}".format(account_id))
            args = {
                "col": "order",
            }
            # 查询 NEW 类型的订单
            order_res = MongoDb(args).find({"accountId": account_id,"state":1,'symbolId':symbol_id})
            logger.info("mongo查询参数:{}".format({"accountId": account_id,"state":1,'symbolId':symbol_id}))
            for order_items in order_res:
                # 订单ID
                new_order_id = order_items.get("_id")
                # 订单类型
                orderType = "ORDER" if order_items.get("orderType") == 1 else "ENTRUST"
                # 对NEW 订单进行取消操作
                result = order_entrust_cancel_all(symbol)
                logger.warning('场景-[{}]的请求order_id是[{}],请求orderType是：{}'.\
                               format(scene,new_order_id,orderType))
                logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
                order_res = MongoDb(args).find_one({"_id": new_order_id})
                assert order_res.get('state') != 1
                assert result.status_code == 200
                assert code == result.response["returnCode"]
                return

        result = order_entrust_cancel_all(symbol)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        assert result.status_code == 200
        assert code == result.response["returnCode"]
        if code == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "Test_order_entrust_cancel_all.py"])

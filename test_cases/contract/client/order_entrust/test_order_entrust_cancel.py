#!/usr/bin/python
# -*- encoding: utf-8 -*-
from common.mongodb_operate import MongoDb
from common.set_up_balance_and_position import set_up_position
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.order_entrust.order_entrust_cancel import order_entrust_cancel
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_order_entrust_cancel():
    '''
      撤销委托:
         1, 查询当前账户存在的 New类型订单，得到 订单ID,订单类型
         2, 对此订单进行撤销操作，撤销成功，订单类型不再是1
    '''
    @pytest.mark.single
    @pytest.mark.parametrize("scene,id,type,code,except_msg",
                             api_order_entrust_cancel["order_entrust_cancel"])
    def test_order_entrust_cancel(self,scene,id,type,code,except_msg):

        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{id}-{type}-{code}-"{except_msg}"')

        if scene.endswith("订单ID与订单类型匹配") or scene.endswith('订单ID与订单类型不匹配'):
            # 获取当前用户 accoundId
            accountId = get_account_info().response.get("result").get("accountId")
            logger.info("当前用户的accountId 是{}".format(accountId))
            args = {
                "col": "order",
            }
            order_res = MongoDb(args).find_one({"accountId": accountId,"state":1})
            # 当前没有 订单
            if order_res is None:
                # 下单
                set_up_position()
            else:
                # 订单ID
                new_order_id = order_res.get("_id")
                # 订单类型
                orderType = "ORDER" if order_res.get("orderType") == 1 else "ENTRUST"
                # 对NEW 订单进行取消操作
                if scene.endswith('订单ID与订单类型不匹配'):
                    result = order_entrust_cancel(new_order_id , "ORDER" if order_res.get("orderType") != 1 else "ENTRUST" )
                    assert result.status_code == 200
                    assert code == result.response["returnCode"]
                    return
                else:
                    result = order_entrust_cancel(new_order_id,orderType)
                logger.warning('场景-[{}]的请求order_id是[{}],请求orderType是：{}'.\
                               format(scene,new_order_id,orderType))
                logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
                import time
                time.sleep(3)
                order_res = MongoDb(args).find_one({"_id": new_order_id})
                logger.info("该订单在数据库存储为{}".format(order_res))
                assert order_res.get('state') == 4
                assert result.status_code == 200
                assert code == result.response["returnCode"]
            return

        # 非数据库字段部分判断
        result = order_entrust_cancel(id,type)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        assert result.status_code == 200
        assert code == result.response["returnCode"]
        # 其他字段校验
        if code == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "Test_order_entrust_cancel.py"])

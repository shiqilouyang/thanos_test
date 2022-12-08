#!/usr/bin/python
# -*- encoding: utf-8 -*-
from common.mongodb_operate import MongoDb
from common.set_up_balance_and_position import set_down_position
from operation.contract.client.account import get_account_info
from operation.contract.client.order.order_request import OrderRequest
from operation.contract.client.order_entrust.order_entrust_cancel import order_entrust_cancel
from operation.contract.client.position.adjust_leverage import adjust_leverage
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import *
from common.logger import logger
from model.symbol import symbol as s
from tools.contract.adjust_leverage import get_position_max_adjust_leverage

class Test_adjust_leverage:
    '''
      调整杠杆倍数:
         1, 更改状态之后，数据库对比对应状态
         2，获取用户当前可以开最大杠杆倍数与管理端进行对比
=    '''
    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,leverage,positionSide,symbol,except_result, except_returnCode, except_msg",
                             api_position_data["adjust_leverage"])
    def test_adjust_leverage(self,scene,leverage,positionSide,symbol,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{leverage}-{positionSide}-{symbol}-{except_result}-{except_returnCode}-"{except_msg}"')
        # 调用获取用户信息的接口，得到accountId
        account_info = get_account_info.get_account_info()
        curl_accountId = account_info.response.get("result").get("accountId")

        if scene.endswith('调整杠杆倍数,仓位方向为LONG'):
            set_down_position(symbol)
        if scene.endswith( '杠杆倍数等于设定值上限') or scene.endswith('杠杆倍数大于设定值上限'):
            # 获取用户当前可以开最大杠杆倍数
            position_leverage = get_position_max_adjust_leverage(symbol)
            logger.info("用户当前可以开最大杠杆倍数 为{}".format(position_leverage))
            position_max_adjust_leverage = position_leverage.get(positionSide).get('position_max_adjust_leverage')
            if scene.endswith( '杠杆倍数大于设定值上限'):
                set_down_position(symbol)
                # 将上限值加1
                position_max_adjust_leverage = int(position_max_adjust_leverage)+ 1
            result = adjust_leverage(position_max_adjust_leverage, positionSide, symbol)
            assert result.status_code == 200
            assert except_result == result.response["msgInfo"]
            assert except_returnCode == result.response["returnCode"]
            if except_returnCode == 0:
                assert except_msg in str(result.response["result"])
            else:
                assert except_msg in result.response["error"]["msg"]
            return

        result = adjust_leverage(leverage, positionSide, symbol)
        import time
        time.sleep(2)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        args = {
            "col": "position",
        }
        logger.info("当前用户 accountId 是{}".format(curl_accountId))
        if scene.endswith('调整杠杆倍数,仓位方向为LONG') or scene.endswith('调整杠杆倍数,仓位方向为SHORT') \
                or scene.endswith('交易对大写显示') or scene.endswith('杠杆倍数等于设定值上限'):
            symbolId = s.query.filter(s.symbol == symbol).first().id
            #   根据 accountId,coin 在mongo查询杠杆信息
            if positionSide == "LONG":
                res = MongoDb(args).find_one({"accountId": curl_accountId,"positionSide":1,'symbolId':symbolId})
                logger.info("mongo 查询条件".format({"accountId": curl_accountId,"positionSide":1,'symbolId':symbolId}))
                logger.info("mongo 查询结果为{}".format(res))
                assert leverage == res.get("leverage")
            elif positionSide == "SHORT":
                res = MongoDb(args).find_one({"accountId": curl_accountId,"positionSide":2,'symbolId':symbolId})
                logger.info("mongo 查询条件".format({"accountId": curl_accountId,"positionSide":2,'symbolId':symbolId}))
                logger.info("mongo 查询结果为{}".format(res))
                assert leverage == res.get("leverage")
            else:
                logger.error("当前leverage 状态为{}".format(positionSide))

        if scene.endswith('存在活跃订单不能更改杠杆倍数'):
            # 获取最新的指数价格
            index_price = round(float(qoute_symbol_index_price(symbol).response['result']["p"]),2)
            # 发起限价委托
            parms_user2 = {
                'orderSide': "BUY",
                'orderType': 'LIMIT',
                'origQty': 10,
                'positionSide': positionSide,
                'symbol': symbol,
                'price': index_price,
                "timeInForce": "GTX"
            }
            logger.info('user2 创建限价单  {}'.format(parms_user2))
            res1 = OrderRequest().create(parm=parms_user2)
            logger.info("user2 创建限价单成功,创建响应  {}".format(res1))
            result = adjust_leverage(leverage, positionSide, symbol)
        #   对创建的限价单委托取消
            order_entrust_cancel(res1.get('result'), 'ORDER')
        logger.info("调整杠杆倍数接口响应为{}".format(result))
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_adjust_leverage.py"])

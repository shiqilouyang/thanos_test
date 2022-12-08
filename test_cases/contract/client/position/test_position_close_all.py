#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_position_close_all.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/19 10:10 上午   shuai.xu      1.0         None
'''
#!/usr/bin/python
# -*- encoding: utf-8 -*-
from common.set_up_balance_and_position import set_up_position
from model.symbol import symbol as s
from common.mongodb_operate import MongoDb
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.order_entrust.order_entrust_list import order_entrust_list
from operation.contract.client.position.get_position import get_position
from operation.contract.client.position.position_close_all import position_close_all
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_position_close_all:
    '''
       一键平仓:
          1，调用接口获取用户 accountId,symbolId
          2, mongo 得到用户的持仓信息
          3, position_close_all 一键平仓
          4, 查看全部委托接口找到当前 平仓订单
    '''
    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,symbol,except_result, except_returnCode, except_msg",
                             api_position_close_all["position_close_all"])
    def test_position_close_all(self,scene,symbol,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{symbol}-{except_result}-{except_returnCode}-"{except_msg}"')

        # 调用获取用户信息的接口，得到accountId
        account_id = get_account_info().response.get("result").get("accountId")
        logger.info("当前用户 accountId 是{}".format(account_id))

        args = {
            "col": "position",
        }
        if scene == '该交易对有仓位':
            # 初始化仓位信息
            set_up_position()
            # 数据库获取该交易对信息
            symbol_id = s.query.filter(s.symbol == '{}'.format(symbol)).first().id
            #根据 accountId,symbol_id 在mongo找到position(持仓)信息
            res_all = MongoDb(args).find({"accountId": account_id, 'symbolId': symbol_id})
            if res_all is not None:
                for res in res_all:
                    if res.get('entryPrice') !='0':
                        # 获取毫秒级别的时间戳
                        millisecond = int(round((time.time()) * 1000))
                        time.sleep(1)
                        result = position_close_all(symbol)
                        # 找到平仓订单
                        order_list = order_entrust_list("", "", "", "", "", millisecond, "", "", "").response
                        for item in order_list.get("result").get("items"):
                            # 平仓订单时间均大于等于当前时间
                            assert item.get('createdTime') > millisecond
                            # 平仓订单 状态为 CANCELED(已撤销)
                            assert item.get('state') == 'CANCELED'
                        assert result.status_code == 200
                        assert except_result == result.response["msgInfo"]
                        assert except_returnCode == result.response["returnCode"]
                        if except_returnCode == 0:
                            assert except_msg in str(result.response["result"])
                        else:
                            assert except_msg in result.response["error"]["msg"]
                        return
        result = get_position(symbol)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "Test_position_close_all.py"])

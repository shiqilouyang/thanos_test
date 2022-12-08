#!/usr/bin/python
# -*- encoding: utf-8 -*-

from model.symbol import symbol as s
from common.mongodb_operate import MongoDb
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.position.get_position import get_position
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_get_position:
    '''
       获取持仓信息:
           1，根据用户信息找到用户持仓信息,拿到持仓信息中的交易对
           2,该交易对作为接口传参
           3,mongo 查询到的数据与接口返回数据对比
    '''
    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,symbol,except_result, except_returnCode, except_msg",
                             api_position_data["get_position"])
    def test_get_position(self,scene,symbol,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{symbol}-{except_result}-{except_returnCode}-"{except_msg}"')

        # 调用获取用户信息的接口，得到accountId
        account_id = get_account_info().response.get("result").get("accountId")
        # 获取当前symbol 的symbolId
        logger.info("当前用户 accountId 是{}".format(account_id))

        args = {
            "col": "position",
        }
        #   根据 accountId 在mongo找到一条position(持仓)信息
        if scene.endswith("正常查询"):
            symbolId = s.query.filter(s.symbol == symbol).first().id
            res_all = MongoDb(args).find({"accountId": account_id,'symbolId': symbolId})
            if res_all is not None:
                for res in res_all:
                    if res.get("positionSide") == 2:
                        result = get_position(symbol)
                        symbol_position_message = result.response.get("result")
                        for i in symbol_position_message:
                            if i.get('positionSide') == 'SHORT':
                                assert str(float(i.get("positionSize"))) == str(float(str(res.get('positionSize'))))
                                assert i.get('closeOrderSize') == str(res.get('closeOrderSize'))
                                assert i.get('entryPrice') == str(res.get('entryPrice'))
                                assert i.get('leverage') == res.get('leverage')
                    if res.get("positionSide") == 1:
                        result = get_position(symbol)
                        symbol_position_message = result.response.get("result")
                        for i in symbol_position_message:
                            if i.get('positionSide') == 'LONG':
                                assert str(float(i.get("positionSize"))) == str(float(str(res.get('positionSize'))))
                                assert i.get('closeOrderSize') == str(res.get('closeOrderSize'))
                                assert i.get('entryPrice') == str(res.get('entryPrice'))
                                assert i.get('leverage') == res.get('leverage')
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
    pytest.main(["-q", "-s", "test_get_position.py"])

#!/usr/bin/python
# -*- encoding: utf-8 -*-
from common.mongodb_operate import MongoDb
from common.set_up_balance_and_position import set_up_position
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.position.adjust_auto_margin import adjust_auto_margin
from test_cases.contract.client.conftest import *
from common.logger import logger
from model.symbol import symbol as s



class Test_adjust_auto_margin:
    '''
       修改自动追加保证金:
           1，根据用户信息找到用户持仓信息,拿到持仓信息中positionSide，symbol
           2,positionSide，symbol ,autoMargin 对作为接口传参
           3,调用接口修改自动追加保证金
           4,判断是否按照预期进行修改
    '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,autoMargin,positionSide,symbol,except_result, except_returnCode, except_msg",
                             api_position_data["adjust_auto_margin"])
    def test_adjust_auto_margin(self,scene,autoMargin,positionSide,symbol,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{autoMargin}-{positionSide}-{symbol}-{except_result}-{except_returnCode}-"{except_msg}"')

        # 调用获取用户信息的接口，得到accountId
        account_id = get_account_info().response.get("result").get("accountId")
        # 获取当前symbol 的symbolId
        logger.info("当前用户 accountId 是{}".format(account_id))
        args = {
            "col": "position",
        }
        if scene.endswith("自动追加保证金正常，仓位方向LONG") or scene.endswith('自动追加保证金正常，仓位方向SHORT') or \
                scene.endswith("关闭自动追加保证金正常，仓位方向LONG") or scene.endswith('关闭自动追加保证金正常，仓位方向SHORT'):
            #   根据 accountId 在mongo找到一条position(持仓)信息
            res = MongoDb(args).find({"accountId": account_id})
            if scene.endswith('自动追加保证金正常，仓位方向LONG'):
                # 初始化交易对
                set_up_position(symbol="dao_usdt")
            for symbol_res in res:
                # entryPrice= 0 是垃圾数据
                if str(symbol_res.get('entryPrice')) != '0':
                    if symbol_res is not None:
                        logger.info("当前 {} 了自动追加保证金".format("开启" if symbol_res.get("autoMargin") else "关闭"))
                        if symbol_res.get('positionSide') == 2:
                            positionSide = 'SHORT'
                        if symbol_res.get('positionSide') == 1:
                            positionSide = 'LONG'
                        if symbol_res.get('positionSide') == 0:
                            positionSide = 'BOTH'
                        # 数据库获取当前持仓的交易对
                        symbol = s.query.filter(s.id == int(symbol_res.get("symbolId"))).first().symbol
                        logger.info("当前用户持仓信息中的交易对是:{} 持仓方向:{} autoMargin:{} ".format(symbol,positionSide,autoMargin))
                        # positionSide，symbol ,autoMargin 对作为接口传参
                        result = adjust_auto_margin(autoMargin, positionSide, symbol)
                        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
                        time.sleep(2)
                        chenge_autoMargin = MongoDb(args).find_one({"accountId": account_id,"_id":symbol_res.get("_id")})
                        logger.info("当前 {} 了自动追加保证金".format("开启" if chenge_autoMargin.get("autoMargin") else "关闭"))
                        # 判断是否按照预期进行修改
                        assert chenge_autoMargin.get('autoMargin') == autoMargin
                        return

        # 判断非数据库参数
        result = adjust_auto_margin(autoMargin, positionSide, symbol)
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
    pytest.main(["-q", "-s", "Test_adjust_auto_margin.py"])

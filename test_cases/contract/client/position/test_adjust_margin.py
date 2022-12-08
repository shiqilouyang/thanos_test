#!/usr/bin/python
# -*- encoding: utf-8 -*-
from common.mongodb_operate import MongoDb
from common.set_up_balance_and_position import set_up_position, set_up_balance
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.fund.get_balance_coin import get_balance_coin
from operation.contract.client.position.adjust_margin import adjust_margin
from operation.contract.client.position.get_position import get_position
from operation.contract.client.position.position_class import Positon
from test_cases.contract.client.conftest import *
from common.logger import logger
from model.symbol import symbol as s
from decimal import Decimal


from tools.contract.margin import margin_max_and_min


class Test_adjust_margin:
    '''
      修改保证金:
            1，获取当前用户的accountId,以及 指定交易的的持仓信息
            2, 遍历持仓信息，对所有的持仓进行 执行操作
            3, 修改保证金之后的与修改保证金之前的相等 保留三位有效小数之后进行对比
    '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,margin,positionSide,symbol,type,except_result, except_returnCode, except_msg",
                             api_position_data["adjust_margin"])
    def test_adjust_margin(self,scene,margin,positionSide,symbol,type,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{margin}-{positionSide}-{symbol}-{except_result}-{except_returnCode}-"{except_msg}"')
        # 调用获取用户信息的接口，得到accountId
        account_id = get_account_info().response.get("result").get("accountId")

        # 获取当前symbol 的symbolId
        logger.info("当前用户 accountId 是{}".format(account_id))
        args = {
            "col": "position",
        }
        if scene.endswith( "增加逐仓保证金，持仓方向LONG") or scene.endswith( '增加逐仓保证金，持仓方向SHORT') or \
                scene.endswith( "减少逐仓保证金，持仓方向LONG") or scene.endswith( '减少逐仓保证金，持仓方向SHORT')\
                    or scene.endswith( "增加数量等于账户余额") or scene.endswith( '减少后保证金等于初始保证金') :
            if scene.endswith('增加逐仓保证金，持仓方向LONG'):
                # 初始化 仓位配置
                set_up_position(symbol="dao_usdt")
                set_up_balance()
            # 根据 symbol 获取 symbolId
            symbol_id = s.query.filter(s.symbol == symbol).first().id
            #   根据 accountId 在mongo找到一条position(持仓)信息
            res = MongoDb(args).find({"accountId": account_id,'symbolId':symbol_id})
            position_list = get_position(symbol).response["result"]
            logger.info("当前仓位信息{}".format(position_list))
            for symbol_res in res:
                # entryPrice= 0 是垃圾数据
                if str(symbol_res.get('entryPrice')) != '0':
                    if symbol_res is not None:
                        if symbol_res.get('positionSide') == 2:
                            positionSide = 'SHORT'
                        if symbol_res.get('positionSide') == 1:
                            positionSide = 'LONG'
                        if symbol_res.get('positionSide') == 0:
                            positionSide = 'BOTH'
                        # 数据库获取当前持仓的交易对
                        symbol = s.query.filter(s.id == int(symbol_res.get("symbolId"))).first().symbol

                        logger.info("当前用户持仓信息中的交易对是:{} 持仓方向:{} 调整方向:{} 数量:{}".format(symbol,positionSide,type,margin))
                        logger.info("修改保证金之前的仓位保证金是: {}".format(symbol_res.get('isolatedMargin')))
                        if scene.endswith( "增加数量等于账户余额"):
                            res = get_balance_coin(coin='usdt').response
                            # 可增加最大保证金为
                            margin = float(str(round(float(str(res.get('result').get('availableBalance'))),4))[:-1])
                            logger.info("当前可增加最大保证金是 {}".format(margin))
                        if scene.endswith('减少后保证金等于初始保证金'):
                            margin_results = margin_max_and_min(account_id, symbol, 1)
                            logger.info("做多的仓位 保证金信息 {}".format(margin_results))
                            margin = float(str(round(float(Decimal(str(symbol_res.get('isolatedMargin')))) \
                                    - float(Decimal(str(margin_results.get("start_margin")))),3))[:-1])
                        result = adjust_margin(margin, positionSide, symbol, type)
                        # {'max_margin': '2215.77564746', 'min_margin': 2215.77564746 ,'start_margin' : '3.6844'  }
                        # 更改之后的数据查询
                        time.sleep(3)
                        symbolId = s.query.filter(s.symbol == symbol).first().id
                        re = MongoDb(args).find_one({"accountId": account_id, 'symbolId': symbolId,'positionSide':symbol_res.get('positionSide')})
                        logger.info("修改保证金之后的仓位保证金是: {}".format(re.get('isolatedMargin')))
                        if type == "ADD":
                            # 修改保证金之后的与之前的相等 当前对比 选择 保留三位有效小数之后进行对比
                            assert round(float(Decimal(str(re.get('isolatedMargin')))),3) ==\
                                   round(float(Decimal(margin)) +float(Decimal(str(symbol_res.get('isolatedMargin')))),3)
                        else:
                            # 修改保证金之后的与之前的相等 当前对比 选择 保留三位有效小数之后进行对比
                            assert round(float(Decimal(str(re.get('isolatedMargin')))), 3) == \
                                   round(float(Decimal(str(symbol_res.get('isolatedMargin')))) - float(Decimal(margin)) ,
                                         3)
                        assert result.status_code == 200
                        assert except_result == result.response["msgInfo"]
                        assert except_returnCode == result.response["returnCode"]
                        if except_returnCode == 0:
                            assert except_msg in str(result.response["result"])
                        else:
                            assert except_msg in result.response["error"]["msg"]
                        return

        result = adjust_margin(margin,positionSide,symbol,type)
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
    pytest.main(["-q", "-s", "test_adjust_margin.py"])

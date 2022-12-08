#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random
from model.symbol import symbol as s
from operation.contract.client.symbol_info.get_symbol_list_info import get_symbol_list_info
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_get_symbol_list_info:
    '''
       获取所有交易对配置信息:
        1,对返回结果随机选择一个
        2,根据选择的 symbol交易对mysql中获取数据信息
        3,比对信息
    '''
    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,except_result, except_returnCode, except_msg",api_symbol_data["symbol_list_info"])
    def test_get_symbol_list_info(self, scene,except_result, except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'信息分别是：{except_result}-{except_returnCode}-{except_msg}')
        result = get_symbol_list_info()
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        # 对返回结果随机选择一个
        choice_one = random.choice(result.response.get("result"))
        # 根据选择的 symbol交易对mysql中获取数据信息
        symbol_res = s.query.filter(s.symbol == choice_one.get("symbol")).first()

        # 接口返回信息与mysql数据对比
        assert choice_one.get("contractType") == \
               symbol_res.get_contract_type(symbol_res.contract_type)
        assert choice_one.get("underlyingType") == \
               symbol_res.get_underlying_type(symbol_res.underlying_type)
        assert str(float(choice_one.get("contractSize"))) == str(float(symbol_res.contract_size))
        assert choice_one.get("tradeSwitch") == symbol_res.trade_switch
        assert choice_one.get("state") == symbol_res.state
        assert choice_one.get("baseCoin") == symbol_res.base_coin
        assert choice_one.get("quoteCoin") == symbol_res.quote_coin
        assert choice_one.get("baseCoinPrecision") == symbol_res.base_coin_precision
        assert choice_one.get("quoteCoinPrecision") == symbol_res.quote_coin_precision
        # assert choice_one.get("supportOrderType") == \
        #        symbol_res.get_support_order_type(symbol_res.support_order_type)
        assert choice_one.get("quoteCoin") == symbol_res.quote_coin
        assert choice_one.get("supportTimeInForce") == \
               symbol_res.get_support_time_in_force(symbol_res.support_time_in_force)
        assert choice_one.get("supportEntrustType") == \
               symbol_res.get_support_entrust_type(symbol_res.support_entrust_type)
        assert float(choice_one.get("minQty")) == float(symbol_res.min_qty)
        assert float(choice_one.get("multiplierDown")) == float(symbol_res.multiplier_down)
        assert float(choice_one.get("multiplierUp")) == float(symbol_res.multiplier_up)
        assert choice_one.get("maxOpenOrders") == symbol_res.max_open_orders
        assert choice_one.get("maxEntrusts") == symbol_res.max_entrusts
        assert float(choice_one.get("makerFee")) == float(symbol_res.maker_fee)
        assert float(choice_one.get("takerFee")) == float(symbol_res.taker_fee)
        assert choice_one.get("depthPrecisionMerge") == symbol_res.depth_precision_merge

        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode != 0:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_symbol_list_info.py"])

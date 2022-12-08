#!/usr/bin/python
# -*- encoding: utf-8 -*-
from operation.contract.client.symbol_info.get_symbol_info import get_symbol_info
from test_cases.contract.client.conftest import *
from common.logger import logger
from model.symbol import symbol as s

class Test_get_symbol_info:
    '''
       获取单个交易对的配置信息：
          1, mysql symbol 表根据交易对获取数据信息
          2, 校验接口数据与 mysql 数据
    '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,symbol,except_result,except_code,except_msg",api_symbol_data["symbol_info"])
    def test_get_symbol_info(self, scene, symbol,except_result, except_code, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'信息分别是：{symbol}-{except_result}-{except_code}-{except_msg}')
        result = get_symbol_info(symbol)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')

        if symbol != "":
            symbol_res = s.query.filter(s.symbol == symbol).first()
            if symbol_res is not None:
                assert result.response.get("result").get("contractType") == \
                       symbol_res.get_contract_type(symbol_res.contract_type)
                assert result.response.get("result").get("underlyingType") == \
                       symbol_res.get_underlying_type(symbol_res.underlying_type)
                assert result.response.get("result").get("contractSize") == str(int(symbol_res.contract_size))
                assert result.response.get("result").get("tradeSwitch") == symbol_res.trade_switch
                assert result.response.get("result").get("state") == symbol_res.state
                assert result.response.get("result").get("baseCoin") == symbol_res.base_coin
                assert result.response.get("result").get("quoteCoin") == symbol_res.quote_coin
                assert result.response.get("result").get("baseCoinPrecision") == symbol_res.base_coin_precision
                assert result.response.get("result").get("quoteCoinPrecision") == symbol_res.quote_coin_precision
                assert result.response.get("result").get("supportOrderType") == \
                       symbol_res.get_support_order_type(symbol_res.support_order_type)
                assert result.response.get("result").get("quoteCoin") == symbol_res.quote_coin
                assert result.response.get("result").get("supportTimeInForce") == \
                       symbol_res.get_support_time_in_force(symbol_res.support_time_in_force)
                assert result.response.get("result").get("supportEntrustType") == \
                       symbol_res.get_support_entrust_type(symbol_res.support_entrust_type)
                assert float(result.response.get("result").get("minQty")) == float(symbol_res.min_qty)
                assert float(result.response.get("result").get("multiplierDown")) == float(symbol_res.multiplier_down)
                assert float(result.response.get("result").get("multiplierUp")) == float(symbol_res.multiplier_up)
                assert result.response.get("result").get("maxOpenOrders") == symbol_res.max_open_orders
                assert result.response.get("result").get("maxEntrusts") == symbol_res.max_entrusts
                assert float(result.response.get("result").get("makerFee")) == float(symbol_res.maker_fee)
                assert float(result.response.get("result").get("takerFee")) == float(symbol_res.taker_fee)
                assert result.response.get("result").get("depthPrecisionMerge") == symbol_res.depth_precision_merge

        # 非数据库信息对比
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_code == result.response["returnCode"]
        if except_code != 0:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_symbol_info.py"])

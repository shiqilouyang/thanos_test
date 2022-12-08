#!/usr/bin/python
# -*- encoding: utf-8 -*-
import operator

from model.exchange_coin import exchange_coin
from operation.contract.client.symbol_info.get_symbol_fund_rate import get_symbol_coins
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_get_symbol_coins:
    '''
        获取交易对币种：
           1，数据库查询所有的 交易对币种
           2, 与接口返回交易对币种进行对比
    '''
    @pytest.mark.parametrize("scene,except_result, except_returnCode, except_msg",api_symbol_data["test_get_symbol_coins"])
    def test_get_symbol_coins(self, scene,except_result, except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'信息分别是：-{except_result}-{except_returnCode}-{except_msg}')
        result = get_symbol_coins()
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        symbol_coins_list = []
        # 数据库查询所有的 交易对币种
        exchange_coin_all = exchange_coin.query.all()
        for coin in exchange_coin_all:
            symbol_coins_list.append(coin.coin)
        # 与接口返回交易对币种进行对比
        for i in result.response.get("result"):
            assert i in symbol_coins_list
        # 对比数据库之外的字段
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode != 0:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_symbol_coins.py"])

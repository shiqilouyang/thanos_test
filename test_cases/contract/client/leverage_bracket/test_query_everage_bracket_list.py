#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random

from model.leverage_bracket import leverage_bracket
from model.symbol import symbol as s
from operation.contract.client.leverage_bracket.query_leverage_bracket_list import query_leverage_bracket_list
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_query_leverage_bracket_list:
    ''' 查询所有交易对杠杆分层
        1,从接口返回结果随机选择一个交易对与数据库进行对比
        2,根据交易对，数据库查找对应交易分层信息
        3,对比分层信息
     '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,except_result, except_returnCode, except_msg",
                             api_leverage_data["query_leverage_bracket_list"])
    def test_query_leverage_bracket_list(self,scene,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{except_result}-{except_returnCode}-"{except_msg}"')
        result = query_leverage_bracket_list()
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        try:
            # 从返回结果随机选择一个交易对
            leverage_result = random.choice(result.response["result"])
            symbol = leverage_result.get("symbol")
            # 数据库获取该交易对信息
            symbol_single = s.query.filter(s.symbol == '{}'.format(symbol)).first()
            # 根据 根据交易对 symbol_id 获取分层详细信息
            symbol_list = leverage_bracket.query.filter(leverage_bracket.symbol_id == symbol_single.id).all()
            if symbol_list is not None:
                for symbol_ in symbol_list:
                    for res in leverage_result.get('leverageBrackets'):
                        if symbol_.bracket == res['bracket']:
                            assert float(symbol_.max_nominal_value) == \
                                   float(res['maxNominalValue'])
                            assert float(symbol_.max_nominal_value) == \
                                   float(res['maxNominalValue'])
                            assert float(symbol_.maint_margin_rate) == \
                                   float(res['maintMarginRate'])
                            assert float(symbol_.start_margin_rate) == \
                                   float(res['startMarginRate'])
                            assert float(symbol_.max_leverage) == \
                                   float(res['maxLeverage'])
                            assert float(symbol_.min_leverage) == \
                                   float(res['minLeverage'])
            else:
                # 该交易对不在数据库之中
                assert leverage_result is not None
                logger.error("查询所有交易对杠杆分层接口返回了数据库不存在的交易对")
        except Exception as e:
            logger.error(e)
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_query_leverage_bracket_list.py"])

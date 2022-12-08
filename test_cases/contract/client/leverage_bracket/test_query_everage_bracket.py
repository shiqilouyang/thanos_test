#!/usr/bin/python
# -*- encoding: utf-8 -*-
from model.leverage_bracket import leverage_bracket
from model.symbol import symbol as s
from operation.contract.client.leverage_bracket.query_leverage_bracket import query_leverage_bracket
from test_cases.contract.client.conftest import *
from common.logger import logger

class Test_query_leverage_bracket:

    ''' 查询单个交易对杠杆分层
        1,传参交易对获取杠杆分层与数据库进行对比
        2,数据库查找对应交易分层信息
        3,对比分层信息
     '''
    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,symbol,except_result, except_returnCode, except_msg",
                             api_leverage_data["query_leverage_bracket"])
    def test_query_leverage_bracket(self,scene,symbol,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{symbol}-{except_result}-{except_returnCode}-"{except_msg}"')
        result = query_leverage_bracket(symbol)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        assert result.status_code == 200
        try:
            # 数据库获取该交易对信息
            symbol_single = s.query.filter(s.symbol == '{}'.format(symbol)).first()
            # 根据 symbol_id 获取 分层详细信息
            symbol_list = leverage_bracket.query.filter(leverage_bracket.symbol_id == symbol_single.id).all()
            if symbol_list is not None:
                for symbol_ in symbol_list:
                    for res in result.response["result"].get('leverageBrackets'):
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
                assert result.response["result"].get("leverageBrackets") is not None
                logger.warning("交易对杠杆分层接口返回了数据库不存在的交易对")
        except Exception as e:
            logger.error(e)
        #  接口其他字段的判断
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_query_leverage_bracket.py"])

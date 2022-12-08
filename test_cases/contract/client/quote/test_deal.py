"""
encode:utf-8
Author:aidan.hu
Data:2022/1/7
"""
import pytest
from common.redis_operate import redis_cli
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data
from common.logger import logger


class TestDeal:
    """行情类接口的所有用例"""
    quote_request = Qoute()
    test_data = get_data("quote_test_deal_data.yml")

    # 获取交易对的最新成交信息正向测试用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_deal_success") == {} else [test_data])
    def test_deal_success(self,test_data):
        cases_data = test_data["test_deal_success"]
        for value in cases_data.values():
            name, parameter = value["name"], value["parameter"]
            expected_result = value["expect_result"]
            res = self.quote_request.deal(param=parameter)
            logger.info(f'获取最新成交价格接口返回：{name}的返回结果---》{res}')
            # redis_res = redis_cli.get_symbol_deal(parameter.get("symbol"), 0, parameter.get("num"))
            # logger.info("redis 获取结果为{}".format(redis_res))
            assert res["msgInfo"] == expected_result["msgInfo"]
            if parameter.get("msg"):
                assert res["error"]["msg"] == expected_result["msg"]

    #
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_deal_failed") == {} else [test_data])
    def test_by_symbol(self,test_data):
        cases_data = test_data["test_deal_failed"]
        for value in cases_data.values():
            name, parameter = value["name"], value["parameter"]
            expected_result = value["expect_result"]
            # 1、获取请求的返回数据
            res = self.quote_request.deal(param=parameter)
            logger.info(f'获取最新成交价格接口返回：{name}的返回结果---》{res}')
            assert res["msgInfo"] == expected_result["msgInfo"]
            if parameter.get("msg"):
                assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_deal.py'])

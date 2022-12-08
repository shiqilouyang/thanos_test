"""
encode:utf-8
Author:aidan.hu
Data:2022/1/11
"""
import pytest

from common.logger import logger
from operation.contract.client.quote.qoute_class import Qoute
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import get_data


class TestIndexPrice:
    """获取单个交易对的指数价格"""
    qoute_request = Qoute()
    test_data = get_data("quote_test_index_price_data.yml")

    # 获取指数价格接口正向测试用例，详情见数据文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_success") == {} else [test_data])
    def test_success(self,test_data):
        cases_data = test_data["test_success"]
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 放入参数发起请求，获取请求结果
            res = qoute_symbol_index_price(parameter.get("symbol"))
            logger.info(f"获取指定交易对的指数价格 ==>> {case_name}的参数{parameter}返回结果 ==>> {res.response}")
            # 断言
            assert res.response["msgInfo"] == expected_result["msgInfo"]

    # 反向用例，用例详情查看数据文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_unsuccess") == {} else [test_data])
    def test_unsuccess(self,test_data):
        qoute_request = self.qoute_request
        cases_data = test_data["test_unsuccess"]
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 放入参数发起请求，获取请求结果
            res = qoute_request.index_price(param=parameter)
            logger.info(f"获取指定交易对的指数价格 ==>> {case_name}的参数{parameter}返回结果 ==>> {res}")
            # 断言
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_index_price.py'])

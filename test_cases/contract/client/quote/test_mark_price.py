"""
encode:utf-8
Author:aidan.hu
Data:2022/1/11
"""
import pytest
from common.logger import logger
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestKline:
    """获取单个交易对的标记价格测试类"""
    qoute_request = Qoute()
    test_data = get_data("quote_test_mark_price_data.yml")

    # 正向用例，详情见数据文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_success") == {} else [test_data])
    def test_success(self, test_data):
        cases_data = test_data["test_success"]
        qoute_request = self.qoute_request
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 发起请求
            res = qoute_request.mark_price(param=parameter)
            logger.info(f"获取交易对的标记价格 ==>> {case_name}的参数{parameter}返回结果 ==>> {res}")
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]

    @pytest.mark.parametrize("test_data", [] if test_data.get("test_unsucces") == {} else [test_data])
    def test_unsucces(self,test_data):
        cases_data = test_data["test_unsucces"]
        qoute_request = self.qoute_request
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 发起请求
            res = qoute_request.mark_price(param=parameter)
            logger.info(f"获取交易对的标记价格 ==>> {case_name}的参数{parameter}返回结果 ==>> {res}")
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_mark_price.py'])

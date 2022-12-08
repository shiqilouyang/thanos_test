"""
encode:utf-8
Author:aidan.hu
Data:2022/1/10
"""
import pytest
from common.logger import logger
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestFundingRate:
    """获取资金费率用例"""
    quote_request = Qoute()
    test_data = get_data("quote_test_funding_rate_data.yml")


    # 正确获取资金费率
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_success") == {} else [test_data])
    def test_success(self, test_data):
        case_data = test_data["test_success"]["correct_symbol"]
        parm, name, expected_result = case_data["parameter"], case_data["name"], case_data["expected_result"]
        res = self.quote_request.funding_rate(param=parm)
        logger.info(f"获取资金费率 ==>> {name}的返回结果 ==>> {res}")
        assert res["msgInfo"] == expected_result["msg"]
        assert res["result"]["symbol"] == parm["symbol"]

    # 获取资金费率反向用例：交易对为空，无效交易对
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_unsuccess") == {} else [test_data])
    def test_unsuccess(self, test_data):
        cases_data = test_data["test_unsuccess"]
        for key in cases_data.keys():
            case_data = cases_data[key]
            parm, name, expected_result = case_data["parameter"], case_data["name"], case_data["expected_result"]
            res = self.quote_request.funding_rate(param=parm)
            logger.info(f"获取资金费率 ==>> {name}的返回结果 ==>> {res}")
            assert res["error"]["msg"] == expected_result["msg"]
            assert res["msgInfo"] == expected_result["msgInfo"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_funding_rate.py'])

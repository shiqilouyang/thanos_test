"""
encode:utf-8
Author:aidan.hu
Data:2022/1/7
"""
import pytest
from common.logger import logger
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestDepth:
    """交易对的深度信息"""
    quote_request = Qoute()
    test_data = get_data("quote_test_depth_data.yml")

    # 正确输入档位和交易对查询查询: 档位为1、50、1-50
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_correct") == {} else [test_data])
    def test_correct(self, test_data):
        test_correct = test_data["test_correct"]
        for case_data in test_correct.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 发起请求，获取接口返回数据
            res = self.quote_request.depth(param=parameter)
            logger.info(f"获取指定交易对的深度信息 ==>> {case_data}的返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]

    # 反向的用例，yml文件的注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_unsuccessful") == {} else [test_data])
    def test_unsuccess(self, test_data):
        cases_data = test_data["test_unsuccessful"]
        for key in cases_data.keys():
            case_data = cases_data[key]
            parm, name, expected_result = case_data["parameter"], case_data["name"], case_data["expected_result"]
            res = self.quote_request.depth(param=parm)
            logger.info(f"获取指定交易对的深度信息 ==>> {name}的返回结果 ==>> {res}")
            assert expected_result["msg"] == res["error"]["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_depth.py'])

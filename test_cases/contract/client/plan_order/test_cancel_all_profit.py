"""
encode:utf-8
Author:aidan.hu
Data:2022/1/26
"""
import pytest
from common.logger import logger
from operation.contract.client.plan_order.plan_request import PlanRequest
from test_cases.contract.client.conftest import get_data


class TestCancelAllProfit:
    """撤销所有止盈止损"""
    plan_request = PlanRequest()
    test_data = get_data("plan_cancel_all_profit_data.yml")

    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_all_profit_success") == {} else [test_data])
    def test_cancel_all_profit_success(self, test_data):
        """撤销所有订单的正向测试用例，详情见数据文件注释"""
        cases_data = test_data["cancel_all_profit_success"]
        self.plan_request.mongo.update_col("profit")
        for case_data in cases_data.values():
            # （1）读取文件数据
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # (2) 获取接口返回数据
            res = self.plan_request.cancel_all_profit_stop(parm=parameter)
            logger.info(f"撤销所有止盈止损 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            import time
            time.sleep(2)
            # （3）根据参数判断查询mongo的条件，查询数据并断言
            if parameter.get("symbol"):
                mongo_res = [profit for profit in self.plan_request.mongo.find(
                    {"accountId": self.plan_request.account_id,
                     "symbol": self.plan_request.get_symbolid(parameter["symbol"]), "state": {"$in": [1, 2]}})]
                logger.info("parameter.get('symbol')条件下mongo 查询数据为 {}".format({"accountId": self.plan_request.account_id,
                     "symbol": self.plan_request.get_symbolid(parameter["symbol"]), "state": {"$in": [1, 2]}}))
                assert not mongo_res
            else:
                mongo_res = [profit for profit in self.plan_request.mongo.find(
                    {"accountId": self.plan_request.account_id, "state": {"$in": [1, 2]}})]
                logger.info("mongo 查询数据为 {}".format({"accountId": self.plan_request.account_id, "state": {"$in": [1, 2]}}))
                assert not mongo_res

    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_all_profit_failed") == {} else [test_data])
    def test_cancel_all_profit_failed(self, test_data):
        """撤销所有订单的正向测试用例，详情见数据文件注释"""
        cases_data = test_data["cancel_all_profit_failed"]
        for case_data in cases_data.values():
            # （1）读取文件数据
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # (2) 发起请求并进行断言
            res = self.plan_request.cancel_all_profit_stop(parm=parameter)
            logger.info(f"撤销所有止盈止损 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_cancel_all_profit.py'])

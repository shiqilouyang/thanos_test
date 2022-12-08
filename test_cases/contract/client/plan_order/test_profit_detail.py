"""
encode:utf-8
Author:aidan.hu
Data:2022/1/27
"""
import pytest
from decimal import Decimal
from common.logger import logger
from operation.contract.client.plan_order.plan_request import PlanRequest
from test_cases.contract.client.conftest import get_data


class TestProfitDetail:
    """根据profitId查询止盈止盈测试类"""
    plan_request = PlanRequest()
    test_data = get_data("plan_profit_detail_data.yml")

    @pytest.mark.parametrize("test_data", [] if test_data.get("plan_detail_failed") == {} else [test_data])
    def test_profit_detail_success(self, test_data):
        """id查询止盈止损的正向测试类"""
        self.plan_request.mongo.update_col("profit")
        cases_data = test_data["profit_detail_success"]
        for case_data in cases_data.values():
            name, expected_result = case_data["name"], case_data["expected_result"]
            # (1)从数据库中查找任一止盈止损id
            mongo_res = self.plan_request.mongo.find_one({"accountId": self.plan_request.account_id})
            # (2) 获取id,发起请求
            profit_id = mongo_res.get("_id")
            if profit_id:
                logger.info("从数据库中查找任一止盈止损id 为{}".format(profit_id))
                res = self.plan_request.profit_detail(profit_id=profit_id)
                logger.info(f"查询止盈止损正向用例 ==>{name}===>>profit_id为{profit_id}=====>>返回结果 ==>> {res}")
                assert res["msgInfo"] == expected_result["msgInfo"]
                result = res.get("result")
                assert self.plan_request.get_symbolid(result["symbol"]) == mongo_res["symbolId"]
                assert self.plan_request.get_num_by_position_side(result["positionSide"]) == mongo_res["positionSide"]
                assert result["origQty"] == mongo_res["origQty"]
                assert Decimal(result["triggerProfitPrice"]) if result["triggerProfitPrice"] else None == Decimal(mongo_res["triggerProfitPrice"])
                if result.get("triggerStopPrice") is not None:
                    assert Decimal(result.get("triggerStopPrice")) ==\
                                                                   Decimal(mongo_res.get("triggerStopPrice"))
                assert self.plan_request.get_num_by_entrust_state(result["state"]) == mongo_res["state"]

    @pytest.mark.parametrize("test_data", [] if test_data.get("profit_detail_failed") == {} else [test_data])
    def test_profit_detail_failed(self, test_data):
        """根据id查询止盈止损反向用例"""
        cases_data = test_data["profit_detail_failed"]
        for case_data in cases_data.values():
            profit_id, case_name, expected_result = case_data["parameter"]["profitId"], case_data["name"], case_data[
                "expected_result"]
            res = self.plan_request.profit_detail(profit_id=profit_id)
            logger.info(f"查询止盈止损正向用例 ==>{case_name}===>>profit_id为{profit_id}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_profit_detail.py'])

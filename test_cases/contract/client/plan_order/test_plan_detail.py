"""
encode:utf-8
Author:aidan.hu
Data:2022/1/25
"""
import pytest

from common.logger import logger
from operation.contract.client.plan_order.plan_request import PlanRequest
from test_cases.contract.client.conftest import get_data


class TestPlanDetail:
    """根据计划单id查询计划委托详情"""
    plan_request = PlanRequest()
    test_data = get_data("plan_detail_data.yml")

    # 查看计划单详情正向用例
    @pytest.mark.parametrize("test_data", [] if test_data.get("plan_detail_success") == {} else [test_data])
    def test_plan_detail_success(self, test_data):
        cases_data = test_data["plan_detail_success"]
        self.plan_request.mongo.update_col("entrust")
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            mongo_res = self.plan_request.mongo.find_one({"accountId":self.plan_request.account_id})
            entrust_id = mongo_res.get("_id")
            if entrust_id:
                res = self.plan_request.plan_detail(entrust_id=entrust_id)
                logger.info(f"查询止盈止损正向用例 ==>{case_name}===>>entrust_id为{entrust_id}=====>>返回结果 ==>> {res}")
                result = res["result"]
                assert res["msgInfo"] == expected_result["msgInfo"]
                assert self.plan_request.get_symbolid(result["symbol"]) == mongo_res["symbolId"]
                assert self.plan_request.get_num_by_entrust_type(result["entrustType"]) == mongo_res["entrustType"]
                assert self.plan_request.get_num_by_order_side(result["orderSide"]) == mongo_res["orderSide"]
                assert self.plan_request.get_num_by_position_side(result["positionSide"]) == mongo_res["positionSide"]
                assert self.plan_request.get_num_by_timeInforce(result["timeInForce"]) == mongo_res["timeInForce"]
                assert result["price"] == mongo_res["price"]
                assert result["origQty"] == mongo_res["origQty"]
                assert result["stopPrice"] == mongo_res["stopPrice"]
                assert self.plan_request.get_num_by_triggerPriceType(result["triggerPriceType"]) == mongo_res["triggerPriceType"]
                assert self.plan_request.get_num_by_entrust_state(result["state"]) == mongo_res["state"]

    # 查看计划单详情反向用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("plan_detail_failed") == {} else [test_data])
    def test_plan_detail_failed(self, test_data):
        cases_data = test_data["plan_detail_failed"]
        for case_data in cases_data.values():
            # （1）解析参数
            entrust_id, case_name, expected_result = case_data["parameter"].get("entrust_id"), case_data["name"], case_data[
                "expected_result"]
            # （2）发起请求并断言
            res = self.plan_request.plan_detail(entrust_id=entrust_id)
            logger.info(f"查询计划委托单反向用例 ==>{case_name}===>>entrust_id为{entrust_id}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_plan_detail.py'])
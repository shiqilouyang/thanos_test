"""
encode:utf-8
Author:aidan.hu
Data:2022/1/24
"""
from decimal import Decimal
import pytest
from common.logger import logger
from operation.contract.client.plan_order.plan_request import PlanRequest
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestCancelPlan:
    """撤销订单测试类"""
    plan_request = PlanRequest()
    mark_price = Decimal(Qoute().mark_price()["result"]["p"])
    test_data = get_data("plan_cancel_plan_data.yml")

    # 正确撤销计划委托,详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_plan_success") == {} else [test_data])
    def test_cancel_plan_success(self, test_data):
        cases_data = test_data["cancel_plan_success"]
        self.plan_request.mongo.update_col("entrust")
        for case_data in cases_data.values():
            # （1）读取文件数据
            parameter, case_name, expected_result = case_data["create_parameter"], case_data["name"], case_data[
                "expected_result"]
            # （2）拼接创建计划委托的参数
            parameter["price"] = str(round(self.mark_price + Decimal(0.1),2))
            parameter["stopPrice"] = str(round(self.mark_price + Decimal(0.1),2))
            # （3）创建计划委托，从接口获取委托订单
            res = self.plan_request.create_plan(parm=parameter)
            logger.info(f"撤销计划单前置下计划单 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            entrust_id = int(res["result"])
            # （4）撤销该委托
            cancel_res = self.plan_request.cancel_plan(entrust_id=entrust_id)
            logger.info(f"撤销计划单接口 ==>{case_name}===>>撤销委托单id为{entrust_id}=====>>返回结果 ==>> {cancel_res}")
            # （5）链接Mongo，比对状态数据
            mongo_res = self.plan_request.mongo.find_one({"_id": entrust_id})
            assert mongo_res["state"] == 4

    # 撤销计划委托的反向测试用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_plan_failed") == {} else [test_data])
    def test_cancel_plan_failed(self, test_data):
        cases_data = test_data["cancel_plan_failed"]
        self.plan_request.mongo.update_col("entrust")
        for case_data in cases_data.values():
            # （1）读取文件数据
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # （2）根据参数确定去mongo拿已有的订单号还是自定义订单号
            if parameter.get("state"):
                mongo_res = self.plan_request.mongo.find_one(
                    {"accountId": self.plan_request.account_id, "state": parameter["state"]})
                if mongo_res:
                    entrust_id = mongo_res.get("_id")
                else:
                    entrust_id = None
            else:
                entrust_id = parameter["entrustId"]
            if entrust_id:
                # （3）发起结果，进行断言
                res = self.plan_request.cancel_plan(entrust_id=entrust_id)
                logger.info(f"撤销计划单 ==>{case_name}===>>entrust_id为{entrust_id}=====>>返回结果 ==>> {res}")
                assert res["msgInfo"] == expected_result["msgInfo"]
                assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_cancel_entrust.py'])

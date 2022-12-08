"""
encode:utf-8
Author:aidan.hu
Data:2022/1/24
"""
import time
import pytest

from common.logger import logger
from common.set_up_balance_and_position import set_up_position
from operation.contract.client.plan_order.plan_request import PlanRequest
from operation.contract.client.quote.qoute_class import Qoute
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import get_data


class TestCreatePlan:
    """创建计划委托测试类"""
    plan_request = PlanRequest()
    mark_price = qoute_symbol_index_price('dao_usdt').response['result']["p"]
    latest_price = float(Qoute().deal()["result"][0]["p"])
    test_data = get_data("plan_create_plan_data.yml")

    # 前置处理，创建持仓
    def setup_class(self):
        set_up_position()

    # 创建计划委托的正向测试用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("create_plan_success") == {} else [test_data])
    def test_create_plan_success(self, test_data):
        """1、动态拼接价格和触发价格
           2、根据拼接的参数发起请求
           3、断言，比对数据"""
        cases_data = test_data["create_plan_success"]
        self.plan_request.mongo.update_col("entrust")
        price_dict = {
            "good_than_mark_price": round(float(self.mark_price) + 0.1, 3),
            "less_than_mark_price": round(float(self.mark_price) - 0.1, 3),
            "good_than_latest_price": round(float(self.mark_price) + 0.1, 3),
            "less_than_latest_price": round(float(self.mark_price) - 0.1, 3)
        }
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 根据参数动态传入触发价格和止盈止盈价格
            parameter["price"] = price_dict.get(parameter.get("price"))
            parameter["stopPrice"] = price_dict.get(parameter.get("stopPrice"))
            # 发起请求获取断言
            res = self.plan_request.create_plan(parm=parameter)
            logger.info(f"创建计划委托正向测试用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            # 去mongo获取数据
            entrust_id = int(res["result"])
            time.sleep(0.5)
            mongo_res = self.plan_request.mongo.find_one({"_id": entrust_id})
            # 断言，进行数据比对
            assert mongo_res["entrustType"] == self.plan_request.get_num_by_entrust_type(parameter["entrustType"])
            assert mongo_res["orderSide"] == self.plan_request.get_num_by_order_side(parameter["orderSide"])
            assert str(mongo_res["origQty"]) == parameter["origQty"]
            assert mongo_res["positionSide"] == self.plan_request.get_num_by_position_side(parameter["positionSide"])
            assert mongo_res["timeInForce"] == self.plan_request.get_num_by_timeInforce(parameter["timeInForce"])
            assert mongo_res["triggerPriceType"] == self.plan_request.get_num_by_triggerPriceType(
                parameter["triggerPriceType"])
            assert float(mongo_res["price"]) == parameter["price"]
            assert float(mongo_res["stopPrice"])  == parameter["stopPrice"]

    @pytest.mark.parametrize("test_data", [] if test_data.get("create_plan_failed") == {} else [test_data])
    def test_create_plan_failed(self, test_data):
        """创建计划委托的反向用例，详情见数据文件"""
        cases_data = test_data["create_plan_failed"]
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 根据参数动态传入触发价格和止盈止盈价格
            if parameter["triggerPriceType"] == "MARK_PRICE":
                if parameter["price"] == "gt":
                    parameter["price"] = str(float(self.mark_price) + 0.3)
                elif parameter["price"] == "lt":
                    parameter["price"] = str(float(self.mark_price) - 0.3)
            elif parameter["triggerPriceType"] == "LATEST_PRICE":
                if parameter["price"] == "gt":
                    parameter["price"] = str(float(self.latest_price) + 0.3)
                elif parameter["price"] == "lt":
                    parameter["price"] = str(float(self.latest_price) - 0.3)
            else:
                if parameter["price"] == "gt":
                    parameter["price"] = str(float(self.mark_price) + 0.3)
                elif parameter["price"] == "lt":
                    parameter["price"] = str(float(self.mark_price) - 0.3)
            if parameter["stopPrice"] == "gt":
                parameter["stopPrice"] = str(float(self.mark_price) + 0.3)
            elif parameter["stopPrice"] == "lt":
                parameter["stopPrice"] = str(float(self.mark_price) - 0.3)
            res = self.plan_request.create_plan(parm=parameter)
            logger.info(f"创建计划委托反向测试用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]

    def teardown_class(self):
        """后置处理，撤销所有的计划委托"""
        self.plan_request.cancel_all_plan()


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_create_plan.py'])

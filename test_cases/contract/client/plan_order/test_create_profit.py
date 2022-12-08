"""
encode:utf-8
Author:aidan.hu
Data:2022/1/26
"""
from decimal import Decimal

import pytest

from common.logger import logger
from common.set_up_balance_and_position import set_up_position, set_down_position
from operation.contract.client.plan_order.plan_request import PlanRequest
from operation.contract.client.position.position_class import Positon
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestCreateProfit:
    """创建止盈止损测试类"""
    plan_request = PlanRequest()
    test_data = get_data("plan_create_profit_data.yml")

    def setup_class(self):
        """前置处理，撤销所有的止盈止损，创建持仓"""
        self.plan_request.cancel_all_profit_stop()
        set_up_position()

    @pytest.mark.parametrize("test_data", [] if test_data.get("plan_create_profit_success") == {} else [test_data])
    def test_plan_create_profit_success(self, test_data):
        """创建止盈止损的正向测试用例，详情见数据文件"""
        cases_data = test_data["plan_create_profit_success"]
        self.plan_request.mongo.update_col("profit")
        long_entry = float(Positon().get_entry_price(position="LONG"))
        short_entry = float(Positon().get_entry_price(position="SHORT"))
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # (1)根据参数动态拼接止盈止损价格
            if parameter.get("positionSide") == "LONG":
                if "triggerProfitPrice" in parameter.keys():
                    parameter["triggerProfitPrice"] = str(round(Decimal(long_entry) + Decimal(0.3),2))
                if "triggerStopPrice" in parameter.keys():
                    parameter["triggerStopPrice"] = str(round(Decimal(long_entry) - Decimal(0.2),2))
            elif parameter.get("positionSide") == "SHORT":
                if "triggerProfitPrice" in parameter.keys():
                    parameter["triggerProfitPrice"] = str(round(Decimal(short_entry) - Decimal(0.3),2))
                if "triggerStopPrice" in parameter.keys():
                    parameter["triggerStopPrice"] = str(round(Decimal(short_entry) + Decimal(0.2),2))
            # （2）发起请求获取接口返回
            res = self.plan_request.create_profit(parm=parameter)
            logger.info(f"创建止盈止损正向用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            # (3)比对mongo数据进行断言
            profit_id = int(res["result"])
            mongo_res = self.plan_request.mongo.find_one({"_id": profit_id})
            assert self.plan_request.get_num_by_position_side(parameter["positionSide"]) == mongo_res["positionSide"]
            if parameter.get("triggerProfitPrice"):
                assert float(parameter["triggerProfitPrice"]) == float(mongo_res["triggerProfitPrice"])
            if parameter.get("triggerStopPrice"):
                assert float(parameter["triggerStopPrice"]) == float(mongo_res["triggerStopPrice"])

    @pytest.mark.parametrize("test_data", [] if test_data.get("had_profit_create_profit") == {} else [test_data])
    def test_had_profit_create_profit(self, test_data):
        """已有止盈止损创建止盈止损的测试用例，详情见数据文件"""
        cases_data = test_data["had_profit_create_profit"]
        long_entry = float(Positon().get_entry_price(position="LONG"))
        short_entry = float(Positon().get_entry_price(position="SHORT"))
        long_position_size = int(Positon().get_position_size(position_side="LONG"))
        short_position_size = int(Positon().get_position_size(position_side="SHORT"))
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # (1)根据参数动态拼接止盈止损价格
            if parameter.get("positionSide") == "LONG":
                parameter["origQty"] = long_position_size
                parameter["triggerProfitPrice"] = long_entry + 0.3
                parameter["triggerStopPrice"] = long_entry - 0.2
            elif parameter.get("positionSide") == "SHORT":
                parameter["origQty"] = short_position_size
                parameter["triggerProfitPrice"] = long_entry - 0.3
                parameter["triggerStopPrice"] = long_entry + 0.2
            # (2)连续发两次请求，第二次失败
            res = self.plan_request.create_profit(parm=parameter)
            res_2 = self.plan_request.create_profit(parm=parameter)
            logger.info(f"创建止盈止损反向用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res_2}")
            assert res_2["msgInfo"] == expected_result["msgInfo"]
            assert res_2["error"]["msg"] == expected_result["msg"]

    @pytest.mark.parametrize("test_data", [] if test_data.get("create_profit_without_position") == {} else [test_data])
    def test_create_profit_without_position(self, test_data):
        """没有仓位损创建止盈止损的测试用例，详情见数据文件"""
        cases_data = test_data["create_profit_without_position"]
        # (1) 获取当前标记价格
        dao_mark_price = float(Qoute().mark_price()["result"]["p"])
        # (2) 检查所有持仓并将当前用户参数平仓
        set_down_position("dao_usdt")
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            if parameter.get("positionSide") == "LONG":
                parameter["triggerProfitPrice"] = round(Decimal(dao_mark_price) + Decimal(0.3),2)
                parameter["triggerStopPrice"] = round(Decimal(dao_mark_price) - Decimal(0.2),2)
            elif parameter.get("positionSide") == "SHORT":
                parameter["triggerProfitPrice"] = round(Decimal(dao_mark_price) - Decimal(0.3),2)
                parameter["triggerStopPrice"] = round(Decimal(dao_mark_price) + Decimal(0.2),2)
            res = self.plan_request.create_profit(parm=parameter)
            logger.info(f"创建止盈止损反向用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            # assert res["error"]["msg"] == expected_result["msg"]

    @pytest.mark.parametrize("test_data", [] if test_data.get("invalid_parameter_create_profit") == {} else [test_data])
    def test_invalid_parameter_create_profit(self, test_data):
        """无效参数创建止盈止损用例，详情见数据文件"""
        cases_data = test_data["invalid_parameter_create_profit"]
        # (1) 检查是否有持仓，没有持仓的时候创建持仓
        set_up_position()
        # (2) 从持仓中获取仓位价格
        long_entry = float(Positon().get_entry_price(position="LONG"))
        short_entry = float(Positon().get_entry_price(position="SHORT"))
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # (1)根据参数动态拼接止盈止损价格
            if parameter.get("positionSide") == "LONG":
                if parameter.get("triggerProfitPrice") == "by_position":
                    # round(Decimal(long_entry) + Decimal(0.3),2)
                    parameter["triggerProfitPrice"] = round(Decimal(long_entry) + Decimal(0.3),2)
                if parameter.get("triggerStopPrice") == "by_position":
                    parameter["triggerStopPrice"] = round(Decimal(long_entry) - Decimal(0.2),2)
            elif parameter.get("positionSide") == "SHORT":
                if parameter.get("triggerProfitPrice") == "by_position":
                    parameter["triggerProfitPrice"] = round(Decimal(long_entry) - Decimal(0.3),2)
                if parameter.get("triggerStopPrice") == "by_position":
                    parameter["triggerStopPrice"] =round(Decimal(long_entry) + Decimal(0.2),2)
            else:
                if parameter.get("triggerProfitPrice") == "by_position":
                    parameter["triggerProfitPrice"] = round(Decimal(long_entry) - Decimal(0.3),2)
                if parameter.get("triggerStopPrice") == "by_position":
                    parameter["triggerStopPrice"] = round(Decimal(long_entry) + Decimal(0.2),2)
            # （2）发起请求，获取接口返回数据
            res = self.plan_request.create_profit(parm=parameter)
            logger.info(f"创建止盈止损反向用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]

    def teardown_class(self):
        """后置处理，撤销所有的计划委托"""
        self.plan_request.cancel_all_profit_stop()


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_create_profit.py'])

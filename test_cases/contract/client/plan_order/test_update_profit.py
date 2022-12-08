"""
encode:utf-8
Author:aidan.hu
Data:2022/1/27
"""
from decimal import Decimal
import pytest
from common.logger import logger
from operation.contract.client.plan_order.plan_request import PlanRequest
from operation.contract.client.position.position_class import Positon
from test_cases.contract.client.conftest import get_data


class TestUpdateProfit:
    """修改止盈止损测试类"""
    plan_request = PlanRequest()
    test_data = get_data("plan_update_profit_data.yml")
    long_profit_id = None
    short_profit_id = None
    long_entry_price = None
    short_entry_price = None

    def setup_class(self):
        """前置处理，初始化止盈止损，得到止盈止盈id、开仓价格"""
        self.long_profit_id = int(self.plan_request.create_default_profit())
        self.short_profit_id = int(self.plan_request.create_default_profit(position="SHORT"))
        self.long_entry_price = Positon().get_entry_price(position="LONG")
        self.short_entry_price = Positon().get_entry_price(position="SHORT")

    @pytest.mark.parametrize("test_data", [] if test_data.get("update_profit_success") == {} else [test_data])
    def test_update_profit_success(self, test_data):
        """修改止盈止损的正向测试用例
            1、读取用例数据
            2、动态凭借修改止盈止损的参数，数据文件中止盈止损价格为空时，根据仓位动态拼接止盈止损价格
            3、发起请求，得到响应数据
            4、断言，比对接口返回数据和mongo数据
        """
        cases_data = test_data["update_profit_success"]
        self.plan_request.mongo.update_col("profit")
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # (1)通过参数判断止盈止损的仓位方向，并拼接参数
            if parameter.get("profitId") == "long_position":
                if "triggerProfitPrice" in parameter.keys():
                    parameter["triggerProfitPrice"] = float(round(Decimal(self.short_entry_price) + Decimal(0.12), 2))
                if "triggerStopPrice" in parameter.keys():
                    parameter["triggerStopPrice"] = float(round(Decimal(self.short_entry_price) - Decimal(0.12), 2))
                parameter["profitId"] = self.long_profit_id
            elif parameter.get("profitId") == "short_position":
                if "triggerProfitPrice" in parameter.keys():
                    parameter["triggerProfitPrice"] = float(round(Decimal(self.short_entry_price) - Decimal(0.12), 2))
                if "triggerStopPrice" in parameter.keys():
                    parameter["triggerStopPrice"] = float(round(Decimal(self.short_entry_price) + Decimal(0.12), 2))
                parameter["profitId"] = self.short_profit_id

            logger.info("修改止盈止损传参为{}".format(parameter))
            # (2) 获取接口返回数据
            res = self.plan_request.update_profit_stop(parm=parameter)
            logger.info(f"修改止盈止损正向用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            # （3）断言，比对mongo数据
            assert res["msgInfo"] == expected_result["msgInfo"]
            mongo_res = self.plan_request.mongo.find_one({"_id": parameter["profitId"]})
            if parameter.get("triggerProfitPrice"):
                assert str(parameter["triggerProfitPrice"]) == mongo_res["triggerProfitPrice"]
            else:
                assert not mongo_res.get("triggerProfitPrice")
            if parameter.get("triggerStopPrice"):
                assert str(parameter["triggerStopPrice"]) == mongo_res["triggerStopPrice"]
            else:
                assert not mongo_res.get("triggerStopPrice")

    @pytest.mark.parametrize("test_data", [] if test_data.get("update_profit_failed") == {} else [test_data])
    def test_update_profit_failed(self, test_data):
        """修改止盈止损的反向测试用例
            1、读取用例数据
            2、根据数据文件动态拼接参数，数据文件为空时拼接正确参数，gt_short_position拼接
            大于空仓开仓均价，lt_long_position拼接小于多仓开仓价
            4、发起请求，得到响应数据
            5、断言，比对接口返回数据和mongo数据
        """
        cases_data = test_data["update_profit_failed"]
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            profit_dict = {
                "less_than_long_position_price": round(self.long_entry_price - Decimal(0.12), 4),
                "good_than_short_position_price": round(self.short_entry_price + Decimal(0.12), 4),
                "good_than_long_position_price": round(self.long_entry_price + Decimal(0.12), 4),
                "less_than_short_position_price": round(self.short_entry_price - Decimal(0.12), 4)
            }
            if parameter.get("profitId") == "LONG":
                parameter["profitId"] = self.long_profit_id
            elif parameter.get("profitId") == "SHORT":
                parameter["profitId"] = self.short_profit_id
            if parameter.get("triggerProfitPrice") and parameter.get("triggerProfitPrice") in profit_dict.keys():
                parameter["triggerProfitPrice"] = profit_dict.get(parameter["triggerProfitPrice"])
            if parameter.get("triggerStopPrice") and parameter.get("triggerStopPrice") in profit_dict.keys():
                parameter["triggerStopPrice"] = profit_dict.get(parameter["triggerStopPrice"])
            res = self.plan_request.update_profit_stop(parm=parameter)
            logger.info(f"修改止盈止损反向用例 ==>{case_name}===>>参数为{parameter}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_update_profit.py'])

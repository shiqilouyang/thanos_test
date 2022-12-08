"""
encode:utf-8
Author:aidan.hu
Data:2022/1/26
"""
import pytest

from common.logger import logger
from common.set_up_balance_and_position import set_up_position
from operation.contract.client.plan_order.plan_request import PlanRequest
from operation.contract.client.position.position_class import Positon
from test_cases.contract.client.conftest import get_data


class TestCancelProfit:
    """根据止盈止损订单id撤销止盈止损测试类"""
    plan_request = PlanRequest()
    test_data = get_data("plan_cancel_profit_data.yml")

    # 前置处理，创建持仓
    def setup_class(self):
        set_up_position()
        self.plan_request.cancel_all_profit_stop()

    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_profit_success") == {} else [test_data])
    def test_cancel_profit_success(self, test_data):
        """根据止盈止损id撤销止盈止损正向测试用例,详情见数据文件格式"""
        cases_data = test_data["cancel_profit_success"]
        self.plan_request.mongo.update_col("profit")
        # (1) 获取多仓、空仓的开仓均价
        long_entry = float(Positon().get_entry_price(position="LONG"))
        short_entry = float(Positon().get_entry_price(position="SHORT"))
        for case_data in cases_data.values():
            # （2）读取参数，动态凭借创建止盈止损价格
            create_profit_parameter, case_name, expected_result = case_data["create_profit_parameter"], case_data[
                "name"], case_data["expected_result"]
            if create_profit_parameter.get("positionSide") == "LONG":
                create_profit_parameter["triggerProfitPrice"] = round(long_entry + 0.2, 3)
                create_profit_parameter["triggerStopPrice"] = round(long_entry - 0.2, 3)
            elif create_profit_parameter.get("positionSide") == "SHORT":
                create_profit_parameter["triggerProfitPrice"] = round(short_entry - 0.2, 3)
                create_profit_parameter["triggerStopPrice"] = round(short_entry + 0.2, 3)
            # (3) 创建止盈止损
            create_profit_res = self.plan_request.create_profit(parm=create_profit_parameter)
            if create_profit_res.get("result"):
                profit_id = int(create_profit_res["result"])
                cancel_profit_res = self.plan_request.cancel_profit_stop(profit_id=profit_id)
                logger.info(
                    f"根据id撤销止盈止损正向用例 ==>{case_name}===>>profit_id为{profit_id}=====>>返回结果 ==>> {cancel_profit_res}")
                assert cancel_profit_res["msgInfo"] == expected_result["msgInfo"]
                mongo_res = self.plan_request.mongo.find_one({"_id": profit_id})
                assert mongo_res["state"] == expected_result["state"]

    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_profit_failed") == {} else [test_data])
    def test_cancel_profit_failed(self, test_data):
        """根据止盈止损id撤销止盈止损反向测试用例,详情见数据文件格式"""
        cases_data = test_data["cancel_profit_failed"]
        for case_data in cases_data.values():
            # （1）读取参数
            profit_id, case_name, expected_result = case_data["parameter"]["profit_id"], case_data[
                "name"], case_data["expected_result"]
            # （2）获取接口返回数据
            cancel_profit_res = self.plan_request.cancel_profit_stop(profit_id=profit_id)
            logger.info(
                f"根据id撤销止盈止损反向用例 ==>{case_name}===>>profit_id为{profit_id}=====>>返回结果 ==>> {cancel_profit_res}")
            # (3)断言
            assert cancel_profit_res["msgInfo"] == expected_result["msgInfo"]
            assert cancel_profit_res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_cancel_profit.py'])

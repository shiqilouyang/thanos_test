"""
encode:utf-8
Author:aidan.hu
Data:2022/1/25
"""
import time

import pytest

from common.logger import logger
from operation.contract.client.plan_order.plan_request import PlanRequest
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestCancelAll:
    """撤销所有订单的测试类"""
    plan_request = PlanRequest()
    dao_mark_price = Qoute().mark_price()["result"]["p"]
    test_data = get_data("plan_cancel_all_plan_data.yml")
    ada_mark_price = Qoute().mark_price(param={"symbol": "dao_usdt"})["result"]["p"]

    # 正确撤销计划委托,详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_all_plan_success") == {} else [test_data])
    def test_cancel_all_plan_success(self, test_data):
        cases_data = test_data["cancel_all_plan_success"]
        self.plan_request.mongo.update_col("entrust")
        for case_data in cases_data.values():
            # （1）读取文件数据
            case_name, expected_result = case_data["name"], case_data["expected_result"]
            create_parameter_1, create_parameter_2 = case_data["create_parameter_1"], case_data["create_parameter_2"]
            # （2）拼接创建计划委托的参数
            create_parameter_1["price"] = float(self.dao_mark_price) + 0.1
            create_parameter_1["stopPrice"] = float(self.dao_mark_price) + 0.1
            if create_parameter_2["symbol"] == "dao_usdt":
                create_parameter_2["price"] = float(self.ada_mark_price) + 0.1
                create_parameter_2["stopPrice"] = float(self.ada_mark_price) + 0.1
            else:
                create_parameter_2["price"] = float(self.dao_mark_price) + 0.1
                create_parameter_2["stopPrice"] = float(self.dao_mark_price) + 0.1
            # (3) 两个不同的交易对下计划委托单
            create_entrust_1 = self.plan_request.create_plan(parm=create_parameter_1)
            create_entrust_2 = self.plan_request.create_plan(parm=create_parameter_2)
            # (4) 发起撤销所有计划委托单的请求,根据参数判断是撤销交易对还是所有计划单
            if case_data.get("parameter"):
                res = self.plan_request.cancel_all_plan(parm=case_data["parameter"])
                logger.info(f"撤销所有计划单 ==>{case_name}==传参==>{case_data['parameter']}===>>返回结果 ==>> {res}")
                symbol_id = self.plan_request.get_symbolid(case_data.get("parameter").get("symbol"))
                mongo_res = self.plan_request.mongo.get_list_by_find(
                    {"accountId": self.plan_request.account_id, "state": 1, "symbolId": symbol_id})
                logger.info('case_data.get("parameter") 条件下 mongo查询结果为{}'.format(
                    {"accountId": self.plan_request.account_id, "state": 1, "symbolId": symbol_id}
                ))
                assert not mongo_res
            else:
                res = self.plan_request.cancel_all_plan()
                time.sleep(2)
                logger.info(f"撤销所有计划单 ==>{case_name}=====>>返回结果 ==>> {res}")
                mongo_res = self.plan_request.mongo.get_list_by_find(
                    {"accountId": self.plan_request.account_id, "state": 1})
                logger.info(' mongo查询结果为{}'.format(
                    {"accountId": self.plan_request.account_id, "state": 1}
                ))
                assert not mongo_res

    # 撤销所有交易对的反向用例,详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_all_plan_failed") == {} else [test_data])
    def test_cancel_all_plan_failed(self, test_data):
        cases_data = test_data["cancel_all_plan_failed"]
        for case_data in cases_data.values():
            # （1）读取文件数据
            case_name, expected_result = case_data["name"], case_data["expected_result"]
            parameter = case_data["parameter"]
            res = self.plan_request.cancel_all_plan(parm=parameter)
            logger.info(f"撤销所有计划单反向用例 ==>{case_name}=====>>返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_cancel_all_entrust.py'])

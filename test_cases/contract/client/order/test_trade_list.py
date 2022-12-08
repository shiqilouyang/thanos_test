"""
encode:utf-8
Author:aidan.hu
Data:2022/1/21
"""
import pytest

from common.logger import logger
from operation.contract.client.order.order_request import OrderRequest
from test_cases.contract.client.conftest import get_data


class TestTradeList:
    """查询交易明细测试类"""
    order_request = OrderRequest()
    test_data = get_data("order_test_trade_list_data.yml")

    # 查询交易明细的正向测试用例
    @pytest.mark.parametrize("test_data",[] if test_data.get("trade_list_success") == {} else [test_data])
    def test_trade_list_success(self,test_data):
        order_request = self.order_request
        cases_data = test_data["trade_list_success"]
        for value in cases_data.values():
            # 获取用例数据
            order_request.mongo.update_col("order")
            case_name, parameter = value["name"], value["parameter"]
            expected_result = value["expected_result"]
            # 根据参数判断是否有订单id,没有动态去mongo获取一个已经成交的订单id
            order_request.mongo.update_col("order")
            if not parameter["orderId"]:
                order_res = order_request.mongo.find_one({"accountId":order_request.account_id,"state":3})
                parameter["orderId"] = order_res["_id"]
            # 发送请求，获取结果返回数据
            res = order_request.trade_list(parm=parameter)
            logger.info(f'查询交易明细的正向测试用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            # 去mongo拿成交信息
            order_request.mongo.update_col("trade")
            mongo_res = order_request.mongo.ascending_sort_find(query={"orderId":parameter["orderId"]},sort_field="id")
            assert res["msgInfo"] == expected_result["msgInfo"]
            if parameter.get("page"):
                assert parameter["page"] == res["result"]["page"]
            else:
                assert res["result"]["page"] == 1
            if parameter.get("size"):
                assert parameter["size"] == res["result"]["ps"]
            else:
                assert res["result"]["ps"] == 10
            if res.get("result").get("items"):
                first_trade = res.get("result").get("items")[-1]
                assert first_trade.get("timestamp") == mongo_res[0]["timestamp"]
                assert first_trade["quantity"] == str(mongo_res[0]["quantity"])
                assert first_trade["price"] == str(mongo_res[0]["price"])
                assert float(first_trade["fee"]) == float(mongo_res[0]["fee"])
                assert first_trade["feeCoin"] == str(mongo_res[0]["feeCoin"])

    # 查询交易明细反向测试用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("trade_list_failed") == {} else [test_data])
    def test_trade_list_failed(self, test_data):
        order_request = self.order_request
        cases_data = test_data["trade_list_failed"]
        for value in cases_data.values():
            # 获取用例数据
            case_name, parameter = value["name"], value["parameter"]
            expected_result = value["expected_result"]
            # 根据参数判断是否有订单id,没有动态去mongo获取一个已经成交的订单id
            order_request.mongo.update_col("order")
            if parameter.get("orderId") == "mongo":
                order_res = order_request.mongo.find_one({"accountId": order_request.account_id, "state": 3})
                parameter["orderId"] = order_res["_id"]
            res = order_request.trade_list(parm=parameter)
            logger.info(f'查询交易明细的反向测试用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_trade_list.py'])
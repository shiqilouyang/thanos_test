"""
encode:utf-8
Author:aidan.hu
Data:2022/1/19
"""
import pytest

from common.logger import logger
from operation.contract.client.order.order_request import OrderRequest
from test_cases.contract.client.conftest import get_data


class TestDetail:
    """根据id查询订单测试类"""
    # 获取dao_usdt的指数价格
    order_request = OrderRequest()
    test_data = get_data("order_test_detail_data.yml")

    # 通过订单id查询订单信息正向用例,详情见数据文件
    @pytest.mark.parametrize("test_data",  [] if test_data.get("detail_success") == {} else [test_data])
    def test_detail_success(self, test_data):
        order_request = self.order_request
        # 从数据文件获取数据
        case_data = test_data["detail_success"]["correct"]
        case_name = case_data["name"]
        expected_result = case_data["expected_result"]
        # 去mongo获取任意一条订单
        order_request.mongo.update_col("order")
        mongo_res = order_request.mongo.find_one({"accountId": self.order_request.account_id})
        order_id = mongo_res["_id"]
        # 通过订单id获取接口返回数据
        res = order_request.detail(order_id=order_id)
        logger.info(f'订单id查询订单接口--->{case_name}-->参数为{order_id}--->返回结果{res}')
        # 断言，比对数据
        assert res["msgInfo"] == expected_result["msgInfo"]
        order_res = res["result"]
        assert float(order_res["avgPrice"]) == float(mongo_res["avgPrice"])
        assert order_request.get_enumerate_by_order_side(order_res["orderSide"]) == mongo_res["orderSide"]
        assert order_request.get_enumerate_by_order_type(order_res["orderType"]) == mongo_res["orderType"]
        assert order_res["origQty"] == mongo_res["origQty"]

    # 通过订单id查询订单信息反向向用例,详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("detail_failed") == {} else [test_data])
    def test_detail_failed(self, test_data):
        order_request = self.order_request
        # 从数据文件获取数据
        case_data = test_data["detail_failed"]
        for value in case_data.values():
            case_name, order_id, expected_result = value["name"], value["parameter"]["orderId"], value["expected_result"]
            # 发送请求
            res = order_request.detail(order_id=order_id)
            logger.info(f'订单id查询订单接口--->{case_name}-->参数为{order_id}--->返回结果{res}')
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_create_order.py'])
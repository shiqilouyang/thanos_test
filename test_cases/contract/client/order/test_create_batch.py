"""
encode:utf-8
Author:aidan.hu
Data:2022/1/18
"""
import pytest

from common.logger import logger
from operation.contract.client.order.order_request import OrderRequest
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import get_data


class TestCreateBatch:
    """批量下单测试类"""
    index_price = round(float(qoute_symbol_index_price("dao_usdt").response['result']["p"]),2)
    order_request = OrderRequest()
    test_data = get_data("order_test_create_batch_data.yml")

    # 批量下单的正向测试用例
    @pytest.mark.parametrize("test_data", [] if test_data.get("create_batch_success")=={} else [test_data])
    def test_order_success(self,test_data):
        order_request = self.order_request
        cases_data = test_data["create_batch_success"]
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            parameter["list"] = parameter["list"].replace("dao_price",str(self.index_price))
            res = order_request.create_batch(parm=parameter)
            logger.info("传参为{},结果为{}".format(parameter,res))
            assert res["msgInfo"] == expected_result["msgInfo"]

    @pytest.mark.parametrize("test_data", [] if test_data.get("create_batch_failed")=={} else [test_data])
    def test_order_failed(self, test_data):
        order_request = self.order_request
        cases_data = test_data["create_batch_failed"]
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            parameter["list"] = parameter["list"].replace("dao_price",self.index_price)
            res = order_request.create_batch(parm=parameter)
            assert res["msgInfo"] == expected_result["msgInfo"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_create_batch.py'])
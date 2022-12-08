"""
encode:utf-8
Author:aidan.hu
Data:2022/1/15
"""
import time
from decimal import Decimal

import pytest
from common.logger import logger
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.order.order_request import OrderRequest
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import get_data


class TestCancelOrder:
    """撤销订单的测试类,包括单个定单和撤销多个订单的用例"""
    index_price =  Decimal(qoute_symbol_index_price("dao_usdt").response['result']["p"])
    order_request = OrderRequest()
    test_data = get_data("order_test_cancel_data.yml")

    # 撤销单个订单的正向用例，详情数据见数据文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_success") == {} else [test_data])
    def test_cancel_success(self,test_data):
        order_request = self.order_request
        cases_data = test_data["cancel_success"]
        order_request.mongo.update_col("order")
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["order_parameter"], value["expected_result"]
            if "price" in list(parameter.keys()):
                parameter["price"] = round(self.index_price)
            if "triggerProfitPrice" in list(parameter.keys()):
                # self.index_price + Decimal(0.5)
                parameter["triggerProfitPrice"] = round(self.index_price + Decimal(1))
            if "triggerStopPrice" in list(parameter.keys()):
                parameter["triggerStopPrice"] = round(self.index_price - Decimal(0.5))
            # 下单并从返回结果中获取order_id
            res = order_request.create(parm=parameter)
            logger.info("下单响应结果为{}".format(res))
            order_id = int(res["result"])
            import time
            time.sleep(2)
            # 根据参数判断是否是撤销部分成交单，如果是部分成交单就用用户2市场价吃到一部分单
            if "taker_order_parameter" in list(value.keys()):
                user2_order = order_request.create(parm=value["taker_order_parameter"], test_user='test_user2')
            # 撤销订单
            res_cancel = order_request.cancel(order_id=order_id)
            logger.info(f'撤销单个订单接口正向用例--->{case_name}-->参数为{order_id}--->返回结果{res_cancel}')
            # 比对接口返回数据
            assert res_cancel["msgInfo"] == expected_result["msgInfo"]
            # mongo查询数据
            time.sleep(2)
            mongo_res = order_request.mongo.find_one({"_id": order_id})
            # 比对mongo的状态码
            assert mongo_res["state"] == expected_result["state"]

    # 撤销单个订单的反向用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("cancel_failed") == {} else [test_data])
    def test_cancel_failed(self, test_data):
        order_request = self.order_request
        cases_data = test_data["cancel_failed"]
        order_request.mongo.update_col("order")
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            # 如果是状态码，去mongo查询该状态下的任一订单号
            if "state" in list(parameter.keys()):
                mongo_res = order_request.mongo.find_one({"state": parameter["state"]})
                order_id = mongo_res["_id"]
            else:
                order_id = parameter["order_id"]
            # 将查询到的订单号传入发起请求获取接口返回数据
            res = order_request.cancel(order_id=order_id)
            logger.info(f'撤销单个订单反向用例--->{case_name}-->参数为{order_id}--->返回结果{res}')
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]

    # 撤销所有订单的接口正向测试用例，详情见数据文件的注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_create_batch_success")=={} else [test_data])
    def test_create_batch_success(self,test_data):
        order_request = self.order_request
        cases_data = test_data["test_create_batch_success"]
        order_request.mongo.update_col("order")
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            # 组装批量下单的的参数，将动态获取的指数价格组装仅批量下单参数
            order_parameter = value["order_parameter"]
            order_list = str(order_parameter["list"])
            order_parameter["list"] = order_list.replace("dao_price", str(self.index_price)).replace(
                "xrp_price", str(self.xrp_index_price))
            # 前置处理：限价批量下单，dao、xrp各下一个单
            res_create_batch = order_request.create_batch(parm=order_parameter)
            logger.info(f'撤销所有订单接口前置处理下单--->{case_name}-->参数为{order_parameter}--->返回结果{res_create_batch}')
            # 传入参数访问接口获取数据
            res = order_request.cancel_all(parm=parameter)
            logger.info(f'撤销所有订单正向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            assert res["msgInfo"] == expected_result["msgInfo"]
            query = {"accountId": get_account_info().response["result"]["accountId"], "state": {"$in": [1, 2]}}
            # 根据参数判断是撤销单个交易对订单还是撤销所有交易对订单
            if parameter:
                query["symbol"] = self.order_request.get_symbolid(parameter["symbol"])
            mongo_res = order_request.mongo.find_one(query)
            assert not mongo_res

    # 撤销所有订单接口的反向测试用例
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_create_batch_failed") == {} else [test_data])
    def test_create_batch_failed(self,test_data):
        order_request = self.order_request
        cases_data = test_data["test_create_batch_failed"]
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            # 访问接口，获取接口返回数据
            res = order_request.cancel_all(parm=parameter)
            logger.info(f'撤销所有订单反向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_cancel_order.py'])

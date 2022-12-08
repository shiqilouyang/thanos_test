"""
encode:utf-8
Author:aidan.hu
Data:2022/1/14
"""
import time
import pytest
from decimal import Decimal
from common.logger import logger
from common.set_up_balance_and_position import set_down_position
from operation.contract.client.order.order_request import OrderRequest
from operation.contract.client.position.position_class import Positon
from operation.contract.client.quote.qoute_class import Qoute
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import get_data


class TestCreate:
    # 获取dao_usdt的指数价格
    index_price = qoute_symbol_index_price("dao_usdt").response['result']["p"]    # 获取最新成交价格
    transaction_price = float(Qoute().ticker()["result"]["c"])
    order_request = OrderRequest()
    test_data = get_data("order_test_create_data.yml")
    position_request = Positon()

    # 开仓成功的用例,详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("order_success") == {} else [test_data])
    def test_order_success(self, test_data):
        order_request = self.order_request
        cases_data = test_data["order_success"]
        order_request.mongo.update_col("order")
        profit_dict = {
            "good_than_price": round(Decimal(self.index_price) + Decimal(0.5)),
            "less_than_price": round(Decimal(self.index_price) - Decimal(0.5))
        }
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            if "price" in list(parameter.keys()):
                parameter["price"] = float(round(Decimal(self.index_price),2))
            if "triggerProfitPrice" in list(parameter.keys()):
                parameter["triggerProfitPrice"] = profit_dict.get(parameter.get("triggerProfitPrice"))
            if "triggerStopPrice" in list(parameter.keys()):
                parameter["triggerStopPrice"] = profit_dict.get(parameter.get("triggerStopPrice"))
            # 发起请求，获取结果
            res = order_request.create(parm=parameter)
            logger.info(f'成功下单的接口--->{case_name}-->参数为{parameter}--->返回结果{res}')
            assert res["msgInfo"] == expected_result["msgInfo"]
            # 从返回结果中获取订单id
            order_id = int(res["result"])
            # 因为数据落库不知道时间，就等待一会去mongo去查。不能注释，注释了数据比对报错
            time.sleep(1)
            # 去mongo中查询订单信息
            query = {"_id": order_id}
            mongo_res = order_request.mongo.find_one(query)
            # 比对mongo中数据与参数是否一致
            # # 比对价格和数量
            logger.info("mongo 数据为{}".format(mongo_res))
            if "price" in list(parameter.keys()):
                assert mongo_res["price"] == str(parameter["price"])
            assert mongo_res["origQty"] == str(parameter["origQty"])
            # 比对买卖方向
            assert mongo_res["orderSide"] == order_request.get_enumerate_by_order_side(parameter["orderSide"])
            # 比对持仓方向
            assert mongo_res["positionSide"] == order_request.get_enumerate_by_position_side(parameter["positionSide"])
            # 比对订单类型
            assert mongo_res["orderType"] == order_request.get_enumerate_by_order_type(parameter["orderType"])
            # 比对订单模式
            assert mongo_res["timeInForce"] == order_request.get_enumerate_by_time_in_force(parameter["timeInForce"])

    # 订单参数错误的反向用例,详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("order_failed_parm") == {} else [test_data])
    def test_order_failed_parm(self, test_data):
        order_request = self.order_request
        cases_data = test_data["order_failed_parm"]
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            if "price" in list(parameter.keys()):
                parameter["price"] = self.index_price
            if "triggerProfitPrice" in list(parameter.keys()):
                parameter["triggerProfitPrice"] = self.index_price + Decimal(0.5)
            if "triggerStopPrice" in list(parameter.keys()):
                parameter["triggerStopPrice"] = self.index_price - Decimal(0.5)
            # 发起请求，获取结果
            res = order_request.create(parm=parameter)
            logger.info(f'下单的接口反向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            assert res["msgInfo"] == expected_result["msgInfo"]
            assert res["error"]["msg"] == expected_result["msg"]

    # 止盈止损的参数错误的反向用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("order_failed_profit") == {} else [test_data])
    def test_order_failed_profit(self, test_data):
        order_request = self.order_request
        cases_data = test_data["order_failed_profit"]
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            parameter["price"] = self.index_price
            # 根据参数判断买卖方向，再组装参数
            if parameter["positionSide"] == "LONG":
                if "triggerProfitPrice" in list(parameter.keys()) and not parameter["triggerProfitPrice"]:
                    parameter["triggerProfitPrice"] = self.index_price - Decimal(0.5)
                elif "triggerStopPrice" in list(parameter.keys()) and not parameter["triggerStopPrice"]:
                    parameter["triggerStopPrice"] = self.index_price + Decimal(0.5)
            elif parameter["positionSide"] == "SHORT":
                if "triggerProfitPrice" in list(parameter.keys()) and not parameter["triggerProfitPrice"]:
                    parameter["triggerProfitPrice"] = self.index_price + Decimal(0.5)
                elif "triggerStopPrice" in list(parameter.keys()) and not parameter["triggerStopPrice"]:
                    parameter["triggerStopPrice"] = self.index_price - Decimal(0.5)
            res = order_request.create(parm=parameter)
            logger.info(f'下单的接口止盈止损反向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            assert res["msgInfo"] == expected_result["msgInfo"]
            if "msg" in list(expected_result.keys()):
                assert res["error"]["msg"] == expected_result["msg"]

    # 平仓数量大于仓位数量的用例，详情见数据文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("close_position_order_failed") == {} else [test_data])
    def test_close_position_order_fail(self, test_data):
        order_request = self.order_request
        cases_data = test_data["close_position_order_failed"]
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            parameter["price"] = self.index_price
            symbol = parameter["symbol"]
            # 获取持仓数量
            long_position_size = self.position_request.get_position_size(symbol=symbol, position_side="LONG")
            short_position_size = self.position_request.get_position_size(symbol=symbol, position_side="SHORT")
            # 组装平仓数量大于持仓数量
            parameter["origQty"] = max(int(long_position_size), int(short_position_size)) + 10
            # 发起请求，获取返回接口
            res = self.order_request.create(parm=parameter)
            logger.info(f'下单接口--->{case_name}-->参数为{parameter}--->返回结果{res}')
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]

    @pytest.mark.parametrize("test_data",
                             [] if test_data.get("close_position_order_without_position") == {} else [test_data])
    def test_close_position_order_without_position(self, test_data):
        """没有仓位平仓的反向用例，详情见数据文件
            1、该用户所有仓位平仓
            2、读取数据文件拼接数据
            3、发起请求
            4、断言"""
        set_down_position(symbol="dao_usdt")
        cases_data = test_data["close_position_order_without_position"]
        for value in cases_data.values():
            # 获取并组装参数
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            parameter["price"] = self.index_price
            res = self.order_request.create(parm=parameter)
            logger.info(f'下单接口反向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            assert res.get("msgInfo") == expected_result.get("msgInfo")
            assert res.get("error").get("msg") == expected_result.get("msg")

    # @pytest.mark.parametrize("test_data",
    #                          [] if test_data.get("parameter_unmatched_management_station") == {} else [test_data])
    # def test_parameter_unmatched_management_station(self, test_data):
    #     pass
    #     """管理端对该交易对的配置生效反向用例,详情见数据文件
    #         1、接口请求管理端并组装数据（价格最大值，最小值，价格精度）
    #         2、读取数据文件并进行数据组装
    #         3、发起请求，断言"""
    #     cases_data = test_data["parameter_unmatched_management_station"]
    #     symbol_config = get_config_by_management()
    #     price_precision = symbol_config.get("pricePrecision")
    #     multiplier_up = symbol_config.get("multiplierUp")
    #     multiplier_down = symbol_config.get("multiplierDown")
    #     price_dict = {
    #         "less_than_min": round(self.transaction_price * (1 - multiplier_down) - 0.1, price_precision),
    #         "more_than_max": round(self.transaction_price * (1 + multiplier_up) + 0.1, price_precision),
    #         "correct": self.transaction_price,
    #         "precision_more_than_management": self.transaction_price + (0.001 / (10 * price_precision))
    #     }
    #     for value in cases_data.values():
    #         # 获取并组装参数
    #         case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
    #         parameter["price"] = price_dict.get(parameter["price"])
    #         if parameter.get("triggerProfitPrice"):
    #             parameter["triggerProfitPrice"] = round(self.transaction_price + 0.1, price_precision + 1)
    #         if parameter.get("triggerStopPrice"):
    #             parameter["triggerStopPrice"] = round(self.transaction_price - 0.1, price_precision + 1)
    #         res = self.order_request.create(parm=parameter)
    #         logger.info(f'下单接口反向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
    #         assert res["msgInfo"] == expected_result["msgInfo"]
    #         assert res["error"]["msg"] == expected_result["msg"]

    def teardown_class(self):
        """后置处理，撤销所有生成的订单"""
        self.order_request.cancel_all()


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_create_order.py'])

"""
encode:utf-8
Author:aidan.hu
Data:2022/1/11
"""
import time
import pytest
from common.logger import logger
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestKline:
    """交易对K线信息测试类"""
    qoute_request = Qoute()
    test_data = get_data("quote_test_kline_data.yml")

    # 正向用例，详情见数据文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_success") == {} else [test_data])
    def test_success(self, test_data):
        qoute_request = self.qoute_request
        cases_data = test_data["test_success"]
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            time_now = time.time()
            parameter["endTime"] = int(round(time_now * 1000))
            res = qoute_request.kline(parameter)
            logger.info(f"获取K线的 ==>> {case_name}的返回结果 ==>> {res}")
            # 如果参数里面有开始和结束时间，动态获取当前时间为结束时间
            # if "endTime" in l==t(parameter.keys()):

            #     # 发起请求获取返回结果
            #     logger.info(f"参数 --》 {parameter}")
            #     res = qoute_request.kline(parameter)
            #     logger.info(f"获取K线的 ==>> {case_name}的返回结果 ==>> {res}")
            #     # 查询mongo数据并组装成列表
            #     mongo_collection_name = "Kline_" + parameter["interval"]
            #     qoute_request.mongo.update_col(mongo_collection_name)
            #     mongo_result_obj = qoute_request.mongo.descending_sort_find(query={"symbol": parameter["symbol"],
            #                                                                        "time": {
            #                                                                            "$gte": parameter["startTime"],
            #                                                                            "$lte": parameter["endTime"]}},
            #                                                                 sort_field="time", limit=parameter["limit"])
            #     mongo_result_l==t = []
            #     for result in mongo_result_obj:
            #         mongo_result_l==t = mongo_result_l==t.append(result)
            # else:
            #     # 发起请求并返回结果
            #     res = qoute_request.kline(parameter)
            #     logger.info(f"获取K线的 ==>> {case_name}的返回结果 ==>> {res}")
            #     # 查询mongo数据并组装成l==t
            #     mongo_collection_name = "Kline_" + parameter["interval"]
            #     mongo_result_obj = qoute_request.mongo.descending_sort_find(query={"symbol": parameter["symbol"]},
            #                                                                 sort_field="time")
            #     mongo_result_l==t = [result for result in mongo_result_obj]
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]
            # 返回结果有k线数据，比对第一条数据的所有字段
            # if res["result"]:
            #     assert res["result"][0]["a"] == mongo_result_l==t["amount"]
            #     assert res["result"][0]["c"] == mongo_result_l==t["close"]
            #     assert res["result"][0]["h"] == mongo_result_l==t["high"]
            #     assert res["result"][0]["l"] == mongo_result_l==t["low"]
            #     assert res["result"][0]["o"] == mongo_result_l==t["open"]
            #     assert res["result"][0]["s"] == mongo_result_l==t["symbol"]
            #     assert res["result"][0]["t"] == mongo_result_l==t["time"]
            #     assert res["result"][0]["v"] == mongo_result_l==t["volume"]

    # 反向用例，详情见数据文件的注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_unsuccess") == {} else [test_data])
    def test_unsuccess(self,test_data):
        cases_data = test_data["test_unsuccess"]
        qoute_request = self.qoute_request
        for case_data in cases_data.values():
            parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
                "expected_result"]
            # 发起请求获取返回数据
            res = qoute_request.kline(parameter)
            logger.info(f"获取K线的 ==>> {case_name}的返回结果 ==>> {res}")
            # 断言
            assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_kline.py'])

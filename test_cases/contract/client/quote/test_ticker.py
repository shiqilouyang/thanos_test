"""
encode:utf-8
Author:aidan.hu
Data:2022/1/12
"""
import time

import pytest

from common.common_util import get_timestamp_now, before_timestamp_by_day
from common.logger import logger
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestTicker:
    """查询指定交易对的行情信息和全交易对的行情信息测试类"""
    qoute_request = Qoute()
    test_data = get_data("quote_ticker_data.yml")

    # 正确获取指定行情交易对信息
    @pytest.mark.parametrize("test_data", [] if test_data.get("ticker").get('test_success') is None  else [test_data])
    def test_ticker_success(self,test_data):
        qoute_request = self.qoute_request
        case_data = test_data["ticker"]["test_success"]
        parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
            "expected_result"]
        res = qoute_request.ticker(param=parameter)
        logger.info(f"获取指定交易对的行情信息接口 ==>> {case_name}的返回结果 ==>> {res}")
        # 获取当前时间戳和24小时前的时间戳
        now_timestamp, timestamp_before_24h = get_timestamp_now(), before_timestamp_by_day(1)
        # 通过mongodb查询之前24小时的最新价格、最低价格、第一笔成交的价格
        mongo_result = {}
        qoute_request.mongo.update_col("trade")
        symbol_id = qoute_request.get_symbolid(parameter["symbol"])
        query = {"symbolId": symbol_id, "timestamp": {"$gt": timestamp_before_24h, "$lt": now_timestamp}}
        # 查询最近价格
        find_result = qoute_request.mongo.descending_sort_find(query=query, sort_field="timestamp", limit=1)
        for value in find_result:
            mongo_result["c"] = value.get("price")
        # 查询最低价格
        find_result = qoute_request.mongo.ascending_sort_find(query=query, sort_field="price", limit=1)
        for value in find_result:
            mongo_result["l"] = value.get("price")
        # 查询最高价格
        find_result = qoute_request.mongo.descending_sort_find(query=query, sort_field="price", limit=1)
        for value in find_result:
            mongo_result["h"] = value.get("price")
        assert res["msgInfo"] == expected_result["msgInfo"]
        # assert res["result"]["c"] == mongo_result["c"]
        assert float(res["result"]["l"]) == float(mongo_result["l"])
        assert float(res["result"]["h"]) == float(mongo_result["h"])

    # 获取指定交易对的反向用例
    @pytest.mark.parametrize("test_data", [] if test_data.get("ticker").get('test_unsuccess') is None else [test_data])
    def test_ticker_unsuccess(self,test_data):
        qoute_request = self.qoute_request
        case_data = test_data["ticker"]["test_unsuccess"]
        parameter, case_name, expected_result = case_data["parameter"], case_data["name"], case_data[
            "expected_result"]
        res = qoute_request.ticker(param=parameter)
        logger.info(f"获取指定交易对的行情信息接口 ==>> {case_name}的返回结果 ==>> {res}")

    # 获取全交易对的行情信息
    @pytest.mark.parametrize("test_data", [] if test_data.get("tickers") == {} else [test_data])
    def test_tickers(self,test_data):
        qoute_request = self.qoute_request
        case_data = test_data["tickers"]["tickers_success"]
        case_name, expected_result = case_data["name"], case_data["expected_result"]
        res = qoute_request.tickers()
        logger.info(f"获取全交易对的行情信息接口 ==>> {case_name}的返回结果 ==>> {res}")
        assert res["msgInfo"] == expected_result["msgInfo"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_ticker.py'])

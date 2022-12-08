"""
encode:utf-8
Author:aidan.hu
Data:2022/1/6
"""
import time

import requests

from api.thanos_http import xtthanos_market_http
from common.common_util import CommonUtil
from common.get_signature import generate_auth_info
from common.logger import logger
from test_cases.contract.client.conftest import  request_data


class Qoute(CommonUtil):
    """行情类接口封装,供其他地方调用，不需要URL和请求方式，只需要参数即可，不输入参数时根据默认参数请求"""
    request_data = request_data

    # 获取交易对的最新成交信息接口请求
    def deal(self, param=None,test_user='test_user'):
        if not param:
            param = {"num": 1, "symbol": "dao_usdt"}
        path, method = self.request_data["deal"]["route"] + self.request_data["deal"]["path"], \
                       self.request_data["deal"]["method"]
        header = generate_auth_info(path=path, method=method, params=param, test_user=test_user)
        res = xtthanos_market_http.deal(headers=header, params=param)
        logger.info('获取交易对的最新成交信息接口响应{}'.format(res.json()))
        return res.json()

    # 获取交易对的深度信息接口请求
    def depth(self, param=None, test_user='test_user'):
        if not param:
            param = {"level": 5, "symbol": "dao_usdt"}
        path, method = self.request_data["depth"]["route"] + self.request_data["depth"]["path"], \
                       self.request_data["depth"]["method"]
        header = generate_auth_info(path=path, method=method, params=param, test_user=test_user)
        res = xtthanos_market_http.depth(headers=header, params=param)
        logger.info('获取交易对的深度信息接口响应{}'.format(res.json()))
        return res.json()

    # 获取资金费率接口请求
    def funding_rate(self, param=None, test_user='test_user'):
        if not param:
            param = {"symbol": "dao_usdt"}
        path, method = self.request_data["funding_rate"]["route"] + self.request_data["funding_rate"]["path"], \
                       self.request_data["funding_rate"]["method"]
        header = generate_auth_info(path=path, method=method, params=param, test_user=test_user)
        res = xtthanos_market_http.funding_rate(headers=header, params=param)
        logger.info('获取资金费率接口请求响应{}'.format(res.json()))
        return res.json()

    # 正确获取资金费率记录
    def funding_rate_record(self, param=None, test_user="test_user"):
        if not param:
            param = {"symbol": "dao_usdt", "page": 1, "size": 10}
        path, method = self.request_data["funding_rate_record"]["route"] + self.request_data["funding_rate_record"]["path"], \
                       self.request_data["funding_rate_record"]["method"]
        header = generate_auth_info(path=path, method=method, params=param, test_user=test_user)
        res = xtthanos_market_http.funding_rate_record(headers=header, params=param)
        logger.info('获取资金费率记录接口响应{}'.format(res.json()))
        return res.json()


    # 获取交易对的K线信息接口请求
    def kline(self, param=None, test_user="test_user"):
        if not param:
            param = {"symbol": "dao_usdt", "interval": "1h", "limit": 10}
        path, method = self.request_data["kline"]["route"] + self.request_data["kline"]["path"], \
                       self.request_data["kline"]["method"]
        header = generate_auth_info(path=path, method=method, params=param, test_user=test_user)
        res = xtthanos_market_http.kline(headers=header, params=param)
        logger.info('获取交易对的K线信息接口响应{}'.format(res.json()))
        return res.json()

    # 获取单个交易对的标记价格
    def mark_price(self, param=None, test_user="test_user"):
        if not param:
            param = {"symbol": "dao_usdt"}
        path, method = self.request_data["mark_price"]["route"] + self.request_data["mark_price"]["path"], \
                       self.request_data["mark_price"]["method"]
        header = generate_auth_info(path=path, method=method, params=param, test_user=test_user)
        res = xtthanos_market_http.mark_price(headers=header, params=param)
        logger.info('获取交易对的标记价格接口响应{}'.format(res.json()))
        return res.json()

    # 获取交易对的行情信息接口请求
    def ticker(self, param=None,  test_user="test_user"):
        if not param:
            param = {"symbol": "dao_usdt"}
        path, method = self.request_data["ticker"]["route"] + self.request_data["ticker"]["path"], \
                       self.request_data["ticker"]["method"]
        header = generate_auth_info(path=path, method=method, params=param, test_user=test_user)
        res = xtthanos_market_http.ticker(headers=header, params=param)
        logger.info('获取交易对的标记价格接口响应{}'.format(res.json()))
        return res.json()


    # 获取全交易对的行情信息接口请求
    def tickers(self, headers=None):
        mark_price_data = self.requests_data["tickers"]
        url, method = self.thanos_http_url + mark_price_data["path"], mark_price_data["method"]
        if headers:
            header = self.header_token.update(headers)
            return requests.request(url=url, method=method, headers=header).json()
        else:
            return requests.request(url=url, method=method, headers=self.header_token).json()


if __name__ == '__main__':
    qoute = Qoute()
    print(qoute.mark_price()["result"]["p"])

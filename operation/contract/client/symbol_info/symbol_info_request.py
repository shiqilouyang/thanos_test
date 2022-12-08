"""
encode:utf-8
Author:aidan.hu
Data:2022/1/6
"""
import requests

from common.common_util import CommonUtil
from test_cases.contract.client.conftest import get_data


class SymbolInfoRequests(CommonUtil):
    """获取交易对配置信息的各个接口的封装"""

    data = get_data("symbol_info_request_data.yml")

    # 获取交易对币种
    def coins(self, **kwargs):
        coins_data = self.data["coins"]
        url, method = self.thanos_http_url + coins_data["path"], coins_data["method"]
        res = requests.request(url=url, method=method, **kwargs).json()
        return res

    # 获取单个币种
    def detail(self, symbol="dao_usdt", **kwargs):
        detail_data = self.data["detail"]
        url, param = self.thanos_http_url + detail_data["path"], {"symbol": symbol}
        res = requests.get(url=url, params=param, **kwargs).json()
        return res

    # 获取所有交易对
    def list(self, **kwargs):
        list_data = self.data["list"]
        url, method = self.thanos_http_url + list_data["path"], list_data["method"]
        res = requests.request(method=method, url=url, **kwargs).json()
        return res


if __name__ == '__main__':
    sq = SymbolInfoRequests()
    coin_list = sq.list()
    print(coin_list["result"])

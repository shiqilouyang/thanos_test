"""
encode:utf-8
Author:aidan.hu
Data:2022/1/6
"""

import json
from functools import lru_cache

import requests

demain_name = "http://thanos-admin-web-test.xtthanos.com"


# 1、隐藏交易对
def conceal_symbol_dao():
    url = demain_name + "/api/v1/admin/symbol/39/off"
    method = "POST"
    res = requests.request(url=url, method=method).json()
    return res


# 2、修改配置
def update_symbol_dao():
    url = demain_name + "/api/v1/admin/symbol/39"
    header = {"Content-Type": "application/json"}
    data = {"cnName": "合约名称中文", "contractSize": 0.1, "enName": "合约名称英文", "initLeverage": 20, "liquidationFee": 0.0075,
            "makerFee": 0.1, "maxMultiple": "", "maxOpenOrders": 1000, "minQty": 2, "minStepPrice": 0.002,
            "multiplierDown": 0.3, "multiplierUp": 0.2, "pricePrecision": 4, "quantityPrecision": 8,
            "supportPositionType": "2", "symbol": "dao_usdt", "symbolGroupId": 2, "takerFee": 0.2, "baseCoin": "dao",
            "quoteCoin": "usdt", "baseCoinPrecision": 4, "quoteCoinPrecision": 5,
            "chLabels": [{"label": "中文标签1"}, {"label": "中文标签2"}, {"label": "中文标签3"}, {"label": "中文标签4"}],
            "enLabels": [{"label": "英文标签1"}, {"label": "英文标签2"}, {"label": " 英文标签3"}], "riskMarginAccountId": 2,
            "marketTakeBound": 0.001, "priceDeviation": 0.02, "maxEntrusts": "100",
            "onboardDate": "2021-11-26T18:16:28.000Z", "makeIds": None, "depthPrecisionMerge": 6}
    request_data = json.dumps(data)
    res = requests.put(url=url, data=request_data, headers=header).json()
    return res


# 3、修改风险限额
def config_dao_leverage_bracket():
    url = demain_name + "/api/v1/admin/symbol/39/leverage-bracket"
    data = {"bracket": 1, "startMarginRate": 0.1, "maintMarginRate": 0.05, "maxLeverage": 20,
            "maxNominalValue": 3000000}
    res = requests.post(url=url, data=data)
    return res


# 4、开启交易
def trade_on_dao():
    url = demain_name + "/api/v1/admin/symbol/39/trade-on"
    res = requests.post(url=url).json()
    return res

@lru_cache
def get_config_by_management(symbol="dao_usdt"):
    """根据交易对获取管理端的该币种配置"""
    url = demain_name + "/api/v1/admin/symbol/list"
    parm = {"symbol": symbol}
    res = requests.request(method="get", url=url, params=parm).json()
    return res.get("result").get("items")[0]


if __name__ == '__main__':
    trade_on_dao()

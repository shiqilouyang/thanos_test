#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
from api.http_api import http_api
from common.read_data import get_data
import requests

thanos_admin_http_url = get_data().get_ini_data("host","thanos_admin_http_url")

class thanos_admin_http(http_api):

    def __init__(self,thanos_admin_http_url, **kwargs):
        super().__init__(thanos_admin_http_url, **kwargs)
        # super(binance_http, self.__init__(binance_http_url, **kwargs)

    # 动态条件查询列表
    def query_order_list(self, **kwargs):
        return self.get("/api/v1/admin/order/list", **kwargs)

    # 撤销
    def cancel_orderId(self, orderId, **kwargs):
        return self.post(f"/api/v1/admin/order/{orderId}/cancel", **kwargs)

    # 合约配置-查询
    def query_symbols_info(self, **kwargs):
        return self.get("/api/v1/admin/symbol", **kwargs)



xtthanos_admin_http = thanos_admin_http(thanos_admin_http_url)
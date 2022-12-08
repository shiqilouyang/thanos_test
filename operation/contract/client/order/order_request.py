"""
encode:utf-8
Author:aidan.hu
Data:2022/1/12
"""
import requests

from api.thanos_http import xtthanos_trade_http, logger
from common.common_util import CommonUtil
from common.get_signature import generate_auth_info
from operation.contract.client.account.get_account_info import get_account_info
from test_cases.contract.client.conftest import get_data, request_data


class OrderRequest(CommonUtil):
    """订单类，封装订单模块的请求，不用输入请求方式和url,可直接调用方法用默认值发送请求，也可以通过参数自定义请求数据
    也可以通过传入不同的header使用指定账户发送请求"""
    request_data = request_data
    account_id = get_account_info().response.get("result").get("accountId")

    # 撤销订单，必须传入订单Id
    def cancel(self, order_id, test_user='test_user'):
        parm = {"orderId": order_id}
        path, method = self.request_data["cancel"]["route"] +self.request_data["cancel"]["path"], self.request_data["create"]["method"]
        header = generate_auth_info(path=path, method=method,params=parm,test_user=test_user)
        res = xtthanos_trade_http.cancel(headers=header, params=parm)
        logger.info('撤销订单，必须传入id响应为{}'.format(res.json()))
        return res.json()


    # 撤销所有订单,默认撤销所有订单，也可通过传参撤销指定交易对的订单。
    def cancel_all(self, parm=None, header=None):
        path, method = self.request_data["cancel_all"]["path"], self.request_data["cancel_all"]["method"]
        if not header:
            header = generate_auth_info(path=path, method=method)
        url = self.thanos_http_url + path
        if parm:
            res = requests.request(method=method, url=url, data=parm, headers=header).json()
            return res
        res = requests.request(method=method, url=url, headers=header).json()
        return res

    # 下单,默认下买多市价单,也可以通过传参下自定义订单
    def create(self, parm=None,test_user='test_user'):
        if not parm:
            parm = {
                'orderSide': 'BUY',
                'orderType': 'MARKET',
                'origQty': '20',
                'positionSide': 'LONG',
                'symbol': 'dao_usdt',
            }
        path, method = self.request_data["create"]["route"] +self.request_data["create"]["path"], self.request_data["create"]["method"]
        header = generate_auth_info(path=path, method=method,params=parm,test_user=test_user)
        res = xtthanos_trade_http.create(headers=header, params=parm)
        logger.info('下单接口响应为{}'.format(res.json()))
        return res.json()

    # 批量下单,默认下两个dao_usdt市价单
    def create_batch(self, parm=None,test_user='test_user'):
        if not parm:
            parm = {
                'list': '[{orderSide: BUY, orderType: MARKET, origQty: 40, positionSide: LONG, symbol: dao_usdt, timeInForce: GTC},\
                 {orderSide: BUY, orderType: MARKET, origQty: 40, positionSide: LONG, symbol: dao_usdt,timeInForce: GTC}]'
            }
        path, method = self.request_data["create_batch"]["route"] +self.request_data["create_batch"]["path"], self.request_data["create_batch"]["method"]
        header = generate_auth_info(path=path, method=method,params=parm,test_user=test_user)
        res = xtthanos_trade_http.create_batch(headers=header, params=parm)
        logger.info('批量下单接口响应为{}'.format(res.json()))
        return res.json()

    # 根据id查询订单,必须传入订单id
    def detail(self, order_id, test_user='test_user'):
        path, method = self.request_data["detail"]["route"] +self.request_data["detail"]["path"], self.request_data["detail"]["method"]
        parm = {"orderId": order_id}
        header = generate_auth_info(path=path, method=method,params=parm,test_user=test_user)
        res = xtthanos_trade_http.detail(headers=header, params=parm)
        logger.info('根据id查询订单响应为{}'.format(res.json()))
        return res.json()

    # 查询订单，默认查询所有币种的新建订单
    def list(self, parm=None, test_user='test_user'):
        path, method = self.request_data["list"]["route"] + self.request_data["list"]["path"], \
                       self.request_data["list"]["method"]
        if parm is not None:
            parm={"state": "NEW"}
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.list(headers=header, params=parm)
        logger.info('根据id查询订单响应为{}'.format(res.json()))
        return res.json()

    # 查询交易明细，参数为字典，字典里面必须有orderId，page和size选填
    def trade_list(self, parm, test_user='test_user'):
        path, method = self.request_data["trade_list"]["route"] + self.request_data["trade_list"]["path"], self.request_data["trade_list"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.trade_list(headers=header, params=parm)
        logger.info('根据id查询订单响应为{}'.format(res.json()))
        return res.json()

    # 查询历史订单，必须传入参数parm,parm为一个字典，键有direction、id、limit
    def list_history(self, parm, header=None):
        path, method = self.request_data["list_history"]["path"], self.request_data["list_history"]["method"]
        if not header:
            header = generate_auth_info(path=path, method=method)
        url = self.thanos_http_url + path
        res = requests.request(method=method, url=url, params=parm, headers=header).json()
        return res

    # 根据买卖方向返回订单的枚举值
    @staticmethod
    def get_enumerate_by_order_side(order_side: str):
        if order_side == "BUY":
            return 1
        elif order_side == "SELL":
            return 2

    @staticmethod
    def get_enumerate_by_position_side(positon_side: str):
        if positon_side == "LONG":
            return 1
        elif positon_side == "SHORT":
            return 2

    @staticmethod
    def get_enumerate_by_time_in_force(time_in_force: str):
        if time_in_force == "GTC":
            return 1
        elif time_in_force == "FOK":
            return 2
        elif time_in_force == "IOC":
            return 3
        elif time_in_force == "GTX":
            return 4

    @staticmethod
    def get_enumerate_by_order_type(order_type: str):
        if order_type == "LIMIT":
            return 1
        elif order_type == "MARKET":
            return 2

    @staticmethod
    def get_enumerate_by_state(state: str):
        if state == "NEW":
            return 1
        elif state == "PARTIALLY_FILLED":
            return 2
        elif state == "FILLED":
            return 3
        elif state == "CANCELED":
            return 4
        elif state == "REJECTED":
            return 5
        elif state == "EXPIRED":
            return 6


if __name__ == '__main__':
    order_request = OrderRequest()
    order_request.create()
    # res = order_request.list()
    # print(order_request.list())
    # data = get_data("order_test_create_batch_data.yml")
    # print(data["case"])
    # OrderRequest

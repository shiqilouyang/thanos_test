"""
encode:utf-8
Author:aidan.hu
Data:2022/1/20
"""
import requests
from jsonpath import jsonpath

from api.thanos_http import xtthanos_trade_http, logger
from common.common_util import CommonUtil
from common.get_signature import generate_auth_info
from common.set_up_balance_and_position import set_up_position
from operation.contract.client.position.position_class import Positon
from operation.contract.client.quote.qoute_symbol_index_price import qoute_symbol_index_price
from test_cases.contract.client.conftest import request_data


class PlanRequest(CommonUtil):
    """计划委托和止盈止损请求类的封装，用户调用该类的方法向结果发送请求，不用输入url和请求方式,不传参数时有默认值"""
    request_data = request_data
    index_price = qoute_symbol_index_price('dao_usdt').response['result']["p"]

    # 撤销所有计划委托
    def cancel_all_plan(self,test_user='test_user'):
        path, method = self.request_data["cancel_all_plan"]["route"] + self.request_data["cancel_all_plan"]["path"], \
                       self.request_data["cancel_all_plan"]["method"]
        header = generate_auth_info(path=path, method=method, params={}, test_user=test_user)
        res = xtthanos_trade_http.cancel_all_plan(headers=header)
        logger.info('创建计划委托响应为{}'.format(res.json()))
        return res.json()

    # 撤销所有止盈止损
    def cancel_all_profit_stop(self, parm=None,test_user='test_user'):
        path, method = self.request_data["cancel_all_profit_stop"]["route"] + self.request_data["cancel_all_profit_stop"]["path"], \
                       self.request_data["cancel_all_profit_stop"]["method"]
        header = generate_auth_info(path=path, method=method, params={}, test_user=test_user)
        res = xtthanos_trade_http.cancel_all_profit_stop(headers=header)
        logger.info('撤销所有止盈止损为{}'.format(res.json()))
        return res.json()


    # 撤销计划委托,必须传委托id
    def cancel_plan(self, entrust_id, test_user='test_user'):
        parm = {"entrustId": entrust_id}
        path, method = self.request_data["cancel_plan"]["route"] + self.request_data["cancel_plan"]["path"], \
                       self.request_data["cancel_plan"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.cancel_plan(headers=header, params=parm)
        logger.info('撤销计划委托响应为{}'.format(res.json()))
        return res.json()

    # 撤销止盈止损,必须传委托id
    def cancel_profit_stop(self, profit_id, test_user="test_user"):
        parm = {"profitId": profit_id}
        path, method = self.request_data["cancel_profit_stop"]["route"] + self.request_data["cancel_profit_stop"]["path"], \
                       self.request_data["cancel_profit_stop"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.cancel_profit_stop(headers=header, params=parm)
        logger.info('撤销止盈止损为{}'.format(res.json()))
        return res.json()

    # 创建计划委托,可以自己传参数，默认下dao_usdt的买多计划单，价格是当前价格的指数价格加4
    def create_plan(self, parm=None, test_user="test_user"):
        if not parm:
            parm = {'entrustType': 'STOP', 'orderSide': 'BUY', 'origQty': '6',
                    'positionSide': 'LONG', 'symbol': 'ada_usdt', 'timeInForce': 'GTC',
                    'triggerPriceType': 'INDEX_PRICE', 'price': self.index_price + 4, 'stopPrice': self.index_price + 4}

        path, method = self.request_data["create_plan"]["route"] + self.request_data["create_plan"]["path"], \
                       self.request_data["create_plan"]["method"]
        header = generate_auth_info(path=path, method=method,params=parm,test_user=test_user)
        res = xtthanos_trade_http.create_plan(headers=header, params=parm)
        logger.info('创建计划委托响应为{}'.format(res.json()))
        return res.json()

    # 创建止盈止损,可以自己传参数，默认下dao_usdt的买多计划单，价格是当前价格的指数价格加4
    def create_profit(self, parm=None, test_user="test_user"):
        if not parm:
            parm = {'origQty': '10', 'positionSide': 'LONG',
                    'symbol': 'dot_usdt', 'triggerProfitPrice': self.index_price + 0.6,
                    'triggerStopPrice': self.index_price - 0.6, 'orderSide': 'SELL'}

        path, method = self.request_data["create_profit"]["route"] + self.request_data["create_profit"]["path"], \
                       self.request_data["create_profit"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.create_profit(headers=header, params=parm)
        logger.info('创建止盈止损,可以自己传参数响应为{}'.format(res.json()))
        return res.json()

    # 根据id查询计划委托,必须传达计划委托id
    def plan_detail(self, entrust_id, test_user="test_user"):
        parm = {'entrustId': entrust_id}
        path, method = self.request_data["plan_detail"]["route"] + self.request_data["plan_detail"][
            "path"], \
                       self.request_data["plan_detail"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.plan_detail(headers=header, params=parm)
        logger.info('撤销止盈止损为{}'.format(res.json()))
        return res.json()

    # 查询计划委托,默认查询新建的计划委托
    def plan_list(self, parm=None, header=None):
        if not parm:
            parm = {"state": "NOT_TRIGGERED"}
        if not header:
            header = self.header_token
        request_data = self.data["plan-list"]
        url, method = self.thanos_http_url + request_data["path"], request_data["method"]
        return requests.request(url=url, method=method, headers=header, params=parm).json()

    # 查询历史计划委托,必须传递计划委托单号,默认查询该订单往前3条的订单
    def plan_list_history(self, entrust_id, header=None):
        parm = {"id": entrust_id, "direction": "PREV", "limit": 3}
        if not header:
            header = self.header_token
        request_data = self.data["plan-list-history"]
        url, method = self.thanos_http_url + request_data["path"], request_data["method"]
        return requests.request(url=url, method=method, headers=header, params=parm).json()

    # 根据id查询止盈止损详情,必须传递止盈止损单号
    def profit_detail(self, profit_id,test_user="test_user"):
        parm = {"profitId": profit_id}
        path, method = self.request_data["profit_detail"]["route"] + self.request_data["profit_detail"][
            "path"], \
                       self.request_data["profit_detail"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.profit_detail(headers=header, params=parm)
        logger.info('撤销止盈止损为{}'.format(res.json()))
        return res.json()

    # 查询止盈止损,默认查询状态为新建的委托
    def profit_list(self, parm, test_user="test_user"):
        if not parm:
            parm = {"state": "UNFINISHED"}
        path, method = self.request_data["profit_list"]["route"] + self.request_data["profit_list"][
            "path"], \
                       self.request_data["profit_list"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.profit_list(headers=header, params=parm)
        logger.info('撤销止盈止损为{}'.format(res.json()))
        return res.json()

    # 修改止盈止损,必须传达参数
    def update_profit_stop(self, parm, test_user="test_user"):
        path, method = self.request_data["update_profit_stop"]["route"] + self.request_data["update_profit_stop"][
            "path"], \
                       self.request_data["update_profit_stop"]["method"]
        header = generate_auth_info(path=path, method=method, params=parm, test_user=test_user)
        res = xtthanos_trade_http.update_profit_stop(headers=header, params=parm)
        logger.info('撤销止盈止损为{}'.format(res.json()))
        return res.json()

    # 根据id、用户、方向创建仓位并创建止盈止损并返回止盈止损id
    def create_default_profit(self, symbol="dao_usdt", header=None, position="LONG", origQty=3,test_user="test_user"):
        # 查询是否有止盈止盈，如果有，就直接返回止盈止损id
        profit_list_res = self.profit_list(parm={"symbol":symbol,"state":"NOT_TRIGGERED"})
        profit_list = jsonpath(profit_list_res,"$..items")
        if profit_list:
            id_list = [profit.get("profitId") for profit in profit_list[0] if profit.get("positionSide") == position]
            if id_list:
                return id_list[0]
        # (1)根据参数创建持仓
        set_up_position(symbol=symbol)
        # (2)获取持仓价格
        long_entry_price = float(Positon().get_entry_price(position="LONG"))
        short_entry_price = float(Positon().get_entry_price(position="SHORT"))
        parm = {"symbol": symbol,
                "origQty": origQty,
                "positionSide": position}
        # (3)根据仓位拼接止盈止损价
        if position == "LONG":
            parm["triggerProfitPrice"] = round(long_entry_price + long_entry_price*0.1, 2)
            parm["triggerStopPrice"] = round(short_entry_price - long_entry_price*0.1, 2)
        elif position == "SHORT":
            parm["triggerProfitPrice"] = round(long_entry_price - long_entry_price*0.1, 2)
            parm["triggerStopPrice"] = round(short_entry_price + long_entry_price*0.1, 2)
        else:
            return None
        create_profit_res = self.create_profit(parm=parm)
        logger.info("根据id、用户、方向创建仓位并创建止盈止损并返回止盈止损id 参数为{} 结果{}".\
                    format(parm,create_profit_res))
        return create_profit_res.get("result")

    # 根据有效方式获取状态码
    @staticmethod
    def get_num_by_timeInforce(time_in_force):
        timeInforce_dict = {"GTC": 1, "FOK": 2,
                            "IOC": 3, "GTX": 4}
        return timeInforce_dict.get(time_in_force)

    # 根据委托类型获取状态码
    @staticmethod
    def get_num_by_entrust_type(entrust_type):
        entrust_type_dict = {"TAKE_PROFIT": 1, "STOP": 2}
        return entrust_type_dict.get(entrust_type)

    # 根据购买方向获取状态码
    @staticmethod
    def get_num_by_order_side(order_side):
        order_side_dict = {"BUY": 1, "SELL": 2}
        return order_side_dict.get(order_side)

    # 根据仓位方向获取状态码
    @staticmethod
    def get_num_by_position_side(position_side):
        position_side_dict = {"LONG": 1, "SHORT": 2}
        return position_side_dict.get(position_side)

    # 根据触发价格类型获取状态码
    @staticmethod
    def get_num_by_triggerPriceType(triggerPriceType):
        triggerPriceType_dict = {"LATEST_PRICE": 3, "MARK_PRICE": 2}
        return triggerPriceType_dict.get(triggerPriceType)

    # 根据触发状态获取状态码
    @staticmethod
    def get_num_by_entrust_state(state):
        state_dict = {"NOT_TRIGGERED": 1, "TRIGGERING": 2,
                      "TRIGGERED": 3, "USER_REVOCATION": 4,
                      "PLATFORM_REVOCATION": 5, "EXPIRED": 6}
        return state_dict.get(state)


if __name__ == '__main__':
    # res = PlanRequest().cancel_all_profit_stop()
    # print(res)
    # res = PlanRequest().create_default_profit()
    # print(res)
    # res_2 = PlanRequest().create_default_profit(position="SHORT")
    # print(res_2)
    # profit_list_res = PlanRequest().profit_list(parm={"symbol": "dao_usdt"})
    # print(profit_list_res)
    # data = jsonpath(profit_list_res, "$..items")
    # print(data)
    long_profit_id = int(PlanRequest().create_default_profit())
    short_profit_id = int(PlanRequest().create_default_profit(position="SHORT"))
    print(long_profit_id)
    print(short_profit_id)
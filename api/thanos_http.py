#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.http_api import http_api
import requests

from test_cases.contract.client.conftest import *

from common.read_data import get_data
thanos_http_url = get_data().get_ini_data("host","thanos_http_url")


class thanos_http(http_api):

    def __init__(self, thanos_http_url, **kwargs):
        super().__init__(thanos_http_url)

    # 调整杠杆倍数
    def adjust_leverage(self, **kwargs):
        adjust_leverage = request_data.get("adjust_leverage")
        requests = getattr(self, adjust_leverage.get('method'))
        return requests(adjust_leverage.get('path'), **kwargs)

    # 获取ADL信息
    def get_adl(self, **kwargs):
        position_adl = request_data.get("position_adl")
        requests = getattr(self, position_adl.get('method'))
        return requests(position_adl.get('path'), **kwargs)

    # 修改自动追加保证金
    def adjust_auto_margin(self, **kwargs):
        auto_margin = request_data.get("auto_margin")
        requests = getattr(self, auto_margin.get('method'))
        return requests(auto_margin.get('path'), **kwargs)

    # 获取风险限额设置
    def get_leverage_bracket(self, **kwargs):
        return self.get("/api/v1/position/leverage-bracket", **kwargs)

    # 获取持仓信息
    def get_position(self, **kwargs):
        position_list = request_data.get("position_list")
        requests = getattr(self, position_list.get('method'))
        return requests(position_list.get('path'), **kwargs)

    # 修改保证金
    def adjust_margin(self, **kwargs):
        position_margin = request_data.get("position_margin")
        requests = getattr(self, position_margin.get('method'))
        return requests(position_margin.get('path'), **kwargs)

    # 查询单个交易对杠杆分层
    def query_leverage_bracket(self, **kwargs):
        # leverage_request_data
        leverage_bracket_detail = request_data.get("leverage_bracket_detail")
        requests = getattr(self, leverage_bracket_detail.get('method'))
        return requests(leverage_bracket_detail.get('path'), **kwargs)

    # 查询所有交易对杠杆分层
    def query_leverage_bracket_list(self, **kwargs):
        leverage_bracket_list = request_data.get("leverage_bracket_list")
        requests = getattr(self, leverage_bracket_list.get('method'))
        return requests(leverage_bracket_list.get('path'), **kwargs)

    # 获取账户相关信息
    def get_account_info(self, **kwargs):
        account_info = request_data.get('account_info')
        requests = getattr(self,account_info.get('method'))
        return requests(account_info.get('path'), **kwargs)

    # 开通合约
    def open_thanos(self, **kwargs):
        account_open = request_data.get('account_open')
        requests = getattr(self, account_open.get('method'))
        return requests(account_open.get('path'), **kwargs)

    # 获取用户单币种资金
    def get_balance_coin(self, **kwargs):
        balance_detail = request_data.get("balance_detail")
        requests = getattr(self, balance_detail.get('method'))
        return requests(balance_detail.get('path'), **kwargs)

    # 获取用户账务流水
    def get_balance_bills(self, **kwargs):
        balance_bills = request_data.get("balance_bills")
        requests = getattr(self, balance_bills.get('method'))
        return requests(balance_bills.get('path'), **kwargs)

    # 获取用户资金
    def get_balance_list(self, **kwargs):
        balance_list = request_data.get("balance_list")
        requests = getattr(self, balance_list.get('method'))
        return requests(balance_list.get('path'), **kwargs)

    # 资金划转
    def transfer(self, **kwargs):
        balance_transfer = request_data.get("balance_transfer")
        requests = getattr(self, balance_transfer.get('method'))
        return requests(balance_transfer.get('path'), **kwargs)

    # 获取单个交易对的配置信息
    def get_symbol_info(self, **kwargs):
        # symbol_info_request_data
        symbol_detail = request_data.get("symbol_detail")
        requests = getattr(self, symbol_detail.get('method'))
        return requests(symbol_detail.get('path'), **kwargs)

    # 获取所有交易对的配置信息
    def get_symbol_list_info(self, **kwargs):
        symbol_list = request_data.get("symbol_list")
        requests = getattr(self, symbol_list.get('method'))
        return requests(symbol_list.get('path'), **kwargs)

    # 获取交易对币种
    def get_symbol_coins(self, **kwargs):
        symbol_coins = request_data.get("symbol_coins")
        requests = getattr(self, symbol_coins.get('method'))
        return requests(symbol_coins.get('path'), **kwargs)

    # 查询全部委托
    def order_entrust_list(self,**kwargs):
        order_entrust_cancel_list = request_data.get("order_entrust_cancel_list")
        requests = getattr(self, order_entrust_cancel_list.get('method'))
        return requests(order_entrust_cancel_list.get('path'), **kwargs)

    # 撤销委托
    def order_entrust_cancel(self,**kwargs):
        order_entrust_cancel = request_data.get("order_entrust_cancel")
        requests = getattr(self, order_entrust_cancel.get('method'))
        return requests(order_entrust_cancel.get('path'), **kwargs)

    # 撤销所有委托
    def order_entrust_cancel_all(self, **kwargs):
        order_entrust_cancel_all = request_data.get("order_entrust_cancel_all")
        requests = getattr(self, order_entrust_cancel_all.get('method'))
        return requests(order_entrust_cancel_all.get('path'), **kwargs)

    # 收藏交易对
    def collection_add(self,**kwargs):
        collection_add = request_data.get('collection_add')
        requests = getattr(self, collection_add.get('method'))
        return requests(collection_add.get('path'), **kwargs)

    # 收藏交易对列表
    def collection_list(self, **kwargs):
        collection_list = request_data.get('collection_list')
        requests = getattr(self, collection_list.get('method'))
        return requests(collection_list.get('path'), **kwargs)

    # 取消收藏交易对
    def collection_cancel(self, **kwargs):
        collection_cancel = request_data.get('collection_cancel')
        requests = getattr(self, collection_cancel.get('method'))
        return requests(collection_cancel.get('path'), **kwargs)

    # 一键平仓
    def position_close_all(self, **kwargs):
        position_list_close_all = request_data.get("position_list_close_all")
        requests = getattr(self, position_list_close_all.get('method'))
        return requests(position_list_close_all.get('path'), **kwargs)


    # 获取token
    def get_token(self, **kwargs):
        return requests.post('http://47.97.73.44:30001/authorize/token', **kwargs)


class thanos_user_http(thanos_http):

    def __init__(self, api_root_url):
        api_root_url += "/user"
        super().__init__(api_root_url)


class thanos_trade_http(thanos_http):

    def __init__(self, api_root_url):
        api_root_url += "/trade"
        super().__init__(api_root_url)

    # 根据id列表查询订单（订单id用, 分隔）
    def order_list_by_ids(self, **kwargs):
        list_by_ids = order_request_data.get("list_by_ids")
        requests = getattr(self, list_by_ids.get('method'))
        return requests(list_by_ids.get('path'), **kwargs)

    # 下单
    def create(self, **kwargs):
        create = request_data.get("create")
        requests = getattr(self, create.get('method'))
        return requests(create.get('path'), **kwargs)

    # 撤销订单
    def cancel(self, **kwargs):
        cancel = request_data.get("cancel")
        requests = getattr(self, cancel.get('method'))
        return requests(cancel.get('path'), **kwargs)

    # 批量下单
    def create_batch(self, **kwargs):
        create_batch = request_data.get("create_batch")
        requests = getattr(self, create_batch.get('method'))
        return requests(create_batch.get('path'), **kwargs)

#     detail
    def detail(self, **kwargs):
        detail = request_data.get("detail")
        requests = getattr(self, detail.get('method'))
        return requests(detail.get('path'), **kwargs)

    # 创建计划委托
    def create_plan(self, **kwargs):
        create_plan = request_data.get("create_plan")
        requests = getattr(self, create_plan.get('method'))
        return requests(create_plan.get('path'), **kwargs)

    # 撤销所有计划委托
    def cancel_all_plan(self, **kwargs):
        cancel_all_plan = request_data.get("cancel_all_plan")
        requests = getattr(self, cancel_all_plan.get('method'))
        return requests(cancel_all_plan.get('path'), **kwargs)

    # 撤销计划委托
    def cancel_plan(self, **kwargs):
        cancel_plan = request_data.get("cancel_plan")
        requests = getattr(self, cancel_plan.get('method'))
        return requests(cancel_plan.get('path'), **kwargs)

    # 撤销计划委托
    def create_profit(self, **kwargs):
        create_profit = request_data.get("create_profit")
        requests = getattr(self, create_profit.get('method'))
        return requests(create_profit.get('path'), **kwargs)

    # 撤销计划委托
    def cancel_all_profit_stop(self, **kwargs):
        cancel_all_profit_stop = request_data.get("cancel_all_profit_stop")
        requests = getattr(self, cancel_all_profit_stop.get('method'))
        return requests(cancel_all_profit_stop.get('path'), **kwargs)

    # 撤销止盈止损
    def cancel_profit_stop(self, **kwargs):
        cancel_profit_stop = request_data.get("cancel_profit_stop")
        requests = getattr(self, cancel_profit_stop.get('method'))
        return requests(cancel_profit_stop.get('path'), **kwargs)

    # 计划委托细节
    def plan_detail(self, **kwargs):
        plan_detail = request_data.get("plan_detail")
        requests = getattr(self, plan_detail.get('method'))
        return requests(plan_detail.get('path'), **kwargs)

    # 止盈止损细节
    def profit_detail(self, **kwargs):
        profit_detail = request_data.get("profit_detail")
        requests = getattr(self, profit_detail.get('method'))
        return requests(profit_detail.get('path'), **kwargs)

    # 止盈止损细节
    def profit_list(self, **kwargs):
        profit_list = request_data.get("profit_list")
        requests = getattr(self, profit_list.get('method'))
        return requests(profit_list.get('path'), **kwargs)

        # 止盈止损细节

    def update_profit_stop(self, **kwargs):
        update_profit_stop = request_data.get("update_profit_stop")
        requests = getattr(self, update_profit_stop.get('method'))
        return requests(update_profit_stop.get('path'), **kwargs)

    # 查询交易明细
    def trade_list(self, **kwargs):
        trade_list = request_data.get("trade_list")
        requests = getattr(self, trade_list.get('method'))
        return requests(trade_list.get('path'), **kwargs)

    def list(self, **kwargs):
        list = request_data.get("list")
        requests = getattr(self, list.get('method'))
        return requests(list.get('path'), **kwargs)

class thanos_market_http(thanos_http):

    def __init__(self, api_root_url):
        api_root_url += "/market"
        super().__init__(api_root_url)

    def qoute_agg_ticker(self,**kwargs):
        # 获取指定交易对的聚合行情信息
        qoute_agg_ticker = request_data.get("qoute_agg_ticker")
        requests = getattr(self, qoute_agg_ticker.get('method'))
        return requests(qoute_agg_ticker.get('path'), **kwargs)

    def qoute_agg_tickers(self,**kwargs):
        # 获取指定交易对的聚合行情信息
        qoute_agg_tickers = request_data.get("qoute_agg_tickers")
        requests = getattr(self, qoute_agg_tickers.get('method'))
        return requests(qoute_agg_tickers.get('path'), **kwargs)

    def qoute_symbol_index_price(self,**kwargs):
        # 获取指定交易对的聚合行情信息
        qoute_symbol_index_price = request_data.get("qoute_symbol_index_price")
        requests = getattr(self, qoute_symbol_index_price.get('method'))
        return requests(qoute_symbol_index_price.get('path'), **kwargs)

    def symbol_mark_price(self,**kwargs):
        # 获取指定交易对的聚合行情信息
        qoute_symbol_mark_price = request_data.get("qoute_symbol_mark_price")
        requests = getattr(self, qoute_symbol_mark_price.get('method'))
        return requests(qoute_symbol_mark_price.get('path'), **kwargs)

    def deal(self,**kwargs):
        # 获取交易对的最新成交信息
        deal = request_data.get("deal")
        requests = getattr(self, deal.get('method'))
        return requests(deal.get('path'), **kwargs)

    def depth(self,**kwargs):
        # 获取交易对的深度信息接口请求
        depth = request_data.get("depth")
        requests = getattr(self, depth.get('method'))
        return requests(depth.get('path'), **kwargs)

    def funding_rate(self,**kwargs):
        # 获取资金费率接口请求
        funding_rate = request_data.get("funding_rate")
        requests = getattr(self, funding_rate.get('method'))
        return requests(funding_rate.get('path'), **kwargs)

    def funding_rate_record(self,**kwargs):
        # 获取资金费率记录接口请求
        funding_rate_record = request_data.get("funding_rate_record")
        requests = getattr(self, funding_rate_record.get('method'))
        return requests(funding_rate_record.get('path'), **kwargs)

    def mark_price(self,**kwargs):
        # 获取交易对的标记价格接口请求
        mark_price = request_data.get("mark_price")
        requests = getattr(self, mark_price.get('method'))
        return requests(mark_price.get('path'), **kwargs)

    def ticker(self,**kwargs):
        # 获取交易对的标记价格接口请求
        ticker = request_data.get("ticker")
        requests = getattr(self, ticker.get('method'))
        return requests(ticker.get('path'), **kwargs)

    def kline(self,**kwargs):
        # 获取交易对的标记价格接口请求
        kline = request_data.get("kline")
        requests = getattr(self, kline.get('method'))
        return requests(kline.get('path'), **kwargs)


xtthanos_user_http = thanos_user_http(thanos_http_url)
xtthanos_trade_http = thanos_trade_http(thanos_http_url)
xtthanos_market_http = thanos_market_http(thanos_http_url)
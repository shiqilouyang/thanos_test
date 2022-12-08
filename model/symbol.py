"""
encode:utf-8
Author:aidan.hu
Data:2022/1/5
与数据库表的映射，并转换为接口数据
"""
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, BigInteger
from model import app

db = SQLAlchemy(app)


class symbol(db.Model):
    __tablename__ = 'symbol'

    id = Column(BigInteger, primary_key=True)
    symbol = Column(String(40))
    pair = Column(String(40))
    contract_type = Column(Integer)
    underlying_type = Column(Integer)
    contract_size = Column(Integer)
    trade_switch = Column(Integer)
    state = Column(Integer)
    init_leverage = Column(Integer)
    base_coin = Column(String(20))
    quote_coin = Column(String(20))
    base_coin_precision = Column(Integer)
    quote_coin_precision = Column(Integer)
    # quantity_precision = Column(Integer)
    price_precision = Column(Integer)
    support_order_type = Column(String(40))
    support_time_in_force = Column(String(40))
    support_entrust_type = Column(String(40))
    min_qty = Column(Integer)
    multiplier_down = Column(Integer)
    multiplier_up = Column(Integer)
    max_open_orders = Column(Integer)
    max_entrusts = Column(Integer)
    taker_fee = Column(Integer)
    maker_fee = Column(Integer)
    depth_precision_merge = Column(Integer)

    # support_position_type = Column(String(20))
    # min_notional
    # price_deviation
    # init_position_type
    # min_step_price
    # trigger_protect
    # market_take_bound
    # liquidation_fee
    # cn_name
    # en_name
    # make_ids
    # icon_url
    # risk_margin_user_id
    # risk_margin_account_id
    # risk_margin_user_group_id
    # thanos_switch
    # onboard_date
    # delivery_date
    # sequence
    # created_time
    # creator
    # updated_time
    # updater

    def __str__(self):
        return str({"symbol": self.symbol,
                    "pair": self.pair,
                    "contractType": self.get_contract_type(self.contract_type),
                    "underlyingType": self.get_underlying_type(self.underlying_type),
                    "contractSize": str(float(self.contract_size)),
                    "tradeSwitch": self.get_thanos_switch(self.trade_switch),
                    "state": self.state,
                    "initLeverage": self.init_leverage,
                    "baseCoin": self.base_coin,
                    "quoteCoin": self.quote_coin,
                    "baseCoinPrecision": self.base_coin_precision,
                    "quoteCoinPrecision": self.quote_coin_precision,
                    "quantityPrecision": self.quantity_precision,
                    "pricePrecision": self.price_precision,
                    "supportOrderType": self.get_support_order_type(self.support_order_type),
                    "supportTimeInForce": self.get_support_time_in_force(self.support_time_in_force),
                    "supportEntrustType": self.get_support_entrust_type(self.support_entrust_type),
                    "minPrice": None,
                    "maxPrice": None,
                    "minQty": str(int(self.min_qty)),
                    "multiplierDown": str(float(self.multiplier_down)),
                    "multiplierUp": str(float(self.multiplier_up)),
                    "maxOpenOrders": self.max_open_orders,
                    "maxEntrusts": self.max_entrusts,
                    "makerFee": str(float(self.maker_fee)),
                    "takerFee": str(float(self.taker_fee)),
                    "depthPrecisionMerge": self.depth_precision_merge
                    })

    def tostr(self):
        import json
        return json.dumps(self.__str__())

    def todict(self):
        return eval(self.__str__())

    @staticmethod
    def find_symbol(symbol_name):
        article1 = symbol.query.filter(symbol.symbol == symbol_name).first()
        return article1.todict()

    @staticmethod
    def get_contract_type(num: int):
        if num == 1:
            return "PERPETUAL"

    @staticmethod
    def get_underlying_type(num: int):
        if num == 2:
            return "U_BASED"

    @staticmethod
    def get_thanos_switch(num: int):
        if num == 1:
            return True
        elif num == 0:
            return False

    @staticmethod
    def get_support_order_type(code: str):
        if code == '1,2':
            return "LIMIT,MARKET"

    @staticmethod
    def get_support_time_in_force(code: str):
        if code == '1,2,3,4':
            return "GTC,FOK,IOC,GTX"

    @staticmethod
    def get_support_entrust_type(code: str):
        if code == '1,2,3,4,5':
            return "TAKE_PROFIT,STOP,TAKE_PROFIT_MARKET,STOP_MARKET,TRAILING_STOP_MARKET"

    @staticmethod
    def get_symbolId(symbol_name):
        article1 = symbol.query.filter(symbol.symbol == symbol_name).first()
        return article1.id


if __name__ == '__main__':
    res = symbol().get_symbolId("dao_usdt")
    print(res)

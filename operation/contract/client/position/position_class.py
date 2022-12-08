"""
encode:utf-8
Author:aidan.hu
Data:2022/1/13
"""
from decimal import Decimal
from common.common_util import CommonUtil
from operation.contract.client.position.get_position import get_position


class Positon(CommonUtil):
    """持仓相关的接口封装"""

    # 获取持仓信息接口，可通过传参指定交易对和用户，默认交易对dao_usdt,用户test_user1
    def list(self, parm={"symbol": "dao_usdt"}):
        return get_position(parm.get('symbol')).response

    # 根据交易对和持仓方向获取持仓数量
    def get_position_size(self, symbol=None, position_side="SHORT",header=None):
        if not symbol:
            symbol = "dao_usdt"
        if not header:
            header = self.header_token
        parm = {"symbol": symbol}
        list_res = self.list(parm=parm)
        for value in list_res["result"]:
            if value["positionSide"] == position_side:
                return value["positionSize"]

    def get_entry_price(self, parm={"symbol": "dao_usdt"}, position="LONG"):
        """根据交易对和持仓方向获取开仓均价"""
        list_res = self.list(parm=parm)
        for value in list_res["result"]:
            if value["positionSide"] == position and value["entryPrice"] !='0':
                return round(Decimal(value["entryPrice"]),2)


#             Decimal
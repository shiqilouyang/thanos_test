orderTypes = {
    "LIMIT" : 1,
    "" : 0,
    "MARKET" : 2,
}

# 下单方向
orderSides = {
    "BUY" : 1,
    "SELL" :2
}
# 仓位模式
positionSides = {
    "BOTH":0,
    "LONG" : 1,
    'SHORT':2
}

# 有效方式
timeInForces = {
    "GTC" : 1, # 挂单直到撤单（计划、限价）
    # //全部成交或撤销（限价）
    "FOK" :2,
    # //立即成交或撤销（止盈止损市价、部分强平、市价）
    "IOC":3,
    # //post_only，只挂单（限价-及只做maker）
    "GTX":4
}

orderStates ={
    # 创建
    "NEW":1,
    # 部分成交
    "PARTIALLY_FILLED":2,
    # 全部成交
    "FILLED":3,
    # 用户撤单
    'CANCELED' : 4,
#     下单失败
    'REJECTED' :5,
    # 过期，time_in_force撤单或溢价撤单
    "EXPIRED":6,
    'PARTIALLY_CANCELED':6,
    'HISTORY':7

}

# 资金流水
balance_bill_type ={
    'TAKE_OVER':3,
    'ADL':7,
    'FEE':6,
    'CLOSE_POSITION':2,
    'QIANG_PING_MANAGER':4,
    'EXCHANGE':1,
    'FUN':5
}
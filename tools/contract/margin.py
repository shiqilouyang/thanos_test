# 仓位保证金可追加的最大值
from common.logger import logger
from common.mongodb_operate import MongoDb
from common.set_up_balance_and_position import set_down_position, set_up_position
from common.websockets import get_sub_mark_price
from model.symbol import symbol as s
from operation.contract.client.fund.get_balance_coin import get_balance_coin


def margin_max_and_min(accountId,symbol,positionSide):
    '''
    追加保证金:
       accountId : 当前accountId     eg:39
       symbol:交易对   eg: sand_usdt
       positionSide:持仓方向   eg: 1(LONG)
    return {
        "max_margin" : max_margin,   #当前仓位可以开最大的保证金
        "min_margin" : min_margin,    #当前仓位可以开最小的保证金
        "start_margin" : start_margin  # 初始保证金(下单时候)
    }
    '''
    symbol_single = s.query.filter(s.symbol == symbol).first()
    symbol_id = symbol_single.id
    # 合约面值
    contract_size = symbol_single.contract_size

    # 当前用户的起始保证金
    args = {
        "col": "position",
    }
    # set_down_position(symbol)
    entryPrice = set_up_position()
    # 用户持仓信息
    user_positions = MongoDb(args).find_one({
        "accountId": accountId,
        'positionSide':positionSide,
        'symbolId':symbol_id
    })
    #  杠杆倍数
    leverage = user_positions.get("leverage")
    start_margin = float(str(user_positions.get('positionSize'))) * float(str(contract_size)) * float(str((entryPrice))) / float(str(leverage))
    logger.info("起始保证金为:{}".format(start_margin))
    # headers = generate_auth_info_for_test()
    # res = xtthanos_http.get_balance_coin(headers=headers,params ={'coin':"usdt"}).json()
    res = get_balance_coin('usdt').response

    # 可增加最大保证金为
    max_margin = res.get('result').get('availableBalance')
    logger.info("当前净资产余额以及当前可增加最大保证金是 {}".format(max_margin))
    isolated_margin = user_positions.get("isolatedMargin")
    logger.info("当前仓位的当前保证金（包括起起始的和能够减少的）是{}".format(isolated_margin))
    # 浮动盈亏 = 数量 * 面值 * (标记价格 - 开仓均价)
    price =  get_sub_mark_price(symbol).get('data').get('p')
    # 40 * float(str(contract_size)) * ( 标记价格 - 4.6112)
    logger.info("当前标记价格是:{}".format(price))
    float_ = float(str(user_positions.get('positionSize'))) * float(str(contract_size)) * (float(price) - entryPrice)
    logger.info("当前浮动盈余是:{}".format(float_))
    min_margin = max(0,min(float(str(isolated_margin))-start_margin,\
                           float(str(isolated_margin))-start_margin+float_))
    return {
        "max_margin" : max_margin,
        "min_margin" : min_margin,
        "start_margin" : start_margin
    }

if __name__ == '__main__':
    print(margin_max_and_min(58, 'dao_usdt', 1))
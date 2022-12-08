#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   adjust_leverage.py    
@Contact :   raogx.vip@hotmail.com
@License :   (C)Copyright 2017-2018, Liugroup-NLPR-CASIA

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/18 2:08 下午   gxrao      1.0         None
'''
from common.websockets import get_sub_mark_price
from model.symbol import symbol as s
from common.get_signature import generate_auth_info_for_test
from common.logger import logger
from operation.contract.client.leverage_bracket.query_leverage_bracket import query_leverage_bracket
from operation.contract.client.position.get_position import get_position
from operation.contract.client.position.position_class import Positon
from operation.contract.client.quote.qoute_symbol_mark_price import qoute_symbol_mark_price


def get_position_max_adjust_leverage(symbol,header=None):
    '''
       获取用户 最大可开杠杆倍数

       return:
        {'LONG':
           {
              'user_bracket': 1,   # 当前所在档位
               'position_value': 16.5368 ,      # 当前仓位最大名义价值
                position_max_adjust_leverage : 5   #所在档位最大的杠杆倍数
               },
        'SHORT':
             {
             'user_bracket': 1,# 当前所在档位
              'position_value': 16.5376, # 当前仓位最大名义价值
              position_max_adjust_leverage : 5   #所在档位最大的杠杆倍数
              }
        }
    '''
    # 查看 test_user 的持仓
    position_list_user = get_position(symbol).response["result"]
    logger.info("user 的持仓情况为{}".format(position_list_user))
    symbol_single = s.query.filter(s.symbol == symbol).first()
    # 合约面值
    contract_size = symbol_single.contract_size
    user_positions = {
        "SHORT":{
            'user_bracket': 1,   # 当前所在档位
             'position_value': 0 ,      # 当前仓位最大名义价值
            "position_max_adjust_leverage" : 5   #所在档位最大的杠杆倍数
             },
        "LONG":{
            'user_bracket': 1,   # 当前所在档位
             'position_value': 0 ,      # 当前仓位最大名义价值
            "position_max_adjust_leverage" : 5   #所在档位最大的杠杆倍数
             }
    }
    # 档位最大名义价值
    leverageBrackets = []
    for leverageBracket in query_leverage_bracket(symbol).response.get('result').get('leverageBrackets'):
        leverageBrackets.append(int(leverageBracket.get('maxNominalValue')))

    for positions in position_list_user:
        if positions.get("entryPrice") != '0':
            position_num = positions.get("positionSize")
            mark_price = qoute_symbol_mark_price(symbol).get('result').get("p")
            # 当前仓位名义价值 = 数量 * 面值 * 标记价格
            position_value = float(position_num) * float(mark_price)* float(contract_size)
            if positions.get("positionSide") == "SHORT":
                leverageBrackets.append(float(position_value))
                # 将当前名义价值与所有的最大名义价值进行排序
                lbs = sorted(leverageBrackets)
                logger.info("持仓方向为SHORT,名义价值(持仓的名义价值与所有的最大名义价值)排序{}".format(lbs))
                user_positions.get("SHORT").update({
                    # 当前仓位最大名义价值
                    "position_value" : position_value,
                    # 去当前名义价值的位置
                    'user_bracket':lbs.index(position_value) +1
                })
                leverageBrackets.remove(position_value)
            else:
                leverageBrackets.append(float(position_value))
                lbl = sorted(leverageBrackets)
                logger.info("持仓方向为LONG,名义价值(持仓的名义价值与所有的最大名义价值)排序{}".format(lbl))
                leverageBrackets.append(float(position_value))
                user_positions.get("LONG").update({
                    "position_value": position_value,
                    'user_bracket': lbl.index(position_value) + 1
                })
                leverageBrackets.remove(position_value)
    # 将 最大杠杆数量与 user_positions绑定
    for k,v in user_positions.items():
        for leverageBracket in query_leverage_bracket(symbol).response.get('result').get('leverageBrackets'):
            if leverageBracket.get('bracket') == v.get('user_bracket') and k == 'LONG':
                user_positions.get("LONG").update({
                    "position_max_adjust_leverage" : leverageBracket.get('maxLeverage')
                })
            if leverageBracket.get('bracket') == v.get('user_bracket') and k == 'SHORT':
                user_positions.get("SHORT").update({
                    "position_max_adjust_leverage": leverageBracket.get('maxLeverage')
                })
    logger.info("当前用户持仓与风险限额为{}".format(user_positions))
    return user_positions

if __name__ == '__main__':
    get_position_max_adjust_leverage("dao_usdt")
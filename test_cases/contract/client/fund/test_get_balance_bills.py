#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_get_balance_bills.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/21 4:34 下午   shuai.xu      1.0         None
'''
from pprint import pprint

from common.mongodb_operate import MongoDb
from config.contract_enum import balance_bill_type
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.fund.get_balance_bills import get_balance_bills
from test_cases.contract.client.conftest import *
from common.logger import logger



class Test_get_balance_bills():
    '''
       获取用户账务流水:
         1，获取当前用户的 accountId

    '''
    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,coin,direction,endTime,id,limit,startTime,\
                                symbol,type,except_result,except_code,except_msg",
                             api_balance_bills["get_balance_bills"])
    def test_get_balance_coin(self,scene,coin,direction,endTime,id,limit,startTime,\
                                    symbol,type,except_result,except_code,except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{coin}-{direction}-{endTime}-{id}-{limit}-\
                             {startTime}-{symbol}-{type}-{except_result}\
                                {except_code}-"{except_msg}"')
        curl_accountId = get_account_info().response.get("result").get("accountId")
        args = {
            "col": "balanceBill",
        }
        logger.info("当前用户 accountId 是{}".format(curl_accountId))
         # 根据时间排序，取出最老的一条数据
        if scene.endswith('正确的币种'):
            if MongoDb(args).find_one({"accountId": curl_accountId}) is None:
                res = None
            else:
                # 取当前账户最新的一条数据
                res = MongoDb(args).descending_sort_find(
                    {"coin": "{}".format(coin.strip()), "accountId": curl_accountId},
                    'createdTime', 1,
                )
                result = get_balance_bills(coin, direction, endTime, res[0].get('bizId'), limit, startTime, symbol, type)
                for item in result.response.get('result').get('items'):
                    assert res[0].get('createdTime') >= item.get('createdTime')
                    # 测试limit
                    assert len(item) <= limit
                    # 接口返回的币种都是 coin
                    assert coin == item.get('coin')
            return
        if scene.endswith("正确的类型"):
            # 去除当前类型数据为null的场景
            if MongoDb(args).find_one({"accountId": curl_accountId,'type':balance_bill_type.get(type)}) is None:
                res = None
            else:
                res = MongoDb(args).descending_sort_find(
                    {"accountId": curl_accountId,'type':balance_bill_type.get(type)},'createdTime'
                )
            if res is not None:
                result = get_balance_bills(coin, direction, endTime, res[0].get('_id'), limit, startTime, symbol, type)
                for item in result.response.get('result').get('items'):
                    assert res.get[0]('createdTime') >= item.get('createdTime')
                    assert type == item.get('type')
            return
        if scene.endswith('startTime大于endTime') or scene.endswith('startTime小于等于endTime'):
            # 取出最小值时间与最大值时间 createdTime
            # 两个时间作为 get_balance_bills 入参
            # 接口返回的时间 在最大值,最小值之间
            first_res = MongoDb(args).ascending_sort_find(
                {"accountId": curl_accountId},
                'createdTime',1
            )
            end_res = MongoDb(args).descending_sort_find(
                {"accountId": curl_accountId},
                'createdTime',1
            )
            result = get_balance_bills(coin, direction, end_res[0].get('createdTime'), first_res[0].get('_id'), limit, first_res[0].get('createdTime'), symbol, type)
            for item in result.response.get('result').get('items'):
                assert end_res[0].get('createdTime') >= item.get('createdTime') >= first_res[0].get('createdTime')
                assert coin == item.get('coin')
            return

        if scene.endswith('其他账户的产生的订单Id进行查找'):
            ''' 接口返回的所有流水都是该用户的，就可以判断出没有权限越界 '''
            user_orders = MongoDb(args).ascending_sort_find(
                {"coin": "{}".format(coin.strip()),"accountId": curl_accountId},
                'createdTime'
            )
            # 默认最大返回 201 条
            result = get_balance_bills(coin, direction, endTime, user_orders[0].get('bizId'), \
                                  len(user_orders), startTime, symbol, type)
            user_bills = []
            for i in user_orders[:len(result.response.get('result').get('items'))]:
                user_bills.append(i.get('_id') )
            res_bills = []
            for item in result.response.get('result').get('items'):
                res_bills.append(int(item.get('id')))
            for i in res_bills:
                assert i in user_bills
            return

        res = MongoDb(args).descending_sort_find(
            {"accountId": curl_accountId},
            'createdTime', 1,
        )
        result = get_balance_bills(coin,direction,endTime,res[0].get('bizId'),limit,startTime,symbol,type)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        # 非数据库字段进行比对
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_code == result.response["returnCode"]
        if except_code == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_balance_coin.py"])

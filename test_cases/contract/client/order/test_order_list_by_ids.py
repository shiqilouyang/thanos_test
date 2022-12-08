#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_order_list_by_ids.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/3/3 3:46 下午   shuai.xu      1.0         None
'''
import pytest

from common.mongodb_operate import MongoDb
from operation.contract.client.account.get_account_info import get_account_info
from operation.contract.client.order.order_list_by_ids import order_list_by_ids
from test_cases.contract.client.conftest import api_order_list_by_ids

class Test_order_list_by_ids():

    @pytest.mark.parametrize("scene,ids,except_result,except_code,except_msg",
                             api_order_list_by_ids["order_list_by_ids"])
    def test_order_list_by_ids(self,scene,ids,except_result,except_code,except_msg):

        accountId = get_account_info().response.get('result').get("accountId")
        args = {
            "col": "order",
        }
        user_ids = MongoDb(args).find_one({"accountId": 10002})
        if user_ids is not None:
            for items in user_ids:
                order_list_by_ids('68473626639415040,68473626639415040')

        pass

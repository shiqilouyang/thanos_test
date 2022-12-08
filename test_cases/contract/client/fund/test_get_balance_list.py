#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_get_balance_list.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/21 4:35 下午   shuai.xu      1.0         None
'''
from common.mongodb_operate import MongoDb
from operation.contract.client.fund.get_balance_list import get_balance_list
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_get_balance_list():
    '''获取用户资金
        1, 获取当前用户 accountId
        2, 根据 accountId mongo查询所有的币种资金信息
        3, 进行信息比对
      '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,except_result, except_returnCode, except_msg",
                             api_fund_data["get_balance_list"])
    def test_get_balance_list(self,scene,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{except_result}-{except_returnCode}-"{except_msg}"')
        result = get_balance_list()
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        try:
            from operation.contract.client.account import get_account_info
            # 调用获取用户信息的接口，得到accountId
            account_info = get_account_info.get_account_info()
            curl_accountId = account_info.response.get("result").get("accountId")
            args = {
                "MONGO_COL": "balance",
            }
            logger.info("当前用户 accountId 是{}".format(curl_accountId))
            # 根据accountId mongo查询用户所有的币种信息
            res = MongoDb(args).find({"accountId": curl_accountId})
            # 进行比对
            for item in res:
                for r in result.response.get("result"):
                    if item.get("coin") == r.get("coin"):
                        assert str(item.get("walletBalance")) == r.get('walletBalance')
                        assert str(item.get("openOrderMarginFrozen")) == r.get('openOrderMarginFrozen')
                        #  availableBalance = walletBalance + openOrderMarginFrozen
                        assert float(str(item.get("walletBalance"))) + float(str(item.get("openOrderMarginFrozen"))) \
                               == float(r.get('availableBalance'))
        except Exception as e:
            logger.error(e)
        # 非数据库字段进行比对
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_balance_list.py"])

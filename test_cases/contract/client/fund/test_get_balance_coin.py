#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_get_balance_coin.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/1/21 4:34 下午   shuai.xu      1.0         None
'''
from common.mongodb_operate import MongoDb
from operation.contract.client.fund.get_balance_coin import get_balance_coin
from test_cases.contract.client.conftest import *
from common.logger import logger



class Test_get_balance_coin():
    '''
       获取用户单币种资金
        1, 获取当前用户 accountId
        2, 根据 accountId,coin 在mongo查询资金信息
        3, 进行信息比对
    '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,coin,except_result, except_returnCode, except_msg",
                             api_fund_data["get_balance_coin"])
    def test_get_balance_coin(self,scene,coin,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{coin}-{except_result}-{except_returnCode}-"{except_msg}"')
        result = get_balance_coin(coin)
        try:
            from operation.contract.client.account import get_account_info
            # 调用获取用户信息的接口，得到accountId
            account_info = get_account_info.get_account_info()
            curl_accountId = account_info.response.get("result").get("accountId")
            args = {
                "col": "balance",
            }
            logger.info("当前用户 accountId 是{}".format(curl_accountId))
            #   根据 accountId,coin 在mongo查询资金信息
            res = MongoDb(args).find_one({"coin": "{}".format(coin.strip()), "accountId": curl_accountId})
            logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
            # 进行信息比对
            if res is not None:
                assert str(res.get("walletBalance")) == result.response.get("result").get('walletBalance')
                assert str(res.get("openOrderMarginFrozen")) == result.response.get("result").get('openOrderMarginFrozen')
                #  availableBalance = walletBalance + openOrderMarginFrozen
                assert float(str(res.get("walletBalance"))) + float(str(res.get("openOrderMarginFrozen"))) \
                       == float(result.response.get("result").get('availableBalance'))
            else:
                logger.warning("当前币种{} 没有在数据库查到".format(coin))
        except Exception as e:
            logger.error(e)
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
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
    pytest.main(["-q", "-s", "test_get_balance_coin.py"])

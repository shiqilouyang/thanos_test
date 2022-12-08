#!/usr/bin/python
# -*- encoding: utf-8 -*-
from model.account_info import account_info
import json
from operation.contract.client.account import get_account_info
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_get_account_info:
    '''
        获取账户相关信息:
           1,接口获取 accountId
           2,根据 accountId 数据库获取对应的账户信息
           3,接口返回信息与数据库信息对比
    '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,except_result, except_returnCode, except_msg",
                             api_account_data["get_account_info"])
    def test_get_account_info(self,scene,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{except_result}-{except_returnCode}-"{except_msg}"')
        result = get_account_info.get_account_info()
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        account = account_info.query.filter\
            (account_info.account_id == result.response.get("result").\
             get("accountId")).first()
        account_info_from_db = json.loads(account.tostr())
        logger.info("数据库查询得到结果为{}".format(account_info_from_db))
        # 数据库信息与 接口信息进行比对
        assert account_info_from_db == str(result.response.get("result"))
        # 非数据库字段比对
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_account_info.py"])

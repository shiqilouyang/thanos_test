#!/usr/bin/python
# -*- encoding: utf-8 -*-

from operation.contract.client.account.open_thanos import open_thanos
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_open_thanos:
    '''
      用户开启合约:
        只判断接口返回信息，无数据库查询
    '''

    @pytest.mark.single
    # @pytest.mark.usefixtures("step_first")
    @pytest.mark.parametrize("scene,except_result, except_returnCode, except_msg",
                             api_account_data["open_thanos"])
    def test_open_thanos(self,scene,except_result,except_returnCode, except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{except_result}-{except_returnCode}-"{except_msg}"')
        result = open_thanos()
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        # assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_returnCode == result.response["returnCode"]
        if except_returnCode == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_open_thanos.py"])

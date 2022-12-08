#!/usr/bin/python
# -*- encoding: utf-8 -*-
from operation.contract.client.position.get_adl import get_adl
from test_cases.contract.client.conftest import *
from common.logger import logger

class Test_get_adl:
    '''
      获取ADL信息:

    '''

    @pytest.mark.single
    @pytest.mark.parametrize("scene,except_result,except_code,except_msg",api_position_data["get_adl"])
    def test_get_adl(self,scene,except_result,except_code,except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：-{except_result}-{except_code}-"{except_msg}"')
        result = get_adl()
        logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
        assert result.status_code == 200
        assert except_result == result.response["msgInfo"]
        assert except_code == result.response["returnCode"]
        if except_code == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")

if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_adl.py"])

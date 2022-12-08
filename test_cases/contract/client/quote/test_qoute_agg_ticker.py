#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   test_qoute_agg_ticker.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/3/13 1:51 下午   shuai.xu      1.0         None
'''

from operation.contract.client.quote.qoute_agg_ticker import qoute_agg_ticker
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_qoute_agg_ticker:
    '''
        获取指定交易对的聚合行情信息:

    '''

    @pytest.mark.single
    @pytest.mark.parametrize("scene,symbol,except_result,except_code,except_msg",
                             api_quote_data["qoute_agg_ticker"])
    def test_qoute_agg_ticker(self,scene,symbol,except_result,except_code,except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{except_result}-{except_code}-"{except_msg}"')
        result = qoute_agg_ticker(symbol)
        assert except_result == result.response["msgInfo"]
        assert except_code == result.response["returnCode"]
        if except_code == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "test_get_account_info.py"])

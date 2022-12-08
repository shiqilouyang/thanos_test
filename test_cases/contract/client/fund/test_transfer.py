# #!/usr/bin/env python
# # -*- encoding: utf-8 -*-
# '''
# @File    :   test_transfer.py
# @Contact :   shuai.xu
#
# @Modify Time      @Author    @Version    @Desciption
# ------------      -------    --------    -----------
# 2022/1/21 4:35 下午   shuai.xu      1.0         None
# '''
# from decimal import Decimal
# from common.mongodb_operate import MongoDb
# from operation.contract.client.account import get_account_info
# from operation.contract.client.fund.transfer import transfer
# from test_cases.contract.client.conftest import *
# from common.logger import logger
#
#
# class Test_transfer():
#     ''' 资金划转
#           当前接口是对测试使用的，不需要自动化
#     '''
#
#     @pytest.mark.single
#     # @pytest.mark.usefixtures("step_first")
#     @pytest.mark.parametrize("scene,amount,billSide,coin,except_result, except_returnCode, except_msg",
#                              api_fund_data["transfer"])
#     def test_transfer(self,scene,amount,billSide,coin,except_result,except_returnCode, except_msg):
#         # logger.info("*************** 开始执行用例 ***************")
#         logger.info(f'场景【{scene}】信息：{amount}-{billSide}-{coin}-{except_result}-{except_returnCode}-"{except_msg}"')
#
#         if scene.endswith('划转正常，方向转入') or scene.endswith('划转正常，方向转出') or scene.endswith('持续划转，方向转入'):
#             account_info = get_account_info.get_account_info()
#             curl_accountId = account_info.response.get("result").get("accountId")
#             args = {
#                 "col": "balance",
#             }
#             logger.info("当前用户 accountId 是{}".format(curl_accountId))
#             #   根据 accountId,coin 在mongo查询 划转前
#             res_pre = MongoDb(args).find_one({"coin": "{}".format(coin.strip()), "accountId": curl_accountId})
#             result = transfer(amount, billSide, coin)
#             time.sleep(2)
#             # 查询划转之后的资金情况
#             res_after = MongoDb(args).find_one({"coin": "{}".format(coin.strip()), "accountId": curl_accountId})
#             if scene.endswith('划转正常，方向转入') or scene.endswith('持续划转，方向转入'):
#                 assert Decimal(str(res_after.get('walletBalance'))) == Decimal(str(res_pre.get('walletBalance'))) \
#                        + Decimal(str(amount))
#             else:
#                 assert Decimal(str(res_after.get('walletBalance'))) == Decimal(str(res_pre.get('walletBalance'))) \
#                        - Decimal(str(amount))
#             assert result.status_code == 200
#             assert except_result == result.response["msgInfo"]
#             assert except_returnCode == result.response["returnCode"]
#             if except_returnCode == 0:
#                 assert except_msg in str(result.response["result"])
#             else:
#                 assert except_msg in result.response["error"]["msg"]
#             return
#
#         result = transfer(amount, billSide, coin)
#         logger.warning(f'场景-[{scene}]的返回信息是：{result.response}')
#         assert result.status_code == 200
#         assert except_result == result.response["msgInfo"]
#         assert except_returnCode == result.response["returnCode"]
#         if except_returnCode == 0:
#             assert except_msg in str(result.response["result"])
#         else:
#             assert except_msg in result.response["error"]["msg"]
#         # logger.info("*************** 结束执行用例 ***************")
#
# if __name__ == '__main__':
#     pytest.main(["-q", "-s", "test_get_balance_coin.py"])

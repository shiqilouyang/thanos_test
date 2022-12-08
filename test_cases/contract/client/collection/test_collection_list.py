#!/usr/bin/python
# -*- encoding: utf-8 -*-
from common.mongodb_operate import MongoDb
from model.symbol import symbol as s
from operation.contract.client.collection import collection_list, collection_add
from test_cases.contract.client.conftest import *
from common.logger import logger


class Test_collection_list:
    '''
       交易对收藏列表:
            1, 查询当前账户 accountId
            2, 根据accountId 查询 mongo userCollection 所有的收藏交易对Id
            3, 根据当前用户收藏的所有的交易对Id,查询所有的交易对名称
            4, 判断交易对收藏列表是不是与接口返回相同
    '''

    @pytest.mark.single
    @pytest.mark.parametrize("scene,except_result,except_code,except_msg",
                             api_collection_list["test_collection_list"])
    def test_collection_list(self,scene,except_result,except_code,except_msg):
        # logger.info("*************** 开始执行用例 ***************")
        logger.info(f'场景【{scene}】信息：{except_result}-{except_code}-"{except_msg}"')
        # 准备数据
        collection_add.collection_add("fil_usdt")
        result = collection_list.collection_list()
        try:
            if result.response.get("msgInfo") !="failure":
                from operation.contract.client.account import get_account_info
                # 调用获取用户信息的接口，得到accountId
                accountId = get_account_info.get_account_info().response.get("result").get("accountId")
                args = {
                    "col": "userCollection",
                }
                # 根据 accountId 查询 所有的收藏交易对Id
                res = MongoDb(args).find_one({"accountId": int(accountId)})
                # 交易对名称列表
                collection_all = []
                # 根据 当前用户收藏的所有的交易对Id,查询所有的交易对名称
                for i in res.get("symbolIds").split(","):
                    collection_all.append(s.query.filter(s.id == int(i)).first().symbol)

                logger.info("还用户收藏了这些交易对 {}".format(collection_all))
                # 判断交易对收藏列表是不是与接口返回相同
                assert result.response.get("result") == collection_all
        except Exception as e:
            logger.error(e)

        # 非数据库字段比对
        assert except_result == result.response["msgInfo"]
        assert except_code == result.response["returnCode"]
        if except_code == 0:
            assert except_msg in str(result.response["result"])
        else:
            assert except_msg in result.response["error"]["msg"]
        # logger.info("*************** 结束执行用例 ***************")


if __name__ == '__main__':
    pytest.main(["-q", "-s", "Test_collection_list.py"])

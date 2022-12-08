"""
encode:utf-8
Author:aidan.hu
Data:2022/1/20
"""
import pytest

from common.get_signature import generate_auth_info
from common.logger import logger
from operation.contract.client.order.order_request import OrderRequest
from test_cases.contract.client.conftest import get_data


class TestListHistory:
    """查询历史订单测试类"""
    order_request = OrderRequest()
    test_data = get_data("order_test_list_history_data.yml")

    # 查询历史订单接口正向测试用例，用例详见数据文件注释
    @pytest.mark.parametrize("test_data",  [] if test_data.get("list_history_success") == {} else [test_data])
    def test_list_history_success(self, test_data):
        order_request = self.order_request
        order_request.mongo.update_col("order")
        cases_data = test_data["list_history_success"]
        for value in cases_data.values():
            case_name, parameter = value["name"], value["parameter"]
            expected_result, query = value["expected_result"], value["query"]
            # 前置处理去mongo查询一条任意一条order的id
            if "sort" in query.keys():
                if query["sort"] == 1:
                    order_id = order_request.mongo.ascending_sort_find(query={"accountId": order_request.account_id},
                                                                       sort_field="_id", limit=1)[0]['_id']
                else:
                    order_id = order_request.mongo.descending_sort_find(query={"accountId": order_request.account_id},
                                                                        sort_field="_id", limit=1)[0]['_id']
            else:
                query["accountId"] = order_request.account_id
                query_res = order_request.mongo.find_one(data=query)
                order_id = query_res["_id"]
            parameter["id"] = order_id
            # 发送请求，获取接口返回数据
            res = order_request.list_history(parm=parameter)
            logger.info(f'查询历史订单正向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            assert res["msgInfo"] == expected_result["msgInfo"]
            # 去mongo获取数据
            mongo_query = expected_result["mongo_query"]
            if mongo_query == "$lt":
                mongo_res = order_request.mongo.descending_sort_find(
                    query={"accountId": order_request.account_id, "_id": {mongo_query: order_id}}, sort_field="_id",
                    limit=parameter["limit"])
                if res["result"]["items"]:
                    assert len(res["result"]["items"]) == len(mongo_res)
                    assert res["result"]["items"][0]["orderId"] == str(mongo_res[0]["_id"])
                else:
                    assert not mongo_res
            elif mongo_query == "$gt":
                mongo_res = order_request.mongo.ascending_sort_find(
                    query={"accountId": order_request.account_id, "_id": {"$gt": order_id}}, sort_field="_id",
                    limit=parameter["limit"])
                # 对查询的结果反转
                mg_res = list(reversed(mongo_res))
                if res["result"]["items"]:
                    assert len(res["result"]["items"]) == len(mongo_res)
                    assert res["result"]["items"][0]["orderId"] == str(mg_res[0]["_id"])
                else:
                    assert not mongo_res

    # 查询历史订单接口反向测试用例，用例详见数据文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("list_history_failed") == {} else [test_data])
    def test_list_history_success(self, test_data):
        order_request = self.order_request
        order_request.mongo.update_col("order")
        cases_data = test_data["list_history_failed"]
        request_data = get_data("order_request_data.yml")
        for value in cases_data.values():
            # 获取用例数据
            case_name, parameter = value["name"], value["parameter"]
            expected_result = value["expected_result"]
            if not parameter["id"]:
                query_res = order_request.mongo.find_one(data={"accountId":order_request.account_id})
                parameter["id"] = query_res["_id"]
            path, method = request_data["list_history"]["path"], request_data["list_history"]["method"]
            header = generate_auth_info(path=path, method=method,params=parameter)
            # 发送请求，获取返回结果
            res = order_request.list_history(parm=parameter,header=header)
            logger.info(f'查询历史订单反向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]
            # 根据预期参数判断断言
            if "msg" in list(expected_result.keys()):
                assert res["error"]["msg"] == expected_result["msg"]
            elif "items" in list(expected_result.keys()):
                assert not res["result"]["items"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_list_history.py'])

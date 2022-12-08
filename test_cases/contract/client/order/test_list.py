"""
encode:utf-8
Author:aidan.hu
Data:2022/1/19
"""
import pytest

from common.common_util import get_timestamp_now, before_timestamp_by_day
from common.get_signature import generate_auth_info
from common.logger import logger
from operation.contract.client.order.order_request import OrderRequest
from test_cases.contract.client.conftest import get_data


class TestOrderList:
    """条件查询订单类列表测试类"""
    order_request = OrderRequest()
    test_data = get_data("order_test_list_data.yml")
    request_data = get_data("order_request_data.yml")

    # 条件查询的正向测试用例，详情见文件注释
    @pytest.mark.parametrize("test_data", [] if test_data.get("list_success") == {} else [test_data])
    def test_list_success(self, test_data):
        order_request = self.order_request
        now_time = get_timestamp_now()
        five_day_ago = before_timestamp_by_day(5)
        case_data = test_data["list_success"]
        order_request.mongo.update_col("order")
        for value in case_data.values():
            # 从文件中读取数据
            case_name, parameter, expected_result = value["name"], value["parameter"], value["expected_result"]
            # 用户1的accountId,修改账户时要修改common_util的account_id
            query = {"accountId": order_request.account_id}
            logger.info(f'查询订单列表接口参数初始值--->{parameter}')
            # 根据参数组装mongo查询条件
            if parameter:
                if "startTime" in list(parameter.keys()) and "endTime" in list(parameter.keys()):
                    parameter["startTime"] = five_day_ago
                    parameter["endTime"] = now_time
                    query["createdTime"] = {"$gte": five_day_ago, "$lte": now_time}
                elif "endTime" in list(parameter.keys()):
                    parameter["endTime"] = now_time
                    query["createdTime"] = {"$lte": now_time}
                elif "startTime" in list(parameter.keys()):
                    parameter["startTime"] = five_day_ago
                    query["createdTime"] = {"$gte": five_day_ago}

                if "symbol" in list(parameter.keys()):
                    query["symbolId"] = order_request.get_symbolid(parameter["symbol"])
                if "forceClose" in list(parameter.keys()):
                    query["forceClose"] = parameter["forceClose"]
                if "state" in list(parameter.keys()):
                    if parameter["state"] == "UNFINISHED":
                        query["state"] = {"$in": [1, 2]}
                    elif parameter["state"] != "HISTORY":
                        query["state"] = order_request.get_enumerate_by_state(parameter["state"])

            # 获取返回数据
            res = order_request.list(parm={} if parameter is None else parameter)
            logger.info(f'查询订单列表接口--->{case_name}-->参数为{parameter}--->返回结果{res}')
            mongo_count = order_request.mongo.get_find_count(query)
            # result = res["result"]
            assert res["msgInfo"] == expected_result["msgInfo"]
            # assert result["total"] == mongo_count
            logger.info(f'查询订单列表接口--->{case_name}-->查询参数为{query}--->返回结果{mongo_count}')

    # 条件查询订单的反向用例，详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("list_failed") == {} else [test_data])
    def test_list_failed(self, test_data):
        order_request = self.order_request
        # 从数据文件中获取数据
        case_data = test_data["list_failed"]
        path, method = self.request_data["list"]["path"], self.request_data["list"]["method"]
        for value in case_data.values():
            case_name, parameter, expected_result = value["name"], value["parameter"], value[
                "expected_result"]
            header = generate_auth_info(path=path, method=method, params=parameter)
            # 获取返回数据
            res = order_request.list(parm=parameter, header=header)
            logger.info(f'查询订单列表接口反向用例--->{case_name}-->参数为{parameter}--->返回结果{res}')
            # 断言
            assert res["msgInfo"] == expected_result["msgInfo"]
            if "msg" in list(expected_result.keys()):
                assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-v', '-s', './test_order.py'])

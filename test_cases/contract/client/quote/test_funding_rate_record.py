"""
encode:utf-8
Author:aidan.hu
Data:2022/1/10
"""
import pytest
from model.symbol import symbol as s
from common.logger import logger
from common.mongodb_operate import MongoDb
from model.fund_rate import fund_rate
from operation.contract.client.quote.qoute_class import Qoute
from test_cases.contract.client.conftest import get_data


class TestFundingRateRecord:
    '''获取资金费率记录测试类'''
    qoute_request = Qoute()
    test_data = get_data("quote_test_funding_rate_record_data.yml")

    # 正确获取资金费率记录的所有用例：详情见数据文件
    @pytest.mark.parametrize("test_data", [] if test_data.get("test_success") == {} else [test_data])
    def test_success(self,test_data):
        cases_data = test_data["test_success"]
        for key, value in cases_data.items():
            parm, name, expected_result = value["parameter"], value["name"], value["expected_result"]
            res = self.qoute_request.funding_rate_record(param=parm)
            logger.info(f"获取资金费率记录 ==>> {name}的传参为 ==>> {parm}")
            logger.info(f"获取资金费率记录 ==>> {name}的返回结果 ==>> {res}")
            assert res["msgInfo"] == expected_result["msg"]
            args = {
                "col": "fundRateRecord",
            }
            if name.endswith('只传入交易对名称'):
                # 收取间隔(时)
                symbol_id = s.query.filter(s.symbol == parm.get('symbol')).first().id
                collectionInternal = fund_rate.query.filter(fund_rate.symbol_id == symbol_id).first().collection_interval
                if "page" not in list(parm.keys()):
                    symbol_fundRateRecord_result = MongoDb(args).descending_sort_find \
                        ({'symbol': parm.get('symbol'), 'collection': True}, 'createdTime', 10)
                    for item in symbol_fundRateRecord_result:
                        assert { 'id': str(item.get('_id')),
                                   'symbol': parm.get('symbol'),
                                   'fundingRate': str(float(item.get('fundingRate'))),
                                   'createdTime': item.get('createdTime'),
                                   'collectionInternal': float(collectionInternal)*3600
                               } in res.get("result").get('items')
    # 获取资金费率记录的反向用例，详情仅数据文件注释
    # @pytest.mark.parametrize("test_data", [test_data])
    # def test_unsuccess(self, test_data):
    #     cases_data = test_data["test_unsuccess"]
    #     for value in cases_data.values():
    #         parm, name, expected_result = value["parameter"], value["name"], value["expected_result"]
    #         # 传入参数获取请求数据
    #         res = self.qoute_request.funding_rate_record(param=parm)
    #         logger.info(f"获取资金费率记录 ==>> {name}的返回结果 ==>> {res}")
    #         # 比较返回数据与预期数据
    #         assert res["msgInfo"] == expected_result["msgInfo"]
    #         assert res["error"]["msg"] == expected_result["msg"]


if __name__ == '__main__':
    pytest.main(['-s', '-v', './test_funding_rate_record.py'])

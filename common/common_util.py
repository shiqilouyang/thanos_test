"""
codeing:utf-8
Author:aidan.hu
Data:2021/12/30
"""
import os
import time

from common.get_signature import generate_auth_info_for_test
from common.mongodb_operate import MongoDb
from common.read_data import ReadFileData, get_data
from common.redis_operate import RedisData

# 将鉴权信息、数据库连接、redis连接、mongo连接整合到一个类，可以通过继承调用
from model import account_info
from model.symbol import symbol

# 获取各种项目路径的类
from operation.contract.client.account.get_account_info import get_account_info


class ProjectPath:
    def __init__(self):
        self.project_top_path = os.path.dirname(os.path.dirname(__file__))

    # 获取数据目录路径
    def get_common_path(self):
        return os.path.join(self.project_top_path, "common")

    # 获取配置目录路径
    def get_config_path(self):
        return os.path.join(self.project_top_path, "config")

    # 获取到公共目录路径
    def get_data_path(self):
        return os.path.join(self.project_top_path, "data")


class CommonUtil:
    """公共类，常用的方法封装"""
    mongo = MongoDb()
    redis = RedisData()
    thanos_http_url = get_data().get_ini_data("host", "thanos_http_url")
    data_path = ProjectPath().get_data_path()
    account_id = get_account_info().response.get("result").get("accountId")
    # header_token = generate_auth_info_for_test()
    # 根据传参判断数据文件路径并读取文件
    def get_test_data(self, file_name, module_name=None):
        if module_name:
            module_path = os.path.join(self.data_path, module_name)
            file_path = os.path.join(module_path, file_name)
        else:
            file_path = os.path.join(self.data_path, file_name)
        return ReadFileData().load_yaml(file_path)

    # 通过交易对名字查询symbolId
    @staticmethod
    def get_symbolid(symbol_name):
        if symbol_name is None:
            return None
        else:
            symbol_id = symbol().get_symbolId(symbol_name)
            return symbol_id

# 获取当前时间的毫秒级时间戳
def get_timestamp_now():
    now = time.time()
    return int(round(now * 1000))


# 获取几天前的时间戳
def before_timestamp_by_day(day: int):
    # 获取当前时间
    now_timestamp = get_timestamp_now()
    # 将时间差换算成毫秒
    interval_time = day * 24 * 60 * 60 * 1000
    # 计算之前的时间戳
    timestamp = now_timestamp - interval_time
    return timestamp


if __name__ == '__main__':
    ct = CommonUtil()
    # ct.mongo.update_col("order")
    # # res = ct.mongo.ascending_sort_find(query={"symbolId": 31}, sort_field="_id",
    # #             limit=1)
    # # print(res)
    # # for i in res:
    # #     print(i)
    # # print("end")
    # res = ct.mongo.find_one({"accountId":39,"state":3})
    # print(res)
    print(ct.account_id)
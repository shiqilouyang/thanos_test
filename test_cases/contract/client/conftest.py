#!/usr/bin/python
# -*- encoding: utf-8 -*-
import random
from functools import lru_cache

import pytest
import os
import time

from common.config_dao_usdt import conceal_symbol_dao, update_symbol_dao, config_dao_leverage_bracket, trade_on_dao
from common.read_data import ReadFileData
from common.logger import logger

BASE_PATH = os.path.dirname(os.path.dirname(os.path.dirname \
                                                (os.path.dirname(os.path.realpath(__file__)))))

@lru_cache
def get_data(yaml_file_name):
    try:
        data_file_path = os.path.join(BASE_PATH, "data/contract/client/{}".format \
            (yaml_file_name.split("_")[0]), yaml_file_name)
        yaml_data = ReadFileData().load_yaml(data_file_path)
        setting_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname\
                         (os.path.dirname(os.path.realpath(__file__))))), "config", "setting.ini")
        pytest_set = ReadFileData().load_ini(setting_path)["pytest_set"]
        # 随机取一个值
        case, case_arge = random.choice(list(yaml_data.items()))
        # 格式 {"test_collection_add":[["收藏存在的交易对","btc_usdt",success, 0, ""], ["收藏不存在的交易对","shib_usdt1",failure, 1, "invalid"]]}
        if type(case_arge) == list:
            if pytest_set.get("is_Smoking_Test") == '1':
                for k,v in yaml_data.items():
                    for i in range(len(v)-1,-1,-1):
                        if "main-" not in v[i][0]:
                            v.remove(v[i])
        else:
            # 三级格式
            if "path" not in case_arge:
                if pytest_set.get("is_Smoking_Test") == '1':
                    for v in yaml_data.values():
                        for k in list(v.keys()):
                            if "main-" not in v.get(k).get("name"):
                                v.pop(k)
    except Exception as ex:
        raise ex
        # pytest.skip(str(ex))
    else:
        return yaml_data

api_quote_data= get_data("quote_data.yml")
api_order_data = get_data("order_data.yml")
api_match_data = get_data("match_data.yml")
api_fund_data = get_data("fund_data.yml")
api_balance_bills= get_data("fund_data.yml")
api_cancel_data = get_data("cancel_order_data.yml")
api_symbol_data = get_data("symbol_info_data.yml")
api_position_data = get_data("position_data.yml")
api_leverage_data = get_data("leverage_data.yml")
api_account_data = get_data("account_data.yml")
request_data = get_data("request_data.yml")
api_order_entrust = get_data("orderEntrust_data.yml")
api_order_entrust_cancel = get_data("orderEntrust_data.yml")
api_order_entrust_cancel_all = get_data("orderEntrust_data.yml")
api_collection_add = get_data("collection_data.yml")
api_collection_list = get_data("collection_data.yml")
api_collection_cancel = get_data("collection_data.yml")
api_position_close_all = get_data("position_data.yml")
api_taker_match = get_data("match_data.yml")
api_order_list_by_ids = get_data("order_data.yml")
order_request_data = get_data("order_request_data.yml")

if __name__ == '__main__':
    print(f'测试用例数据--{api_plan_data["query_entrustId"]}')

@pytest.fixture()
def step_first():
    logger.info("******************************")
    logger.info("前置步骤开始 ==>> 清理数据")
    print('*-'*20)


def step_last():
    logger.info("后置步骤开始 ==>> 清理数据")


def step_login(username, password):
    logger.info("前置步骤 ==>> 管理员 {} 登录，返回信息 为：{}".format(username, password))

    # print(api_data["open_trade"])
# @pytest.fix.pture(scope="session")
# def login_fixture():
#     username = base_data["init_admin_user"]["username"]
#     password = base_data["init_admin_user"]["password"]
#     header = {
#         "Content-Type": "application/x-www-form-urlencoded"
#     }
#     payload = {
#         "username": username,
#         "password": password
#     }
#     loginInfo = bcts_user.login(data=payload, headers=header)
#     step_login(username, password)
#     yield loginInfo.json()


# @pytest.fixture(scope="function")
# def insert_delete_user():
#     """删除用户前，先在数据库插入一条用户数据"""
#     insert_sql = base_data["init_sql"]["insert_delete_user"][0]
#     db.execute_db(insert_sql)
#     step_first()
#     logger.info("删除用户操作：插入新用户--准备用于删除用户")
#     logger.info("执行前置SQL：{}".format(insert_sql))
#     yield
#     # 因为有些情况是不给删除管理员用户的，这种情况需要手动清理上面插入的数据
#     del_sql = base_data["init_sql"]["insert_delete_user"][1]
#     db.execute_db(del_sql)
#     step_last()
#     logger.info("删除用户操作：手工清理处理失败的数据")
#     logger.info("执行后置SQL：{}".format(del_sql))


# @pytest.fixture(scope="function")
# def delete_register_user():
#     """注册用户前，先删除数据，用例执行之后，再次删除以清理数据"""
#     del_sql = base_data["init_sql"]["delete_register_user"]
#     db.execute_db(del_sql)
#     step_first()
#     logger.info("注册用户操作：清理用户--准备注册新用户")
#     logger.info("执行前置SQL：{}".format(del_sql))
#     yield
#     db.execute_db(del_sql)
#     step_last()
#     logger.info("注册用户操作：删除注册的用户")
#     logger.info("执行后置SQL：{}".format(del_sql))
#
#
# @pytest.fixture(scope="function")
# def update_user_telephone():
#     """修改用户前，因为手机号唯一，为了使用例重复执行，每次需要先修改手机号，再执行用例"""
#     update_sql = base_data["init_sql"]["update_user_telephone"]
#     db.execute_db(update_sql)
#     step_first()
#     logger.info("修改用户操作：手工修改用户的手机号，以便用例重复执行")
#     logger.info("执行SQL：{}".format(update_sql))
# 初始化dao_usdt管理端配置
def set_up_dao():
    conceal_symbol_dao()
    update_symbol_dao()
    config_dao_leverage_bracket()
    trade_on_dao()


# 初始化用户余额和仓位
def set_up_user():
    from common.set_up_balance_and_position import set_up_balance, set_up_position
    set_up_balance()
    set_up_position()

def pytest_configure(config):
    from common.read_data import get_data
    thanos_http_url = get_data().get_ini_data("host", "thanos_http_url")
    config._metadata['测试url'] = thanos_http_url
    config._metadata['当前项目'] = '合约项目'
    config._metadata['自动化范围'] = '客户端'
    config._metadata['测试时间'] = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
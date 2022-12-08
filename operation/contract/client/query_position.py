#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_http
from api.http_api import ResultBase
from common.logger import logger
from common.read_data import get_data
from common.get_signature import generate_auth_info

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
def query_positionSide():
    '''查询持仓方向'''
    result = ResultBase()
    message, headers = generate_auth_info(access_key, secret_key)
    res = xtthanos_http.query_positionSide(headers=headers,params=message)
    result.success = False
    # if ["code"] not in res.text:
    #     result.success = True
    #     result.token = res.json()
    # else:
    #     result.error = "接口返回码是 【 {} 】, 返回信息：{} ".format(res.json(), res.json())
    # result.msg = res.json()["msg"]
    result.response = res.json()
    logger.info(f"查询持仓方向 ==>> 返回结果 ==>> {res.text}")
    return result

if __name__ == '__main__':
    query_positionSide()
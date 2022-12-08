#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_http
from common.logger import logger
from common.read_data import get_data
from common.utils import caught_exception

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
token_data = get_data().get_group_data("api_token")
def get_token():
    '''查询交易对的最新成交信息'''
    params = {
        "countryCode": token_data["countryCode"],
        "loginPwd": token_data["loginPwd"],
        "userName": token_data["userName"]
    }
    headers = {}
    headers["device"] = "web"
    try:
        res = xtthanos_http.get_token(headers=headers,json=params)
        token = res.json()["data"]["accessToken"]
    except:
        caught_exception()
    return token

if __name__ == '__main__':
    get_token()
    # print(1111,token_data)
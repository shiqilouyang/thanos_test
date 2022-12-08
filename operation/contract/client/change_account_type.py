#!/usr/bin/python
# -*- encoding: utf-8 -*-
from api.thanos_http import xtthanos_http
from api.http_api import ResultBase
from common.logger import logger
from common.read_data import get_data
from common.get_signature import generate_auth_info

access_key = get_data().get_ini_data("api_key","access_key")
secret_key = get_data().get_ini_data("api_key","secret_key")
def change_account_type():
    url = 'http://thanos-web-test.xtthanos.com' + '/api/v1/admin/user-info/update-type?accountId=40&type=1'
    message, headers = generate_auth_info(access_key, secret_key)

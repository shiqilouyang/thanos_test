"""
encode:utf-8
Author:aidan.hu
Data:2022/1/13
"""
import requests

from common.common_util import CommonUtil
from common.get_signature import generate_auth_info
from test_cases.contract.client.conftest import fund_request_data


class Balance:
    """用户资金相关的接口封装，不用输入路径和方法，可自定义参数访问接口，没有参数有默认参数"""
    thanos_http_url = CommonUtil().thanos_http_url

    # 获取用户资金 可通过传入不同用户的header来获取该用户的资金
    def list(self,header=None):
        path = fund_request_data.get('balance_list').get('path')
        method = fund_request_data.get('balance_list').get('method')
        if not header:
            header = generate_auth_info(path=path,method=method,params={})
        url = self.thanos_http_url + path
        res = requests.request(method=method,url=url,headers=header).json()
        print(res)
        return res

    # 资金划转，可通过传入不同用户的header来划转，参数可以自定义，不传参数使用默认参数,默认向该账户转入1000usdt
    def transfer(self,parm=None,header=None):
        path = fund_request_data.get('balance_transfer').get('path')
        method = fund_request_data.get('balance_transfer').get('method')
        default_parm = {
            'amount': '5000',
            'billSide': 'ADD',
            'coin': 'usdt'
        }
        if not parm:
            parm = default_parm
        if not header:
            header = generate_auth_info(path=path,method=method)
        url = self.thanos_http_url + fund_request_data.get('balance_transfer').get('path')
        res = requests.request(method=method, url=url,data=parm, headers=header).json()
        return res


if __name__ == '__main__':
    b = Balance()
    print(b.list())
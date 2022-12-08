from api.thanos_http import xtthanos_trade_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def order_entrust_cancel_all(symbol,test_user='test_user'):
    '''撤销所有委托'''
    result = ResultBase()
    order_entrust_cancel_all = request_data.get('order_entrust_cancel_all')
    params = {
        "symbol":symbol,
    }
    path = order_entrust_cancel_all.get('route') + order_entrust_cancel_all.get('path')
    method = order_entrust_cancel_all.get('method')
    headers = generate_auth_info(path=path, method=method, params=params, bodymod='x-www-form-urlencoded',test_user=test_user)
    res = xtthanos_trade_http.order_entrust_cancel_all(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()

    logger.info(f"撤销所有委托 返回结果 ==>> {res.text}")
    return result


if __name__ == '__main__':
    order_entrust_cancel_all('dao_usdt')
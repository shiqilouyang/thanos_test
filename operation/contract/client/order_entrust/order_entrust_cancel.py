from api.thanos_http import xtthanos_trade_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def order_entrust_cancel(id,type):
    '''撤销委托'''
    result = ResultBase()
    order_entrust_cancel = request_data.get('order_entrust_cancel')
    params = {
        "id":id,
        "type":type
    }
    path = order_entrust_cancel.get('route') + order_entrust_cancel.get('path')
    method = order_entrust_cancel.get('method')
    headers = generate_auth_info(path=path, method=method, params=params, bodymod='x-www-form-urlencoded')
    res = xtthanos_trade_http.order_entrust_cancel(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"撤销委托 返回结果 ==>> {res.text}")
    return result
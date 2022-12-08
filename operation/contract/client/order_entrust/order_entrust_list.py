from api.thanos_http import xtthanos_trade_http, request_data
from api.http_api import ResultBase
from common.logger import logger
from common.get_signature import generate_auth_info


def order_entrust_list(scene,endTime,forceClose,page,size,startTime,state,symbol,type):
    '''查询全部委托'''
    result = ResultBase()
    order_entrust_cancel_list = request_data.get('order_entrust_cancel_list')
    params = {
        "endTime":endTime,
        "forceClose":forceClose,
        "page":page,
        "size":size,
        "startTime":startTime,
        "state":state,
        "symbol":symbol,
        "type":type
    }
    path = order_entrust_cancel_list.get('route') + order_entrust_cancel_list.get('path')
    method = order_entrust_cancel_list.get('method')
    headers = generate_auth_info(path=path, method=method, params=params)
    res = xtthanos_trade_http.order_entrust_list(headers=headers, params=params)
    result.status_code = res.status_code
    result.response = res.json()
    logger.info(f"查询全部委托 返回结果 ==>> {res.text}")
    return result
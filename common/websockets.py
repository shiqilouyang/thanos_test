#coding=utf-8
import json
import os
from websocket import create_connection

from common.read_data import ReadFileData

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
data = ReadFileData().load_ini(data_file_path)["websockets"]



def get_sub_mark_price(symbol):
    ''' 实时获取标记价格 '''
    from common.get_signature import generate_auth_info_for_test
    # 获取 token
    token = generate_auth_info_for_test()
    ws = create_connection(data.get("url"))
    # 监听 标记价格参数
    params = {"req":"sub_mark_price", "token":token.get("Authorization")}
    ws.send(json.dumps(params))
    ws.recv()
    is_open = True
    num = 0
    while is_open:
        result = ws.recv()
        results = json.loads(result)
        if results.get("data").get("s") == symbol:
            ws.close()
            return results
        else:
            num += 1
            # 避免一直循环下去，此参数管理循环次数
            if num >= int(data.get("num")):
                ws.close()
                return {}





if __name__ == '__main__':
    print(get_sub_mark_price("dao_usdt"))

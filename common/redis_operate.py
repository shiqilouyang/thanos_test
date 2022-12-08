#!/usr/bin/python
# -*- encoding: utf-8 -*-
from pprint import pprint

import redis
import os
from common.read_data import ReadFileData

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
data = ReadFileData().load_ini(data_file_path)["redis"]

DB_CONF = {
    "host": data["REDIS_HOST"],
    "port": int(data["REDIS_PORT"]),
    "db": int(data["DB"]),
    "password": data["REDIS_PASSWD"],
    'username': data['REDIS_USER']
}

class RedisData:

    def __init__(self,db_conf=DB_CONF):
        self.conn = redis.StrictRedis(**db_conf, decode_responses=True,ssl=True)

    def __del__(self):  # 对象资源被释放时触发，在对象即将被删除时的最后操作
        # 关闭游标
        self.conn.close()
#
    def get_keys(self):
        '''获取redis所有key'''
        return self.conn.keys()

    def get_type_keys(self,keys):
        '''获取redis key 的类型
          eg: keys = user_balance:116
          '''
        return self.conn.type(keys)

    def get_symbol_deal(self,symbol,min,max):
        '''获取交易对所有成交价格'''
        key = 'RECENT_DEAL:{}'.format(symbol)
        return self.conn.zrange(key,min,max)

    def get_user_info(self,userId):
        '''获取用户订单信息'''
        key = 'user:'+userId
        res = self.conn.hgetall(key)
        return self.conn.hgetall(key)

    def get_balance(self,userId):
        key = 'user_balance:' + userId
        return self.conn.hgetall(key)

    def get_index_price(self,symbol):
        '''获取交易所价格'''
        key = 'PRICE:INDEX:MAP:' + symbol
        return self.conn.hgetall(key)

    def get_order_deep(self):
        '''获取订单深度'''
        key = 'ORDER_DEEP:1:2'
        return self.conn.hgetall(key)

    def get_1(self):
        key = 'BEST_PRICE:1:1'
        print(self.conn.hgetall(key))


redis_cli = RedisData()

if __name__ == '__main__':
    redis_cli = RedisData()
    pprint(redis_cli.get_keys())
    # pprint(redis_cli.get_symbol_deal("dao_usdt"))
    # pprint(redis_cli.conn.get('RECENT_DEAL:dao_usdt'))
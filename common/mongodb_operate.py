#!/usr/bin/python
# -*- encoding: utf-8 -*-

import pymongo
import os
from common.read_data import ReadFileData

BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
data_file_path = os.path.join(BASE_PATH, "config", "setting.ini")
data = ReadFileData().load_ini(data_file_path)["mongo"]

DB_CONF = {
    "url": data["MONGO_URL"],
    "db": data["MONGO_DB"],
    'col': data["MONGO_COL"],
}


class MongoDb():

    def __init__(self, arg=None, db_conf=DB_CONF):
        if arg:
            DB_CONF.update(arg)
        # 通过字典拆包传递配置信息，建立数据库连接
        self.client = pymongo.MongoClient(db_conf["url"])
        # 连接数据库
        self.db = self.client[db_conf["db"]]
        # print(f'数据库所有集合信息：{self.db.list_collection_names()}')
        # 连接指定集合
        self.db_col = self.db[db_conf["col"]]

    def __del__(self):
        # 断开连接
        self.client.close()

    def find_one(self, data):
        """查询一条数据"""
        return self.db_col.find_one(data)

    def find(self, data):
        """查询所有数据"""
        return self.db_col.find(data)

    def insert_one(self, data):
        '''插入单条数据'''
        return self.db_col.insert_one(data)

    def insert_many(self, data):
        '''插入多条数据'''
        return self.db_col.insert_many(data)

    def update_one(self, data, up_data):
        '''更新一条数据'''
        return self.db_col.update_one(data, up_data)

    def update_many(self, query, up_data):
        '''更新多条数据'''
        return self.db_col.update_many(query, up_data)

    def delete_one(self, data):
        '''删除一条数据'''
        return self.db_col.delete_one(data)

    def delete_many(self, dta):
        '''删除多条数据'''
        return self.db_col.delete_many(data)

    def drop(self):
        '''删除集合'''
        return self.db_col.drop()

    def update_col(self, col_name):
        '''更新连接的集合'''
        self.db_col = self.db[col_name]

    def descending_sort_find(self, query, sort_field, limit=None):
        """根据条件降序排序和截取ascending"""
        try:
            if limit:
                return [value for value in self.db_col.find(query).sort(sort_field, -1).limit(limit)]
            else:
                return [value for value in self.db_col.find(query).sort(sort_field, -1)]
        except Exception as e:
            return None

    def ascending_sort_find(self, query, sort_field, limit=None):
        """根据条件升序排序和截取descending"""
        try:
            if limit:
                return [value for value in self.db_col.find(query).sort(sort_field, 1).limit(limit)]
            else:
                return [value for value in self.db_col.find(query).sort(sort_field, 1)]
        except Exception as e:
            return None

    def get_list_by_find(self, query):
        """查询结果返回list"""
        return [value for value in self.db_col.find(query)]

    # 统计查询结果的总数
    def get_find_count(self, query={}):
        return self.db_col.find(query).count()
    
    def get_repeat_date(self, field}):
        # 查找集合中有重复的数据，显示重复的数据和重复的个数
        pipeline =[
            { $group: { _id : '${}'.format(field), count: { $sum : 1 } } },
            { $match: { count: { $gt : 1} } }
          ]
        return list(db.db_col.aggregate(pipeline))
        
    '''
        db.getCollection('users').aggregate([
        { $group: { _id : '$openid', count: { $sum : 1 } } },
        { $match: { count: { $gt : 1} } }
      ])
    '''

def update_account_balance(data):
    '''更新账户余额'''
    account_id = DB_CONF["id"]
    query = {'userId': int(account_id)}
    print(query, {'$set': data})
    MongoDb().update_one(query, {"$set": data})


if __name__ == '__main__':
    args = {
        "col": "order",
    }
    res = MongoDb(args).find({
        '_id': 41299220258368384
    })
    print(res.count())

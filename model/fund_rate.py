#!/usr/bin/env python
# -*- encoding: utf-8 -*-
'''
@File    :   fund_rate.py    
@Contact :   shuai.xu

@Modify Time      @Author    @Version    @Desciption
------------      -------    --------    -----------
2022/2/9 5:34 下午   shuai.xu      1.0         None
'''
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from model import  app
# 绑定 flask 对象, 每一个数据库文件都要绑定 app
db = SQLAlchemy(app)

class fund_rate(db.Model):
    # 表名称
    __tablename__ = 'fund_rate'

    id = Column(String(3), primary_key=True)
    symbol_id = Column(String(50), nullable=False)
    collection_interval = Column(String(10), nullable=False)


    def __str__(self):
        # 为数据库字段进行重新命名
        return str({
            "id" :self.id,
            "symbol_id" : self.symbol_id ,
            "collection_interval" : self.collection_interval
        })

    def tostr(self):
        import json
        return json.dumps(self.__str__())



if __name__ == '__main__':
    print(fund_rate.query.filter(fund_rate.symbol_id == 39).first().collection_interval)
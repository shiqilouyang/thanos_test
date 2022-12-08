from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from model import  app
# 绑定 flask 对象, 每一个数据库文件都要绑定 app
db = SQLAlchemy(app)

class exchange_coin(db.Model):
    # 表名称
    __tablename__ = 'exchange_coin'

    id = Column(String(3), primary_key=True)
    coin = Column(String(50), nullable=False)
    is_exchange = Column(String(10), nullable=False)
    is_open = Column(String(10), nullable=False)
    display_precision = Column(String(10))
    actual_precision = Column(String(10))
    creator = Column(String(10))
    created_time = Column(String(10))
    updater = Column(String(10))
    updated_time = Column(String(10))


    def __str__(self):
        # 为数据库字段进行重新命名
        return str({
            "coin" :self.coin,
            "isExchange" : self.is_exchange ,
            "isOpen" : float(self.is_open),
            'displayPrecision' : float(self.display_precision),
            'actualPrecision' : float(self.actual_precision),
            'reator' :self.creator,
            "createdTime":self.created_time,
            "updater":self.updater,
            "updatedTime":self.updated_time
            })

    def tostr(self):
        import json
        return json.dumps(self.__str__())


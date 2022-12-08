from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from model import  app
# 绑定 flask 对象, 每一个数据库文件都要绑定 app
db = SQLAlchemy(app)

class account_info(db.Model):
    ''' 使用 nullable/String 来限制字符串数据库字段  '''
    __tablename__ = 'account_info'

    account_id = Column(String(3), primary_key=True)
    user_id = Column(String(50), nullable=False)
    user_group_id = Column(String(10), nullable=False)
    allow_transfer = Column(String(10), nullable=False)
    allow_trade = Column(String(10), nullable=False)
    allow_open_position = Column(String(10), nullable=False)
    open_time = Column(String(10), nullable=False)
    type = Column(String(10), nullable=False)

    def __str__(self):
        # 为数据库字段进行重新命名
        return str({
                "accountId":self.account_id,
                "userId":self.user_id,
                "allowTransfer": True if self.allow_transfer !=0 else False,
                "allowTrade":True if self.allow_transfer !=0 else False,
                "allowOpenPosition":True if self.allow_transfer !=0 else False,
                "openTime":self.open_time.strftime("%Y-%m-%dT%H:%M:%S"),  # 数据库时间字段转换成 24小时时间字符串
            "state":self.type
            })

    def tostr(self):
        import json
        return json.dumps(self.__str__())


if __name__ == '__main__':
    import json
    article1 = account_info.query.filter(account_info.account_id == 2).first()
    print(json.loads(article1.tostr()))
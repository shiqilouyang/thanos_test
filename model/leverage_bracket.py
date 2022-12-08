from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String
from model import  app
# 绑定 flask 对象, 每一个数据库文件都要绑定 app
db = SQLAlchemy(app)

class leverage_bracket(db.Model):
    # 表名称
    __tablename__ = 'leverage_bracket'

    id = Column(String(3), primary_key=True)
    symbol_id = Column(String(50), nullable=False)
    symbol_group_id = Column(String(10), nullable=False)
    bracket = Column(String(10), nullable=False)
    max_qty = Column(String(10), nullable=False)
    # 最大名义价值
    max_nominal_value = Column(String(10))
    # 维持保证金率
    maint_margin_rate = Column(String(10))
    # 其实保证金率
    start_margin_rate = Column(String(10))
    # max_start_margin_rate = Column(String(10))
    max_leverage = Column(String(10), nullable=False)
    min_leverage = Column(String(10), nullable=False)


    def __str__(self):
        # 为数据库字段进行重新命名
        return str({
            "symbol" :self.symbol_id,
            "bracket" : self.bracket ,
            "maxNominalValue" : float(self.max_nominal_value),
            'maintMarginRate' : float(self.maint_margin_rate),
            'startMarginRate' : float(self.start_margin_rate),
            'maxStartMarginRate' : None,
            "maxLeverage":self.max_leverage,
            "minLeverage":self.min_leverage
            })

    def tostr(self):
        import json
        return json.dumps(self.__str__())


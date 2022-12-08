from flask_mongoengine import MongoEngine

from model import app

db = MongoEngine(app)

class Order(db.Document):
      meta = {
            'collection': 'order',
            'ordering': ['-create_at'],
            'strict': False,
      }
      accountId = db.StringField(required=True, max_length=200)
      avgPrice  = db.StringField(required=True, max_length=200)

      def __str__(self):
            return 'User(email="{}", username="{}")'.format(self.username, self.password)


print(Order.objects().first())

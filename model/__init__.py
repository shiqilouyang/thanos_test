import pymysql
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://thanos_admin:YbNmkTD4DMVgxvCeTest@thanos-test.c2bgxjastqgq.ap-southeast-1.rds.amazonaws.com:3306/thanos?charset=utf8mb4'
# app.config['MONGODB_SETTINGS'] = {
#      "db" : "thanos",
#      "host" : 'mongodb+srv://thanos_test:tLXPWF68%40run@cluster0.2ksbi.mongodb.net/myFirstDatabase?retryWrites=true&w=majority',
# }


app.config['MONGODB_SETTINGS'] = {
     "db" : "thanos",
     "host" : 'cluster0.2ksbi.mongodb.net',
     'username': 'thanos_test',
     'connect': True,
     'password': 'tLXPWF68%40run',
}
db = SQLAlchemy(app)

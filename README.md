# pytest_framework 自动化测试框架
### 项目结构
```
api ====>> 接口封装层，包括封装HTTP接口为Python接口和requests请求方法封装
common ====>> 各种工具类
config ====>> 配置文件
data ====>> 测试数据文件管理
log =====>> 测试日志
operation ====>> 关键字封装层，如把多个Python接口封装为关键字
pressureTest ====>> 常用的几种场景编写的压测脚本
test_cases ====>> 测试用例
pytest.ini ====>> pytest配置文件
```

### jenkins 发版后的测试报告位置
```angular2html
<!-- html 报告-->
http://thanos-test-report.xtthanos.com

<!--log 报告,log按照天来生成-->
http://thanos-test-report.xtthanos.com/log

<!--gunicorn log-->
http://thanos-test-report.xtthanos.com/log/log

<!--重跑测试用例-->
http://thanos-test-report.xtthanos.com/rerun
```

### 使用流程
1,下载code(配置免密登录)
```
git clone -b xs_thanos_test \
   ssh://git@gitssh.hmswork.space:8222/thanos_test/thanos_test.git
```
2,安装对应依赖
```angular2html
pip3 install -i https://pypi.doubanio.com/simple/ \
    -r requirements.txt
```
3,test_cases/* 编写测试代码

4,run.py文件中修改测试接口,运行测试脚本
```angular2html
   py3 run.py
```
5,生成测试报告
```angular2html
report/report.html
```
6,只跑主流程的测试用例(冒烟),默认不开启
```angular2html
  1. config/setting.ini 设置is_Smoking_Test = 1, 开启Smoking_Test
  2, py3 run.py # 运行pytest项目
  3, 只会跑以main-开头的scene/name 的测试用例.
```
### 开发须知
1,开发流程
```angular2html
  1,   开发人员写完自己的测试代码，将代码推到自己的分支之中，
     待代码稳定，然后合并到master之中。
  2, 开发过程之中，希望按照项目目录结构进行开发
```
2,注释
```
   1,文件注释:关于这个Python文件实现的功能一些注意点，可能会发生的错误
   2,类注释
   3,方法注释
   4,关键部分进行注释:重要代码/调用其他服务代码/逻辑代码
```
### 自动化项目分布式执行与测试报告高并发处理
1,使用 pytest-xdist 插件处理项目分布式,进程级别的并发

```angular2html
<!-- 1, 需要安装 pytest-xdist插件
     2, -vs 启动该插件  -n auto 自动检测系统的cpu数 -->
      pytest -vs test_cases/contract/client/order_entrust -n auto
```
2,测试报告高并发
```angular2html
<!--  使用 gunicorn + gevent 方式异步处理并发, 支持并发数 worker * worker-connections = 4000-->
        gunicorn -w4 -b 0.0.0.0:8081  --access-logfile ./log/log.log \
            --worker-connections 1000 -k 'gevent' -preload  report.app:app
```
### 常见问题
1,pytest-html 中文乱码问题
```
# 修改文件 ./site-packages/pytest_html/plugin.py
代码部分:
  # self.test_id = report.nodeid.encode("utf-8").decode("unicode_escape")
改为:
  # self.test_id = report.nodeid
```
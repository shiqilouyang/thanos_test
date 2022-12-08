# -*- coding: utf-8 -*-
import os
import time
from concurrent.futures.thread import ThreadPoolExecutor

import pytest
from flask import Flask, render_template, jsonify, redirect, url_for, Response
from common.logger import logger

executor = ThreadPoolExecutor(2)


app = Flask(__name__,template_folder='../report/templates')
# 支持中文显示
app.config['JSON_AS_ASCII'] = False


@app.route('/<html_name>')
def html(html_name):
    try:
        return render_template('{}-report.html'.format(html_name))
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


@app.route('/')
def index():
    try:
        return redirect(url_for('html',html_name=time.strftime("%Y%m%d")))
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


@app.route('/log')
def index_log():
    try:
        return redirect(url_for('log',file_name=time.strftime("%Y%m%d")))
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


@app.route('/log/<file_name>')
def log(file_name):
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    log_fil = os.path.join(BASE_PATH, "log","{}.log{}".format(file_name.split("-")[0] \
              if '-' not in file_name.split("-") else file_name.split("-")[0],\
                       "."+ file_name.split("-")[1] \
                            if '-'  in file_name else "" ))
    logger.info("加载日志文件{}".format(log_fil))
    try:
        resp = Response(open(log_fil).read(),mimetype='text/plain')
        return resp
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


def task1():
    BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
    testpaths = os.path.join(BASE_PATH, 'test_cases', 'contract', 'client')
    report_path = os.path.join(os.path.join(BASE_PATH, "report"), 'templates')
    pytest.main(['-s', testpaths, '--capture=sys', '--junit-xml={}/{}-report.xml' \
                    .format(report_path,time.strftime("%Y%m%d")), \
                     '--html={}/{}-report.html'.format(report_path,time.strftime("%Y%m%d"))])


@app.route('/rerun')
def rerun():
    try:
        BASE_PATH = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        testpaths = os.path.join(BASE_PATH, 'test_cases', 'contract', 'client')
        # 异步重启测试用例
        executor.submit(task1)
        return jsonify({"message":"重新运行测试用例","测试路径":testpaths,"测试时间":\
             time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),'测试项目':'contract'})
    except Exception as e:
        return jsonify({"code": "异常", "message": "{}".format(e)})


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8081,debug=False)

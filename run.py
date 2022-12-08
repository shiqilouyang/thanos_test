#!/usr/bin/python
# -*- encoding: utf-8 -*-
import os
import time
import pytest

if __name__ == '__main__':
    pytest.main(['-s','test_cases/contract/client','--capture=sys','--junit-xml=report/templates/{}-report.xml'\
                .format(time.strftime("%Y%m%d")),\
                 '--html=report/templates/{}-report.html'.format(time.strftime("%Y%m%d"))])
    os.system(" \
     gunicorn -w4 -b 0.0.0.0:8081  --access-logfile ./log/log.log --worker-connections 1000 -k 'gevent' -preload  report.app:app")

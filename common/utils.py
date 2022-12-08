#!/usr/bin/python
# -*- encoding: utf-8 -*-

import os
import sys
import time
from datetime import datetime

def caught_exception():
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    print(exc_type, fname, exc_tb.tb_lineno)

_sequence = int(datetime.utcnow().timestamp())%10000*100000

def nex_sequence():
    global _sequence
    _sequence += 1
    return _sequence


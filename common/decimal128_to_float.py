#!/usr/bin/python
# -*- encoding: utf-8 -*-
from bson.decimal128 import Decimal128

def decimal_to_float(num):
    return float(Decimal128(str(num)).to_decimal())
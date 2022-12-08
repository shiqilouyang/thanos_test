#!/usr/bin/python
# -*- encoding: utf-8 -*-

from operation.contract.client.order import create_order
import random
import time
from operation.contract.client.quote import get_depth


def order_range():
    while True:
        price = random.randint(0,5)
        num = random.randint(2,5)
        get_depth(50, "cfx_usdt")
        create_order('SELL', 'LIMIT', num, 'SHORT', 'cfx_usdt', '', price, '', 'GTC', '', '', '5566')
        get_depth(50, "cfx_usdt")
        create_order('BUY', 'MARKET', num, 'LONG', 'cfx_usdt', 1, '', '', 'IOC', '', '', '5566')
        get_depth(50, "cfx_usdt")
        time.sleep(60)

if __name__ == '__main__':
    order_range()
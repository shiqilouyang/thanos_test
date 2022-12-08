#!/usr/bin/python
# -*- encoding: utf-8 -*-
import websocket
import threading
import time
from common.read_data import get_data

api_wss_url = get_data().get_ini_data("host","binance_wss_url")
def on_message(self, ws, message):
    print(message)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

class wss_api():
    def __init__(self, api_wss_url):
        self.api_wss_url = api_wss_url

    def _ws_func(self,stream_api):
        websocket.enableTrace(True)
        ws = websocket.WebSocketApp(self.api_wss_url + '/ws/' +stream_api,
                                  on_message = on_message,
                                  on_error = on_error,
                                  on_close = on_close)
        ws.run_forever(sslopt={"check_hostname": False})

    def start(self,stream_api):
        self.__thread = threading.Thread(target=self._ws_func, args=[stream_api])
        self.__thread.start()

if __name__ == '__main__':
    # print(api_wss_url)
    wss_api = wss_api(api_wss_url)

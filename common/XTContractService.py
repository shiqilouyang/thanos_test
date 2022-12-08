from XTContractUtils import http_get_request, api_key_get, api_key_post


class XT:
    def __init__(self, url, access_key, secret_key):
        self.__url = url
        self.__access_key = access_key
        self.__secret_key = secret_key
        # print(self.__url)

    def get_funding_rate(self, symbol):
        """
        :return:获取资金费率
        """
        params = {"symbol": symbol}
        url = self.__url + "/future/market" + '/v1/public/q/funding-rate'
        return http_get_request(url, params=params)

    def get_agg_tiker(self, symbol):
        """
        :return:返回聚合行情
        """
        params = {"symbol": symbol}
        url = self.__url + "/future/market" + '/v1/public/q/agg-ticker'
        return http_get_request(url, params=params)

    def get_last_price(self, symbol, length):
        """
        :return:获取最近成交记录
        """
        params = {"symbol": symbol, "num": length}
        url = self.__url + "/future/market" + '/v1/public/q/deal'
        return http_get_request(url, params=params)

    def get_depth(self, symbol, depth):
        """
        :return:获取深度数据
        """
        params = {"symbol": symbol, "level": depth}
        url = self.__url + "/future/market" + '/v1/public/q/depth'
        return http_get_request(url, params=params)

    def get_account_capital(self):
        """
        :return:获取账户资金
        """

        bodymod = "application/x-www-form-urlencoded"
        path = "/future/user" + '/v1/balance/list'
        url = self.__url + path
        return api_key_get(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                           bodymod=bodymod, params={})

    def send_order(self, symbol, price, amount, order_side, order_type, position_side):
        """
        :return:获取账户资金
        """
        params = {"orderSide": order_side,
                  "orderType": order_type,
                  "origQty": amount,
                  "positionSide": position_side,
                  "symbol": symbol,
                  "price": price}

        bodymod = "application/x-www-form-urlencoded"
        path = "/future/trade" + '/v1/order/create'
        url = self.__url + path
        return api_key_post(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                            bodymod=bodymod, params=params)

    def get_history_order(self):
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/trade" + '/v1/order/list-history'
        url = self.__url + path
        return api_key_get(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                           bodymod=bodymod, params={})

    def get_account_order(self, symbol, state, page, size):
        """
        state:
        订单状态 NEW：新建订单（未成交）；
        PARTIALLY_FILLED：部分成交；
        FILLED：全部成交；CANCELED：用户撤销；
        REJECTED：下单失败；EXPIRED：已过期；
        UNFINISHED：未完成；HISTORY：（历史）
        """
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/trade" + '/v1/order-entrust/list'
        url = self.__url + path
        params = {
            "symbol": symbol,
            "state": state,
            "page": page,
            "size": size
        }
        return api_key_get(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                           bodymod=bodymod, params=params)

    def cancel_order(self, order_id):
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/trade" + '/v1/order/cancel'
        url = self.__url + path
        params = {
            "orderId": order_id
        }
        return api_key_post(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                            bodymod=bodymod, params=params)

    def cancel_all_order(self, symbol):
        bodymod = "json"
        path = "/future/trade" + '/v1/order/cancel-all'
        url = self.__url + path
        params = {
            "symbol": symbol
        }
        return api_key_post(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                            bodymod=bodymod, params=params)

    def get_index_price(self, symbol, size):
        """
        :return:获取深度数据
        """
        params = {"symbol": symbol, "size": size}
        url = self.__url + "/future/market" + '/v1/public/q/symbol-mark-price'
        return http_get_request(url, params=params)

    def get_order_id(self, order_id):
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/api" + '/v1/order/detail'
        url = self.__url + path
        params = {
            "orderId": order_id
        }
        return api_key_get(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                           bodymod=bodymod, params=params)

    def get_batch_order_id(self, order_id_list: list):
        bodymod = "application/x-www-form-urlencoded"
        path = "/future/trade" + '/v1/order/list-by-ids'
        url = self.__url + path
        order_id_query = ",".join(order_id_list)
        params = {
            "ids": order_id_query
        }
        return api_key_post(path=path, url=url, access_key=self.__access_key, secret_key=self.__secret_key,
                            bodymod=bodymod, params=params)


if __name__ == '__main__':
    # {"id":9,
    # "userAccountId":"1493425198580502530",
    # "userAccountLevel":1,
    # "userId":130955,
    # "userName":"13636468690",
    #
    # "keyName":"测试4",
    # "bindIps":null,
    # "accessKey":"3976eb88-76d0-4f6e-a6b2-a57980770085",
    # "secretKey":"bc6630d0231fda5cd98794f52c4998659beda290",
    # "payOutPwd":null,"isLock":0,"isAct":1,"isDel":0,"roleScopes":"QUERY_NO_TRADE","tags":"测试","createId":null,"updateId":null,"createTime":"2022-02-16 11:29:45.000","updateTime":"2022-03-02 16:26:43.000"}
    TestAddress = "http://api-thanos-test.xtthanos.com"
    xt = XT(url=TestAddress, access_key='ea81f569-9f44-4833-929b-b7c47088c3cf',
            secret_key='cd26a5b1f4f6304460d7ebaa68cf676070e9f1fa')
    # res = xt.get_funding_rate("btc_usdt")
    # print(res)
    # #
    # res = xt.get_agg_tiker("btc_usdt")
    # print(res)
    # #
    # res = xt.get_last_price("btc_usdt", 10)
    # print(res)
    # #
    # res = xt.get_depth("btc_usdt", 10)
    # print(res)
    #
    # res = xt.get_account_capital()
    # print(res)
    #
    # res = xt.send_order(symbol="btc_usdt", price=40001, amount=10, order_side="BUY", order_type="LIMIT",
    #                     position_side="LONG")
    # print(res)

    # 开多 BUY - LONG
    # 平多 SELL - LONG
    # 开空 SELL - SHORT
    # 平空 BUY - SHORT

    # res = xt.get_batch_order_id(order_id_list=['71676480133190912'])
    # print(res)

    # res = xt.get_history_order()
    # print(res)

    # res = xt.get_account_order(symbol="btc_usdt", state="FILLED", page=1, size=100)
    # print(res)

    res = xt.cancel_order(order_id='72509073051892352')
    print(res)

    # res = xt.cancel_all_order(symbol='dao_usdt')
    # print(res)
    # res = xt.get_index_price(symbol="btc_usdt", size=1)
    # print(res)

    # res = xt.get_index_price(symbol="btc_usdt", size=1)
    # print(res)

    # 准生产环境吃单后，订单薄没有改变

    # 问题描述：返回账户资产接口403
    # url:'http://fapi.ifunv.com/future/user/v1/balance/list'
    # hearder:{'Content-type': 'application/x-www-form-urlencoded', 'xt-validate-appkey': '0a10789e-af1b-4f35-ab5d-cf4ba1577a79', 'xt-validate-timestamp': '1646808973823', 'xt-validate-signature': '3397ba5636420f7f3941eefa4c05842452d77253b04873220ab90c0078242e64', 'xt-validate-algorithms': 'HmacSHA256'}

    # 问题描述：批量获取订单状态接口200 没有数据
    # url:'http://fapi.ifunv.com/future/trade/v1/order/list-by-ids?ids=71676480133190912'
    # hearder:{'Content-type': 'application/x-www-form-urlencoded', 'xt-validate-appkey': '0a10789e-af1b-4f35-ab5d-cf4ba1577a79', 'xt-validate-timestamp': '1646809660543', 'xt-validate-signature': '1b59416942b05869e6ee1f14dea8381ae4668fca8ec434980c55e6fa276b467c', 'xt-validate-algorithms': 'HmacSHA256'}
    # params:'ids':'71676480133190912'

    # 问题描述：下单接口502错误
    # url:'http://fapi.ifunv.com/future/trade/v1/order/create'
    # hearder:{'xt-validate-appkey': '0a10789e-af1b-4f35-ab5d-cf4ba1577a79', 'xt-validate-timestamp': '1646819791215', 'xt-validate-signature': '0b56e60bdb52987bf80b53e170fcdcec23640e8c1d0a990fa526ecc481a4a114', 'xt-validate-algorithms': 'HmacSHA256'}
    # params:{'orderSide': 'BUY', 'orderType': 'LIMIT', 'origQty': 100, 'positionSide': 'LONG', 'symbol': 'btc_usdt', 'price': 40001}

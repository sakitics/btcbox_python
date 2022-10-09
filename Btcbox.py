#!/usr/bin/python
# -**- coding:utf8 -**-
import time
import hashlib
import hmac
import json
from typing import Dict

import configparser
import numpy
import requests


class Btcbox:

    def __init__(self) -> None:

        config: configparser.ConfigParser = configparser.ConfigParser()
        config.read("config.ini")
        self.base: str = config.get("DEEP", "base")
        self.symbol: str = config.get("DEEP", "coin")
        self.key: str = config.get("DEEP", "key")
        self.sec: str = config.get("DEEP", "sec")

        self.price: int = 0
        self.symbol_coin: str = self.symbol.upper() + "/JPY"

        print(self.symbol_coin)

    @staticmethod
    def nonce() -> str:
        return str(int(time.time() * 1000))

    def signature(self, param_dic: Dict) -> str:
        msg: str = ""
        for index, (key, val) in enumerate(param_dic.items()):
            msg += str(key) + "=" + str(val)
            if index < len(list(param_dic.keys())) - 1:
                msg += "&"

        param_bin: bytes = bytes(msg, "utf8")
        api_secret_md5: str = hashlib.md5(self.sec.encode()).hexdigest()
        secret: bytes = bytes(api_secret_md5, "utf8")

        return hmac.new(secret, param_bin,
                        digestmod=hashlib.sha256).hexdigest()

    def base_dic_sig(self) -> Dict:
        return {"key": self.key, "nonce": self.nonce()}

    # 1.1 ticker public
    def ticker(self) -> None:
        url: str = self.base + "/api/v1/ticker/?coin=" + self.symbol
        res: Dict = requests.get(url).json()
        self.price = numpy.mean([res["buy"], res["sell"]])

        print("ticker\n url: %s\n result: %s \n price: %d "
              "\n---------------" % (url, json.dumps(res), self.price))

    # 1.2 depth public
    def deep(self) -> None:
        url: str = self.base + "/api/v1/depth/?coin=" + self.symbol
        res: Dict = requests.get(url).json()

        print("deep\n url: %s \n deep: %s "
              "\n---------------" % (url, json.dumps(res)))

    # 1.3 orders public
    def orders(self) -> None:
        url: str = self.base + "/api/v1/orders?coin=" + self.symbol
        res: Dict = requests.get(url).json()

        print("orders\n url: %s \n result: %s "
              "\n---------------" % (url, json.dumps(res)))

    # 1.4 balance
    def balance(self) -> None:
        url: str = self.base + "/api/v1/balance"
        param: Dict = self.base_dic_sig()
        param["signature"] = self.signature(param)
        res: Dict = requests.post(url, param).json()

        print("balance\n url: %s \n result: %s "
              "\n---------------" % (url, json.dumps(res)))

    # 1.5 wallet
    def wallet(self) -> None:
        url: str = self.base + "/api/v1/wallet?coin=" + self.symbol
        param: Dict = self.base_dic_sig()
        param["signature"] = self.signature(param)
        res: Dict = requests.post(url, param).json()

        print("wallet\n url: %s \n result: %s "
              "\n---------------" % (url, json.dumps(res)))

    # 1.6 trade_list
    def trade_list(self) -> None:
        url: str = self.base + "/api/v1/trade_list"
        param: Dict = self.base_dic_sig()
        param["signature"] = self.signature(param)
        res: Dict = requests.post(url, param).json()

        print("trade_list\n url: %s \n result: %s "
              "\n---------------" % (url, json.dumps(res)))

    # 1.7 trade_view
    def trade_view(self, order_id: str = "") -> None:
        url: str = self.base + "/api/v1/trade_view"
        param: Dict = self.base_dic_sig()
        param["id"] = order_id
        param["signature"] = self.signature(param)
        res: Dict = requests.post(url, param).json()

        print("trade_view\n url: %s \n result: %s "
              "\n---------------" % (url, json.dumps(res)))

    # 1.8 trade_cancel
    def trade_cancel(self, order_id: str = "") -> None:
        url: str = self.base + "/api/v1/trade_cancel"
        param: Dict = self.base_dic_sig()
        param["id"] = order_id
        param["signature"] = self.signature(param)
        res: Dict = requests.post(url, param).json()

        print("trade_cancel\n url: %s \n result: %s "
              "\n---------------" % (url, json.dumps(res)))

    # 1.9 trade_add
    def trade_add(self, direction: str = "buy", amount: float = 0.0,
                  price: int = 0) -> None:
        url = self.base + "/api/v1/trade_add"
        param = self.base_dic_sig()
        param["amount"] = float(amount)
        param["coin"] = self.symbol
        param["type"] = direction
        param["price"] = int(numpy.ceil(price))
        param["signature"] = self.signature(param)
        res: Dict = requests.post(url, param).json()

        print("trade_add\n url: %s \n result: %s "
              "\n---------------" % (url, json.dumps(res)))


if __name__ == "__main__":

    box = Btcbox()

    try:
        # 1.1 ticker
        box.ticker()
        # 1.2 depth
        box.deep()
        # 1.3 orders
        box.orders()
        # 1.4 balance
        box.balance()
        # 1.5 wallet
        box.wallet()
        # 1.6 trade_list
        box.trade_list()
        # 1.7 trade_view
        box.trade_view("889554")
        # 1.8 trade_cancel
        box.trade_cancel("889554")
        # 1.9 trade_add
        box.trade_add("buy", 0.001, box.price)

    except Exception as exc:
        print("error：" + str(exc))

    else:
        pass

    finally:
        del box

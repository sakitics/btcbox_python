import datetime
import json
import time
import traceback
import urllib.parse

import numpy
import pandas
import requests


class Btcbox(object):

    __nan: float = numpy.nan

    endpoint: str = "https://www.btcbox.co.jp/api/v1"
    exchange: str = "btcbox"
    markets: dict = {
        "btcjpy": {
            "pair": "BTC_JPY",
            "symbol": "btc",
        },
        "bchjpy": {
            "pair": "BCH_JPY",
            "symbol": "bch",
        },
        "ltcjpy": {
            "pair": "LTC_JPY",
            "symbol": "ltc",
        },
        "ethjpy": {
            "pair": "ETH_JPY",
            "symbol": "eth",
        },
        "dogejpy": {
            "pair": "DOGE_JPY",
            "symbol": "doge",
        },
        "dotjpy": {
            "pair": "DOT_JPY",
            "symbol": "dot",
        },
        "trxjpy": {
            "pair": "TRX_JPY",
            "symbol": "trx",
        },
    }
    request_retry: int = 3
    request_retry_interval: float = 0.3
    request_timeout: float = 3.0
    timezone: str = "Asia/Tokyo"

    def __init__(self) -> None:
        pass

    @staticmethod
    def create_nonce():
        return str(int(time.time() * 10000000))

    # TODO: Unimplemented
    def fetch_balance(self) -> tuple[dict, int]:
        data = {
            "id": "",
            "exchange": self.exchange,
            "timestamp": datetime.datetime.now().timestamp(),
        }
        status_code = 500

        return data, status_code

    def fetch_ohlc(self, pair: str = "btcjpy", side: str = "sell", timeframe: str = "60S") -> dict:
        orders, _ = self.fetch_orders(pair)
        orders_table: pandas.core.frame.DataFrame = pandas.DataFrame(orders)
        orders_table.index = pandas.to_datetime(orders_table["timestamp"], unit="s", utc=True)
        ohlc_table: pandas.core.frame.DataFrame = orders_table[orders_table["side"] == side]

        ohlc = ohlc_table["price"].resample(timeframe).ohlc()
        ohlc["date"] = ohlc.index.tz_convert(self.timezone)
        try:
            ohlc = ohlc.astype({"date": str})
        except KeyError:
            data = [{
                "open": self.__nan,
                "high": self.__nan,
                "low": self.__nan,
                "close": self.__nan,
                "date": "",
                "pair": pair,
                "exchange": self.exchange,
                "side": side,
                "timeframe": timeframe,
            }]
        else:
            ohlc["pair"] = pair
            ohlc["exchange"] = self.exchange
            ohlc["side"] = side
            ohlc["timeframe"] = timeframe
            data = ohlc.to_dict(orient="records")
        finally:
            pass

        return data

    def fetch_orderbook(self, pair: str = "btcjpy") -> tuple[dict, int]:
        path: str = "/depth"

        symbol: str = self.markets[pair]["symbol"]
        url: str = "".join([
            self.endpoint,
            path,
            "?",
            urllib.parse.urlencode(dict(
                coin=symbol,
            ))
        ])

        ret: dict = {}
        status_code: int = 500
        for request_retry_count in range(self.request_retry):
            time.sleep(self.request_retry_interval * request_retry_count)

            ret, status_code = self.request_get(url)

            if status_code == 200:
                break
            else:
                continue

        key: list = ["price", "volume"]
        asks: float = ret["asks"] if "asks" in ret else []
        bids: float = ret["bids"] if "bids" in ret else []

        data = {
            "pair": pair,
            "exchange": self.exchange,
            "sell": [dict(zip(key, numpy.array(item, dtype="float"))) for item in asks],
            "buy": [dict(zip(key, numpy.array(item, dtype="float"))) for item in bids],
            "timestamp": datetime.datetime.now().timestamp(),
        }

        return data, status_code

    def fetch_orders(self, pair: str = "btcjpy") -> tuple[list, int]:
        path: str = "/orders"

        symbol: str = self.markets[pair]["symbol"]
        url: str = "".join([
            self.endpoint,
            path,
            "?",
            urllib.parse.urlencode(dict(
                coin=symbol,
            ))
        ])

        ret: dict = {}
        status_code: int = 500
        for request_retry_count in range(self.request_retry):
            time.sleep(self.request_retry_interval * request_retry_count)

            ret, status_code = self.request_get(url)

            if status_code == 200:
                break
            else:
                continue

        data: list = []
        for trade in ret:
            data.append({
                "timestamp": float(trade["date"]) if "date" in trade else self.__nan,
                "pair": pair,
                "price": float(trade["price"]) if "price" in trade else self.__nan,
                "volume": float(trade["amount"]) if "amount" in trade else self.__nan,
                "side": trade["type"] if "type" in trade else None,
                "exchange": self.exchange,
            })

        return data, status_code

    def fetch_ticker(self, pair: str = "btcjpy") -> tuple[dict, int]:
        path: str = "/ticker"

        symbol: str = self.markets[pair]["symbol"]
        url: str = "".join([
            self.endpoint,
            path,
            "?",
            urllib.parse.urlencode(dict(
                coin=symbol,
            ))
        ])

        ret: dict = {}
        status_code: int = 500
        for request_retry_count in range(self.request_retry):
            time.sleep(self.request_retry_interval * request_retry_count)

            ret, status_code = self.request_get(url)

            if status_code == 200:
                break
            else:
                continue

        data = {
            "pair": pair,
            "exchange": self.exchange,
            "sell": float(ret["sell"]) if "sell" in ret else self.__nan,
            "buy": float(ret["buy"]) if "buy" in ret else self.__nan,
            "last": float(ret["last"]) if "last" in ret else self.__nan,
            "volume": float(ret["vol"]) if "vol" in ret else self.__nan,
            "timestamp": datetime.datetime.now().timestamp(),
        }

        return data, status_code

    def get_coins(self) -> list:
        return [market[1]["symbol"] for market in self.markets.items()]

    def request_get(self, url: str) -> tuple[dict, int]:
        status_code: int = 200

        res: requests.models.Response = None
        try:
            res = requests.get(url, timeout=self.request_timeout)
            res.raise_for_status()
        except requests.exceptions.Timeout:
            data: dict = {
                "error": "Request timeout",
                "response": str(res),
                "url": url,
            }
            status_code = 408
        except requests.exceptions.RequestException as exception:
            data: dict = {
                "error": traceback.format_exception_only(type(exception), exception)[0],
                "response": str(res),
                "url": url,
            }
            status_code = 500
        else:
            data: dict = json.loads(res.text)

        return data, status_code

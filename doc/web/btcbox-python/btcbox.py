import datetime
import json
import time
import traceback
import urllib.parse

import numpy
import pandas
import requests


class Btcbox(object):

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
    request_retry: int = 5
    request_retry_interval: float = 0.3
    timeout: float = 3.0
    timezone: str = "Asia/Tokyo"

    def __init__(self) -> None:
        self.__nan = numpy.nan

    def __fetch_orders(self, pair: str = "btcjpy") -> tuple[dict, int]:
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

        data: dict = []
        for trade in ret:
            timestamp: float = float(trade["date"]) if "date" in trade else self.__nan
            price: float = float(trade["price"]) if "price" in trade else self.__nan
            volume: float = float(trade["amount"]) if "amount" in trade else self.__nan
            side: str = trade["type"] if "type" in trade else None

            data.append({
                "timestamp": timestamp,
                "pair": pair,
                "price": price,
                "volume": volume,
                "side": side,
                "exchange": self.exchange,
            })

        return data, status_code

    def fetch_ohlc(self, pair: str = "btcjpy", side: str = "sell", timeframe: str = "60S") -> dict:
        orders, _ = self.__fetch_orders(pair)
        orders_table: pandas.core.frame.DataFrame = pandas.DataFrame(orders)
        orders_table.index = pandas.to_datetime(orders_table["timestamp"], unit="s", utc=True)
        ohlc_table: pandas.core.frame.DataFrame = orders_table[orders_table["side"] == side]

        ohlc = ohlc_table["price"].resample(timeframe).ohlc()
        ohlc["date"] = ohlc.index.tz_convert(self.timezone)
        ohlc = ohlc.astype({"date": str})
        ohlc["pair"] = pair
        ohlc["exchange"] = self.exchange
        ohlc["side"] = side
        ohlc["timeframe"] = timeframe

        data = ohlc.to_dict(orient="records")

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
        sell: float = [dict(zip(key, numpy.array(item, dtype="float"))) for item in asks]
        buy: float = [dict(zip(key, numpy.array(item, dtype="float"))) for item in bids]
        timestamp: float = datetime.datetime.now().timestamp()

        data = {
            "pair": pair,
            "exchange": self.exchange,
            "sell": sell,
            "buy": buy,
            "timestamp": timestamp,
        }

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

        sell: float = float(ret["sell"]) if "sell" in ret else self.__nan
        buy: float = float(ret["buy"]) if "buy" in ret else self.__nan
        last: float = float(ret["last"]) if "last" in ret else self.__nan
        volume: float = float(ret["vol"]) if "vol" in ret else self.__nan
        timestamp: float = datetime.datetime.now().timestamp()

        data = {
            "pair": pair,
            "exchange": self.exchange,
            "sell": sell,
            "buy": buy,
            "last": last,
            "volume": volume,
            "timestamp": timestamp,
        }

        return data, status_code

    def get_coins(self) -> list:
        return [market[1]["symbol"] for market in self.markets.items()]

    def request_get(self, url: str) -> tuple[dict, int]:
        status_code: int = 200

        res: requests.models.Response = None
        try:
            res = requests.get(url, timeout=self.timeout)
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

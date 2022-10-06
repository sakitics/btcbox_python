import time
import unittest

import numpy

from btcbox import Btcbox


class BtcboxTestCase(unittest.TestCase):

    def setUp(self) -> None:
        self.base: Btcbox = Btcbox()
        self.perf_rapid: float = 0.03
        self.perf_normal: float = 0.3
        self.perf_slow: float = 3.0

    def test_create_nonce(self) -> None:
        expect_perf: float = self.perf_rapid

        start: float = time.perf_counter()
        result: str = self.base.create_nonce()
        end: float = time.perf_counter()

        result_perf: float = end - start

        self.assertTrue(isinstance(result, str))
        self.assertLessEqual(result_perf, expect_perf)

    # TODO: Unimplemented
    def test_fetch_balance(self) -> None:
        expect_data: dict = {
            "id": "<class 'str'>",
            "exchange": "<class 'str'>",
            "timestamp": "<class 'float'>",
        }
        expect_status_code: int = 500
        expect_perf: float = self.perf_normal

        start: float = time.perf_counter()
        result_data, result_status_code = self.base.fetch_balance()
        end: float = time.perf_counter()

        result_perf: float = end - start

        self.assertEqual(expect_status_code, result_status_code)
        for key in expect_data.keys():
            self.assertTrue(key in result_data)
            self.assertEqual(expect_data.get(key, ""), str(type(result_data[key])))
        self.assertLessEqual(result_perf, expect_perf)

    def test_fetch_ohlc(self) -> None:
        expect_data: dict = {
            "open": "<class 'float'>",
            "high": "<class 'float'>",
            "low": "<class 'float'>",
            "close": "<class 'float'>",
            "date": "<class 'str'>",
            "pair": "<class 'str'>",
            "exchange": "<class 'str'>",
            "side": "<class 'str'>",
            "timeframe": "<class 'str'>",
        }
        expect_perf: float = self.perf_slow

        result_perf: float = 0.0
        for pair in self.base.markets.keys():
            for side in ["sell", "buy"]:
                for timeframe in ["60S", "30T", "1H"]:
                    start: float = time.perf_counter()
                    result_data = self.base.fetch_ohlc(pair, side, timeframe)
                    end: float = time.perf_counter()

                    result_perf = numpy.maximum(end - start, result_perf)

                    print(result_data)

                    for item in result_data:
                        for key in expect_data.keys():
                            self.assertTrue(key in item)
                            self.assertEqual(expect_data.get(key, ""), str(type(item[key])))

        self.assertLessEqual(result_perf, expect_perf)

    def test_fetch_orderbook(self) -> None:
        expect_data: dict = {
            "pair": "<class 'str'>",
            "exchange": "<class 'str'>",
            "sell": "<class 'list'>",
            "buy": "<class 'list'>",
            "timestamp": "<class 'float'>",
        }
        expect_status_code: int = 200
        expect_perf: float = self.perf_slow

        result_perf: float = 0.0
        for item in self.base.markets.keys():
            start: float = time.perf_counter()
            result_data, result_status_code = self.base.fetch_orderbook(item)
            end: float = time.perf_counter()

            result_perf = numpy.maximum(end - start, result_perf)

            self.assertEqual(expect_status_code, result_status_code)
            for key in expect_data.keys():
                self.assertTrue(key in result_data)
                self.assertEqual(expect_data.get(key, ""), str(type(result_data[key])))

        self.assertLessEqual(result_perf, expect_perf)

    def test_fetch_orders(self) -> None:
        expect_data: dict = {
            "timestamp": "<class 'float'>",
            "pair": "<class 'str'>",
            "price": "<class 'float'>",
            "volume": "<class 'float'>",
            "side": "<class 'str'>",
            "exchange": "<class 'str'>",
        }
        expect_status_code: int = 200
        expect_perf: float = self.perf_normal

        result_perf: float = 0.0
        for item in self.base.markets.keys():
            start: float = time.perf_counter()
            result_data, result_status_code = self.base.fetch_orders(item)
            end: float = time.perf_counter()

            result_perf = numpy.maximum(end - start, result_perf)

            self.assertEqual(expect_status_code, result_status_code)
            self.assertTrue(isinstance(result_data, list))
            for item2 in result_data:
                for key in expect_data.keys():
                    self.assertTrue(key in item2)
                    self.assertEqual(expect_data.get(key, ""), str(type(item2[key])))

        self.assertLessEqual(result_perf, expect_perf)

    def test_fetch_ticker(self) -> None:
        expect_data: dict = {
            "pair": "<class 'str'>",
            "exchange": "<class 'str'>",
            "sell": "<class 'float'>",
            "buy": "<class 'float'>",
            "last": "<class 'float'>",
            "volume": "<class 'float'>",
            "timestamp": "<class 'float'>",
        }
        expect_status_code: int = 200
        expect_perf: float = self.perf_slow

        result_perf: float = 0.0
        for pair in self.base.markets.keys():
            start: float = time.perf_counter()
            result_data, result_status_code = self.base.fetch_ticker(pair)
            end: float = time.perf_counter()

            result_perf = numpy.maximum(end - start, result_perf)

            self.assertEqual(expect_status_code, result_status_code)
            for key in expect_data.keys():
                self.assertTrue(key in result_data)
                self.assertEqual(expect_data.get(key, ""), str(type(result_data[key])))

        self.assertLessEqual(result_perf, expect_perf)

    def test_get_coins(self) -> None:
        expect: list = ["btc", "bch", "ltc", "eth", "doge", "dot", "trx"]
        expect_perf: float = self.perf_rapid

        start: float = time.perf_counter()
        result: list = self.base.get_coins()
        end: float = time.perf_counter()

        result_perf: float = end - start

        self.assertEqual(expect, result)
        self.assertLessEqual(result_perf, expect_perf)


if __name__ == '__main__':
    unittest.main()

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

    def test_fetch_ohlc(self) -> None:
        expect_data: list = ["open", "high", "low", "close", "date", "pair", "exchange", "side", "timeframe"]
        expect_perf: float = self.perf_slow

        result_perf: float = 0.0
        for pair in self.base.markets.keys():
            for side in ["sell", "buy"]:
                for timeframe in ["60S", "15T", "1H"]:
                    start: float = time.perf_counter()
                    result_data = self.base.fetch_ohlc(pair, side, timeframe)
                    end: float = time.perf_counter()

                    for ohlc in result_data:
                        for key in expect_data:
                            self.assertTrue(key in ohlc)

                    result_perf = numpy.maximum(end - start, result_perf)

        self.assertLessEqual(result_perf, expect_perf)

    def test_fetch_orderbook(self) -> None:
        expect_data: list = ["pair", "exchange", "sell", "buy", "timestamp"]
        expect_status_code: int = 200
        expect_perf: float = self.perf_normal

        result_perf: float = 0.0
        for pair in self.base.markets.keys():
            start: float = time.perf_counter()
            result_data, result_status_code = self.base.fetch_orderbook(pair)
            end: float = time.perf_counter()

            result_perf = numpy.maximum(end - start, result_perf)

            self.assertEqual(expect_status_code, result_status_code)
            for key in expect_data:
                self.assertTrue(key in result_data)

        self.assertLessEqual(result_perf, expect_perf)

    def test_fetch_ticker(self) -> None:
        expect_data: list = ["pair", "exchange", "sell", "buy", "last", "volume", "timestamp"]
        expect_status_code: int = 200
        expect_perf: float = self.perf_normal

        result_perf: float = 0.0
        for pair in self.base.markets.keys():
            start: float = time.perf_counter()
            result_data, result_status_code = self.base.fetch_ticker(pair)
            end: float = time.perf_counter()

            result_perf = numpy.maximum(end - start, result_perf)

            self.assertEqual(expect_status_code, result_status_code)
            for key in expect_data:
                self.assertTrue(key in result_data)

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

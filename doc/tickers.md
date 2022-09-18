### Tickers（全取扱銘柄のリアルタイムレートを取得）

全取扱銘柄のリアルタイムレートを取得します。

#### Request

```http request
GET /tickers
```

#### Request parameters

#### Request example

```python
import json
import traceback
import urllib.parse

import requests


endpoint: str = "https://www.btcbox.co.jp/api/v1"
path: str = "/tickers"
url: str = "".join([
    endpoint,
    path,
])
timeout: float = 3.0
status_code: int = 200

res: requests.models.Response = None
try:
    res = requests.get(url, timeout=timeout)
    res.raise_for_status()
except requests.exceptions.Timeout:
    data = {
        "error": "Request timeout",
        "response": str(res),
        "url": url,
    }
    status_code = 408
except requests.exceptions.RequestException as exception:
    data = {
        "error": traceback.format_exception_only(type(exception), exception)[0],
        "response": str(res),
        "url": url,
    }
    status_code = 500
else:
    data = json.loads(res.text)

print((data, status_code))
```

#### Response

| Name | Type  | Description            |
|------|-------|------------------------|
| pair | str   | 銘柄名（BTC_JPY、BCH_JPYなど） |
| high | int   | 24時間の高値                |
| low  | int   | 24時間の安値                |
| buy  | int   | 買い気配値                  |
| sell | int   | 売り気配値                  |
| last | int   | 最新の約定価格                |
| vol  | float | 24時間の出来高               |

#### Response example

```json
{
    "BTC_JPY": {
        "high": 2884823,
        "low": 2826940,
        "buy": 2850313,
        "sell": 2847378,
        "last": 2847399,
        "vol": 559.1379
    },
    "BCH_JPY": {
        "high": 17646,
        "low": 16889,
        "buy": 16820,
        "sell": 17155,
        "last": 17058,
        "vol": 848.4548
    },
    "LTC_JPY": {
        "high": 8357,
        "low": 8011,
        "buy": 8060,
        "sell": 8149,
        "last": 8102,
        "vol": 783.9139
    },
    "ETH_JPY": {
        "high": 243137,
        "low": 210000,
        "buy": 210000,
        "sell": 246776,
        "last": 228389,
        "vol": 249.2947
    },
    "DOGE_JPY": {
        "high": 8.92,
        "low": 8.63,
        "buy": 8.68,
        "sell": 8.68,
        "last": 8.68,
        "vol": 21529.8022
    },
    "DOT_JPY": {
        "high": 1023,
        "low": 980,
        "buy": 983,
        "sell": 984,
        "last": 984,
        "vol": 21283.3837
    },
    "TRX_JPY": {
        "high": 8.93,
        "low": 8.79,
        "buy": 8.91,
        "sell": 8.91,
        "last": 8.91,
        "vol": 21447.7862
    }
}
```

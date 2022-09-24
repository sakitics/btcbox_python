### Orderbook（取扱銘柄の板情報を取得）

指定した暗号資産の板情報を取得します。  

#### Request

```http request
GET /depth
```

#### Request parameters

| Name | Type | Required | Description                                       |
|------|------|----------|---------------------------------------------------|
| coin | str  | no       | 取扱銘柄：btc、bch、ltc、eth、doge、dot、trxのいずれか（デフォルトはbtc） |

#### Request example

```python
import json
import traceback
import urllib.parse

import requests


endpoint: str = "https://www.btcbox.co.jp/api/v1"
path: str = "/depth"
url: str = "".join([
    endpoint,
    path,
    "?",
    urllib.parse.urlencode(dict(
        coin="eth",
    ))
])
timeout: float = 3.0
status_code: int = 200

res: requests.models.Response = None
try:
    res = requests.get(url, timeout=timeout)
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

print((data, status_code))
```

#### Response

| Name | Type | Description               |
|------|------|---------------------------|
| asks | list | 現在の「売り注文価格・数量」を価格順（降順）で表示 |
| bids | list | 現在の「買い注文価格・数量」を価格順（降順）で表示 |

#### Response example

```json
{
    "asks": [
        [
            192485,
            0.05
        ],
        [
            190000,
            0.02
        ],
        [
            185246,
            2.0269
        ],
        [
            185006,
            2.5141
        ],
        [
            184410,
            0.05
        ],
        [
            184282,
            0.05
        ]
    ],
    "bids": [
        [
            183420,
            0.1
        ],
        [
            183331,
            0.05
        ],
        [
            183316,
            0.05
        ],
        [
            182067,
            0.9777
        ],
        [
            181744,
            1.0062
        ],
        [
            181218,
            1.669
        ]
    ]
}
```

#### Errors

[Error Code](error_code.md)を参照してください。

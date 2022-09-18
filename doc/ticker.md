### Ticker（取扱銘柄のリアルタイムレートを取得）

指定した暗号資産のリアルタイムレートを取得します。  

#### Request

```http request
GET /ticker
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
path: str = "/ticker"
url: str = "".join([
    endpoint,
    path,
    "?",
    urllib.parse.urlencode(dict(
        coin="btc",
    ))
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

| Name | Type  | Description |
|------|-------|-------------|
| high | float | 24時間の高値     |
| low  | float | 24時間の安値     |
| buy  | float | 買い気配値       |
| sell | float | 売り気配値       |
| last | float | 最新の約定価格     |
| vol  | float | 24時間の出来高    |

#### Response example

```json
{
    "high": 2884823,
    "low": 2826940,
    "buy": 2856580,
    "sell": 2861988,
    "last": 2856579,
    "vol": 559.3381
}
```

#### Errors

[Error Code](error_code.md)を参照してください。

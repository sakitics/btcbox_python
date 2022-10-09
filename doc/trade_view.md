### Trade view（注文の詳細情報を取得）

指定された注文の詳細情報を取得できます。

#### Request

```http request
GET /api/v1/trade_view
```

#### Request parameters

| Name      | Type | Required | Description                                       |
|-----------|------|----------|---------------------------------------------------|
| coin      | str  | no       | 取扱銘柄：btc、bch、ltc、eth、doge、dot、trxのいずれか（デフォルトはbtc） |
| id        | str  | yes      | 注文ID                                              |
| key       | str  | yes      | APIキー（公開鍵）                                        |
| nonce     | str  | yes      | ノンス                                               |
| signature | str  | yes      | 署名                                                |

#### Request example

```python
import datetime
import hashlib
import hmac
import json
import traceback
import urllib

import configparser
import requests


config: configparser.ConfigParser = configparser.ConfigParser()
config.read("config.ini")
apikey_public: str = config.get("DEEP", "key")
apikey_secret: str = config.get("DEEP", "sec")
symbol: str = config.get("DEEP", "coin")

endpoint: str = "https://www.btcbox.co.jp/api/v1"
path: str = "/trade_view"
url: str = "".join([
    endpoint,
    path,
])
timeout: float = 3.0
status_code: int = 200

timestamp: float = datetime.datetime.now().timestamp() * 1000
body: dict = {
    "coin": symbol,
    "id": "11",
    "key": apikey_public,
    "nonce": timestamp,
}

secret_md5: str = bytearray(hashlib.md5(apikey_secret.encode("utf-8")).hexdigest(), "ascii")
text: bytearray = bytearray(urllib.parse.urlencode(body), "ascii")
sign: str = urllib.parse.quote(hmac.new(secret_md5, text, hashlib.sha256).hexdigest())
body["signature"] = sign

res: requests.models.Response = None
try:
    res = requests.post(url=url, data=body, timeout=timeout)
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

| Name               | Type  | Description                                                     |
|--------------------|-------|-----------------------------------------------------------------|
| id                 | str   | 注文ID                                                            |
| datetime           | str   | 注文日時（yyyy-mm-dd hh:mm:ss形式）                                     |
| type               | str   | 売買区分（sellまたはbuy）                                                |
| price              | int   | 注文価格                                                            |
| amount_original    | float | 注文数量                                                            |
| amount_outstanding | float | 未約定数量                                                           |
| status             | str   | 注文状態（wait: 未約定, part: 未約定または一部約定, cancelled: 取消済み, all: 全て約定済み） |

#### Response example

```json
{  
   "id": 11,
   "datetime": "2014-10-21 10:47:20",
   "type": "sell",
   "price": 42000,
   "amount_original": 1.2,
   "amount_outstanding": 0,
   "status": "all",
   "trades": []
}
```

#### Errors

[Error Code](error_code.md)を参照してください。

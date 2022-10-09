### Trade list（注文一覧の取得）

最新の注文から指定日時まで最大100件の注文情報を取得できます。

#### Request

```http request
GET /api/v1/trade_list
```

#### Request parameters

| Name      | Type  | Required | Description                                       |
|-----------|-------|----------|---------------------------------------------------|
| coin      | str   | no       | 取扱銘柄：btc、bch、ltc、eth、doge、dot、trxのいずれか（デフォルトはbtc） |
| since     | float | no       | 指定日時、UNIX時間で指定（デフォルトは0）                           |
| type      | str   | no       | 指定状態（allまたはopen）                                  |
| key       | str   | yes      | APIキー（公開鍵）                                        |
| nonce     | str   | yes      | ノンス                                               |
| signature | str   | yes      | 署名                                                |

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
apikey_public = config.get("DEEP", "key")
apikey_secret = config.get("DEEP", "sec")
symbol = config.get("DEEP", "coin")

endpoint: str = "https://www.btcbox.co.jp/api/v1"
path: str = "/trade_list"
url: str = "".join([
    endpoint,
    path,
])
timeout: float = 3.0
status_code: int = 200

timestamp: float = datetime.datetime.now().timestamp() * 1000
body: dict = {
    "coin": symbol,
    "since": 1394031600,
    "type": "all",
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

| Name               | Type  | Description                 |
|--------------------|-------|-----------------------------|
| id                 | str   | 注文ID                        |
| datetime           | str   | 注文日時（yyyy-mm-dd hh:mm:ss形式） |
| type               | str   | 売買区分（sellまたはbuy）            |
| price              | int   | 注文価格                        |
| amount_original    | float | 注文数量                        |
| amount_outstanding | float | 未約定数量                       |

#### Response example

```json
[  
   {  
      "id":"7",
      "datetime":"2014-10-20 13:27:38",
      "type":"buy",
      "price":42750,
      "amount_original":0.235,
      "amount_outstanding":0.235
   },
   {  
      "id":"6",
      "datetime":"2014-10-20 13:27:15",
      "type":"buy",
      "price":43299,
      "amount_original":4.789,
      "amount_outstanding":4.789
   },
   {  
      "id":"5",
      "datetime":"2014-10-20 13:26:52",
      "type":"buy",
      "price":42500,
      "amount_original":14,
      "amount_outstanding":14
   },
   {  
      "id":"4",
      "datetime":"2014-10-20 13:26:23",
      "type":"buy",
      "price":43200,
      "amount_original":0.4813,
      "amount_outstanding":0.4813
   },
   {  
      "id":"3",
      "datetime":"2014-10-20 13:25:57",
      "type":"buy",
      "price":43200,
      "amount_original":0.4813,
      "amount_outstanding":0.4813
   }
]
```

#### Errors

[Error Code](error_code.md)を参照してください。

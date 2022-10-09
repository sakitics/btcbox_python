### Balance（残高の取得）

保有している暗号資産と法定通貨の残高を取得できます。

#### Request

```http request
GET /api/v1/balance
```

#### Request parameters

| Name      | Type | Required | Description                                       |
|-----------|------|----------|---------------------------------------------------|
| coin      | str  | no       | 取扱銘柄：btc、bch、ltc、eth、doge、dot、trxのいずれか（デフォルトはbtc） |
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

endpoint: str = "https://www.btcbox.co.jp/api/v1"
path: str = "/balance"
url: str = "".join([
    endpoint,
    path,
])
timeout: float = 3.0
status_code: int = 200

timestamp: float = datetime.datetime.now().timestamp() * 1000
body: dict = {
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

| Name         | Type  | Description            |
|--------------|-------|------------------------|
| uid          | int   | ユーザーID                 |
| nameauth     | int   | 本人認証の状態、0:未認証、1:認証済    |
| moflag       | int   | SMS認証設定の状態、0:未認証、1:認証済 |
| btc_balance  | float | BTC残高                  |
| btc_lock     | float | 注文中のBTC数量              |
| bch_balance  | float | BCH残高                  |
| bch_lock     | float | 注文中のBCH数量              |
| ltc_balance  | float | LTC残高                  |
| ltc_lock     | float | 注文中のLTC数量              |
| eth_balance  | float | ETH残高                  |
| eth_lock     | float | 注文中のETH数量              |
| doge_balance | float | DOGE残高                 |
| doge_lock    | float | 注文中のDOGE数量             |
| dot_balance  | float | DOT残高                  |
| dot_lock     | float | 注文中のDOT数量              |
| trx_balance  | float | TRX残高                  |
| trx_lock     | float | 注文中のTRX数量              |
| jpy_balance  | float | 日本円残高                  |
| jpy_lock     | float | 注文中の日本円数量              |

#### Response example

```json
{
    "uid": 1,
    "nameauth": 1,
    "moflag": 1,
    "btc_balance": 0,
    "btc_lock": 0,
    "bch_balance": 0,
    "bch_lock": 0,
    "ltc_balance": 0,
    "ltc_lock": 0,
    "eth_balance": 0,
    "eth_lock": 0,
    "doge_balance": 0,
    "doge_lock": 0,
    "dot_balance": 0,
    "dot_lock": 0,
    "trx_balance": 0,
    "trx_lock": 0,
    "jpy_balance": 0,
    "jpy_lock": 0
}
```

#### Errors

[Error Code](error_code.md)を参照してください。

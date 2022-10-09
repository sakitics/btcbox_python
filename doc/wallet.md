### Wallet（アドレスの取得）

指定された暗号資産のBTCBOXアカウント内の入金アドレスを取得できます。

#### Request

```http request
GET /api/v1/wallet
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
symbol: str = config.get("DEEP", "coin")

endpoint: str = "https://www.btcbox.co.jp/api/v1"
path: str = "/wallet"
url: str = "".join([
    endpoint,
    path,
])
timeout: float = 3.0
status_code: int = 200

timestamp: float = datetime.datetime.now().timestamp() * 1000
body: dict = {
    "coin": symbol,
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

| Name    | Type | Description               |
|---------|------|---------------------------|
| result  | bool | 処理結果（true: 成功, false: 失敗） |
| address | str  | 入金アドレス                    |

#### Response example

```json
{
    "result": true,
    "address": "xxxxxxxxxxxxxxxxxxxxxxxxx"
}
```

#### Errors

[Error Code](error_code.md)を参照してください。

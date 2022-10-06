### Orders（取扱銘柄の約定履歴を取得）

最新100件分の指定した暗号資産の約定履歴を取得します。

#### Request

```http request
GET /orders
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
path: str = "/orders"
url: str = "".join([
    endpoint,
    path,
    "?",
    urllib.parse.urlencode(dict(
        coin="doge",
    ))
])
timeout: float = 3.0
status_code: int = 200

res: requests.models.Response = None
try:
    res = requests.get(url=url, timeout=timeout)
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

| Name   | Type  | Description      |
|--------|-------|------------------|
| date   | str   | 約定日時（UNIX時間）     |
| price  | float | 約定価格             |
| amount | float | 約定数量             |
| tid    | float | 注文ID             |
| type	  | float | 売買区分（sellまたはbuy） |

#### Response example

```json
[
    {
        "date": "1663856323",
        "price": 8.33,
        "amount": 2.6477,
        "tid": "1753538",
        "type": "sell"
    },
    {
        "date": "1663856329",
        "price": 8.33,
        "amount": 2.5273,
        "tid": "1753539",
        "type": "sell"
    },
    {
        "date": "1663856335",
        "price": 8.33,
        "amount": 1.6441,
        "tid": "1753540",
        "type": "sell"
    },
    {
        "date": "1663856341",
        "price": 8.33,
        "amount": 2.5972,
        "tid": "1753541",
        "type": "sell"
    },
    {
        "date": "1663856348",
        "price": 8.33,
        "amount": 1.1531,
        "tid": "1753542",
        "type": "sell"
    },
    {
        "date": "1663856355",
        "price": 8.32,
        "amount": 0.3804,
        "tid": "1753543",
        "type": "sell"
    },
    {
        "date": "1663856361",
        "price": 8.32,
        "amount": 0.9606,
        "tid": "1753544",
        "type": "sell"
    },
    {
        "date": "1663856368",
        "price": 8.32,
        "amount": 2.5723,
        "tid": "1753545",
        "type": "sell"
    },
    {
        "date": "1663856374",
        "price": 8.32,
        "amount": 2.1024,
        "tid": "1753546",
        "type": "sell"
    },
    {
        "date": "1663856380",
        "price": 8.32,
        "amount": 0.3842,
        "tid": "1753547",
        "type": "sell"
    },
    {
        "date": "1663856386",
        "price": 8.32,
        "amount": 0.9358,
        "tid": "1753548",
        "type": "sell"
    },
    {
        "date": "1663856392",
        "price": 8.32,
        "amount": 1.6868,
        "tid": "1753549",
        "type": "sell"
    },
    {
        "date": "1663856398",
        "price": 8.32,
        "amount": 1.5849,
        "tid": "1753550",
        "type": "sell"
    },
    {
        "date": "1663856405",
        "price": 8.32,
        "amount": 1.6832,
        "tid": "1753551",
        "type": "sell"
    },
    {
        "date": "1663856411",
        "price": 8.32,
        "amount": 0.8054,
        "tid": "1753552",
        "type": "sell"
    },
    {
        "date": "1663856417",
        "price": 8.32,
        "amount": 2.999,
        "tid": "1753553",
        "type": "sell"
    },
    {
        "date": "1663856423",
        "price": 8.32,
        "amount": 1.6325,
        "tid": "1753554",
        "type": "sell"
    },
    {
        "date": "1663856429",
        "price": 8.32,
        "amount": 1.1916,
        "tid": "1753555",
        "type": "sell"
    },
    {
        "date": "1663856435",
        "price": 8.32,
        "amount": 0.3182,
        "tid": "1753556",
        "type": "sell"
    },
    {
        "date": "1663856441",
        "price": 8.32,
        "amount": 2.4486,
        "tid": "1753557",
        "type": "sell"
    },
    {
        "date": "1663856447",
        "price": 8.32,
        "amount": 1.5325,
        "tid": "1753558",
        "type": "sell"
    },
    {
        "date": "1663856456",
        "price": 8.33,
        "amount": 1.5281,
        "tid": "1753559",
        "type": "buy"
    },
    {
        "date": "1663856463",
        "price": 8.33,
        "amount": 0.6541,
        "tid": "1753560",
        "type": "sell"
    },
    {
        "date": "1663856470",
        "price": 8.33,
        "amount": 1.2941,
        "tid": "1753561",
        "type": "sell"
    },
    {
        "date": "1663856477",
        "price": 8.33,
        "amount": 2.1413,
        "tid": "1753562",
        "type": "sell"
    },
    {
        "date": "1663856483",
        "price": 8.33,
        "amount": 0.5978,
        "tid": "1753563",
        "type": "sell"
    },
    {
        "date": "1663856489",
        "price": 8.33,
        "amount": 1.0225,
        "tid": "1753564",
        "type": "sell"
    },
    {
        "date": "1663856494",
        "price": 8.33,
        "amount": 0.6,
        "tid": "1753565",
        "type": "sell"
    },
    {
        "date": "1663856501",
        "price": 8.33,
        "amount": 2.262,
        "tid": "1753566",
        "type": "sell"
    },
    {
        "date": "1663856507",
        "price": 8.33,
        "amount": 0.8431,
        "tid": "1753567",
        "type": "sell"
    },
    {
        "date": "1663856515",
        "price": 8.32,
        "amount": 2.0066,
        "tid": "1753568",
        "type": "sell"
    },
    {
        "date": "1663856521",
        "price": 8.32,
        "amount": 2.2652,
        "tid": "1753569",
        "type": "sell"
    },
    {
        "date": "1663856527",
        "price": 8.32,
        "amount": 2.3343,
        "tid": "1753570",
        "type": "sell"
    },
    {
        "date": "1663856533",
        "price": 8.32,
        "amount": 0.2272,
        "tid": "1753571",
        "type": "sell"
    },
    {
        "date": "1663856542",
        "price": 8.33,
        "amount": 2.8532,
        "tid": "1753572",
        "type": "buy"
    },
    {
        "date": "1663856548",
        "price": 8.33,
        "amount": 1.3385,
        "tid": "1753573",
        "type": "sell"
    },
    {
        "date": "1663856555",
        "price": 8.32,
        "amount": 1.2557,
        "tid": "1753574",
        "type": "sell"
    },
    {
        "date": "1663856563",
        "price": 8.32,
        "amount": 2.4092,
        "tid": "1753575",
        "type": "sell"
    },
    {
        "date": "1663856569",
        "price": 8.32,
        "amount": 1.2137,
        "tid": "1753576",
        "type": "sell"
    },
    {
        "date": "1663856574",
        "price": 8.32,
        "amount": 1.5736,
        "tid": "1753577",
        "type": "sell"
    },
    {
        "date": "1663856581",
        "price": 8.32,
        "amount": 0.4361,
        "tid": "1753578",
        "type": "sell"
    },
    {
        "date": "1663856587",
        "price": 8.32,
        "amount": 2.9847,
        "tid": "1753579",
        "type": "sell"
    },
    {
        "date": "1663856593",
        "price": 8.32,
        "amount": 1.7223,
        "tid": "1753580",
        "type": "sell"
    },
    {
        "date": "1663856599",
        "price": 8.32,
        "amount": 2.3637,
        "tid": "1753581",
        "type": "sell"
    },
    {
        "date": "1663856607",
        "price": 8.32,
        "amount": 2.9307,
        "tid": "1753582",
        "type": "sell"
    },
    {
        "date": "1663856613",
        "price": 8.32,
        "amount": 0.3624,
        "tid": "1753583",
        "type": "sell"
    },
    {
        "date": "1663856618",
        "price": 8.32,
        "amount": 1.2395,
        "tid": "1753584",
        "type": "sell"
    },
    {
        "date": "1663856626",
        "price": 8.31,
        "amount": 2.0106,
        "tid": "1753585",
        "type": "sell"
    },
    {
        "date": "1663856633",
        "price": 8.31,
        "amount": 0.3614,
        "tid": "1753586",
        "type": "sell"
    },
    {
        "date": "1663856640",
        "price": 8.32,
        "amount": 2.2689,
        "tid": "1753587",
        "type": "sell"
    },
    {
        "date": "1663856646",
        "price": 8.32,
        "amount": 2.5121,
        "tid": "1753588",
        "type": "sell"
    },
    {
        "date": "1663856652",
        "price": 8.32,
        "amount": 0.4322,
        "tid": "1753589",
        "type": "sell"
    },
    {
        "date": "1663856659",
        "price": 8.32,
        "amount": 2.6676,
        "tid": "1753590",
        "type": "sell"
    },
    {
        "date": "1663856665",
        "price": 8.32,
        "amount": 0.4101,
        "tid": "1753591",
        "type": "sell"
    },
    {
        "date": "1663856671",
        "price": 8.32,
        "amount": 2.5954,
        "tid": "1753592",
        "type": "sell"
    },
    {
        "date": "1663856677",
        "price": 8.32,
        "amount": 1.8247,
        "tid": "1753593",
        "type": "sell"
    },
    {
        "date": "1663856683",
        "price": 8.32,
        "amount": 1.5761,
        "tid": "1753594",
        "type": "sell"
    },
    {
        "date": "1663856689",
        "price": 8.32,
        "amount": 2.2123,
        "tid": "1753595",
        "type": "sell"
    },
    {
        "date": "1663856695",
        "price": 8.32,
        "amount": 0.5771,
        "tid": "1753596",
        "type": "sell"
    },
    {
        "date": "1663856701",
        "price": 8.32,
        "amount": 1.2686,
        "tid": "1753597",
        "type": "sell"
    },
    {
        "date": "1663856708",
        "price": 8.32,
        "amount": 0.7959,
        "tid": "1753598",
        "type": "sell"
    },
    {
        "date": "1663856714",
        "price": 8.32,
        "amount": 1.2653,
        "tid": "1753599",
        "type": "sell"
    },
    {
        "date": "1663856720",
        "price": 8.32,
        "amount": 0.2354,
        "tid": "1753600",
        "type": "sell"
    },
    {
        "date": "1663856726",
        "price": 8.32,
        "amount": 1.2666,
        "tid": "1753601",
        "type": "sell"
    },
    {
        "date": "1663856732",
        "price": 8.32,
        "amount": 1.2925,
        "tid": "1753602",
        "type": "sell"
    },
    {
        "date": "1663856739",
        "price": 8.32,
        "amount": 1.9504,
        "tid": "1753603",
        "type": "sell"
    },
    {
        "date": "1663856745",
        "price": 8.32,
        "amount": 0.4983,
        "tid": "1753604",
        "type": "sell"
    },
    {
        "date": "1663856750",
        "price": 8.32,
        "amount": 2.0745,
        "tid": "1753605",
        "type": "sell"
    },
    {
        "date": "1663856757",
        "price": 8.32,
        "amount": 2.5058,
        "tid": "1753606",
        "type": "sell"
    },
    {
        "date": "1663856765",
        "price": 8.31,
        "amount": 1.7883,
        "tid": "1753607",
        "type": "sell"
    },
    {
        "date": "1663856773",
        "price": 8.32,
        "amount": 0.9253,
        "tid": "1753608",
        "type": "buy"
    },
    {
        "date": "1663856780",
        "price": 8.32,
        "amount": 2.8935,
        "tid": "1753609",
        "type": "sell"
    },
    {
        "date": "1663856786",
        "price": 8.32,
        "amount": 2.2541,
        "tid": "1753610",
        "type": "sell"
    },
    {
        "date": "1663856794",
        "price": 8.33,
        "amount": 0.6313,
        "tid": "1753611",
        "type": "buy"
    },
    {
        "date": "1663856802",
        "price": 8.32,
        "amount": 0.4453,
        "tid": "1753612",
        "type": "sell"
    },
    {
        "date": "1663856808",
        "price": 8.32,
        "amount": 2.9046,
        "tid": "1753613",
        "type": "sell"
    },
    {
        "date": "1663856814",
        "price": 8.32,
        "amount": 1.0167,
        "tid": "1753614",
        "type": "sell"
    },
    {
        "date": "1663856820",
        "price": 8.32,
        "amount": 0.3458,
        "tid": "1753615",
        "type": "sell"
    },
    {
        "date": "1663856827",
        "price": 8.32,
        "amount": 0.6767,
        "tid": "1753616",
        "type": "sell"
    },
    {
        "date": "1663856833",
        "price": 8.32,
        "amount": 0.2159,
        "tid": "1753617",
        "type": "sell"
    },
    {
        "date": "1663856841",
        "price": 8.33,
        "amount": 1.2118,
        "tid": "1753618",
        "type": "sell"
    },
    {
        "date": "1663856847",
        "price": 8.33,
        "amount": 2.1988,
        "tid": "1753619",
        "type": "sell"
    },
    {
        "date": "1663856854",
        "price": 8.33,
        "amount": 1.4639,
        "tid": "1753620",
        "type": "sell"
    },
    {
        "date": "1663856861",
        "price": 8.32,
        "amount": 1.5134,
        "tid": "1753621",
        "type": "sell"
    },
    {
        "date": "1663856869",
        "price": 8.32,
        "amount": 1.2336,
        "tid": "1753622",
        "type": "sell"
    },
    {
        "date": "1663856874",
        "price": 8.32,
        "amount": 1.5295,
        "tid": "1753623",
        "type": "sell"
    },
    {
        "date": "1663856882",
        "price": 8.32,
        "amount": 1.6091,
        "tid": "1753624",
        "type": "sell"
    },
    {
        "date": "1663856890",
        "price": 8.34,
        "amount": 2.869,
        "tid": "1753625",
        "type": "buy"
    },
    {
        "date": "1663856897",
        "price": 8.35,
        "amount": 1.7409,
        "tid": "1753626",
        "type": "sell"
    },
    {
        "date": "1663856904",
        "price": 8.35,
        "amount": 2.3261,
        "tid": "1753627",
        "type": "sell"
    },
    {
        "date": "1663856910",
        "price": 8.35,
        "amount": 0.3885,
        "tid": "1753628",
        "type": "sell"
    },
    {
        "date": "1663856916",
        "price": 8.35,
        "amount": 0.1936,
        "tid": "1753629",
        "type": "sell"
    },
    {
        "date": "1663856922",
        "price": 8.35,
        "amount": 1.897,
        "tid": "1753630",
        "type": "sell"
    },
    {
        "date": "1663856928",
        "price": 8.35,
        "amount": 0.6533,
        "tid": "1753631",
        "type": "sell"
    },
    {
        "date": "1663856934",
        "price": 8.35,
        "amount": 2.4414,
        "tid": "1753632",
        "type": "sell"
    },
    {
        "date": "1663856940",
        "price": 8.35,
        "amount": 0.4731,
        "tid": "1753633",
        "type": "sell"
    },
    {
        "date": "1663856948",
        "price": 8.35,
        "amount": 1.0032,
        "tid": "1753634",
        "type": "sell"
    },
    {
        "date": "1663856954",
        "price": 8.36,
        "amount": 0.8089,
        "tid": "1753635",
        "type": "sell"
    },
    {
        "date": "1663856961",
        "price": 8.36,
        "amount": 1.9044,
        "tid": "1753636",
        "type": "sell"
    },
    {
        "date": "1663856968",
        "price": 8.36,
        "amount": 0.5453,
        "tid": "1753637",
        "type": "sell"
    }
]
```

#### Errors

[Error Code](error_code.md)を参照してください。

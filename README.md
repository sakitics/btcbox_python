## Overview

はじめに[免責事項](doc/disclaimer.md)をお読みください。

### HTTP API

BTCBOX APIには、大きく2つのAPIが存在します。  
認証が不要な[HTTP Public API](doc/public.md)と、APIキーによる認証が必要なHTTP Private APIです。  

エンドポイントURL: https://www.btcbox.co.jp/api/v1

### Rate limiting

以下のHTTP APIは、呼び出し回数に制限があります。  
これら以外のHTTP APIには、呼び出し回数の制限はありません。ただし、システムに負荷がかかる呼び出しなどが行なわれた場合は、BTCBOX株式会社の判断でAPIの使用が制限される場合があります。  

| Request    | Description | Limit  |
|------------|-------------|--------|
| trade_add  | 新規注文        | 5回 / 秒 |
| trade_list | 注文情報の取得     | 3回 / 秒 |
| balance    | 残高情報の取得     | 5回 / 秒 |

### Authentication

### Pagination

### Install request

以下のオペレーションで、サンプルコード（Python）を動作させるためのライブラリをインストールしてください。  

```shell
pip install --upgrade -r requirements.txt
```

### Reference

* BTCボックス株式会社(2022). BTCBOX API ドキュメント. https://blog.btcbox.jp/archives/8759 (Last accessed 2022/09/01)

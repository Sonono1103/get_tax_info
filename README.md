# Tax Scraping

国税庁APIを用いて、法人番号から名前と所在地を得ます。そのときに取得日時も記録します。
Python3で実装しています。

## インストール・実行方法

いくつかライブラリを使用しているので、それらをインストールします。
windowsの場合はpip3のかわりにpipを使ってください。

```
pip3 install -r requirements.txt
```

実行権限を付与して、`./main.py <読み込みcsvファイル名> > <出力csvファイル名> `で実行します。

読み込みcsvファイルに期待する形式：一列目にイエローページID,二列目に法人番号  
一行目に名前を付けていない場合は、main.pyのコメントで指定してある箇所を削除してください。  
|yp_id|corp_number|  
| ---- | ---- |

## 出力データ

以下の項目をcsv形式で出力します。

- イエローページid
- 法人番号
- 名前
- 所在地
- 取得日時

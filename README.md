E-Hentai-Downloader
===================
#HOW TO USE
同じ場所にE-Hentai,ExHentaiのCookieファイルを置いてください。
Cookieファイルの形式はNetscape形式しか読めません。
エクスポートしたCookieの中身が以下のようになっていたらOKです。
```
# HTTP Cookie File
.exhentai.org	TRUE	/	FALSE	0123456789	ipb_member_id	01234567
...
```

#Release Note

###v0.0.3
ダウンロード用スレッドが同時に同じキューを参照するバグを修正
取得したギャラリー名から保存用のファイル名を生成する際に、
Windowsでファイル名に使用できない文字があった場合取り除くように

###v0.0.2
E-Hentai,ExHentai両対応。
画面のリストから消えるタイミングがダウンロード開始ではなくダウンロード完了に。
画面のリスト表示にStatusを追加。ダウンロード中なのかまだダウンロードされていないのかを表示できるように。

###v0.0.1
ExHentaiのみ対応。E-Hentaiでは使えなかった

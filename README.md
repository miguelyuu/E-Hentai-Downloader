E-Hentai-Downloader
=================
#What is This?
E-Hentai,ExHentaiのギャラリーをZIP形式でダウンロードできるDoggie Bag機能を簡単に使うためのスクリプトです。  
そのため、E-Hentaiのアカウントを持っていることはもちろん十分な量のGPかCreditを持っていることが必要です。  

#How to Use
Python3.4.1で開発しているので、Python3系なら動くのでは無いかと思います。  
wxPythonが動作に必要なので、pip等でインストールしておきます。  

スクリプトと同じ場所にE-Hentai,ExHentaiのCookieファイルをCookie.txtというファイル名で置いてください。  
Cookieファイルの形式はNetscape形式しか読めません。  
Cookieの中身が以下のようになっていたらOKです。
```
# HTTP Cookie File   <=一行目にこれが必要
.exhentai.org	TRUE	/	FALSE	0123456789	ipb_member_id	01234567
...
```

スクリプトを起動するとウィンドウが現れるので、Gallery URLとなっている欄にダウンロードしたいギャラリーのURLを入れてAddボタンを押すとダウンロードキューに追加されます。
ギャラリー名の取得等を行うため、Addボタンを押してから実際に追加されるまで数秒かかります。

Startボタンを押すとダウンロードが始まり、Stopを押すと一時停止になります。

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
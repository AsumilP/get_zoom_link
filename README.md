# get_zoom_link
#### 大学からgmailに送られてくるZoomのリンクをgmail apiを利用して自動取得しLineに通知するスクリプト 
watchコマンドなどで定期的に実行させることもできる  
<img width="573" alt="スクリーンショット 2020-05-23 19 00 56" src="https://user-images.githubusercontent.com/40427919/82727853-ff41a900-9d27-11ea-8761-e4fb964ec7bd.png">

### 背景  
オンライン講義のたびにメールでリンクが送られてくるが、大量にメールが届いていて探すのが大変だったため確認作業を自動化したかった。

### 現状は東工大仕様
addrの部分を変えることで任意の送信元に対応できるはず  
メール本文のzoomのリンクの部分とその前の数行を取得しているので、メールフォーマットが異なるとうまくいかないかもしれません。
## setup
https://news.mynavi.jp/article/zeropython-22/ を参考にしてGmail apiを取得し、credentials-gmail.jsonとclient_id.jsonを同じフォルダに作成  
https://notify-bot.line.me/ja/ からLineのtokenを発行してget_zoom_link.pyのtokenに記入  
setupが終了したら、python3 get_zoom_link.pyで実行可能
### Pythonライブラリ関連
pip3 install --upgrade google-api-python-client  
pip3 install oauth2client  
pip3 install python-dateutil

#### 参考
https://news.mynavi.jp/article/zeropython-22/

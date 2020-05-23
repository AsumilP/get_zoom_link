# get_zoom_link
#### 大学からgmailに送られてくるZoomのリンクをgmail apiを利用して自動取得しLineに通知するスクリプト   
watchコマンドなどで定期的に実行させることもできる  
setupが終了したら、python3 get_zoom_link.pyで実行可能

## 現状は東工大仕様
addrの部分を変えることで任意の送信元に対応できる
## setup
#### https://news.mynavi.jp/article/zeropython-22/ を参考にしてGmail apiを取得し  
credentials-gmail.jsonとclient_id.jsonを同じフォルダに作成  
https://notify-bot.line.me/ja/ からLineのtokenを発行してget_zoom_link.pyのtokenに記入
### Pythonライブラリ関連
#### pip3 install --upgrade google-api-python-client  
pip3 install oauth2client  
pip3 install python-dateutil

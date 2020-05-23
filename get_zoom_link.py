import httplib2, os
from apiclient import discovery
from oauth2client import client, tools
from oauth2client.file import Storage
import base64, email
import dateutil.parser
import requests
from datetime import datetime

token = "Line_Notify_token"
url = "https://notify-api.line.me/api/notify"
headers = {"Authorization": "Bearer " + token}


# 保存先
save_dir = os.path.join(os.curdir, 'gmaildata')
if not os.path.exists(save_dir):
    os.mkdir(save_dir)

# Gmail権限のスコープを指定
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
# 認証ファイル
CLIENT_SECRET_FILE = 'client_id.json'
USER_SECRET_FILE = 'credentials-gmail.json'
# ------------------------------------
# ユーザ認証データの取得
def gmail_user_auth():
    store = Storage(USER_SECRET_FILE)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = 'Python Gmail API'
        credentials = tools.run_flow(flow, store, None)
        print('認証結果を保存しました:' + USER_SECRET_FILE)
    return credentials
# Gmailのサービスを取得
def gmail_get_service():
    credentials = gmail_user_auth()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    return service
# ------------------------------------
def email_extract_text(raw):
    # Emailを解析する
    eml = email.message_from_bytes(raw)
    # 件名を取得
    subject = ''
    lines = email.header.decode_header(eml.get('Subject'))
    for frag, encoding in lines:
        if encoding:
            sub = frag.decode(encoding)
            subject += sub
        else:
            if isinstance(frag, bytes):
              sub = frag.decode('iso-2022-jp')
            else:
              sub = frag
            subject += sub
    # 差出人を取得
    addr = ''
    lines = email.header.decode_header(eml.get('From'))
    for frag, encoding in lines:
        if encoding:
            sub = frag.decode(encoding)
            addr += sub
        else:
            if isinstance(frag, bytes):
              addr = frag.decode('iso-2022-jp')
            else:
              sub = frag
            addr += sub
    #print("-----------")
    #print("From: " + addr)
    # 本文を取得
    body = ""
    for part in eml.walk():
        if part.get_content_type() != 'text/plain':
            continue
        # ヘッダを辞書型に落とす
        head = {}
        for k,v in part.items():
          head[k] = v
        s = part.get_payload(decode=True)
        # 文字コード
        if isinstance(s, bytes):
            charset = part.get_content_charset() or 'iso-2022-jp'
            s = s.decode(str(charset), errors="replace")
        body += s            
    #print("Body: " + body)
    # 日付
    date = dateutil.parser.parse(eml.get('Date')).strftime("%Y_%m_%d_%H_%M_%S")
    # 件名と本文を結果とする
    return \
      'From: ' + addr + "\n" + \
      'Date: ' + date + "\n" + \
      'Subject:' + subject + "\n\n" + \
      'Body:\n' + body,addr,date,subject,body

def receive_gmail(count):
    # GmailのAPIが使えるようにする
    service = gmail_get_service()
    # メッセージを扱うAPI
    messages = service.users().messages()
    # 自分のメッセージ一覧を30件得る
    msg_list = messages.list(userId='me', maxResults=count).execute()
    for j, msg in enumerate(msg_list['messages']):
        msg_id = msg['id']
        #print(i, "=", msg_id)
        m = messages.get(userId='me', id=msg_id, format='raw').execute()
        raw = base64.urlsafe_b64decode(m['raw'])
        # メールデータを保存
        text,addr,date,subject,body = email_extract_text(raw)
        # date= datetime.strptime(date,'%Y/%m/%d %H:%M:%S')
        if addr=='TOKYO TECH OCW-i <kyomu.ocw@jim.titech.ac.jp>':
            if 'zoom.us' in body:
                body_split=body.split()
                subject=subject[17:].split('] ')[1]
                for i in range(len(body_split)):
                    if 'zoom.us' in body_split[i]:
                        link=body_split[i-6]+body_split[i-5]+body_split[i-4]+body_split[i-3]+body_split[i-2]+'\n'+body_split[i-1]+'\n'+body_split[i]
                        file_text=subject+'\n'+link
                        payload = {"message": file_text}
                fname = os.path.join(save_dir,date+'.txt')
                print(j,file_text)
                print("-----------")
                if os.path.exists(fname)==False:
                    requests.post(url, headers=headers, data=payload)
                    with open(fname, 'wt', encoding='utf-8') as f:
                          f.write(file_text)
                          #f.write(text)

if __name__ == '__main__':
    receive_gmail(30)

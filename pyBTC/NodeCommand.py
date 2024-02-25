import requests
import pandas as pd
import json
from time import sleep



# 트랜잭션 입력하기
headers = {'Content-Type': 'application/json; charset=utf-8'}
data = {
    "sender": "test_from",
    "recipient": "test_to",
    "amount": "100"
}
requests.post("http://127.0.0.1:8080/transactions/new", headers=headers, data=json.dumps(data)).content

# 채굴 명령
headers = {'Content-Type': 'application/json; charset=utf-8'}
res = requests.get("http://127.0.0.1:8080/mine")


# 체인 정보 다시 가져오기
try:
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.get("http://127.0.0.1:8080/chain", headers=headers)
    status_json = res.json()  # 응답을 JSON 객체로 바로 변환
except json.decoder.JSONDecodeError:
    status_json = []

# status_json이 None이 아닐 때에만 아래의 코드를 실행합니다.
if status_json:
    tx_amount_l = []
    tx_sender_l = []
    tx_reciv_l = []
    tx_time_l = []

    for chain_index in range(len(status_json)):
        chain_tx = status_json[chain_index]['transactions']
        for each_tx in range(len(chain_tx)):
            tx_amount_l.append(chain_tx[each_tx]['amount'])
            tx_sender_l.append(chain_tx[each_tx]['sender'])
            tx_reciv_l.append(chain_tx[each_tx]['recipient'])
            tx_time_l.append(chain_tx[each_tx]['timestamp'])

    df_tx = pd.DataFrame()
    df_tx['timestamp'] = tx_time_l
    df_tx['sender'] = tx_sender_l
    df_tx['recipient'] = tx_reciv_l
    df_tx['amount'] = tx_amount_l
    df_tx

    df_sended = pd.DataFrame(df_tx.groupby('sender')['amount'].sum()).reset_index()
    df_sended.columns = ['user', 'sended_amount']
    df_received = pd.DataFrame(df_tx.groupby('recipient')['amount'].sum()).reset_index()
    df_received.columns = ['user', 'received_amount']

    df_status = pd.merge(df_received, df_sended, how='outer').fillna(0)
    df_status['balance'] = df_status['received_amount'] - df_status['sended_amount']
    print(df_status)
else:
    print("status_json이 None입니다.")

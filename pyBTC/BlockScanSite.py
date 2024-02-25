from flask import Flask, render_template
import requests
import pandas as pd
import json

app = Flask(__name__, template_folder='templates')

@app.route('/')
def index():
    try:
        headers = {'Content-Type': 'application/json; charset=utf-8'}
        res = requests.get("http://127.0.0.1:8090/chain", headers=headers)
        res.raise_for_status()  # 응답이 성공적으로 이루어졌는지 확인
        status_json = res.json()
        df_scan = pd.DataFrame(status_json['chain'])
        return render_template('index.html', df_scan=df_scan, block_len=len(df_scan))
    except requests.exceptions.RequestException as e:
        # 요청 중에 예외가 발생한 경우
        print("Request Error:", e)
        return "서버에 연결할 수 없습니다. 관리자에게 문의하세요.", 500
    except json.decoder.JSONDecodeError as e:
        # JSON 디코드 중에 예외가 발생한 경우
        print("JSON Decode Error:", e)
        return "서버가 예상한 형식으로 응답하지 않았습니다. 관리자에게 문의하세요.", 500

app.run(port=8090)

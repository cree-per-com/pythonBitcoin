from flask import Flask, request, jsonify
from pyBTC.BlockChainInstance import Blockchain
import requests

blockchain = Blockchain()
my_ip = '0.0.0.0'
my_port = '8090'
my_url = 'http://127.0.0.1:' + my_port
node_identifier = 'node_' + my_port
mine_owner = 'master'
mine_profit = 0.1

app = Flask(__name__)

@app.route('/chain', methods=['GET'])
def full_chain():
    try:
        print("chain info requested!!!")
        response = {
            'chain': blockchain.chain,
            'length': len(blockchain.chain),
        }
        return jsonify(response), 200
    except Exception as e:
        print("Exception occurred:", str(e))
        return "Internal Server Error", 500


@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    try:
        values = request.get_json()
        print("transactions_new!!! : ", values)
        required = ['sender', 'recipient', 'amount']
        if not all(k in values for k in required):
            return 'missing values', 400

        index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])
        response = {'message': 'Transaction will be added to Block {%s}' % index}
        return jsonify(response), 200
    except Exception as e:
        print("Exception occurred:", str(e))
        return "Internal Server Error", 500


@app.route('/mine', methods=['GET'])
def mine():
    try:
        print("MINING STARTED...")
        last_block = blockchain.last_block
        last_proof = last_block['nonce']
        proof = blockchain.pow(last_proof)

        blockchain.new_transaction(
            sender=mine_owner,
            recipient=node_identifier,
            amount=mine_profit
        )
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(proof, previous_hash)
        print("MINING FINISHED")

        response = {
            'message': 'New Block Found',
            'index': block['index'],
            'transactions': block['transactions'],
            'nonce': block['nonce'],
            'previous_hash': block['previous_hash']
        }
        return jsonify(response), 200
    except Exception as e:
        print("Exception occurred:", str(e))
        return "Internal Server Error", 500

# 네트워크 요청 보내기
try:
    headers = {'Content-Type': 'application/json; charset=utf-8'}
    res = requests.get(url=my_url+"/chain", headers=headers)
    if res.status_code == 200:
        response_json = res.json()  # 응답을 JSON 객체로 변환
        print(response_json)
    else:
        print("Server returned non-200 status code:", res.status_code)
except Exception as e:
    print("Exception occurred during network request:", str(e))

headers = {'Content-Type': 'application/json; charset=utf-8'}
res = requests.get(url=my_url+"/mine")
print(res)
print(res.text)

if __name__ == '__main__':
    app.run(host=my_ip, port=my_port)

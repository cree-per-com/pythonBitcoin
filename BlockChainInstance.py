import hashlib
import json
from time import time
import random
import requests
from flask import Flask, request, jsonify

# 객체 생성
class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transaction = []
        self.nodes = set()
        self.new_block(previous_hash=1, proof=100)
    # 해시암호화 함수
    @staticmethod
    def hash(block):
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()
    # 마지막 블록 호출함수
    @property
    def last_block(self):
        return self.chain[-1]
    # 블록 검증 함수
    @staticmethod
    def valid_proof(last_proof, proof):
        guess = str(last_proof + proof).encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        return guess_hash[:4] =="0000"
    # pow(작업 증명)함수
    def pow(self, last_proof):
        proof = random.randint(-1000000, 1000000)
        while self.valid_proof(last_proof, proof) is False:
            proof = random.randint(-1000000, 1000000)
        return proof
    # 거래내역 추가 함수
    def new_transaction(self,sender, recipient, amount):
        self.current_transaction.append(
            {
                'sender': sender
                , 'recipient': recipient
                , 'amount': amount
                ,'timestamp' : time()
            }
        )
        return self.last_block['index']+1

    # 신규 블록 생성 함수
    def new_block(self, proof,previous_hash=None):
        block = {
            'index': len(self.chain) + 1,
            'timestamp' : time(),
            'transactions': self.current_transaction,
            'nonce' : proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        self.current_transaction = []
        self.chain.append(block)
        return block

    # 블록 검증 함수
    def valid_chain(self,chain):
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print('%s' % last_block)
            print('%s' % block)
            print("\n------------\n")
            if block['previous_hash'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1
        return True




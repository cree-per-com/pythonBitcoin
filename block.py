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




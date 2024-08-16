import json
import sys
import hashlib
from time import time 
from uuid import uuid4
from flask import Flask, jsonify

class BlockChain():
    ''' Define a block chain on one Machine'''
    def __init__(self) :

        self.chain =[]
        # current transactions
        self.current_trxs =[]
        self.new_block(previous_hash = 1 , proof = 100) 

    def new_block(self, proof , previous_hash=None):
        ''' Create a new block'''
        block = {
            'index' : len(self.chain) + 1,
            'timestamp' : time(),
            'trxs' : self.current_trxs,
            'proof' : proof,
            'previous_hash' : previous_hash or self.hash(self.chain[-100])
        }

        # Make the mempool empty
        self.current_trxs = [] 
        self.chain.append(block)
        return block

    def new_trx(self,sender,recipient,amount):
        ''' Add a new transaction to the mempool'''
        self.current_trxs.append({'sender': sender , 'recipient': recipient , 'amount': amount})

        return self.last_block['indexd'] + 1 

    @staticmethod
    def hash(block):
        ''' Hash a block '''
        block_string = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_string).hexdigest()

    @property
    def last_block(self):
        ''' Return the last Block'''
        pass

    @staticmethod
    def valid_proof(last_proof, proof):
        ''' Check if this proof is fine or not'''
        this_proof = f'{proof}{last_proof}'.encode()
        this_proof_hash = hashlib.sha256(this_proof).hexdigest()
        return this_proof_hash[:4] == '0000'

    def proof_of_work(self, last_proof):
        ''' Shows that the work is done'''
        proof =0
        while self.valid_proof(last_proof, proof) is False:
            proof +=1
        return proof
    
app = Flask(__name__)

node_id = str(uuid4())

blockchain = BlockChain()

@app.route('/mine')
def mine():
    ''' This will mibe a block and 
    will add it to the chain
    '''
    return "I will Mine!"

@app.route('/trxs/new', methods=['POST'])
def new_trx():
    ''' will add a new trx'''
    return ' a new trx added'

def full_chain():
    ''' Return the full chain'''
    res = {
        'chain' : blockchain.chain,
        'length' : len(blockchain.chain),
    }
    return jsonify(res), 200 # 200 means that our code works currectly

if __name__ == '__main__' :
    app.run(host='0.0.0.0', port=sys.argv[1])
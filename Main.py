import json
import hashlib
from time import time 

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
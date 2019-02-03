# -*- coding: utf-8 -*-
"""
Created on Sun Feb  3 18:42:21 2019

@author: prateek shukla
"""

# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import hashlib

from flask import Flask,jsonify

import datetime
import json

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.create_block(proof=1,previous_hash = '0')
        
    def create_block(self,proof,previous_hash):
        block={'index' : len(self.chain) + 1,
               'proof' :proof,
               'timestamp' : str(datetime.datetime.now()),
               'previous_hash' : previous_hash,
               'Current_Hash' : ''
               
                }
       # hash_code = self.hash(block)
        #block['Current_Hash'] = hash_code
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return(self.chain[-1])
    
    def proof_of_work(self,previous_proof):
        new_proof = 1
        check_proof = False
        while not check_proof:
            hash_opration = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_opration[:4] == '0000':
                check_proof = True
            else:
                new_proof+=1
        return new_proof
    def hash(self,block):
        encoded_block = json.dumps(block,sort_keys = True).encode()
        return(hashlib.sha256(encoded_block).hexdigest())
    
    
    def is_chain_valid(self,chain):
        previous_block = chain[0]
        block_index = 1
        
        while block_index<len(chain):
            block = chain[block_index]
            
            previous_block_hash = block['previous_hash']
            
            if previous_block_hash != self.hash(previous_block): 
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            
            hash_opration = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            
            if hash_opration[:4] != '0000':
                return False
            previous_block = block
            block_index+=1
        return True
#cREATING A Web App
app = Flask(__name__)

#creating A block chain

blockchain = Blockchain()

#Mining A Block

@app.route('/mine-block',methods = {'GET'})

def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof,previous_hash)
    response = {'message' : 'Congo You Just MINE A Block',
                'index' : block['index'],
                'proof' : block['proof'],
                'timestamp' : block['timestamp'],
                'previous_hash' : block['previous_hash']
            
            }
    return jsonify(response),200
    

@app.route('/get-chain',methods = {'GET'})

def get_chain():
    response = {'chain' : blockchain.chain,
                'length' : len(blockchain.chain)
            }
    return jsonify(response),200
            
    
#Run The App
app.run(host = "0.0.0.0",port = 5000)

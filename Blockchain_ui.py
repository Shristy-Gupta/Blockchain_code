# -*- coding: utf-8 -*-
"""
Created on Thu Jun  3 20:27:23 2021

@author: shris
"""

# Module 1 --> Create BlockChain
import datetime # Each block will have exact date when its mined
import hashlib # We will work with hash functions
import json # Encode the block 
from flask import Flask, jsonify # The messages are returned from the blockchain
# Part 1 Building blockchain
class Blockchain:
    def __init__(self):
        self.chain=[];
        self.create_block(proof=1,previous_hash='0')
    def create_block(self,proof,previous_hash):
        #Each block in the blockchain will have the following property
        # Here Index is block Number
        # Proof is same as nonce
        block = {'index':len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof':proof,
                 'previous_hash':previous_hash
                 }
        self.chain.append(block)
        return block
    def get_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self,previous_proof):
        new_proof=1;
        check_proof=False
        while check_proof is False:
            #This problem/equation is completely chosen as per the choice.
            #The problem can be modified/hardened
            POW=hashlib.sha256(str(previous_proof**2-new_proof**2).encode()).hexdigest();
            # Here the target is only 4 zeros
            if POW[:4]=='0000':
                check_proof = True
            else:
                new_proof+=1
        return new_proof
    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        block_index=1
        while block_index<len(chain):
            current_block=chain[block_index]
            if current_block['previous_hash']!=previous_block['proof']:
                return False
            previous_proof=previous_block['proof']
            current_proof=current_block['proof']
            POW=hashlib.sha256(str(previous_proof**2-current_proof**2).encode()).hexdigest();
            if POW[:4]!='0000':
                return False
            previous_block=current_block
            block_index+=1
        return True


# part 2 --> Mining the blockchain
# Creating the web App
# FLask based web application
app=Flask(__name__)
app.config['JSONIFY_PREETYPRINT_REGULAR']=False

# Creating the Block chain
blockchain=Blockchain()
# Decorator
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    new_proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    new_created_block=blockchain.create_block(new_proof, previous_hash)
    response = {'message':'COngratulate miner you just mined a block!',
                'index':new_created_block['index'],
                'timestamp':new_created_block['timestamp'],
                'proof':new_created_block['proof'],
                'previous_Hash':new_created_block['previous_hash']}
    return jsonify(response),200
    
# Decorator
@app.route('/get_chain', methods=['GET'])     
def get_chain():
    response={'chain':blockchain.chain,
              'length':len(blockchain.chain)}
    return jsonify(response),200

@app.route('/is_valid', methods=['GET']) 
def is_valid():
    is_valid = blockchain.is_chain_valid(blockchain.chain)
    if is_valid:
        response = {'message': 'All good. The Blockchain is valid.'}
    else:
        response = {'message': 'Houston, we have a problem. The Blockchain is not valid.'}
    return jsonify(response), 200
    

# 0.0.0.0 makes the host available to anyone
app.run(host='0.0.0.0', port=5000)
       

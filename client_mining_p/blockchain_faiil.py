
import hashlib
import json
from flask.json import JSONEncoder
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request

# fell behind, spent too much time trying to serialize a custom Block class, which is a giant pain

# Block class index needs to be passed in, or defaults to genesis index, other ones only BlockChain has knowledge of


class Block():
    def __init__(self, index, proof, transactions, previous_hash):
        self.timestamp = time()
        self.index = index
        self.proof = proof
        self.transactions = transactions
        self.previous_hash = previous_hash


class CustomEncoder(JSONEncoder):
    def default(self, obj):
        if type(obj) == 'Block':
            return {
                'timestamp': self.timestamp,
                'index': self.index,
                'proof': self.proof,
                'transactions': self.transactions,
                'previous_hash': self.previous_hash
            }
        else:
            super().default()


# block chain class only needs:
# * chain - an array of the current blocks in the chain (if no block passed in, needs genesis block)
# * current transactions - all the transactions that will be added in the next block


class Blockchain():
    def __init__(self):
        ''' Initializes with a new block.'''
        self.current_transactions = []
        self.chain = [self.__gen_genesis__()]

    def __gen_genesis__(self):
        transactions = self.current_transactions
        return Block(index=0, proof=1337, transactions=transactions, previous_hash='Started from the bottom')

    def __wipe_transactions__(self):
        self.current_transactions = []

    def forge(self, block):
        self.chain.append(block)
        self.__wipe_transactions__()

    def hash(self, block):
        block_string = json.dumps(block, sort_keys=True).encode()
        block_hash = hashlib.sha256(block_string)
        hex_hash = block_hash.hexdigest()
        return hex_hash

    def get_last(self):
        return self.chain[-1]

    def gen_proof(self, block):
        # what do I need to generate a new proof?
        stringified_block = json.dumps(block, sort_keys=True).encode()
        guess = 0
        while self.validate_proof(stringified_block, guess) is False:
            guess += 1
        return guess

    @staticmethod
    def validate_proof(block_string, proof):
        # static method, doesn't need self
        # checks if the block string + proof has the correct amount of zeroes
        guess_string = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess_string).hexdigest()

        # slice the first 3 characters and check if it has at least three coins appended
        return guess_hash[:3] == '000'


app = Flask(__name__)
node_id = str(uuid4()).replace('-', '')

# Instantiate the blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    # get all the appropriate arguments
    last_block = blockchain.get_last()
    current_index = len(blockchain.chain)
    proof = blockchain.gen_proof(last_block)
    previous_hash = blockchain.hash(last_block)
    transactions = blockchain.current_transactions

    new_block = Block(current_index, proof, transactions, previous_hash)
    blockchain.forge(new_block)

    response = {
        'block': new_block.convert_to_dict()
    }

    return jsonify(response), 200


@app.route('/chain', methods=['GET'])
def chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


if __name__ == '__main__':
    app.run(host='localhost', port=5000)

import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain():
    def __init__(self):
        self.chain = []
        self.current_transactions = []

        # Create the genesis block
        self.new_block(previous_hash='started at the bottom', proof=100)

    def new_block(self, proof, previous_hash=None):
        """ Creates a new block in the block chain and appends it. It should contain an index, timestamp
        list of current transactions, proof used to mine this block, the hash of the previous block. """

        block = {
            'index': len(self.chain),
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.last_block)
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        transaction = {
            'sender': sender,
            'recipient': recipient,
            'amount': amount
        }
        self.current_transactions.append(transaction)
        # return the index of the block this transaction will be on
        return self.last_block['index'] + 1

    def hash(self, block):
        """Returns a SHA-256 hash string of a Block"""

        string_block = json.dumps(block, sort_keys=True)
        # hashlib expects a byte string, versus python strings are still objects with metadata
        byte_string = string_block.encode()
        raw_hash = hashlib.sha256(byte_string)

        # SHA256 function returns the hash in a raw string with escaped characters
        # .hexdigest() converts the hash to a string of hexadecimal characters, which is
        # easier to work with and understand
        hex_hash = raw_hash.hexdigest()
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        """ A valid proof is a a randomly generated string (in this case integers), that return a hash with the correct amount of leading zeroes. Determines if the hash generated from the block string and proof is valid, thus proving the proof is valid."""

        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        return guess_hash[:6] == '000000'


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()


@app.route('/mine', methods=['POST'])
def mine():
    data = request.get_json()
    print(f'Client Proof: {data}')
    required = ['proof', 'id']

    if not all(k in data for k in required):
        response = {'message': "missing values"}
        return jsonify(response), 400

    client_proof = data['proof']
    block_string = json.dumps(blockchain.last_block, sort_keys=True).encode()

    if blockchain.valid_proof(block_string, client_proof):
        # reward the miner for finding a valid proof
        blockchain.new_transaction(sender=0, recipient=data['id'], amount=1)

        previous_hash = blockchain.hash(blockchain.last_block)
        block = blockchain.new_block(client_proof, previous_hash=previous_hash)
        response = {'message': 'New Block Forged', 'new_block': block}

        return jsonify(response), 201
    else:
        response = {
            'message': 'Proof was invalid or late'
        }

    return jsonify(response), 403


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def get_last():
    # remember to return a json
    response = {
        'last_block': blockchain.last_block
    }
    return jsonify(response), 200


@app.route('/transactions/new', methods=['POST'])
def add_transaction():
    # data validation
    data = request.get_json()
    required = ['sender', 'recipient', 'amount']
    # for each key in required, check if key is in data
    if not all(key in data for key in required):
        response = {
            'message': 'Please include a sender, recipient, and amount in your transaction request'}
        return jsonify(response), 400

    index = blockchain.new_transaction(
        sender=data['sender'], recipient=data['recipient'], amount=data['amount'])

    response = {
        'message': f'Transaction created, it will be recorded on Block {index}'
    }
    return jsonify(response), 201


# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

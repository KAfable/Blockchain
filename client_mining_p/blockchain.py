import hashlib
import json
from time import time
from uuid import uuid4

# Block class index needs to be passed in, or defaults to genesis index, other ones only BlockChain has knowledge of


class Block():
    def __init__(self, index=1, proof, transactions, previous_hash):
        self.timestamp = time.now()
        self.index = index
        self.proof = proof
        self.transactions = transactions
        self.previous_hash = previous_hash

# block chain class only needs:
# * chain - an array of the current blocks in the chain (if no block passed in, needs genesis block)
# * current transactions - all the transactions that will be added in the next block


class Blockchain():
    def __init__(self):
        ''' Initializes with a new block.'''
        self.chain = [self.__gen_genesis__()]
        self.current_transactions = []

    def __gen_genesis__(self):
        return new Block(proof=1337, transactions=self.current_transactions, previous_hash='Started from the bottom')

    def __wipe_transactions__(self):
        self.current_transactions = []

    def forge(self):
        # get all the appropriate arguments
        current_index = len(self.chain)
        proof = self.gen_proof()
        previous_hash = self.get_last.previous_hash
        new_block = Block(current_index, proof, transactions, previous_hash)
        self.chain.append(new_block)
        self.__wipe_transactions__()

    def get_last(self):
        return self.chain[-1]

    def gen_proof(self, block):
        # what do I need to generate a new proof?
        # needs
        stringified_block = json.dumps(block, sort_keys=True)
        guess = 0
        while self.validate_proof(stringified_block, guess) is False:
            guess += 1
        return guess

    def validate_proof(block_string, proof):
        # static method, doesn't need self
        # checks if the block string + proof has the correct amount of zeroes
        guess_string = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()

        # slice the first 3 characters and check if it has at least three coins appended
        return guess_hash[:3] == '000'


app = Flask(__name__)
node_id = str(uuid4().replace('-', ''))
blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    pass


@app.chain('/chain', methods=['GET'])
def chain():
    pass


if __name__ = '__main__':
    app.run(host='localhost', port=5000)

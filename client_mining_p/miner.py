import hashlib
import requests

from datetime import datetime

import sys
import json


def gen_proof(block):
    """ A simple proof of work algorithm that generates a string from incrementing integers. It attaches this integer to a stringified block and checks if its valid. Returns the number that creates the valid hash as determiend by valid_proof."""

    start = datetime.now()
    print(f"Proof generation started on: {start}")
    block_string = json.dumps(block, sort_keys=True).encode()
    proof = 0
    while valid_proof(block_string, proof) is False:
        proof += 1
    end = datetime.now()
    duration = end - start
    print(f'Total Time(s) : {duration.total_seconds()}')
    return proof


def valid_proof(block_string, proof):
    """ A valid proof is a a randomly generated string (in this case integers), that return a hash with the correct amount of leading zeroes. Determines if the hash generated from the block string and proof is valid, thus proving the proof is valid. This matches the validation algorithm that the server uses so we aren't sending incorrect guesses to the server."""

    guess = f"{block_string}{proof}".encode()
    guess_hash = hashlib.sha256(guess).hexdigest()

    return guess_hash[:6] == '000000'


if __name__ == '__main__':
    # What is the server address? IE `python3 miner.py https://server.com/api/`
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "http://localhost:5000"

    # Load ID
    f = open("my_id.txt", "r")
    id = f.read()
    print("ID is", id)
    f.close()

    coins = 0
    print("Initializing mining session")

    # Run forever until interrupted
    while True:
        r = requests.get(url=node + "/last_block")
        # Handle non-json response
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        block = data['last_block']
        new_proof = gen_proof(block)
        print(f'proof found: {new_proof}')

        # When found, POST it to the server {"proof": new_proof, "id": id}
        post_data = {"proof": new_proof, "id": id}
        r = requests.post(url=node + "/mine", json=post_data)
        try:
            data = r.json()
        except ValueError:
            print("Error:  Non-json response")
            print("Response returned:")
            print(r)
            break

        print(data['message'])
        server_res = data['message']
        if server_res == 'New Block Forged':
            coins += 1
        print(f'Total Coins: {coins}')

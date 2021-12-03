import datetime

# Calculating the hash
import hashlib

# To store data in json format
import json

# Flask is for creating the web
from flask import Flask, jsonify


class Blockchain:

    # This function is created to create the very first block and set it's hash to 0
    def __init__(self):
        self.chain = []
        self.create_block(proof=1, previous_hash='0')

    # This function adds further blocks into the chain
    def create_block(self, proof, previous_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 }
        self.chain.append(block)
        return block

    # This function is created to display the previous block
    def print_previous_block(self):
        return self.chain[-1]

    # This is the function for proof of work
    def proof_of_work(self, previous_proof):
        # miners proof submitted
        new_proof = 1

        # status of proof of work
        check_proof = False

        while check_proof is False:
            # doing the hash operation
            hash_operation = hashlib.sha256(str(new_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            # check miners solution to problem
            # if miners proof results in 4 leading zero's in the hash operation:
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                # if miners solution is wrong, give mine another chance until correct
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()  # dumps encodes python object into json format
        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):
        # get the first block in the chain and it serves as the previous block
        previous_block = chain[0]

        # an index of the blocks in the chain for iteration
        block_index = 1

        while block_index < len(chain):
            # get the current block
            block = chain[block_index]

            # check if the current block link to previous block is the same as the hash of the previous block
            if block["previous_hash"] != self.hash(previous_block):
                return False

            # get the previous proof from the previous block
            previous_proof = previous_block['proof']

            # get the current proof from the current block
            current_proof = block['proof']

            # run the proof data through the algorithm
            hash_operation = hashlib.sha256(str(current_proof ** 2 - previous_proof ** 2).encode()).hexdigest()

            # check if hash operation is invalid
            if hash_operation[:4] != '0000':
                return False

            # set the previous block to the current block after running validation on current block
            previous_block = block
            block_index += 1

        return True


# Creating the Web App using flask
app = Flask(__name__)

# Create the object
blockchain = Blockchain()


# Mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.print_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(proof, previous_hash)

    response = {'message': 'A block Mined Successfully!!',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash']
                }

    return jsonify(response), 200


# Display blockchain in json format
@app.route('/get_chain', methods=['GET'])
def display_chain():
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)}
    return jsonify(response), 200


# # Check validity of blockchain
@app.route('/valid', methods=['GET'])
def valid():
    valid = blockchain.is_chain_valid(blockchain.chain)

    if valid:
        response = {'message': 'The Blockchain is valid.'}
    else:
        response = {'message': 'The Blockchain is not valid.'}
    return jsonify(response), 200


# Run the flask server locally
app.run(host='127.0.0.1', port=5000)
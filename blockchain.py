from block import Block
from transaction import Transaction
import json
from flask import Flask
app = Flask(__name__)

# @app.route("/initiate")
# def genesisBlock():
#     genesisTransaction = Transaction("","",0);
#     tl = []
#     tl.append(genesisTransaction)
#     genesis = Block("",tl)
#     with open("blockchain.json", "w") as blockchain:
#         info = {}
#         info[genesis.getHash()] = genesis.getAllInfo()
#         blockchain.write(json.dumps(info))
#     return "Created genesis block with hash: "+genesis.getHash()

# tl1 = []
# tl1.append(Transaction("Adam", "Bob", 2))
# tl1.append(Transaction("Bob", "Eve", 3))
# block1 = Block(genesis.getHash(),tl1)
# print(genesis.getHash())
# print(block1.getAllInfo())

@app.route('/')
def createBlock():
    #Get the active nodes
    #Create the block
    #Send a request to the active nodes

if __name__ == '__main__':
    port = input("Port: ")
    app.run("127.0.0.1",port)
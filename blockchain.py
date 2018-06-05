from block import Block
from transaction import Transaction
import json, random, string, requests
from flask import Flask, request
app = Flask(__name__)

#Primary node
pnode = 'http://127.0.0.1:5000/chain'

Blockchain = {}
blocksList = []

@app.route("/initiate")
def genesisBlock():
    genesisTransaction = Transaction("","",0);
    tl = []
    tl.append(genesisTransaction)
    genesis = Block("",tl,None)
    blocksList.append(genesis)
    Blockchain[genesis.getHash()] = genesis.getAllInfo()
    # with open("blockchain.json", "w") as blockchain:
    #     info = {}
    #     info[genesis.getIndex()] = genesis.getAllInfo()
    #     blockchain.write(json.dumps(info))
    return "Created genesis block with hash: "+genesis.getHash()

@app.route("/chain")
def printBlockchain():
    return json.dumps(Blockchain)
    # info = {}
    # for block in Blockchain:
    #     info[block.getIndex()] = block.getAllInfo()
        
    # content = ""
    # with open("blockchain.json", "r") as blockchain:
    #     for line in blockchain.readlines():
    #         content = content + line
    # return content

@app.route("/addblock", methods=['GET', 'POST']) 
def addBlock():
    info = ""
    if request.method == 'POST':  
       info = request.form.get('blockInfo')
    blockInfo = json.loads(info)
    #Get the entire blockchain
    r = requests.get(pnode)
    latestBlockchain = json.loads(r.text)

    Blockchain[blockInfo['hash']] = blockInfo
    
    #Create t


# def generateRandomString(num):
#     return ''.join([random.choice(string.ascii_letters + string.digits) for n in xrange(num)])

# def dummyTransactions(num):
#     t = []
#     for x in range(num):
#         t.append(Transaction(generateRandomString(),generateRandomString(),random.randint(1,100)))
#     return t

# def getBlockchain():
#     #Get the updated blockchain from a hard-coded primary node



# @app.route('/')
# def createBlock():
#     #Get the blockchain
#     getBlockchain()
#     #Create the block
 #Parse the transactions
    # allTransactions = []
    # snippets = transactions.split(",")
    # for snippet in snippets:
    #     source = snippet.split(":")[0]
    #     dest = snippet.split(":")[1]
    #     value = int(snippet.split(":")[2])
    #     allTransactions.append(Transaction(source,dest,value))
#     #Send a request to the active nodes

if __name__ == '__main__':
    #Open blockchain.json and add it to a list
    with open("blockchain.json",'r') as b:
        json.loads(b.read())
    port = input("Port: ")
    app.run("127.0.0.1",port)
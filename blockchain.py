from block import Block
import block as block_
from transaction import Transaction
import json, random, string, requests
from flask import Flask, request
app = Flask(__name__)

#Primary node
pnode = 'http://127.0.0.1:5000/chain'

Blockchain = {}
blocksList = []

def generateRandomString(num):
    return ''.join([random.choice(string.ascii_letters + string.digits) for n in range(num)])

def dummyTransactions(num):
    t = []
    for x in range(num):
        t.append(Transaction(generateRandomString(8),generateRandomString(8),random.randint(1,100)))
    return t

def parseTransactions(transaction):
    allTransactions = []
    snippets = transactions.split(",")
    for snippet in snippets:
        source = snippet.split(":")[0]
        dest = snippet.split(":")[1]
        value = int(snippet.split(":")[2])
        allTransactions.append(Transaction(source,dest,value))
    return allTransactions

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

def getBlockchain():
    #Get the updated blockchain from a hard-coded primary node
    r = requests.get(pnode)
    latestBlockchain = json.loads(r.text)
    return latestBlockchain

def getLastBlock():
    previousBlock = {}
    latestBlockchain = getBlockchain()
    lastIndex = len(latestBlockchain) - 1
    for key,value in latestBlockchain.items():
        if value['index'] == lastIndex:
            previousBlock = value
    return previousBlock


@app.route("/addblock", methods=['GET', 'POST']) 
def addBlock():
    info = ""
    if request.method == 'POST':  
       info = request.form.get('blockInfo')
    blockInfo = json.loads(info)
    latestBlockchain = getBlockchain()
    lastIndex = len(latestBlockchain) - 1
    # newBlock = Block(blockInfo['previousHash'],parseTransactions(blockInfo['transactions']))
    previousBlock = getLastBlock()

    if block_.validateJson(previousBlock, blockInfo):
        #Added to the list
        Blockchain[blockInfo['hash']] = blockInfo
        blocksList.append(Block(blockInfo['hash'],parseTransactions(blockInfo['transactions']),int(lastIndex)))
    

@app.route('/createblock')
def createBlock():
    #Get the blockchain
    latestBlockchain = getBlockchain()
    lastIndex = len(latestBlockchain)-1
    previousBlock = getLastBlock()
    #Create the block
    newBlock = Block(previousBlock['hash'],dummyTransactions(6),int(lastIndex))
    newBlockJson = newBlock.getAllInfo()
    if block_.Block.validateJson(getLastBlock(),newBlockJson):
        #Add to the existing chain
        Blockchain[newBlock.getHash()] = newBlockJson
        return json.dumps(Blockchain)
    return "Could not create"
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
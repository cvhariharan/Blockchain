from block import Block
import block as block_
from transaction import Transaction
import json, random, string, requests, time
import _thread
from flask import Flask, request, jsonify, render_template
app = Flask(__name__)

parentNodes = ""
friendNodes = ""
primary = 0
#Primary node
pnodes = []#'http://127.0.0.1:5000'
#Friend nodes
fnodes = []
port = 0
#Update intervals in seconds
uTime = 10

Blockchain = {}
blocksList = []

def getParents():
    t = parentNodes.split(",")
    for pnode in t:
        if len(pnode) != 0:
            pnodes.append(pnode.replace("\n",""))

def getFriends():
    t = friendNodes.split(",")
    for fnode in t:
        if len(fnode) != 0:
            fnodes.append(fnode.replace("\n",""))


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
    Blockchain.clear()
    Blockchain[genesis.getHash()] = genesis.getAllInfo()
    #Send a request to friend nodes to update
    payload = {'blockInfo':json.dumps(genesis.getAllInfo())}
    for fnode in fnodes:
        r = requests.post(fnode+"/addblock", data = payload)
    return "Created genesis block with hash: "+genesis.getHash()

@app.route('/view')
def view():
    return render_template('chain.html', result = Blockchain)

@app.route('/button')
def root():
    return render_template('button.html')

@app.route("/chain")
def printBlockchain():
    return jsonify(Blockchain)
    #return render_template('chain.html', result = Blockchain)

def getBlockchain():
    #Get the updated blockchain from a hard-coded primary node
    latestBlockchain = Blockchain
    if primary == 0:
        for pnode in pnodes:
            r = requests.get(pnode+"/chain")
            if r.status_code == 200:
                latestBlockchain = json.loads(r.text)
                # print("primary")
                # print(latestBlockchain)
    else:
        #If it's a primary node, query all friend nodes to see whose blockchain is the longest
        localLastIndex = len(Blockchain)-1
        for fnode in fnodes:
            r = requests.get(fnode+"/chain")
            if r.status_code == 200:
                temp = json.loads(r.text)
                if len(temp) > 0:
                    if len(temp)-1 > localLastIndex:
                        latestBlockchain = temp
                print(latestBlockchain)
    return latestBlockchain
    

def getLastBlock():
    lastBlock = {}
    latestBlockchain = getBlockchain()
    lastIndex = len(latestBlockchain) - 1
    for key,value in latestBlockchain.items():
        if value['index'] == lastIndex:
            lastBlock = value
    return lastBlock

def getLocalLastBlock():
    #Returns the last block stored locally
    lastBlock = {}
    lastIndex = len(Blockchain) - 1
    for key,value in Blockchain.items():
        if value['index'] == lastIndex:
            lastBlock = value
    return lastBlock

def isUpdated():
    lastBlock = getLastBlock()
    lastIndex = lastBlock['index']
    localLastBlock = getLocalLastBlock()
    localLastIndex = -1

    if len(localLastBlock) != 0:
        localLastIndex = localLastBlock['index']
    
    if localLastIndex < lastIndex:
        print("update")
        return False
    return True

def update():
    #Checks the primary nodes for updated blockchain
    global Blockchain
    if not isUpdated():
        Blockchain = getBlockchain()

def updateThread():
    #Just an infinite loop meant to be run as thread to update the local blockchain
    while True:
        update()
        time.sleep(uTime)


@app.route("/addblock", methods=['GET', 'POST']) 
def addBlock():
    info = ""
    if request.method == 'POST':  
       info = request.form['blockInfo']
    print(info)
    blockInfo = json.loads(info)
    #Check and update the local blockchain
    #if primary == 0:
        #Update only of not primary node
    update()
    lastIndex = len(Blockchain) - 1
    # newBlock = Block(blockInfo['previousHash'],parseTransactions(blockInfo['transactions']))
    previousBlock = getLastBlock()

    if block_.Block.validateJson(previousBlock, blockInfo):
        #Added to the list
        Blockchain[blockInfo['hash']] = blockInfo
        if primary == 1:
            payload = {'blockInfo':info}
            for fnode in fnodes:
                r = requests.post(fnode+"/addblock", data = payload)
        print(Blockchain)
        #blocksList.append(Block(blockInfo['hash'],parseTransactions(blockInfo['transactions']),int(lastIndex)))
        return "Added"
    return "Not Added"
    

@app.route('/createblock')
def createBlock():
    #Get the blockchain
    if primary == 0:
        print("Primary cb")
        #Only for normal nodes
        latestBlockchain = getBlockchain()
        lastIndex = len(latestBlockchain)-1
        previousBlock = getLastBlock()
        #Create the block
        newBlock = Block(previousBlock['hash'],dummyTransactions(6),int(lastIndex))
        newBlockJson = newBlock.getAllInfo()
        if block_.Block.validateJson(previousBlock,newBlockJson):
            #Add to the existing chain
            Blockchain[newBlock.getHash()] = newBlockJson
            #Send a request to primary nodes to update
            payload = {'blockInfo':json.dumps(newBlockJson)}
            for pnode in pnodes:
                r = requests.post(pnode+"/addblock", data = payload)
        # return jsonify(Blockchain)
        return render_template('chain.html', result = Blockchain)
    else:
        previousBlock = getLocalLastBlock()
        lastIndex = previousBlock['index']
        newBlock = Block(previousBlock['hash'],dummyTransactions(6),int(lastIndex))
        newBlockJson = newBlock.getAllInfo()
        if block_.Block.validateJson(previousBlock,newBlockJson):
            #Add to the existing chain
            Blockchain[newBlock.getHash()] = newBlockJson
            #Send a request to friend nodes to update
            payload = {'blockInfo':json.dumps(newBlockJson)}
            for fnode in fnodes:
                r = requests.post(fnode+"/addblock", data = payload)

        #return jsonify(Blockchain)
        return render_template('chain.html', result = Blockchain)
    return "Could not create"

if __name__ == '__main__':
    port = int(input("Port: "))
    primary = int(input("Primary (1 or 0): "))
    if primary == 0:
        parentNodes = input("Parent Nodes (comma separated): ")
        getParents()
        #Start the updateThread to continuously check and update the local blockchain
        _thread.start_new_thread( updateThread , ())
    else:
        friendNodes = input("Other primary nodes (comma separated): ")
        getFriends()
    app.run("127.0.0.1",port)
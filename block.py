#10 minutes
import hashlib, json
import transaction
class Block:
    def __init__(self, previousHash, transactions, index):
        if index != None:
            self.previousHash = previousHash
            self.index = index + 1#blocks[self.previousHash]['index']+1
            self.transactions = transactions
        else:
            self.previousHash = ""
            self.index = 0
            self.transactions = transactions
        hash_object = hashlib.sha1(str((self.previousHash + str(self.index) + str(self.transactions))).encode())
        self.hash = hash_object.hexdigest()
    

    def getHash(self):
        return self.hash

    def getIndex(self):
        return self.index
    
    def getAllTransactions(self):
        allTransactions = []
        for transaction in self.transactions:
            allTransactions.append(transaction.getInfo())
        return allTransactions
    
    def getAllInfo(self):
        block = {}
        transactions = self.getAllTransactions()
        block['transactions'] = transactions
        block['previousHash'] = self.previousHash
        block['index'] = self.index
        block['hash'] = self.hash
        return block

    def validate(previousBlock, block):
        if block.previousHash == previousBlock.getHash():
            if block.getIndex() == (previousBlock.getIndex()+1):
                return True
            else:
                return False
        else:
            return False

    def validateJson(previousJson, blockJson):
        print("old")
        print(previousJson)
        print("new")
        print(blockJson)
        if blockJson['index'] != 0:
            if blockJson['previousHash'] == previousJson['hash']:
                if int(blockJson['index']) == int(previousJson['index']+1):
                    print("True")
                    return True
                else:
                    return False
            else:
                return False
        else:
            #If its genesis block
            if len(previousJson) > 0:
                if previousJson['index'] != blockJson['index']:
                    return True
                else:
                    return False
            else:
                return True


    def getLongestChain(newBlockchain, Blockchain):
        if len(newBlockchain) > Blockchain:
            Blockchain = newBlockchain
        return Blockchain


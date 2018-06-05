#10 minutes
import hashlib
import transaction
class Block:
    def __init__(self, previousHash, transactions):
        self.previousHash = previousHash
        self.transactions = transactions
    

    def getHash(self):
        hash_object = hashlib.sha1(str((self.previousHash + str(self.transactions))).encode())
        return hash_object.hexdigest()
    
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
        return block


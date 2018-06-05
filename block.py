#10 minutes
import hashlib
class Block:
    def __init__(self, previousHash, transactions):
        self.previousHash = previousHash
        self.transactions = transactions
    

    def getHash(self):
        hash_object = hashlib.sha1(str(hash((self.previousHash, self.transactions))).encode())
        return hash_object.hexdigest()


block = Block(None,None)
print(block.getHash())
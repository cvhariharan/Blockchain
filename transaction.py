#1 minute
class Transaction:
    def __init__(self,source,dest,value):
        self.source = source
        self.destination = dest
        self.value = value
    
    def getInfo(self):
        return self.source + ":" + self.destination + ":" + str(self.value)
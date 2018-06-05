#5 minutes
from flask import Flask
app = Flask(__name__)

@app.route('/')
def availableNodes():
    allNodes = ""
    with open('list.txt','r') as nodes:
        for line in nodes.readlines():
           allNodes = allNodes + line
        return allNodes

if __name__ == '__main__':
   app.run()
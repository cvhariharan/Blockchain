# Blockchain
Each instance of blockchain.py will be a new node. If the port is 5000, it is a primary node. There has to be at least one primary node.

Creating a primary node -

    python3 blockchain.py
    port: 5000
    primary (1 or 0): 1
    Other friend nodes (comma separated): http://127.0.0.1:5001,
Creating a normal node - 
```
python3 blockchain.py
port: 2000
primary (1 or 0): 0
Parent nodes (comma separated): http://127.0.0.1:5000,
```

Normal nodes can be created using other port numbers. To create the genesis block, visit http://127.0.0.1:5000/initiate . Genesis block can only be created by the primary node. To add dummy blocks, visit /createblock on any node with appropriate host and port number. 

This was created to get a better understanding of how the blockchain and p2p networking work. Not suitable for any real world applications.


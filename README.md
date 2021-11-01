# Building a layer-2 DAPP on top of Blockchain

## Guide: Prof. Vinay Ribeiro, CS 765, IIT Bombay 

This code is strictly adapted for Windows systems.
### Requirements
- [python](https://www.python.org/downloads/) (recommended >= 3.6)
- [py-sol-cx](https://pypi.org/project/py-solc-x/) 
   - solc version 0.4.25 (refer this [link](https://solcx.readthedocs.io/en/latest/version-management.html?highlight=precompiled#installing-precompiled-binaries))
- [web3](https://pypi.org/project/web3/)
- [geth 1.9.3](https://gethstore.blob.core.windows.net/builds/geth-windows-amd64-1.9.3-cfbb969d.zip)

### Usage
[TO BE FILLED]

<!-- 

Note that we assume the version of go-ethereum is 1.9.3, solidity 0.4.25


1. Run following command to install the requried things (if not already installed)
sh installGo.sh
sh installpy3.sh

2.  Download the go-ethereum code and keep it in $HOME. 

3. cd go-ethereum  
   make

2. Run the following command and copy the address to the genesis.json in the alloc section that adds the balance to the geth account.

geth --datadir $HOME/HW3/test-eth1/ --password $HOME/HW3/password.txt account new


3. Run the following command to set up the Ethereum node.

sh runEthereumNode.sh


4. Run the following command, which will deploy the smart contract and copy the smart contract address to contractAddressList

python3 deployContract.py > contractAddressList


5. Run the following command to send the transaction

python3 sendTransaction.py -->

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
- Run `.\listener.ps1` in a seperate Powershell terminal. This is the listener which will process all the requests.
- Run `python deploy.py` in a separate terminal to deploy the contract `JointAccount.sol`, the address of which will be saved in `files\contractAddressList`. This file will be used to determine the address of the contracts deployed through the aforementioned script.
- Run `interact.py` to call the different functions of the deployed contract.

**NOTE**: Importing py-solc-x prints `INFO: Could not find files for the given pattern(s).` to the terminal, which is probably harmless.

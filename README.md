# Building a layer-2 DAPP on top of Blockchain

## Guide: Prof. Vinay Ribeiro, CS 765, IIT Bombay 

### Requirements
- [python](https://www.python.org/downloads/) (recommended >= 3.6)
- [py-solc-x](https://pypi.org/project/py-solc-x/) 
   - solc version 0.4.25 (refer this [link](https://solcx.readthedocs.io/en/latest/version-management.html?highlight=precompiled#installing-precompiled-binaries))
- [web3](https://pypi.org/project/web3/)
- [geth 1.9.3](https://geth.ethereum.org/downloads/) (Windows or Linux binary)
- [matplotlib](https://pypi.org/project/matplotlib/) (only for `plot.py`)

### Usage
It is assumed that the `geth` binary is placed at the base directory of this repository, which is also the working directory for any of the scripts.

- Run `.\listener.ps1` or `./listener.sh` (depending on your OS) in a seperate terminal. This is the listener which will process all the requests.
- Run `python deploy.py` in a separate terminal to deploy the contract `JointAccount.sol`, the address of which will be saved in `files\contractAddressList`. This file will be used to determine the address of the contracts deployed through the aforementioned script.
- Run `python interact.py` to call the different functions and perform any analysis on the deployed contract. Running this file will produce a log of creation and mining of every transaction generated, in the file `run.log`. Be sure to make a backup of this file for persistence across various runs.
- Run `python plot.py` which will produce the desired plot sand save it to `plot.png`, using the `run.log` file.

**NOTE**: Importing py-solc-x prints `INFO: Could not find files for the given pattern(s).` to the terminal, which is probably harmless.

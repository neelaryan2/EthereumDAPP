# Building a layer-2 DAPP on top of Blockchain

## Guide: Prof. Vinay Ribeiro, CS 765, IIT Bombay

### Requirements

-  [python 3](https://www.python.org/downloads/) (recommended >= 3.6)
-  [py-solc-x](https://pypi.org/project/py-solc-x/) (solc 0.4.25 [installation](https://solcx.readthedocs.io/en/latest/version-management.html?highlight=precompiled#installing-precompiled-binaries))
-  [web3 4.9.0](https://pypi.org/project/web3/)
-  [geth 1.9.3](https://geth.ethereum.org/downloads/) (Windows or Linux precompiled binary)
-  [matplotlib](https://pypi.org/project/matplotlib/) (only for `plot.py`)

### solc 0.4.25 Installation
The following is to be done only once before running the project.
```
Python x.x.x
Type "help", "copyright", "credits" or "license" for more information.
>>> import solcx
>>> solcx.install_solc('0.4.25')
Version('0.4.25')
```

### Usage
It is assumed that the `geth` (or `geth.exe`) binary is placed at the base directory of this repository, which is also the working directory for any of the scripts.
- Run `.\runEthereumNode.ps1` or `./runEthereumNode.sh` (depending on your OS) in a seperate terminal. This is the listener which will process all the requests.
- Run `python deployContract.py` in a separate terminal to deploy the contract `JointAccount.sol`, the address of which will be saved in `files\contractAddressList`. This file will be used to determine the address of the contracts deployed through the aforementioned script.
- Run `python sendTransactions.py` to call the different functions and perform any analysis on the deployed contract. Running this file will produce a log of creation and mining of every transaction generated, in the file `output/run_{}.log`.
```
usage: python sendTransactions.py [-h] [-u USERS] [-a ACCOUNTS] [-t TXNS] [-s SEED]

optional arguments:
-h, --help                        Show this help message and exit
-u USERS, --users USERS           Number of users to be registered. (default: 100)
-a ACCOUNTS, --accounts ACCOUNTS  Number of joint accounts. (default: 500)
-t TXNS, --txns TXNS              Number of sendAmount transactions. (default: 1000)
-s SEED, --seed SEED              Seed to fix randomness. (default: 42)
```
- Run `python plot.py <filename>` which will produce the desired plot sand save it to `output/plot.png`, using the `output/<filename>` file.

**NOTE**: While running in WSL (or possibly in other VMs), do not place this repository in the **mounted** filesystems. Geth is known to have issues with filesystem metadata associated with mounted directories ([issue](https://github.com/Microsoft/WSL/issues/2137)).

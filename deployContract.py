import sys, os
import time
from web3 import *
from solcx import compile_source


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source, solc_version='0.4.25')


def connectWeb3():
    return Web3(HTTPProvider('http://127.0.0.1:1558'))


def deployTxn(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface3 = compiled_sol.popitem()
    curBlock = w3.eth.getBlock('latest')
    tx_hash = w3.eth.contract(
        abi=contract_interface3['abi'], 
        bytecode=contract_interface3['bin']
    ).constructor().transact({
        'txType': '0x0', 
        'from': account, 
        'gas': 1000000
    })
    return tx_hash


def deployContract(source_path, w3, account, file):
    w3.miner.start(1)
    time.sleep(2)

    tx_hash3 = deployTxn(source_path, w3, account)

    receipt3 = w3.eth.getTransactionReceipt(tx_hash3)
    while receipt3 is None:
        time.sleep(0.1)
        receipt3 = w3.eth.getTransactionReceipt(tx_hash3)

    w3.miner.stop()

    assert receipt3 is not None, 'Contract not deployed'
    name = os.path.basename(source_path)[:-4]
    address = receipt3['contractAddress']
    print(f'{name}:{address}', file=file, flush=True)
    print(f'{name}:{address}', file=sys.stdout, flush=True)


w3 = connectWeb3()

with open(os.path.join('files', 'contractAddressList'), 'w') as fp:
    deployContract('JointAccount.sol', w3, w3.eth.accounts[0], fp)
    deployContract('emptyLoop.sol', w3, w3.eth.accounts[0], fp)
import sys, os, copy
import time
from web3 import *
from solcx import compile_source


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source, solc_version='0.4.25')


def read_contract_addresses():
    file = os.path.join('files', 'contractAddressList')
    with open(file, 'r') as fp:
        lines = [l.strip() for l in fp if l.strip()]
    return dict([l.split(':') for l in lines])


def connectWeb3():
    return Web3(HTTPProvider('http://127.0.0.1:1558'))


def sendEmptyLoopTransaction(address):
    compiled_sol = copy.deepcopy(compiled_contract)
    contract_id, contract_interface = compiled_sol.popitem()
    contract_obj = w3.eth.contract(address=address, abi=contract_interface['abi'])
    tx_hash = contract_obj.functions.runLoop(-123).transact({
        'txType': '0x3', 
        'from': w3.eth.accounts[0], 
        'gas': 2409638
    })
    return tx_hash


def getReceipt(txn_hash):
    receipt = w3.eth.getTransactionReceipt(txn_hash)
    while receipt is None:
        time.sleep(0.1)
        receipt = w3.eth.getTransactionReceipt(txn_hash)
    return receipt


base = os.path.dirname(os.path.abspath(__file__))
contract = os.path.join(base, 'emptyLoop.sol')
contract_name = os.path.basename(contract)[:-4]
compiled_contract = compile_source_file(contract)

w3 = connectWeb3()
contract_addresses = read_contract_addresses()

print("Starting Transaction Submission")
w3.miner.start(1)
address = contract_addresses[contract_name]
txn_hash = sendEmptyLoopTransaction(address)
receipt = getReceipt(txn_hash)
print(receipt)

w3.miner.stop()

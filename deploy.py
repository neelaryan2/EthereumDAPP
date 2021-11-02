from utils import *

def deployTxn(contract_source_path, w3, account):
    compiled_sol = compile_source_file(contract_source_path)
    contract_id, contract_interface = compiled_sol.popitem()
    tx_hash = w3.eth.contract(
        abi=contract_interface['abi'], 
        bytecode=contract_interface['bin']
    ).constructor().transact({
        'txType': '0x0', 
        'from': account
    })
    return tx_hash


def deployContract(source_path, w3, account, file):
    tx_hash = deployTxn(source_path, w3, account)
    receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    assert receipt is not None, 'Contract not deployed'
    name = os.path.basename(source_path)[:-4]
    address = receipt['contractAddress']
    print(f'{name}:{address}', file=file, flush=True)
    print(f'{name}:{address}', file=sys.stdout, flush=True)
    return address


def deploy():
    w3 = connectWeb3()
    w3.miner.start(1)
    with open(os.path.join('files', 'contractAddressList'), 'w') as fp:
        deployContract('JointAccount.sol', w3, w3.eth.accounts[0], fp)
        # deployContract('emptyLoop.sol', w3, w3.eth.accounts[0], fp)
    w3.miner.stop()


if __name__ == '__main__':
    deploy()
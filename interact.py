from utils import *


class DAPP:
    def __init__(self):
        self.w3 = connectWeb3()
        self.acct = self.w3.eth.accounts[0]
        self.gas = 2409638
        self.contract = None

    def start(self):
        self.w3.miner.start(1)

    def stop(self):
        self.w3.miner.stop()

    def fetch_contract(self, name='JointAccount'):
        base = os.path.dirname(os.path.abspath(__file__))
        contract_path = os.path.join(base, f'{name}.sol')
        contract_addresses = read_contract_addresses()
        compiled_contract = compile_source_file(contract_path)
        contract_id, contract_interface = compiled_contract.popitem()
        address = contract_addresses[name]
        abi = contract_interface['abi']
        self.contract = self.w3.eth.contract(address, abi=abi)

    def get_receipt(self, txn_hash):
        receipt = self.w3.eth.waitForTransactionReceipt(txn_hash)
        items, hb = [], type(receipt['blockHash'])
        for k, v in dict(receipt).items():
            if type(v) == hb: v = v.hex()
            if k not in ['logsBloom']:
                items.append((k, v))
        return json.dumps(dict(items), indent=4)

    def register_user(self, uid, name):
        txn_hash = self.contract.functions.registerUser(uid, name).transact({
            'txType': '0x3', 
            'from': self.acct, 
            'gas': self.gas
        })
        return self.get_receipt(txn_hash)

    def create_account(self, uid1, uid2, balance):
        txn_hash = self.contract.functions.createAcc(uid1, uid2, balance).transact({
            'txType': '0x3', 
            'from': self.acct, 
            'gas': self.gas
        })
        return self.get_receipt(txn_hash)

    def send_amount(self, uid1, uid2, amt):
        txn_hash = self.contract.functions.sendAmount(uid1, uid2, amt).transact({
            'txType': '0x3', 
            'from': self.acct, 
            'gas': self.gas
        })
        return self.get_receipt(txn_hash)

    def close_account(self, uid1, uid2):
        txn_hash = self.contract.functions.closeAccount(uid1, uid2).transact({
            'txType': '0x3', 
            'from': self.acct, 
            'gas': self.gas
        })
        return self.get_receipt(txn_hash)

    def get_balance(self, uid1, uid2):
        return self.contract.functions.getBalance(uid1, uid2).call(block_identifier='latest')


def execute(dapp):
    print(dapp.register_user(1, 'User1'))
    print(dapp.register_user(2, 'User2'))
    print(dapp.create_account(1, 2, 3))
    # print(dapp.get_balance(1, 2))
    print(dapp.send_amount(1, 2, 5))
    print(dapp.close_account(1, 2))


def execute2(dapp, seed=42):
    users, edges = user_network(nodes=100, edges=500, seed=42)
    random.seed(42)
    
    for i, uid in enumerate(users):
        dapp.register_user(uid, f'User{i + 1}')
    
    for u1, u2, balance in edges:
        dapp.create_account(u1, u2, balance)

    successes = [None for _ in range(1000)]
    for t in range(len(successes)):
        u1, u2 = random.choices(users, k=2)
        dapp.send_amount(u1, u2, 1)

    for u1, u2, balance in edges:
        dapp.close_account(u1, u2)


def main():
    dapp = DAPP()
    try:
        dapp.start()
        dapp.fetch_contract()
        execute(dapp)
    except Exception as e:
        raise e
    finally:
        dapp.stop()


if __name__ == '__main__':
    main()
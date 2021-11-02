from utils import *


class DAPP:
    def __init__(self):
        self.w3 = connectWeb3()
        self.txn_params = {'txType': '0x3', 'from': self.w3.eth.accounts[0]}
        self.load_contract()

        for function in ['registerUser', 'createAcc', 'sendAmount', 'closeAccount']:
            setattr(self, function, self.make_function('transact', function))
        for function in ['getBalance']:
            setattr(self, function, self.make_function('call', function))

    def update_gas(self):
        gas = self.w3.eth.getBlock('latest')['gasLimit']
        self.txn_params.update(gas=gas)

    def start(self, timeout=1):
        self.w3.miner.start(1)
        time.sleep(timeout)

    def stop(self):
        self.w3.miner.stop()

    def load_contract(self, name='JointAccount'):
        base = os.path.dirname(os.path.abspath(__file__))
        contract_path = os.path.join(base, f'{name}.sol')
        contract_addresses = read_contract_addresses()
        compiled_contract = compile_source_file(contract_path)
        contract_id, contract_interface = compiled_contract.popitem()
        address = contract_addresses[name]
        abi = contract_interface['abi']
        self.contract = self.w3.eth.contract(address, abi=abi)
        assert self.w3.eth.getCode(self.contract.address)

    def make_function(self, ftype, name):
        function = getattr(self, ftype + '_function')
        return lambda *args: function(name, args)

    def transact_function(self, function_name, args):
        self.update_gas()
        function = getattr(self.contract.functions, function_name)
        txn_hash = function(*args).transact(self.txn_params)
        receipt = get_receipt(self.w3, txn_hash, timeout=30)
        print(json.dumps(receipt, indent=4))
        return receipt

    def call_function(self, function_name, args):
        function = getattr(self.contract.functions, function_name)
        value = function(*args).call(block_identifier='latest')
        return value


def analysis(seed=42):
    users, edges = user_network(nodes=100, edges=500, seed=seed)
    random.seed(seed)
    dapp = DAPP()
    dapp.start()

    for i, uid in enumerate(users):
        dapp.registerUser(uid, f'User{i + 1}')
    
    for u1, u2, balance in edges:
        dapp.createAcc(u1, u2, balance)

    successes = [None for _ in range(1000)]
    for t in range(len(successes)):
        u1, u2 = random.choices(users, k=2)
        dapp.sendAmount(u1, u2, 1)

    for u1, u2, balance in edges:
        dapp.closeAccount(u1, u2)

    dapp.stop()


def testing():
    dapp = DAPP()
    dapp.start()
    dapp.registerUser(1, 'User1')
    dapp.stop()


if __name__ == '__main__':
    testing()
    # analysis()
    
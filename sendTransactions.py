from utils import *


class DAPP:
    def __init__(self):
        self.default_gas = 50000
        self.pending = []
        self.setup_log()
        self.w3 = connectWeb3()
        self.txn_params = {'txType': '0x3', 'from': self.w3.eth.accounts[0], 'gas': self.default_gas}
        self.load_contract()
        
        for function in ['registerUser', 'createAcc', 'sendAmount', 'closeAccount']:
            setattr(self, function, self.make_function('transact', function))
        for function in ['getBalance']:
            setattr(self, function, self.make_function('call', function))

        self.gas_estimates = {
            'registerUser': 150000,
            'createAcc': 200000,
            'sendAmount': 10000000,
            'closeAccount': 1000000
        }

    def setup_log(self):
        folder = 'output'
        os.makedirs(folder, exist_ok=True)
        counter = 0
        file = os.path.join(folder, f'run_{counter}.log')
        while os.path.isfile(file):
            counter += 1
            file = os.path.join(folder, f'run_{counter}.log')
        self.logfile = open(file, 'w')
    
    def close(self):
        self.w3.miner.stop()
        self.logfile.close()

    def load_contract(self, name='JointAccount'):
        base = os.path.dirname(os.path.abspath(__file__))
        contract_path = os.path.join(base, f'{name}.sol')
        contract_addresses = read_contract_addresses()
        compiled_contract = compile_source_file(contract_path)
        contract_id, contract_interface = compiled_contract.popitem()
        address = contract_addresses[name]
        abi = contract_interface['abi']
        self.contract = self.w3.eth.contract(address, abi=abi)
        assert self.w3.eth.getCode(self.contract.address), 'Contract address is empty'

    def estimate_gas(self, name, function, args):
        # try:
        #     old_gas = self.txn_params.pop('gas', self.default_gas)
        #     gas = function(*args).estimateGas(self.txn_params)
        #     gas += 100000
        # except ValueError as e:
        #     gas = self.default_gas
        gas = self.gas_estimates[name]
        self.txn_params.update(gas=gas)

    def mine(self):
        if not self.pending: return []
        self.w3.miner.start(1)
        statuses = []
        for info, txn_hash in self.pending:
            receipt = get_receipt(self.w3, txn_hash, tries=50, latency=0.5)
            status = check_txn(self.w3, receipt)
            gasUsed = receipt['gasUsed']
            hash_hex = txn_hash.hex()[2:]
            self.log(info, ': ', status, '  gasUsed: ', gasUsed, '  txnHash: ', hash_hex)
            statuses.append(status)
        self.w3.miner.stop()
        del self.pending
        self.pending = []
        return statuses

    def make_function(self, ftype, name):
        function = getattr(self, ftype + '_function')
        return lambda *args: function(name, args)

    def transact_function(self, function_name, args):
        function = self.contract.find_functions_by_name(function_name)[0]
        self.estimate_gas(function_name, function, args)
        txn_hash = function(*args).transact(self.txn_params)
        info = function_name + str(args)
        self.pending.append((info, txn_hash))

    def call_function(self, function_name, args):
        function = getattr(self.contract.functions, function_name)
        value = function(*args).call(block_identifier='latest')
        self.log(function_name, args, ': ', value)
        return value

    def log(self, *args):
        print(*args, sep='', file=self.logfile, flush=True)


def register_users(dapp, users):
    for i, uid in enumerate(users):
        dapp.registerUser(uid, f'User{i + 1}')
    dapp.mine()


def analysis(dapp, users, edges, txns, seed):
    random.seed(seed)
    
    for u1, u2, balance in edges:
        dapp.createAcc(u1, u2, balance)
    dapp.mine()

    successes = []
    for t in range(txns):
        u1, u2 = random.sample(users, k=2)
        dapp.sendAmount(u1, u2, 1)
        success = dapp.mine()[0]
        successes.append(success)

    for u1, u2, balance in edges:
        dapp.closeAccount(u1, u2)
    dapp.mine()

    return successes


def main(dapp, args):
    nodes = args.users
    edges = args.accounts
    seed = args.seed
    txns = args.txns

    users, edges = user_network(nodes=nodes, edges=edges, seed=seed)
    register_users(dapp, users)
    successes = analysis(dapp, users, edges, txns, seed)
    return successes


if __name__ == '__main__':
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument('-u', '--users', type=int, default=100, help='Number of users to be registered.')
    parser.add_argument('-a', '--accounts', type=int, default=500, help='Number of joint accounts.')
    parser.add_argument('-t', '--txns', type=int, default=1000, help='Number of sendAmount transactions.')
    parser.add_argument('-s', '--seed', type=int, default=42, help='Seed to fix randomness.')
    args = parser.parse_args()
    dapp = DAPP()

    try:
        main(dapp, args)
    except KeyboardInterrupt as e:
        dapp.close()
        raise e

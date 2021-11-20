import sys, os
import time, random
import web3
from solcx import compile_source
import argparse
import json


def compile_source_file(file_path):
    with open(file_path, 'r') as fp:
        source = fp.read()
    return compile_source(source, solc_version='0.4.25')


def connectWeb3():
    if os.name == 'nt':
        return web3.Web3(web3.HTTPProvider('http://127.0.0.1:1558'))
    elif os.name == 'posix':
        return web3.Web3(web3.IPCProvider('./files/dapp/geth.ipc'))
    else:
        raise Exception('OS not supported.')


def read_contract_addresses():
    file = os.path.join('files', 'contractAddressList')
    with open(file, 'r') as fp:
        lines = [l.strip() for l in fp if l.strip()]
    return dict([l.split(':') for l in lines])


def json_parseable(obj):
    too_long = set(['logsBloom', 'input'])
    items, hb = [], type(obj['blockHash'])
    for k, v in dict(obj).items():
        if type(v) == hb: v = v.hex()
        if k not in too_long:
            items.append((k, v))
    return dict(items)


def pprint(obj, **kwargs):
    obj = json_parseable(obj)
    obj = json.dumps(obj, indent=4)
    print(obj, **kwargs)


def check_txn(w3, receipt):
    # https://ethereum.stackexchange.com/questions/6002/transaction-status
    txn_hash = bytes(receipt['transactionHash'])
    txn = w3.eth.getTransaction(txn_hash)
    gas = int(txn['gas'])
    gas_used = int(receipt['gasUsed'])
    status = 'SUCCESS' if (gas_used < gas) else 'FAILURE'
    return status


def get_receipt(w3, txn_hash, tries=50, latency=0.1):
    for t in range(tries):
        receipt = w3.eth.getTransactionReceipt(txn_hash)  
        if receipt is not None:
            break
        time.sleep(latency)
        if t == tries // 2:
            latency *= 2

    if receipt is None:
        w3.miner.stop()
        raise Exception('Could not fetch receipt')
    else:
        return receipt


def graph_structure(nodes, edges, seed=42):
    mx = (nodes * (nodes - 1)) // 2
    mn = nodes - 1
    assert mx >= edges >= mn, f'Number of edges ({edges}) should be in [{mn}, {mx}]'
    random.seed(seed)
    idx = list(range(nodes))
    degrees = [0 for _ in idx]
    edges_log = set()

    def add_edge(a, b):
        nonlocal edges, degrees, edges_log
        if a > b: a, b = b, a
        if (a, b) in edges_log: return
        edges_log.add((a, b))
        edges -= 1
        degrees[a] += 1
        degrees[b] += 1

    S, T = set(idx), set()
    n1, n2 = random.sample(idx, k=2)
    S.remove(n1); S.remove(n2)
    T.add(n1); T.add(n2)
    add_edge(n1, n2)

    ## first create connected graph
    while len(S) > 0:
        next_node = random.choice(idx)
        if next_node not in T:
            ## randomly sample node with probability proportional to degree
            neighbour_node = random.choices(idx, weights=degrees)[0]
            while neighbour_node == next_node:
                neighbour_node = random.choices(idx, weights=degrees)[0]
            S.remove(next_node); T.add(next_node)
            add_edge(next_node, neighbour_node)

    ## add extra edges
    while edges > 0:
        next_node = random.choice(idx)
        ## randomly sample node with probability proportional to degree
        neighbour_node = random.choices(idx, weights=degrees)[0]
        while neighbour_node == next_node:
            neighbour_node = random.choices(idx, weights=degrees)[0]
        add_edge(next_node, neighbour_node)

    return list(edges_log)


def user_network(nodes, edges, seed=42):
    if isinstance(edges, int):
        edges = graph_structure(nodes, edges, seed)
    random.seed(seed)

    user_ids = list(range(1, nodes + 1))
    ## randomly initialize amounts
    amounts = [round(random.expovariate(lambd=1/10) / 2) for _ in edges]
    edges = [(user_ids[a], user_ids[b], amt) for (a, b), amt in zip(edges, amounts)]
    return user_ids, edges
    

if __name__ == '__main__':
    print(user_network(10, 50, 42))

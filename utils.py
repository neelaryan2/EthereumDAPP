import sys, os, copy
import time, random
from web3 import *
from solcx import compile_source
import json


def compile_source_file(file_path):
    with open(file_path, 'r') as f:
        source = f.read()
    return compile_source(source, solc_version='0.4.25')


def connectWeb3():
    return Web3(HTTPProvider('http://127.0.0.1:1558'))


def read_contract_addresses():
    file = os.path.join('files', 'contractAddressList')
    with open(file, 'r') as fp:
        lines = [l.strip() for l in fp if l.strip()]
    return dict([l.split(':') for l in lines])


def get_receipt(w3, txn_hash, timeout=120):
        time.sleep(0.01)
        try:
            receipt = w3.eth.waitForTransactionReceipt(txn_hash, timeout=timeout)
        except Exception as e:
            w3.miner.stop()
            raise e
        items, hb = [], type(receipt['blockHash'])
        for k, v in dict(receipt).items():
            if type(v) == hb: v = v.hex()
            if k not in ['logsBloom']:
                items.append((k, v))
        return dict(items)


def graph_structure(nodes, edges, seed=42):
    assert edges >= nodes - 1
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

    while len(S) > 0:
        next_node = random.choice(idx)
        if next_node not in T:
            neighbour_node = random.choices(idx, weights=degrees)[0]
            while neighbour_node == next_node:
                neighbour_node = random.choices(idx, weights=degrees)[0]
            S.remove(next_node); T.add(next_node)
            add_edge(next_node, neighbour_node)

    while edges > 0:
        next_node = random.choice(idx)
        neighbour_node = random.choices(idx, weights=degrees)[0]
        while neighbour_node == next_node:
            neighbour_node = random.choices(idx, weights=degrees)[0]
        add_edge(next_node, neighbour_node)

    return list(edges_log)


def user_network(nodes, edges, seed=42):
    if isinstance(edges, int):
        edges = graph_structure(nodes, edges, seed)
    random.seed(seed)

    user_ids, so_far = [], set()
    for _ in range(nodes):
        uid = random.getrandbits(256)
        while uid in so_far:
            uid = random.getrandbits(256)
        user_ids.append(uid)
        so_far.add(uid)

    amounts = [round(random.expovariate(lambd=1/10) / 2) for _ in edges]
    edges = [(user_ids[a], user_ids[b], amt) for (a, b), amt in zip(edges, amounts)]
    return user_ids, edges
    
if __name__ == '__main__':
    print(user_network(4, 5, 42))

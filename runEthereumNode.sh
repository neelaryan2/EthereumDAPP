#!/bin/bash

BASE="./files"
APP="dapp"

rm -rf $BASE/$APP/geth/chaindata/
rm -rf $BASE/$APP/geth/lightchaindata/
rm -rf $BASE/$APP/geth/nodes/
rm -rf $BASE/$APP/geth/ethash/
rm -rf $BASE/$APP/geth/LOCK
rm -rf $BASE/$APP/geth/transactions.rlp
rm -rf $BASE/$APP/keystore
mkdir -p $BASE/$APP
cp -r $BASE/keystore $BASE/$APP/keystore

./geth --datadir $BASE/$APP --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nousb --nodiscover --nodekey=$BASE/nk.txt init $BASE/genesis.json
./geth --datadir $BASE/$APP --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nousb --nodiscover --nodekey=$BASE/nk.txt --verbosity 5 --allow-insecure-unlock --unlock 0 --password $BASE/password.txt

# console
# ./geth --datadir $BASE/$APP attach

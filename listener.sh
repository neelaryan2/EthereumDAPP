BASE=./files

rm -rf $BASE/test-eth1/geth/chaindata/
rm -rf $BASE/test-eth1/geth/lightchaindata/
rm -rf $BASE/test-eth1/geth/nodes/
rm -rf $BASE/test-eth1/geth/ethash/
rm -rf $BASE/test-eth1/geth/LOCK
rm -rf $BASE/test-eth1/geth/transactions.rlp
rm -rf $BASE/test-eth1/keystore
cp -r $BASE/keystore $BASE/test-eth1/keystore

./geth --datadir $BASE/test-eth1 --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner,debug" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey=$BASE/nk.txt init $BASE/genesis.json
./geth --datadir $BASE/test-eth1 --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner,debug" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey=$BASE/nk.txt --verbosity 5 --allow-insecure-unlock --unlock 0 --password $BASE/password.txt

# console
# ./geth --datadir $BASE/test-eth1 attach

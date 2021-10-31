function force_delete {
    param (
        $file
    )
    if (test-path $file) {
        remove-item $file -recurse -force
    }
}

force_delete .\files\test-eth1\geth\chaindata\
force_delete .\files\test-eth1\geth\lightchaindata\
force_delete .\files\test-eth1\geth\nodes\
force_delete .\files\test-eth1\geth\ethash\
force_delete .\files\test-eth1\geth\LOCK
force_delete .\files\test-eth1\geth\transactions.rlp


.\geth.exe --datadir .\files\test-eth1 --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner,debug" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey=.\files\nk.txt init .\files\genesis.json
.\geth.exe --datadir .\files\test-eth1 --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner,debug" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nodiscover --nodekey=.\files\nk.txt --verbosity 5 --allow-insecure-unlock --unlock 0 --password .\files\password.txt

# console
# .\geth.exe attach ipc:\\.\pipe\geth.ipc

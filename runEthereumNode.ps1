function force_delete {
    param (
        $file
    )
    if (test-path $file) {
        remove-item $file -recurse -force
    }
}

$BASE = ".\files"
$APP = "dapp"

force_delete $BASE\$APP\geth\chaindata\
force_delete $BASE\$APP\geth\lightchaindata\
force_delete $BASE\$APP\geth\nodes\
force_delete $BASE\$APP\geth\ethash\
force_delete $BASE\$APP\geth\LOCK
force_delete $BASE\$APP\geth\transactions.rlp
force_delete $BASE\$APP\keystore
new-item -itemtype directory -force -path $BASE\$APP
copy-item -Path $BASE\keystore -Destination $BASE\$APP\keystore -Recurse

.\geth.exe --datadir $BASE\$APP --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nousb --nodiscover --nodekey=$BASE\nk.txt init $BASE\genesis.json
.\geth.exe --datadir $BASE\$APP --nat=none --rpc --rpcport=1558 --rpcapi "eth,net,web3,miner" --networkid=2310 --port=1547 --syncmode full --gcmode archive --nousb --nodiscover --nodekey=$BASE\nk.txt --verbosity 5 --allow-insecure-unlock --unlock 0 --password $BASE\password.txt

# console
# .\geth.exe attach ipc:\\.\pipe\geth.ipc

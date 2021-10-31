pragma solidity ^0.4.24;

contract Sorter {
    uint256 public loopVar;

    constructor() public {
        loopVar = 50 * 50;
    }

    function runLoop() public view {
        uint256 a = 0;
        for (uint256 i = 0; i < loopVar; i++) {
            a++;
        }
    }
}

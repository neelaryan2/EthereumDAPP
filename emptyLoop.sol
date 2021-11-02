pragma solidity ^0.4.25;

contract Sorter {
    uint256 public loopVar;

    constructor() public {
        loopVar = 50 * 50;
    }

    function runLoop(uint256 v) view public returns (uint256) {
        uint256 a = 0;
        for (uint256 i = 0; i < v; i++) {
            a++;
        }
        return a;
    }
}

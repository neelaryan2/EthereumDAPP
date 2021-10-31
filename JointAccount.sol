pragma solidity ^0.4.25;

// TODO : Verify if only the admin can call the four functions

contract JointAccount {
    address public admin;

    struct Edge {
        int256 user_id;
        uint256 balance;
    }

    struct QueueItem {
        int256 u1;
        int256 u2;
        int256[] path;
        uint256 pathIdx;
    }

    uint256 userCount = 0;
    uint256 edgeCount = 0;

    mapping(int256 => string) public users;

    mapping(int256 => Edge[]) private neighbours;

    mapping(int256 => mapping(int256 => bool)) visited;

    constructor() public {
        admin = msg.sender;
    }

    function registerUser(int256 user_id, string user_name) public {
        // require(msg.sender == admin);

        users[user_id] = user_name;
        userCount++;
    }

    function createAcc(
        int256 user_id_1,
        int256 user_id_2,
        uint256 balance
    ) public {
        // divide balance equally in user_1 and user_2

        // require(msg.sender == admin);

        neighbours[user_id_1].push(Edge(user_id_2, balance / 2));
        neighbours[user_id_2].push(Edge(user_id_1, balance / 2));
        edgeCount += 2;
    }

    function updateBalances(int256 user_id_2, int256[] path, uint256 pathIdx, uint256 amount) private {
        int256 from = user_id_2;
        int256 to;

        for (uint256 idx = pathIdx - 1; idx >= 0 && idx < pathIdx; idx--) {
            to = from;
            from = path[idx];
            for (uint256 i = 0; i < neighbours[from].length; i++) {
                if (neighbours[from][i].user_id == to) {
                    neighbours[from][i].balance -= amount;
                }
            }
            for (i = 0; i < neighbours[to].length; i++) {
                if (neighbours[to][i].user_id == from) {
                    neighbours[to][i].balance += amount;
                }
            }
        }
    }

    function copyPath(QueueItem from, QueueItem to) private pure {
        for (uint256 k = 0; k < from.path.length; k++) {
            to.path[k] = from.path[k];
        }
    }

    function deletePath(QueueItem qi) private pure {
        for (uint256 k = 0; k < qi.pathIdx; k++) {
            delete qi.path[k];
        }
        qi.pathIdx = 0;
    }

    function sendAmount(int256 user_id_1, int256 user_id_2, uint256 amount) public {
        // send amount from user_1 to user_2 if possible

        // require(msg.sender == admin);

        QueueItem[] memory visEdges = new QueueItem[](edgeCount + 1);
        QueueItem[] memory queue = new QueueItem[](edgeCount + 1);
        uint256 visEdgesIdx = 0;
        uint256 queueIdx = 0;

        queue[queueIdx++] = QueueItem(0, user_id_1, new int256[](0), 0);

        bool found = false;
        int256[] memory path;
        uint256 j;

        for (uint256 i = 0; i < queueIdx; i++) {
            int256 u2 = queue[i].u2;
            if (u2 == user_id_2) {
                found = true;
                path = queue[i].path;
                j = queue[i].pathIdx; // use j as pathIdx to avoid creating another local variable
                break;
            }
            for (j = 0; j < neighbours[u2].length; j++) {
                Edge storage e = neighbours[u2][j];
                if (!visited[u2][e.user_id]) {
                    visited[u2][e.user_id] = true;
                    visEdges[visEdgesIdx++] = QueueItem(u2, e.user_id, new int256[](0), 0);
                    if (e.balance >= amount) {
                        QueueItem memory qj = QueueItem(u2, e.user_id, new int256[](userCount), queue[i].pathIdx + 1);
                        copyPath(queue[i], qj);
                        qj.path[queue[i].pathIdx] = u2;
                        qj.pathIdx = queue[i].pathIdx + 1;
                        queue[queueIdx++] = qj;
                    }
                }
            }
            deletePath(queue[i]);
            delete queue[i];
        }

        require(found);

        // update all balances as per path
        // path = [user_id_1, ... , u1 , u2 , ... , u]

        updateBalances(user_id_2, path, j, amount);

        deletePath(queue[i]);

        for (i = 0; i < visEdgesIdx; i++) {
            visited[visEdges[i].u1][visEdges[i].u2] = false;
        }
    }

    function removeNeighbour(int256 user_1, int256 user_2) public {
        // remove user_2 from neighbours of user_1
        bool found = false;
        for (uint256 i = 0; i < neighbours[user_1].length; i++) {
            if (neighbours[user_1][i].user_id == user_2) {
                found = true;
            }
            if (found && i + 1 < neighbours[user_1].length) {
                neighbours[user_1][i] = neighbours[user_1][i + 1];
            }
        }
        delete neighbours[user_1][neighbours[user_1].length - 1];
        neighbours[user_1].length--;
    }

    function closeAccount(int256 user_id_1, int256 user_id_2) public {
        // require(msg.sender == admin);

        removeNeighbour(user_id_1, user_id_2);
        removeNeighbour(user_id_2, user_id_1);
    }
}

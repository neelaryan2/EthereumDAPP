pragma solidity ^0.4.25;

// TODO : Verify if only the admin can call the four functions

contract JointAccount {
    address private admin;

    struct Edge {
        uint256 to;
        uint256 balance;
    }

    uint256 bad;
    uint256[] private user_ids;
    uint256[] private queue;
    
    mapping(uint256 => Edge[]) private adj;
    mapping(uint256 => string) private name;
    mapping(uint256 => bool) private used;
    mapping(uint256 => bool) private visited;
    mapping(uint256 => uint256) private parent;
    
    
    constructor() public {
        bad = 2**256 - 1;
        admin = msg.sender;
    }

    function registerUser(uint256 user_id, string user_name) public {
        // require(msg.sender == admin, "You do not have access to this function.");
        
        if (!used[user_id]) {
            used[user_id] = true;
            visited[user_id] = false;
            name[user_id] = user_name;
            user_ids.push(user_id);
        } else {
            require(false, "User ID already exists.");
        }
    }

    function checkEdge(uint256 uid1, uint256 uid2) view private returns (bool) {
        require(used[uid1] && used[uid2], "User does not exist");
        uint256 i;
        bool found = false;
        
        for (i = 0; i < adj[uid1].length; i++)
            if (adj[uid1][i].to == uid2)
                found = true;

        if (!found)
            return false;

        found = false;
        for (i = 0; i < adj[uid2].length; i++)
            if (adj[uid2][i].to == uid1)
                found = true;
        
        return found;
    }
    
    function getBalance(uint256 uid1, uint256 uid2) view public returns (uint256, uint256) {
        // require(msg.sender == admin, "You do not have access to this function.");
        require(checkEdge(uid1, uid2), "Users are not connected.");
        
        uint256 a;
        uint256 b;
        uint256 i;

        for (i = 0; i < adj[uid1].length; i++)
            if (adj[uid1][i].to == uid2)
                a = adj[uid1][i].balance;
        
        for (i = 0; i < adj[uid2].length; i++)
            if (adj[uid2][i].to == uid1)
                b = adj[uid2][i].balance;
                
        return (a, b);
    }

    function createAcc(uint256 uid1, uint256 uid2, uint256 balance) public {
        // require(msg.sender == admin, "You do not have access to this function.");
        require(!checkEdge(uid1, uid2), "Users already have an account.");
        adj[uid1].push(Edge(uid2, balance));
        adj[uid2].push(Edge(uid1, balance));
    }

    function sendAmount(uint256 uid1, uint256 uid2, uint256 amount) public {
        // send amount from user_1 to user_2 if possible

        // require(msg.sender == admin, "You do not have access to this function.");
        require(used[uid1] && used[uid2], "User does not exist");

        // stack variables
        uint256 i;
        uint256 j;
        uint256 v;
        uint256 u;
        
        // reset from past runs
        for (i = 0; i < user_ids.length; i++) {
            j = user_ids[i];
            visited[j] = false;
            parent[j] = bad;
        }
        delete queue;

        // initialise
        parent[uid1] = uid1;
        visited[uid1] = true;
        queue.push(uid1);
        
        // BFS
        for (i = 0; i < queue.length; i++) {
            v = queue[i];
            if (v == uid2) 
                break;
            for (j = 0; j < adj[v].length; j++) {
                u = adj[v][j].to;
                if (!visited[u]) {
                    visited[u] = true;
                    if (adj[v][j].balance >= amount) {
                        queue.push(u);
                        parent[u] = v;
                    }
                }
            }
        }
        
        // reachability
        require(parent[uid2] != bad, "No viable path exists between these users.");
        
        // path update
        v = uid2;
        while (parent[v] != v) {
            u = parent[v];
            
            for (i = 0; i < adj[u].length; i++)
                if (adj[u][i].to == v)
                    break;
            adj[u][i].balance -= amount;
            
            for (j = 0; j < adj[v].length; j++)
                if (adj[v][j].to == u)
                    break;
            adj[v][j].balance += amount;
            
            v = u;
        }
        
        // sanity check
        require(v == uid1, "Something bad happened.");
    }

    function removeNeighbour(uint256 uid1, uint256 uid2) private {
        // remove user_2 from neighbours of uid1
        
        bool found = false;
        uint256 length = adj[uid1].length;
        uint256 i;
        
        for (i = 0; i < length; i++) {
            if (adj[uid1][i].to == uid2) {
                found = true;
            }
            if (found && i + 1 < length) {
                adj[uid1][i] = adj[uid1][i + 1];
            }
        }
        delete adj[uid1][length - 1];
        adj[uid1].length--;
    }

    function closeAccount(uint256 uid1, uint256 uid2) public {
        // require(msg.sender == admin, "You do not have access to this function.");
        require(checkEdge(uid1, uid2), "Users are not connected.");

        removeNeighbour(uid1, uid2);
        removeNeighbour(uid2, uid1);
    }
}

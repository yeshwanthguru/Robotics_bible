---
title: CS, Data Structures, Algorithms
---

# CS Fundamentals for Robotics Interviews

## Complexity cheatsheet

| Structure | Access | Search | Insert | Notes |
|---|---|---|---|---|
| Array | O(1) | O(n) | O(n) | cache friendly |
| Hash map | – | O(1) avg | O(1) avg | O(n) worst |
| Binary heap | – | – | O(log n) | priority queue → Dijkstra/A* open list |
| BST (balanced) | – | O(log n) | O(log n) | std::map |
| KD-tree | – | O(log n) avg NN | O(log n) | point-cloud nearest neighbour (ICP) |
| Octree / voxel hash | – | O(log n) / O(1) | – | OctoMap, voxblox, nvblox |
| Union-Find | – | ~O(α(n)) | – | Kruskal, loop-closure clusters |

## Algorithms most asked in robotics

- **BFS/DFS**, **Dijkstra** O((V+E)logV), **A\*** (admissible+consistent heuristic ⇒ optimal), **Jump Point Search** for uniform grids.
- **DP**: edit distance, knapsack, Viterbi (HMM), value iteration is DP.
- **Graph**: topological sort, MST, SCC, shortest paths with negative edges (Bellman–Ford).
- **Sorting/selection**: quickselect for medians (robust stats).
- **Two pointers / sliding window**, **binary search on answer**.
- **Geometry**: convex hull, point-in-polygon, segment intersection, line fitting (RANSAC).
- **Bit manipulation**, **intervals**, **matrix ops** (rotate, spiral).

## Systems knowledge

- **Concurrency**: mutex, condition variable, lock-free queue, deadlock conditions (mutual exclusion, hold-and-wait, no preemption, circular wait), priority inversion (solve with priority inheritance).
- **Real-time**: hard vs soft RT, jitter, `PREEMPT_RT`, CPU pinning, avoiding malloc in control loop.
- **Memory**: stack vs heap, cache lines, false sharing, alignment, zero-copy (shared memory transport in ROS2).
- **Networking**: TCP vs UDP, DDS multicast discovery, latency vs throughput.
- **OS**: processes vs threads, virtual memory, context switch, interrupts.

## Python coding patterns you must do from memory

```python
# A* on a grid
import heapq
def astar(grid, s, g):
    h = lambda a: abs(a[0]-g[0]) + abs(a[1]-g[1])
    pq, cost, prev = [(h(s), 0, s)], {s: 0}, {}
    while pq:
        _, c, u = heapq.heappop(pq)
        if u == g:
            path = [u]
            while u in prev: u = prev[u]; path.append(u)
            return path[::-1]
        if c > cost[u]: continue
        for dx, dy in ((1,0),(-1,0),(0,1),(0,-1)):
            v = (u[0]+dx, u[1]+dy)
            if 0 <= v[0] < len(grid) and 0 <= v[1] < len(grid[0]) and grid[v[0]][v[1]] == 0:
                nc = c + 1
                if nc < cost.get(v, 1e18):
                    cost[v], prev[v] = nc, u
                    heapq.heappush(pq, (nc + h(v), nc, v))
    return None
```

## Interview Q&A

**A\* vs Dijkstra?** A\* adds heuristic h; Dijkstra is A\* with h=0. Consistent h ⇒ each node expanded once.

**Why not use `new` in a real-time loop?** Non-deterministic latency, fragmentation. Pre-allocate.

**Mutex vs semaphore?** Mutex has ownership (locker unlocks); semaphore is a counter signalling mechanism.
